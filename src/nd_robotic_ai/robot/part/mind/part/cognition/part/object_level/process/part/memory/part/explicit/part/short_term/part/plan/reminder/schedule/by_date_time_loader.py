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
    _meta_keys = {
        "reminder",
        "reminders",
        "detail",
        "classification",
        "classification",
        "parts",
    }

    def load(self, yaml_file_path: str) -> Tuple[Dict[date, List[ScheduledItem]], Any]:
        path = Path(yaml_file_path)
        if not path.exists():
            raise FileNotFoundError(str(path))

        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file) or {}

        items_by_day: Dict[date, List[ScheduledItem]] = {}

        if not isinstance(raw, dict):
            raise ValueError("by_date_time yaml root must be a mapping")

        for year_key, months in raw.items():
            if not isinstance(months, dict):
                continue

            year_value = int(year_key)

            for month_key, days in months.items():
                if not isinstance(days, dict):
                    continue

                month_value = int(month_key)

                for day_key, entries in days.items():
                    the_day = date(year_value, month_value, int(day_key))
                    normalized_entries = self._normalize_day_entries(entries)

                    parsed_items: List[ScheduledItem] = []
                    for entry in normalized_entries:
                        parsed_items.append(self._parse_entry(the_day, entry))

                    items_by_day.setdefault(the_day, []).extend(parsed_items)

        return items_by_day, raw

    def normalize_and_sort_raw(self, raw: Any) -> Any:
        if not isinstance(raw, dict):
            return raw

        normalized_root: Dict[int, Any] = {}

        year_keys = sorted([int(key) for key in raw.keys()], reverse=True)
        for year_key in year_keys:
            months = raw.get(year_key)
            if months is None:
                months = raw.get(str(year_key))
            if not isinstance(months, dict):
                continue

            normalized_months: Dict[int, Any] = {}

            month_keys = sorted([int(key) for key in months.keys()], reverse=True)
            for month_key in month_keys:
                days = months.get(month_key)
                if days is None:
                    days = months.get(str(month_key))
                if not isinstance(days, dict):
                    continue

                normalized_days: Dict[int, Any] = {}

                day_keys = sorted([int(key) for key in days.keys()], reverse=True)
                for day_key in day_keys:
                    entries = days.get(day_key)
                    if entries is None:
                        entries = days.get(str(day_key))

                    normalized_entries = self._normalize_day_entries(entries)
                    normalized_entries = sorted(normalized_entries, key=self._entry_sort_key)
                    normalized_days[int(day_key)] = normalized_entries

                normalized_months[int(month_key)] = normalized_days

            normalized_root[int(year_key)] = normalized_months

        return normalized_root

    def save(self, yaml_file_path: str, raw: Any) -> None:
        path = Path(yaml_file_path)
        with path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(raw, file, sort_keys=False, allow_unicode=True)

    def _normalize_day_entries(self, entries: Any) -> List[Dict[str, Any]]:
        if entries is None:
            return []

        if isinstance(entries, list):
            normalized_entries: List[Dict[str, Any]] = []
            for entry in entries:
                if isinstance(entry, dict):
                    normalized_entries.append(entry)
            return normalized_entries

        if isinstance(entries, dict):
            return [entries]

        return []

    def _parse_entry(self, the_day: date, entry: Dict[str, Any]) -> ScheduledItem:
        title, time_raw = self._extract_title_and_time(entry)
        time_value = self._parse_time(time_raw)

        detail_value = ""
        if "detail" in entry:
            detail_value = str(entry.get("detail", "")).strip()

        kind_value = ""
        if "classification" in entry:
            kind_value = str(entry.get("classification", "")).strip()
        elif "classification" in entry and not isinstance(entry.get("classification"), list):
            kind_value = str(entry.get("classification", "")).strip()

        children_titles: List[str] = []
        children_raw = entry.get("parts", [])
        if isinstance(children_raw, list):
            for child in children_raw:
                if isinstance(child, dict):
                    child_title = str(child.get("title", "")).strip()
                    if child_title != "":
                        children_titles.append(child_title)

        reminders: List[str] = []

        reminders_raw = entry.get("reminders")
        if isinstance(reminders_raw, list):
            for reminder in reminders_raw:
                reminders.append(str(reminder))

        reminder_raw = entry.get("reminder")
        if isinstance(reminder_raw, list):
            for reminder in reminder_raw:
                reminders.append(str(reminder))

        return ScheduledItem(
            day=the_day,
            time_value=time_value,
            time_raw=time_raw,
            title=title,
            detail=detail_value,
            kind=kind_value,
            children_titles=children_titles,
            reminders=reminders,
        )

    def _extract_title_and_time(self, entry: Dict[str, Any]) -> Tuple[str, str]:
        for key, value in entry.items():
            if key in self._meta_keys:
                continue
            return str(key).strip(), str(value).strip()
        return "", "pending"

    def _parse_time(self, raw: str) -> Optional[time]:
        text = str(raw).strip().lower()

        if text in {"pending", "pernding", "unplanned", ""}:
            return None

        parts = text.split(":")
        if len(parts) != 2:
            return None

        try:
            hour_value = int(parts[0])
            minute_value = int(parts[1])
        except ValueError:
            return None

        try:
            return time(hour=hour_value, minute=minute_value)
        except ValueError:
            return None

    def _entry_sort_key(self, entry: Dict[str, Any]) -> Tuple[int, int, int, str]:
        title, time_raw = self._extract_title_and_time(entry)
        normalized_time = str(time_raw).strip().lower()

        if normalized_time in {"pending", "pernding", "unplanned", ""}:
            return (1, 99, 99, title.lower())

        parts = normalized_time.split(":")
        if len(parts) != 2:
            return (1, 99, 99, title.lower())

        try:
            hour_value = int(parts[0])
            minute_value = int(parts[1])
            return (0, hour_value, minute_value, title.lower())
        except ValueError:
            return (1, 99, 99, title.lower())