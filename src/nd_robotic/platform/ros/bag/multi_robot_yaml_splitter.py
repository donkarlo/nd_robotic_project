#!/usr/bin/env python3
# file: yaml_split_by_robot_ultrafast_named.py
from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, IO, List, Optional

# --- Lightweight regexes for streaming ---
DOC_SEP_RE = re.compile(r"^[ \t]*---[ \t]*\n?$")
TOPIC_LINE_RE = re.compile(r"^#[ \t]*topic:[ \t]*(/[^ \t#]+)", re.IGNORECASE)
COMMENT_LINE_RE = re.compile(r"^#[ \t]*")  # any comment line (for header blocks)


def _sanitize_token(s: str) -> str:
    # Allow letters, digits, underscore; collapse others to "_"
    import re as _re
    s = s.strip()
    s = _re.sub(r"[^A-Za-z0-9_]+", "_", s)
    s = _re.sub(r"_+", "_", s)
    return s.strip("_").lower()


def _split_topic(topic: str | None) -> tuple[str, List[str]]:
    """
    '/uav1/odometry/odom_gps' -> ('uav1', ['odometry','odom_gps'])
    Normalizes to lowercase and strips weird chars.
    """
    if not topic:
        return "", []
    parts = [p for p in topic.split("/") if p]
    if not parts:
        return "", []
    robot = _sanitize_token(parts[0])
    rest = [_sanitize_token(p) for p in parts[1:] if _sanitize_token(p)]
    return robot, rest


