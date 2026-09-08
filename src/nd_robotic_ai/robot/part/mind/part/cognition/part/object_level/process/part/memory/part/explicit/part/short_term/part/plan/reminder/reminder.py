from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from nd_robotic_ai.robot.part.action.kind.core.yaml_kinds_loader import YamlKindsLoader
from nd_robotic_ai.robot.part.action.kind.repository import Repository
from nd_robotic_ai.robot.part.action.kind.time_based.duration_parser import DurationParser
from nd_robotic_ai.robot.part.action.kind.time_based.formatter import Formatter
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.communication.interface.main_window import \
    MainWindow
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.communication.interface.speech_synthesizer import \
    SpeechSynthesizer
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.communication.interface.ui_plan_snapshot import \
    UiPlanSnapshot
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.schedule.by_date_time_loader import \
    ByDateTimeLoader
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.schedule.reminder_offset_parser import \
    ReminderOffsetParser


class Reminder:
    def __init__(self, yaml_action_kinds_file_path: str, yaml_plan_by_date_time_file_path: str,
                 yaml_to_plan_file_path: Optional[str]) -> None:
        self._yaml_action_kinds_file_path = yaml_action_kinds_file_path
        self._yaml_plan_by_date_time_file_path = yaml_plan_by_date_time_file_path
        self._yaml_to_plan_file_path = yaml_to_plan_file_path

        self._duration_parser = DurationParser()
        self._kinds_loader = YamlKindsLoader(duration_parser=self._duration_parser)
        self._by_date_time_loader = ByDateTimeLoader()
        self._reminder_offset_parser = ReminderOffsetParser()

        self._speech = SpeechSynthesizer()
        self._time_formatter = Formatter()

        self._app = QApplication.instance()
        if self._app is None:
            self._app = QApplication([])

        initial_kinds = self._kinds_loader.load(self._yaml_action_kinds_file_path).plans
        self._repository = Repository(plans=initial_kinds, speak_callback=self._speech.speak)

        self._window = MainWindow(
            repository=self._repository,
            time_formatter=self._time_formatter,
            yaml_action_kinds_file_path=self._yaml_action_kinds_file_path,
            yaml_plan_by_date_time_file_path=self._yaml_plan_by_date_time_file_path,
            yaml_to_plan_file_path=self._yaml_to_plan_file_path,
            reload_callback=self.reload_manually,
            move_scheduled_item_callback=self.move_scheduled_item,
            add_scheduled_item_callback=self.add_scheduled_item,
            delete_scheduled_item_callback=self.delete_scheduled_item,
            edit_scheduled_item_callback=self.edit_scheduled_item,
        )

        self._spoken_triggers: Set[str] = set()
        self._last_checked_datetime: datetime = datetime.now()
        self._cached_by_day: Dict[Any, Any] = {}
        self._cached_raw_plan: Any = {}

        self._schedule_timer = QTimer()
        self._schedule_timer.setInterval(1000)
        self._schedule_timer.timeout.connect(self._check_schedule)

        self._reload_all()

    def run(self) -> None:
        self._window.show()
        QTimer.singleShot(500, lambda: self._speech.speak("Reminder started"))
        self._schedule_timer.start()
        self._app.exec()

    def reload_manually(self) -> None:
        self._reload_all()
        self._window.set_status_message("Reloaded")
        self._speech.speak("Reloaded")

    def _reload_all(self) -> None:
        kinds = self._kinds_loader.load(self._yaml_action_kinds_file_path).plans
        self._repository.set_plans(kinds)

        by_day = {}
        raw = {}

        if self._yaml_plan_by_date_time_file_path is not None:
            by_day, raw = self._by_date_time_loader.load(self._yaml_plan_by_date_time_file_path)
            normalized = self._by_date_time_loader.normalize_and_sort_raw(raw)

            if self._safe_dump(raw) != self._safe_dump(normalized):
                self._by_date_time_loader.save(self._yaml_plan_by_date_time_file_path, normalized)
                by_day, raw = self._by_date_time_loader.load(self._yaml_plan_by_date_time_file_path)

        self._cached_by_day = by_day
        self._cached_raw_plan = raw

        to_plan = None
        if self._yaml_to_plan_file_path is not None:
            to_plan = self._load_yaml_file_if_exists(self._yaml_to_plan_file_path)

        self._window.set_snapshot(UiPlanSnapshot(kinds=kinds, by_day=by_day, to_plan=to_plan))

    def add_scheduled_item(self, target_day: date, title: str, time_raw: str) -> None:
        if self._yaml_plan_by_date_time_file_path is None:
            raise ValueError("No by-date-time file path configured")

        if not isinstance(self._cached_raw_plan, dict):
            raise ValueError("Cached plan is not a YAML mapping")

        normalized_time = self._normalize_time_text(time_raw)
        target_entries = self._ensure_day_entries_list(self._cached_raw_plan, target_day, create_missing=True)
        target_entries.append({title: normalized_time})

        normalized = self._by_date_time_loader.normalize_and_sort_raw(self._cached_raw_plan)
        self._by_date_time_loader.save(self._yaml_plan_by_date_time_file_path, normalized)

        self._cached_raw_plan = normalized
        self._reload_all()
        self._window.set_status_message(f"Added: {title} | {target_day.isoformat()} | {normalized_time}")

    def move_scheduled_item(self, source_day: date, target_day: date, time_raw: str, title: str) -> None:
        if self._yaml_plan_by_date_time_file_path is None:
            raise ValueError("No by-date-time file path configured")

        if not isinstance(self._cached_raw_plan, dict):
            raise ValueError("Cached plan is not a YAML mapping")

        source_entries = self._ensure_day_entries_list(self._cached_raw_plan, source_day, create_missing=False)
        if source_entries is None:
            raise ValueError(f"Source day not found: {source_day.isoformat()}")

        entry_index = self._find_entry_index(source_entries, title, time_raw)
        if entry_index is None:
            raise ValueError(f"Could not find task in source day: {title} at {time_raw} on {source_day.isoformat()}")

        moved_entry = source_entries.pop(entry_index)

        target_entries = self._ensure_day_entries_list(self._cached_raw_plan, target_day, create_missing=True)
        target_entries.append(moved_entry)

        normalized = self._by_date_time_loader.normalize_and_sort_raw(self._cached_raw_plan)
        self._by_date_time_loader.save(self._yaml_plan_by_date_time_file_path, normalized)

        self._cached_raw_plan = normalized
        self._reload_all()
        self._window.set_status_message(f"Moved: {title} | {source_day.isoformat()} -> {target_day.isoformat()}")

    def delete_scheduled_item(self, source_day: date, title: str, time_raw: str) -> None:
        if self._yaml_plan_by_date_time_file_path is None:
            raise ValueError("No by-date-time file path configured")

        if not isinstance(self._cached_raw_plan, dict):
            raise ValueError("Cached plan is not a YAML mapping")

        source_entries = self._ensure_day_entries_list(self._cached_raw_plan, source_day, create_missing=False)
        if source_entries is None:
            raise ValueError(f"Source day not found: {source_day.isoformat()}")

        entry_index = self._find_entry_index(source_entries, title, time_raw)
        if entry_index is None:
            raise ValueError(f"Could not find task to delete: {title} at {time_raw} on {source_day.isoformat()}")

        source_entries.pop(entry_index)

        normalized = self._by_date_time_loader.normalize_and_sort_raw(self._cached_raw_plan)
        self._by_date_time_loader.save(self._yaml_plan_by_date_time_file_path, normalized)

        self._cached_raw_plan = normalized
        self._reload_all()
        self._window.set_status_message(f"Deleted: {title} | {source_day.isoformat()} | {time_raw}")

    def edit_scheduled_item(self, source_day: date, source_title: str, source_time_raw: str,
                            target_day: date, target_title: str, target_time_raw: str) -> None:
        if self._yaml_plan_by_date_time_file_path is None:
            raise ValueError("No by-date-time file path configured")

        if not isinstance(self._cached_raw_plan, dict):
            raise ValueError("Cached plan is not a YAML mapping")

        source_entries = self._ensure_day_entries_list(self._cached_raw_plan, source_day, create_missing=False)
        if source_entries is None:
            raise ValueError(f"Source day not found: {source_day.isoformat()}")

        entry_index = self._find_entry_index(source_entries, source_title, source_time_raw)
        if entry_index is None:
            raise ValueError(
                f"Could not find task to edit: {source_title} at {source_time_raw} on {source_day.isoformat()}"
            )

        edited_entry = source_entries.pop(entry_index)
        self._replace_title_and_time(edited_entry, target_title, target_time_raw)

        target_entries = self._ensure_day_entries_list(self._cached_raw_plan, target_day, create_missing=True)
        target_entries.append(edited_entry)

        normalized = self._by_date_time_loader.normalize_and_sort_raw(self._cached_raw_plan)
        self._by_date_time_loader.save(self._yaml_plan_by_date_time_file_path, normalized)

        self._cached_raw_plan = normalized
        self._reload_all()
        self._window.set_status_message(
            f"Edited: {source_title} -> {target_title} | {source_day.isoformat()} -> {target_day.isoformat()}"
        )

    def _ensure_day_entries_list(self, raw_root: Dict[str, Any], the_day: date, create_missing: bool) -> Optional[
        List[Dict[str, Any]]]:
        year_key = the_day.year
        month_key = the_day.month
        day_key = the_day.day

        year_node = raw_root.get(year_key)
        if year_node is None:
            year_node = raw_root.get(str(year_key))

        if year_node is None:
            if not create_missing:
                return None
            year_node = {}
            raw_root[year_key] = year_node

        if not isinstance(year_node, dict):
            raise ValueError(f"Year node is not a mapping for year {year_key}")

        month_node = year_node.get(month_key)
        if month_node is None:
            month_node = year_node.get(str(month_key))

        if month_node is None:
            if not create_missing:
                return None
            month_node = {}
            year_node[month_key] = month_node

        if not isinstance(month_node, dict):
            raise ValueError(f"Month node is not a mapping for {year_key}-{month_key}")

        day_node = month_node.get(day_key)
        if day_node is None:
            day_node = month_node.get(str(day_key))

        if day_node is None:
            if not create_missing:
                return None
            day_node = []
            month_node[day_key] = day_node

        if not isinstance(day_node, list):
            if create_missing:
                normalized_day_node: List[Dict[str, Any]] = []
                if isinstance(day_node, dict):
                    normalized_day_node.append(day_node)
                month_node[day_key] = normalized_day_node
                return normalized_day_node
            return None

        if day_key not in month_node and str(day_key) in month_node:
            month_node[day_key] = day_node
            del month_node[str(day_key)]

        if month_key not in year_node and str(month_key) in year_node:
            year_node[month_key] = month_node
            del year_node[str(month_key)]

        if year_key not in raw_root and str(year_key) in raw_root:
            raw_root[year_key] = year_node
            del raw_root[str(year_key)]

        return day_node

    def _replace_title_and_time(self, entry: Dict[str, Any], new_title: str, new_time_raw: str) -> None:
        normalized_time = self._normalize_time_text(new_time_raw)

        keys_to_keep: List[str] = []
        values_to_keep: Dict[str, Any] = {}
        for key, value in list(entry.items()):
            if key in {"reminder", "reminders", "detail", "parts", "classification", "classification"}:
                keys_to_keep.append(key)
                values_to_keep[key] = value

        entry.clear()
        entry[new_title] = normalized_time
        for key in keys_to_keep:
            entry[key] = values_to_keep[key]

    def _find_entry_index(self, entries: List[Dict[str, Any]], title: str, time_raw: str) -> Optional[int]:
        normalized_target_title = title.strip()
        normalized_target_time = self._normalize_time_text(time_raw)

        for index, entry in enumerate(entries):
            entry_title, entry_time = self._extract_title_and_time(entry)
            if entry_title.strip() == normalized_target_title and self._normalize_time_text(
                    entry_time) == normalized_target_time:
                return index

        return None

    def _extract_title_and_time(self, entry: Dict[str, Any]) -> tuple[str, str]:
        for key, value in entry.items():
            if key in {"reminder", "reminders", "detail", "parts", "classification", "classification"}:
                continue
            return str(key).strip(), str(value).strip()
        return "", "pending"

    def _normalize_time_text(self, text: str) -> str:
        value = str(text).strip().lower()
        if value in {"pending", "pernding", "unplanned", ""}:
            return "pending"
        return value

    def _safe_dump(self, raw: Any) -> str:
        import yaml
        return yaml.safe_dump(raw, sort_keys=False, allow_unicode=True)

    def _check_schedule(self) -> None:
        if self._yaml_plan_by_date_time_file_path is None:
            return

        now = datetime.now()
        last = self._last_checked_datetime

        for day, items in self._cached_by_day.items():
            for item in items:
                event_dt = item.event_datetime()
                if event_dt is None:
                    continue

                for reminder_raw in item.reminders:
                    try:
                        offset = self._reminder_offset_parser.parse(reminder_raw)
                    except Exception:
                        continue

                    trigger_dt = event_dt - timedelta(seconds=int(offset.seconds_before))
                    trigger_key = f"rem|{day.isoformat()}|{event_dt.isoformat()}|{item.title}|{reminder_raw}"

                    if trigger_key in self._spoken_triggers:
                        continue

                    if last < trigger_dt <= now:
                        self._speech.speak(f"Reminder {reminder_raw} for action {item.title}")
                        self._spoken_triggers.add(trigger_key)

                event_key = f"evt|{day.isoformat()}|{event_dt.isoformat()}|{item.title}"
                if event_key not in self._spoken_triggers:
                    if last < event_dt <= now:
                        self._speech.speak(item.title)
                        if item.reminders:
                            self._speech.speak("Reminders: " + ", ".join(item.reminders))
                        self._spoken_triggers.add(event_key)

        self._last_checked_datetime = now

    def _load_yaml_file_if_exists(self, file_path: str) -> Optional[dict]:
        import yaml

        path = Path(str(file_path))
        if not path.exists():
            return None

        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if raw is None:
            return None
        if not isinstance(raw, dict):
            return {"_root": raw}
        return raw
