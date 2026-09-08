from __future__ import annotations

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class SpeechSynthesizer:
    def __init__(self) -> None:
        self._log_file_path = Path(os.environ.get("ND_REMINDER_LOG", "/tmp/nd_reminder_speech.log"))
        self._spd_say_path: Optional[str] = self._resolve_executable(["spd-say", "/usr/bin/spd-say", "/bin/spd-say", "/usr/local/bin/spd-say"])
        self._espeak_path: Optional[str] = self._resolve_executable(["espeak-ng", "espeak", "/usr/bin/espeak-ng", "/usr/bin/espeak"])

    def speak(self, text: str) -> None:
        cleaned = str(text).strip()
        if not cleaned:
            return

        self._log(f"speak requested: {cleaned}")

        # Try spd-say first (preferred).
        if self._spd_say_path is not None:
            if self._run_command([self._spd_say_path, cleaned], label="spd-say"):
                return

        # Fallback: espeak / espeak-ng.
        if self._espeak_path is not None:
            if self._run_command([self._espeak_path, cleaned], label="espeak"):
                return

        self._log("no speech backend succeeded")

    def _run_command(self, command: List[str], label: str) -> bool:
        try:
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, timeout=10)
            if result.returncode == 0:
                self._log(f"{label} ok: {command!r}")
                return True
            self._log(f"{label} failed rc={result.returncode}: {command!r}; stderr={result.stderr.strip()!r}")
            return False
        except Exception as exception:
            self._log(f"{label} exception: {exception!r}; command={command!r}")
            return False

    def _resolve_executable(self, candidates: List[str]) -> Optional[str]:
        for candidate in candidates:
            resolved = shutil.which(candidate)
            if resolved is not None:
                return resolved
            if candidate.startswith("/"):
                if Path(candidate).exists():
                    return candidate
        return None

    def _log(self, message: str) -> None:
        try:
            self._log_file_path.parent.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().isoformat(timespec="seconds")
            with self._log_file_path.open("a", encoding="utf-8") as file:
                file.write(f"[{timestamp}] {message}\n")
        except Exception:
            return
