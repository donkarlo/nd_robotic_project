from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


@dataclass(frozen=True)
class ScheduledItem:
    day: date
    time_value: Optional[time]
    time_raw: str
    title: str
    detail: str
    kind: str
    children_titles: List[str]
    reminders: List[str]

    def event_datetime(self) -> Optional[datetime]:
        if self.time_value is None:
            return None
        return datetime.combine(self.day, self.time_value)


class ByDateTimeLoader:
    def load(self, yaml_file_path: str) -> Tuple[Dict[date, List[ScheduledItem]], Any]:
        path = Path(yaml_file_path)
        if not path.exists():
            raise FileNotFoundError(str(path))

        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file) or {}

        items_by_day: Dict[date, List[ScheduledItem]] = {}

        if not isinstance(raw, dict):
            raise ValueError("by_date_time.yaml root must be a dict")

        for year_key, months in raw.items():
            year = int(year_key)
            if not isinstance(months, dict):
                continue

            for month_key, days in months.items():
                month = int(month_key)
                if not isinstance(days, dict):
                    continue

                for day_key, entries in days.items():
                    day_int = int(day_key)
                    the_day = date(year, month, day_int)

                    normalized_entries = self._normalize_day_entries(entries)
                    parsed_items = []
                    for entry in normalized_entries:
                        parsed_items.append(self._parse_entry(the_day, entry))

                    items_by_day.setdefault(the_day, []).extend(parsed_items)

        return items_by_day, raw

    def normalize_and_sort_raw(self, raw: Any) -> Any:
        if not isinstance(raw, dict):
            return raw

        # Sort year/month/day descending; within day sort by time ascending, pending last
        sorted_years = sorted([int(k) for k in raw.keys()], reverse=True)
        new_root: Dict[int, Any] = {}

        for year in sorted_years:
            months = raw.get(year)
            if months is None:
                months = raw.get(str(year))
            if not isinstance(months, dict):
                continue

            sorted_months = sorted([int(k) for k in months.keys()], reverse=True)
            new_months: Dict[int, Any] = {}

            for month in sorted_months:
                days = months.get(month)
                if days is None:
                    days = months.get(str(month))
                if not isinstance(days, dict):
                    continue

                sorted_days = sorted([int(k) for k in days.keys()], reverse=True)
                new_days: Dict[int, Any] = {}

                for day in sorted_days:
                    entries = days.get(day)
                    if entries is None:
                        entries = days.get(str(day))

                    normalized = self._normalize_day_entries(entries)
                    normalized_sorted = sorted(normalized, key=self._entry_sort_key)
                    new_days[day] = normalized_sorted

                new_months[month] = new_days

            new_root[year] = new_months

        return new_root

    def save(self, yaml_file_path: str, raw: Any) -> None:
        path = Path(yaml_file_path)
        with path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(raw, file, sort_keys=False, allow_unicode=True)

    def _normalize_day_entries(self, entries: Any) -> List[Dict[str, Any]]:
        if entries is None:
            return []

        if isinstance(entries, list):
            normalized: List[Dict[str, Any]] = []
            for item in entries:
                if isinstance(item, dict):
                    normalized.append(item)
            return normalized

        if isinstance(entries, dict):
            return [entries]

        return []

    def _parse_entry(self, the_day: date, entry: Dict[str, Any]) -> ScheduledItem:
        time_raw = str(entry.get("time", "pending")).strip()
        time_value = self._parse_time(time_raw)

        title = str(entry.get("title", entry.get("subject", ""))).strip()
        detail = str(entry.get("detail", "")).strip()
        kind = str(entry.get("composition", "")).strip()

        children_titles: List[str] = []
        children_raw = entry.get("children", [])
        if isinstance(children_raw, list):
            for child in children_raw:
                if isinstance(child, dict):
                    child_title = str(child.get("title", "")).strip()
                    if child_title:
                        children_titles.append(child_title)

        reminders: List[str] = []
        reminder_raw = entry.get("reminder", [])
        if isinstance(reminder_raw, list):
            reminders = [str(x) for x in reminder_raw]

        return ScheduledItem(
            day=the_day,
            time_value=time_value,
            time_raw=time_raw,
            title=title,
            detail=detail,
            kind=kind,
            children_titles=children_titles,
            reminders=reminders,
        )

    def _parse_time(self, raw: str) -> Optional[time]:
        text = str(raw).strip().lower()
        if text == "pending" or text == "":
            return None

        # Accept HH:MM
        parts = text.split(":")
        if len(parts) != 2:
            return None

        try:
            hour = int(parts[0])
            minute = int(parts[1])
            return time(hour=hour, minute=minute)
        except Exception:
            return None

    def _entry_sort_key(self, entry: Dict[str, Any]) -> Tuple[int, int, int]:
        raw_time = str(entry.get("time", "pending")).strip().lower()
        if raw_time == "pending" or raw_time == "":
            return (1, 99, 99)

        parts = raw_time.split(":")
        if len(parts) != 2:
            return (1, 99, 99)

        try:
            hour = int(parts[0])
            minute = int(parts[1])
            return (0, hour, minute)
        except Exception:
            return (1, 99, 99)
