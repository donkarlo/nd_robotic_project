from __future__ import annotations

import re


class DurationParser:
    _PATTERN = re.compile(r"^\s*(\d+)\s*([a-zA-Z]+)\s*$")

    def parse_to_seconds(self, raw: str) -> int:
        if raw is None:
            raise ValueError("Duration is None")

        text = str(raw).strip().lower()
        if text.isdigit():
            # Assume seconds
            return int(text)

        match = self._PATTERN.match(text)
        if match is None:
            raise ValueError(f"Unsupported duration format: {raw!r}")

        value = int(match.group(1))
        unit = match.group(2)

        if unit in ["s", "sec", "secs", "second", "seconds"]:
            return value
        if unit in ["m", "min", "mins", "minute", "minutes"]:
            return value * 60
        if unit in ["h", "hr", "hrs", "hour", "hours"]:
            return value * 3600
        if unit in ["d", "day", "days"]:
            return value * 86400

        raise ValueError(f"Unsupported duration unit: {unit!r}")
