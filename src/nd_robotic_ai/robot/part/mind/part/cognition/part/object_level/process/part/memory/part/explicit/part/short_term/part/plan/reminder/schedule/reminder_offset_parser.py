from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class ReminderOffset:
    raw: str
    seconds_before: int


class ReminderOffsetParser:
    _NUMERIC = re.compile(r"^\s*(\d+)\s*([a-zA-Z]+)\s+before\s*$", re.IGNORECASE)
    _WORD = re.compile(r"^\s*([a-zA-Z]+)\s+([a-zA-Z]+)\s+before\s*$", re.IGNORECASE)

    _WORDS = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    def parse(self, raw: str) -> ReminderOffset:
        text = str(raw).strip().lower()

        match_num = self._NUMERIC.match(text)
        if match_num is not None:
            value = int(match_num.group(1))
            unit = match_num.group(2)
            seconds = self._to_seconds(value=value, unit=unit)
            return ReminderOffset(raw=raw, seconds_before=seconds)

        match_word = self._WORD.match(text)
        if match_word is not None:
            word = match_word.group(1)
            unit = match_word.group(2)
            value = self._WORDS.get(word)
            if value is None:
                raise ValueError(f"Unsupported word number in reminder: {raw!r}")
            seconds = self._to_seconds(value=value, unit=unit)
            return ReminderOffset(raw=raw, seconds_before=seconds)

        raise ValueError(f"Unsupported reminder format: {raw!r}")

    def _to_seconds(self, value: int, unit: str) -> int:
        u = unit.strip().lower()

        if u in ["s", "sec", "secs", "second", "seconds"]:
            return int(timedelta(seconds=value).total_seconds())
        if u in ["m", "min", "mins", "minute", "minutes"]:
            return int(timedelta(minutes=value).total_seconds())
        if u in ["h", "hr", "hrs", "hour", "hours"]:
            return int(timedelta(hours=value).total_seconds())
        if u in ["d", "day", "days"]:
            return int(timedelta(days=value).total_seconds())
        if u in ["month", "months"]:
            # Approximation (30 days)
            return int(timedelta(days=value * 30).total_seconds())

        raise ValueError(f"Unsupported reminder unit: {unit!r}")