class UltraFastNamedSplitter:
    """
    Stream-split a huge multi-doc YAML by robot __name using ONLY the comment header block.
    The header block (# topic/msg_count/timestamp) appears BEFORE the '---' of the next doc.
    We capture a 'pending header/topic' and attach it to the next started document.

    Output:
      - One temporary file per robot during processing: <robot>.tmp.schema.yaml
      - At the end, rename to: <robot>_<type1>_<type2>_... .schema.yaml
        where <describer*> are unique tokens (order of first appearance across the file).
    """

    def __init__(self, src: str | Path, out_dir: str | Path | None = None, emit_unknown: bool = False):
        self.src = Path(src)
        if not self.src.exists():
            raise FileNotFoundError(self.src)
        self.out_dir = Path(out_dir) if out_dir else self.src.parent
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.emit_unknown = emit_unknown

        # Handles to temp outputs: robot -> file handle (robot.tmp.schema.yaml)
        self._handles: Dict[str, IO[str]] = {}
        # Unknown (optional)
        self._unknown: Optional[IO[str]] = None

        # Per-robot ordered unique episodic-describer tokens (for final filename)
        self._robot_types_ordered: Dict[str, List[str]] = {}
        self._robot_types_seen: Dict[str, set] = {}

        # Current doc state
        self.cur_lines: List[str] = []  # body lines
        self.cur_header_lines: List[str] = []  # header comments to prepend on write
        self.cur_robot: str = ""  # robot for current doc
        self.started_doc: bool = False

        # Pending header (belongs to the *next* doc)
        self.pending_header_lines: List[str] = []
        self.pending_topic: Optional[str] = None
        self.capturing_pending_header: bool = False

    # ---------- helpers ----------
    def _out_robot_tmp(self, robot: str) -> IO[str]:
        if robot not in self._handles:
            p = self.out_dir / f"{robot}.tmp.schema.yaml"
            self._handles[robot] = p.open("a", encoding="utf-8", buffering=1024 * 1024)
            self._robot_types_ordered.setdefault(robot, [])
            self._robot_types_seen.setdefault(robot, set())
        return self._handles[robot]

    def _out_unknown(self) -> IO[str]:
        if self._unknown is None:
            p = self.out_dir / "unknown.schema.yaml"
            self._unknown = p.open("a", encoding="utf-8", buffering=1024 * 1024)
        return self._unknown

    def _record_types(self, robot: str, types: List[str]) -> None:
        if not robot or not types:
            return
        seen = self._robot_types_seen.setdefault(robot, set())
        ordered = self._robot_types_ordered.setdefault(robot, [])
        for t in types:
            if t and t not in seen:
                seen.add(t)
                ordered.append(t)

    def _start_new_doc(self):
        # Attach any pending header/topic to the new doc
        self.cur_lines = []
        self.cur_header_lines = self.pending_header_lines
        # Resolve robot + episodic types for this new doc
        robot, types = _split_topic(self.pending_topic)
        self.cur_robot = robot
        self._record_types(robot, types)
        # reset pending for subsequent doc
        self.pending_header_lines = []
        self.pending_topic = None
        self.capturing_pending_header = False
        self.started_doc = True

    def _ensure_doc_started(self):
        # Start lazily when we see first body line (for files without leading '---')
        if not self.started_doc:
            self._start_new_doc()

    def _flush_doc(self):
        if not self.started_doc:
            return
        if not self.cur_lines and not self.cur_header_lines:
            self.started_doc = False
            return
        target: Optional[IO[str]] = None
        if self.cur_robot:
            target = self._out_robot_tmp(self.cur_robot)
        elif self.emit_unknown:
            target = self._out_unknown()
        # Write if we have a bottom (unknown disabled means drop stray docs)
        if target:
            target.write("---\n")
            if self.cur_header_lines:
                target.writelines(self.cur_header_lines)
                if not str(self.cur_header_lines[-1]).endswith("\n"):
                    target.write("\n")
            if self.cur_lines:
                target.writelines(self.cur_lines)
                if not str(self.cur_lines[-1]).endswith("\n"):
                    target.write("\n")
        # Reset current doc state
        self.cur_lines = []
        self.cur_header_lines = []
        self.cur_robot = ""
        self.started_doc = False

    # ---------- main ----------
    def split(self) -> Dict[str, Path]:
        with self.src.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                # New doc separator
                if DOC_SEP_RE.match(line):
                    self._flush_doc()
                    self._start_new_doc()
                    continue

                # Capture pending header for the *next* doc
                mtopic = TOPIC_LINE_RE.match(line)
                if mtopic:
                    self.capturing_pending_header = True
                    self.pending_topic = mtopic.group(1)
                    self.pending_header_lines.append(line)
                    continue

                if self.capturing_pending_header:
                    # Keep only comment/blank lines inside the header block
                    if COMMENT_LINE_RE.match(line) or line.strip() == "":
                        self.pending_header_lines.append(line)
                        continue
                    else:
                        # End of header block; fall through to body handling
                        self.capturing_pending_header = False

                # Normal body line
                self._ensure_doc_started()
                self.cur_lines.append(line)

            # EOF: flush last (possibly half) doc
            self._flush_doc()

        # Close temps and rename to final names with episodic types in order of first appearance
        result: Dict[str, Path] = {}
        for robot, h in self._handles.items():
            tmp_path = Path(h.name)
            h.close()
            types = self._robot_types_ordered.get(robot, [])
            suffix = "_" + "_".join(types) if types else ""
            final_name = f"{robot}{suffix}.schema.yaml"
            final_path = self.out_dir / final_name
            if final_path.exists():
                final_path.unlink()
            tmp_path.rename(final_path)
            result[robot] = final_path

        if self._unknown:
            p = Path(self._unknown.name)
            self._unknown.close()
            result["unknown"] = p

        return result


if __name__ == "__main__":
    # Simple interactive CLI
    src = input("Input YAML file str_path: ").strip()
    while not src or not Path(src).exists():
        print("File not found. Please enter a valid str_path.")
        src = input("Input YAML file str_path: ").strip()

    default_out = str(Path(src).parent)
    out_dir = input(f"Output directory [default: {default_out}]: ").strip() or default_out

    ans = input("Write docs without '# topic:' into unknown.schema.yaml? [y/N]: ").strip().lower()
    emit_unknown = ans == "y"

    splitter = UltraFastNamedSplitter(src, out_dir=out_dir, emit_unknown=emit_unknown)
    out_map = splitter.split()
    for rid, path in out_map.items():
        print(f"{rid}: {path}")
