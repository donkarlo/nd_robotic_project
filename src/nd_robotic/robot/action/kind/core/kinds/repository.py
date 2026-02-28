from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from PySide6.QtCore import QObject, QTimer, Signal

from nd_robotic.robot.action.kind.core.kinds.kind import Kind


@dataclass(frozen=True)
class ActiveState:
    action_title: str
    child_index: int
    remaining_seconds: int
    paused: bool


class Repository(QObject):
    ticked = Signal()
    state_changed = Signal()

    def __init__(self, plans: List[Kind], speak_callback: Optional[Callable[[str], None]] = None) -> None:
        super().__init__()

        self._plans_by_title: Dict[str, Kind] = {}
        self._active_action_title: Optional[str] = None
        self._active_child_index: int = 0
        self._remaining_seconds: int = 0
        self._paused: bool = False

        self._speak_callback = speak_callback

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_tick)

        self.set_plans(plans)

    def set_plans(self, plans: List[Kind]) -> None:
        self._plans_by_title = {plan.title: plan for plan in plans}
        self.state_changed.emit()

    def get_plans(self) -> List[Kind]:
        return list(self._plans_by_title.values())

    def get_plan(self, title: str) -> Optional[Kind]:
        return self._plans_by_title.get(title)

    def get_active_state(self) -> Optional[ActiveState]:
        if self._active_action_title is None:
            return None
        return ActiveState(
            action_title=self._active_action_title,
            child_index=self._active_child_index,
            remaining_seconds=self._remaining_seconds,
            paused=self._paused,
        )

    def is_running(self) -> bool:
        return self._active_action_title is not None and (not self._paused)

    def is_paused(self) -> bool:
        return self._active_action_title is not None and self._paused

    def stop(self, announce_finished: bool = False) -> None:
        """Stop the current action.

        Notes:
            This repository stops the current action for two reasons:
                1) The user starts another action (switching).
                2) The current action reaches its natural end.

            Only in case (2) we announce "Finished".
        """
        if announce_finished and self._active_action_title is not None:
            self._speak("Finished")

        self._timer.stop()
        self._active_action_title = None
        self._active_child_index = 0
        self._remaining_seconds = 0
        self._paused = False
        self.state_changed.emit()

    def pause(self) -> None:
        if self._active_action_title is None:
            return
        self._paused = True
        self.state_changed.emit()

    def resume(self) -> None:
        if self._active_action_title is None:
            return
        self._paused = False
        if not self._timer.isActive():
            self._timer.start()
        self.state_changed.emit()

    def start_action(self, action_title: str, start_child_index: int = 0) -> None:
        plan = self._plans_by_title.get(action_title)
        if plan is None:
            return

        if len(plan.children) == 0:
            self.stop(announce_finished=False)
            self._active_action_title = plan.title
            self._active_child_index = 0
            self._remaining_seconds = 0
            self._paused = False
            self.state_changed.emit()
            self._speak(plan.title)
            return

        if start_child_index < 0:
            start_child_index = 0
        if start_child_index >= len(plan.children):
            start_child_index = len(plan.children) - 1

        # Stop previous action (do not announce 'Finished' while switching).
        self.stop(announce_finished=False)

        self._active_action_title = plan.title
        self._active_child_index = start_child_index
        self._remaining_seconds = plan.children[start_child_index].duration_seconds
        self._paused = False

        self._timer.start()
        self.state_changed.emit()

        self._speak(plan.title)
        self._speak(plan.children[start_child_index].title)

    def _on_tick(self) -> None:
        if self._active_action_title is None:
            self._timer.stop()
            return

        if self._paused:
            self.ticked.emit()
            return

        if self._remaining_seconds > 0:
            self._remaining_seconds -= 1
            self.ticked.emit()
            self.state_changed.emit()

            # If we just reached zero, immediately transition in the same tick.
            if self._remaining_seconds > 0:
                return

        # Move to next child
        plan = self._plans_by_title.get(self._active_action_title)
        if plan is None:
            self.stop(announce_finished=True)
            return

        next_index = self._active_child_index + 1
        if next_index >= len(plan.children):
            self.stop(announce_finished=True)
            return

        self._active_child_index = next_index
        self._remaining_seconds = plan.children[next_index].duration_seconds
        self.ticked.emit()
        self.state_changed.emit()

        self._speak(plan.children[next_index].title)

    def _speak(self, text: str) -> None:
        if self._speak_callback is None:
            return
        try:
            cleaned = str(text).strip()
            if not cleaned:
                return
            self._speak_callback(cleaned)
        except Exception:
            return
