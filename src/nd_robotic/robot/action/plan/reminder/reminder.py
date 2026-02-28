from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Set, Tuple

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from nd_robotic.robot.action.kind.core.kinds.duration_parser import DurationParser
from nd_robotic.robot.action.kind.core.kinds.repository import Repository
from nd_robotic.robot.action.kind.core.kinds.time_formatter import TimeFormatter
from nd_robotic.robot.action.kind.core.kinds.yaml_kinds_loader import YamlKindsLoader
from nd_robotic.robot.action.plan.reminder.communication.interface.main_window import MainWindow, UiPlanSnapshot
from nd_robotic.robot.action.plan.reminder.communication.interface.speech_synthesizer import SpeechSynthesizer
from nd_robotic.robot.action.plan.reminder.schedule.by_date_time_loader import ByDateTimeLoader, ScheduledItem
from nd_robotic.robot.action.plan.reminder.schedule.reminder_offset_parser import ReminderOffsetParser


class Reminder:
    def __init__(self, yaml_action_kinds_file_path: str, yaml_plan_by_date_time_file_path: Optional[str] = None) -> None:
        self._yaml_action_kinds_file_path = yaml_action_kinds_file_path
        self._yaml_plan_by_date_time_file_path = yaml_plan_by_date_time_file_path

        self._duration_parser = DurationParser()
        self._kinds_loader = YamlKindsLoader(duration_parser=self._duration_parser)
        self._by_date_time_loader = ByDateTimeLoader()
        self._reminder_offset_parser = ReminderOffsetParser()

        self._speech = SpeechSynthesizer()
        self._time_formatter = TimeFormatter()

        self._app = QApplication.instance()
        if self._app is None:
            self._app = QApplication([])

        initial_kinds = self._kinds_loader.load(self._yaml_action_kinds_file_path).plans
        self._repository = Repository(plans=initial_kinds, speak_callback=self._speech.speak)

        self._window = MainWindow(repository=self._repository, time_formatter=self._time_formatter)

        # scheduling state
        self._spoken_triggers: Set[str] = set()
        self._last_checked_datetime: datetime = datetime.now()
        self._cached_by_day: Dict = {}

        # periodic refresh
        self._refresh_timer = QTimer()
        self._refresh_timer.setInterval(60_000)
        self._refresh_timer.timeout.connect(self._reload_all)

        # schedule checker (speech)
        self._schedule_timer = QTimer()
        self._schedule_timer.setInterval(1_000)
        self._schedule_timer.timeout.connect(self._check_schedule)

        self._reload_all()

    def run(self) -> None:
        self._window.show()
        QTimer.singleShot(500, lambda: self._speech.speak("Reminder started"))
        self._refresh_timer.start()
        self._schedule_timer.start()
        self._app.exec()

    def _reload_all(self) -> None:
        kinds = self._kinds_loader.load(self._yaml_action_kinds_file_path).plans
        self._repository.set_plans(kinds)

        by_day = {}
        if self._yaml_plan_by_date_time_file_path is not None:
            by_day, raw = self._by_date_time_loader.load(self._yaml_plan_by_date_time_file_path)
            normalized = self._by_date_time_loader.normalize_and_sort_raw(raw)

            # Save only if changed (cheap string compare)
            if self._safe_dump(raw) != self._safe_dump(normalized):
                self._by_date_time_loader.save(self._yaml_plan_by_date_time_file_path, normalized)
                by_day, _ = self._by_date_time_loader.load(self._yaml_plan_by_date_time_file_path)

        self._cached_by_day = by_day

        self._window.set_snapshot(UiPlanSnapshot(kinds=kinds, by_day=by_day))

    def _safe_dump(self, raw) -> str:
        import yaml

        return yaml.safe_dump(raw, sort_keys=False, allow_unicode=True)

    def _check_schedule(self) -> None:
        if self._yaml_plan_by_date_time_file_path is None:
            return

        now = datetime.now()
        last = self._last_checked_datetime

        # Speak only for triggers that became due since the previous tick.
        # This prevents missing events when the check interval is larger than a small "safety window",
        # while still ignoring anything that happened before the program started.
        for day, items in self._cached_by_day.items():
            for item in items:
                event_dt = item.event_datetime()
                if event_dt is None:
                    continue

                # Reminder triggers
                for rem_raw in item.reminders:
                    try:
                        offset = self._reminder_offset_parser.parse(rem_raw)
                    except Exception:
                        continue

                    trigger_dt = event_dt - self._seconds_to_timedelta(offset.seconds_before)
                    trigger_key = f"rem|{day.isoformat()}|{event_dt.isoformat()}|{item.title}|{rem_raw}"

                    if trigger_key in self._spoken_triggers:
                        continue

                    if last < trigger_dt <= now:
                        self._speech.speak(f"Reminder {rem_raw} for action {item.title}")
                        self._spoken_triggers.add(trigger_key)

                # Event trigger
                event_key = f"evt|{day.isoformat()}|{event_dt.isoformat()}|{item.title}"
                if event_key not in self._spoken_triggers:
                    if last < event_dt <= now:
                        self._speech.speak(item.title)
                        if item.reminders:
                            self._speech.speak("Reminders: " + ", ".join(item.reminders))
                        self._spoken_triggers.add(event_key)

        self._last_checked_datetime = now

    def _seconds_to_timedelta(self, seconds: int):
        from datetime import timedelta

        return timedelta(seconds=int(seconds))
