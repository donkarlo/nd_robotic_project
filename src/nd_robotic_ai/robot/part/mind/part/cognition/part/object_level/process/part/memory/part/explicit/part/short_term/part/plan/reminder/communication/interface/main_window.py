from __future__ import annotations

import shutil
import subprocess
from calendar import monthrange
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from PySide6.QtCore import QDate, QPoint, Qt, QUrl, Signal
from PySide6.QtGui import QAction, QBrush, QColor, QDesktopServices
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCalendarWidget,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from nd_robotic_ai.robot.part.action.kind.repository import Repository
from nd_robotic_ai.robot.part.action.kind.time_based.formatter import Formatter
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.communication.interface.refresh_button import RefreshButton
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.communication.interface.to_plan_tree_builder import ToPlanTreeBuilder
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.communication.interface.ui_plan_snapshot import UiPlanSnapshot
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.short_term.part.plan.reminder.schedule.by_date_time_loader import ScheduledItem

ITEM_TYPE_ROLE = Qt.UserRole + 1
DAY_ROLE = Qt.UserRole + 2
TIME_RAW_ROLE = Qt.UserRole + 3
TITLE_ROLE = Qt.UserRole + 4
IS_BLUE_WEEK_ROLE = Qt.UserRole + 5

ITEM_TYPE_DAY_HEADER = "day_header"
ITEM_TYPE_TASK = "task"
ITEM_TYPE_NOTE = "note"
ITEM_TYPE_MONTH_SEPARATOR = "month_separator"


class ScheduleTreeWidget(QTreeWidget):
    task_moved = Signal(date, date, str, str)

    def __init__(self) -> None:
        QTreeWidget.__init__(self)

        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setTextElideMode(Qt.ElideNone)

    def dropEvent(self, event) -> None:
        selected_items = self.selectedItems()
        if len(selected_items) == 0:
            event.ignore()
            return

        dragged_item = selected_items[0]
        if dragged_item.data(0, ITEM_TYPE_ROLE) != ITEM_TYPE_TASK:
            event.ignore()
            return

        source_header = dragged_item.parent()
        if source_header is None:
            event.ignore()
            return

        if source_header.data(0, ITEM_TYPE_ROLE) != ITEM_TYPE_DAY_HEADER:
            event.ignore()
            return

        target_item = self.itemAt(event.position().toPoint())
        target_header = self._resolve_day_header(target_item)

        if target_header is None:
            event.ignore()
            return

        if target_header == source_header:
            event.ignore()
            return

        source_day_text = source_header.data(0, DAY_ROLE)
        target_day_text = target_header.data(0, DAY_ROLE)

        if not isinstance(source_day_text, str) or not isinstance(target_day_text, str):
            event.ignore()
            return

        source_index = source_header.indexOfChild(dragged_item)
        if source_index < 0:
            event.ignore()
            return

        moved_item = source_header.takeChild(source_index)
        target_header.addChild(moved_item)

        self._update_day_role_recursively(moved_item, target_day_text)
        self._adopt_target_week_style(target_header, moved_item)
        self._sort_day_header_children(source_header)
        self._sort_day_header_children(target_header)

        source_header.setExpanded(True)
        target_header.setExpanded(True)
        self.setCurrentItem(moved_item)

        title_text = moved_item.data(2, TITLE_ROLE)
        if not isinstance(title_text, str) or title_text.strip() == "":
            title_text = moved_item.text(2)

        time_raw_text = moved_item.data(1, TIME_RAW_ROLE)
        if not isinstance(time_raw_text, str) or time_raw_text.strip() == "":
            time_raw_text = moved_item.text(1)

        self.task_moved.emit(
            date.fromisoformat(source_day_text),
            date.fromisoformat(target_day_text),
            time_raw_text,
            title_text,
        )

        event.acceptProposedAction()

    def _resolve_day_header(self, item: Optional[QTreeWidgetItem]) -> Optional[QTreeWidgetItem]:
        current = item
        while current is not None:
            if current.data(0, ITEM_TYPE_ROLE) == ITEM_TYPE_DAY_HEADER:
                return current
            current = current.parent()
        return None

    def _update_day_role_recursively(self, item: QTreeWidgetItem, day_text: str) -> None:
        item.setData(0, DAY_ROLE, day_text)
        for index in range(item.childCount()):
            self._update_day_role_recursively(item.child(index), day_text)

    def _adopt_target_week_style(self, header_item: QTreeWidgetItem, moved_item: QTreeWidgetItem) -> None:
        is_blue_week = header_item.data(0, IS_BLUE_WEEK_ROLE)
        if not isinstance(is_blue_week, bool):
            is_blue_week = False

        moved_item.setData(0, IS_BLUE_WEEK_ROLE, is_blue_week)
        self._apply_task_background(moved_item, is_blue_week)

        for index in range(moved_item.childCount()):
            child = moved_item.child(index)
            self._apply_note_background_recursive(child, is_blue_week)

    def _apply_note_background_recursive(self, item: QTreeWidgetItem, is_blue_week: bool) -> None:
        item.setData(0, IS_BLUE_WEEK_ROLE, is_blue_week)
        self._apply_note_background(item, is_blue_week)
        for index in range(item.childCount()):
            self._apply_note_background_recursive(item.child(index), is_blue_week)

    def _sort_day_header_children(self, day_header_item: QTreeWidgetItem) -> None:
        children: List[QTreeWidgetItem] = []

        while day_header_item.childCount() > 0:
            children.append(day_header_item.takeChild(0))

        children.sort(key=self._task_item_sort_key)

        for child in children:
            day_header_item.addChild(child)

    def _task_item_sort_key(self, item: QTreeWidgetItem) -> Tuple[int, int, int, str]:
        time_raw = item.data(1, TIME_RAW_ROLE)
        if not isinstance(time_raw, str) or time_raw.strip() == "" or time_raw.lower() in {"pending", "pernding",
                                                                                           "unplanned"}:
            return (1, 99, 99, item.text(2).lower())

        parts = time_raw.split(":")
        if len(parts) != 2:
            return (1, 99, 99, item.text(2).lower())

        try:
            hour = int(parts[0])
            minute = int(parts[1])
        except ValueError:
            return (1, 99, 99, item.text(2).lower())

        return (0, hour, minute, item.text(2).lower())

    def _apply_task_background(self, item: QTreeWidgetItem, is_blue_week: bool) -> None:
        if is_blue_week:
            color = QBrush(QColor(223, 234, 255))
            item.setBackground(0, color)
            item.setBackground(1, color)
            item.setBackground(2, color)
        else:
            item.setBackground(0, QBrush())
            item.setBackground(1, QBrush())
            item.setBackground(2, QBrush())

    def _apply_note_background(self, item: QTreeWidgetItem, is_blue_week: bool) -> None:
        if is_blue_week:
            color = QBrush(QColor(231, 240, 255))
            item.setBackground(0, color)
            item.setBackground(1, color)
            item.setBackground(2, color)
        else:
            item.setBackground(0, QBrush())
            item.setBackground(1, QBrush())
            item.setBackground(2, QBrush())


class ScheduledItemDialog(QDialog):
    def __init__(self, dialog_title: str, initial_date: date, initial_title: str, initial_time: str,
                 parent: Optional[QWidget] = None) -> None:
        QDialog.__init__(self, parent)

        self.setWindowTitle(dialog_title)
        self.resize(460, 180)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        self._title_input = QLineEdit(initial_title)
        self._time_input = QLineEdit(initial_time)
        self._time_input.setPlaceholderText("9:30 or pending")
        self._date_button = QPushButton(initial_date.isoformat())
        self._selected_date = initial_date

        form_layout.addRow("Title", self._title_input)
        form_layout.addRow("Time", self._time_input)
        form_layout.addRow("Date", self._date_button)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._date_button.clicked.connect(self._choose_date)

    def _choose_date(self) -> None:
        dialog = DatePickerDialog(initial_date=self._selected_date, parent=self)
        if dialog.exec():
            self._selected_date = dialog.selected_python_date()
            self._date_button.setText(self._selected_date.isoformat())

    def selected_python_date(self) -> date:
        return self._selected_date

    def entered_title(self) -> str:
        return self._title_input.text().strip()

    def entered_time(self) -> str:
        return self._time_input.text().strip()


class DatePickerDialog(QDialog):
    def __init__(self, initial_date: date, parent: Optional[QWidget] = None) -> None:
        QDialog.__init__(self, parent)

        self.setWindowTitle("Choose date")
        self.resize(420, 340)

        layout = QVBoxLayout(self)

        self._calendar = QCalendarWidget()
        self._calendar.setGridVisible(True)
        self._calendar.setSelectedDate(QDate(initial_date.year, initial_date.month, initial_date.day))
        layout.addWidget(self._calendar)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def selected_python_date(self) -> date:
        selected = self._calendar.selectedDate()
        return date(selected.year(), selected.month(), selected.day())


class MainWindow(QMainWindow):
    def __init__(
            self,
            repository: Repository,
            time_formatter: Formatter,
            yaml_action_kinds_file_path: Optional[str],
            yaml_plan_by_date_time_file_path: Optional[str],
            yaml_to_plan_file_path: Optional[str],
            reload_callback: Optional[Callable[[], None]] = None,
            move_scheduled_item_callback: Optional[Callable[[date, date, str, str], None]] = None,
            add_scheduled_item_callback: Optional[Callable[[date, str, str], None]] = None,
            delete_scheduled_item_callback: Optional[Callable[[date, str, str], None]] = None,
            edit_scheduled_item_callback: Optional[Callable[[date, str, str, date, str, str], None]] = None,
    ) -> None:
        QMainWindow.__init__(self)

        self._repository = repository
        self._time_formatter = time_formatter
        self._yaml_action_kinds_file_path = yaml_action_kinds_file_path
        self._yaml_plan_by_date_time_file_path = yaml_plan_by_date_time_file_path
        self._yaml_to_plan_file_path = yaml_to_plan_file_path
        self._reload_callback = reload_callback
        self._move_scheduled_item_callback = move_scheduled_item_callback
        self._add_scheduled_item_callback = add_scheduled_item_callback
        self._delete_scheduled_item_callback = delete_scheduled_item_callback
        self._edit_scheduled_item_callback = edit_scheduled_item_callback

        self._snapshot: Optional[UiPlanSnapshot] = None

        self._root = QWidget()
        self.setCentralWidget(self._root)

        self._build_ui()

        self._repository.state_changed.connect(self.refresh_right)
        self._repository.ticked.connect(self.refresh_right)

        self.setWindowTitle("Reminder")
        self.resize(1240, 760)

    def _build_ui(self) -> None:
        root_layout = QHBoxLayout(self._root)

        left_box = self._build_left_box()
        middle_box = self._build_middle_box()
        right_box = self._build_right_box()

        root_layout.addWidget(left_box, 1)
        root_layout.addWidget(middle_box, 1)
        root_layout.addWidget(right_box, 1)

    def _build_left_box(self) -> QGroupBox:
        left_box = QGroupBox("By date_time_based")
        left_layout = QVBoxLayout(left_box)

        top_row = QHBoxLayout()
        self._edit_by_date_time_button = QPushButton("Edit file")
        top_row.addWidget(self._edit_by_date_time_button)
        top_row.addStretch(1)
        left_layout.addLayout(top_row)

        self._left_tree = ScheduleTreeWidget()
        self._left_tree.setColumnCount(3)
        self._left_tree.setHeaderLabels(["Week", "When", "Title"])
        self._left_tree.header().setStretchLastSection(True)
        self._left_tree.header().setSectionResizeMode(0, self._left_tree.header().ResizeMode.Fixed)
        self._left_tree.header().setSectionResizeMode(1, self._left_tree.header().ResizeMode.Fixed)
        self._left_tree.header().setSectionResizeMode(2, self._left_tree.header().ResizeMode.Stretch)
        self._left_tree.setColumnWidth(0, 42)
        self._left_tree.setColumnWidth(1, 125)
        left_layout.addWidget(self._left_tree)

        self._edit_by_date_time_button.clicked.connect(
            lambda: self._open_in_pycharm(self._yaml_plan_by_date_time_file_path)
        )
        self._left_tree.task_moved.connect(self._on_task_moved_between_days)
        self._left_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self._left_tree.customContextMenuRequested.connect(self._open_left_tree_context_menu)

        return left_box

    def _build_middle_box(self) -> QGroupBox:
        middle_box = QGroupBox("Kinds")
        middle_layout = QVBoxLayout(middle_box)

        controls_row = QHBoxLayout()
        self._edit_kinds_button = QPushButton("Edit file")
        controls_row.addWidget(self._edit_kinds_button)
        controls_row.addStretch(1)

        self._refresh_button = RefreshButton()
        self._refresh_button.refresh_requested.connect(self._on_refresh_clicked)
        controls_row.addWidget(self._refresh_button)
        middle_layout.addLayout(controls_row)

        self._status_label = QLabel("MindWandering")
        middle_layout.addWidget(self._status_label)

        self._kinds_tree = QTreeWidget()
        self._kinds_tree.setColumnCount(3)
        self._kinds_tree.setHeaderLabels(["Title", "Remaining", "Control"])
        self._kinds_tree.setSelectionMode(QAbstractItemView.NoSelection)
        self._kinds_tree.setTextElideMode(Qt.ElideNone)
        self._kinds_tree.header().setStretchLastSection(False)
        self._kinds_tree.header().setSectionResizeMode(0, self._kinds_tree.header().ResizeMode.Stretch)
        self._kinds_tree.header().setSectionResizeMode(1, self._kinds_tree.header().ResizeMode.ResizeToContents)
        self._kinds_tree.header().setSectionResizeMode(2, self._kinds_tree.header().ResizeMode.ResizeToContents)
        middle_layout.addWidget(self._kinds_tree)

        self._edit_kinds_button.clicked.connect(
            lambda: self._open_in_pycharm(self._yaml_action_kinds_file_path)
        )

        return middle_box

    def _build_right_box(self) -> QGroupBox:
        right_box = QGroupBox("To plan")
        right_layout = QVBoxLayout(right_box)

        controls_row = QHBoxLayout()
        self._edit_to_plan_button = QPushButton("Edit file")
        controls_row.addWidget(self._edit_to_plan_button)

        self._to_plan_expand_all = QPushButton("Expand all")
        self._to_plan_collapse_all = QPushButton("Close all")
        controls_row.addWidget(self._to_plan_expand_all)
        controls_row.addWidget(self._to_plan_collapse_all)
        controls_row.addStretch(1)
        right_layout.addLayout(controls_row)

        self._to_plan_tree = QTreeWidget()
        self._to_plan_tree.setColumnCount(2)
        self._to_plan_tree.setHeaderLabels(["Item", "Value"])
        self._to_plan_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        self._to_plan_tree.setTextElideMode(Qt.ElideNone)
        self._to_plan_tree.header().setStretchLastSection(True)
        right_layout.addWidget(self._to_plan_tree)

        self._to_plan_expand_all.clicked.connect(self._to_plan_tree.expandAll)
        self._to_plan_collapse_all.clicked.connect(self._to_plan_tree.collapseAll)
        self._to_plan_tree.itemActivated.connect(self._on_to_plan_item_activated)

        self._edit_to_plan_button.clicked.connect(
            lambda: self._open_in_pycharm(self._yaml_to_plan_file_path)
        )

        return right_box

    def set_snapshot(self, snapshot: UiPlanSnapshot) -> None:
        self._snapshot = snapshot
        self.refresh_left()
        self.refresh_right()
        self.refresh_to_plan()

    def set_status_message(self, text: str) -> None:
        self._status_label.setText(text)

    def _on_refresh_clicked(self) -> None:
        if self._reload_callback is not None:
            self._reload_callback()

    def _open_left_tree_context_menu(self, position: QPoint) -> None:
        clicked_item = self._left_tree.itemAt(position)
        if clicked_item is not None:
            self._left_tree.setCurrentItem(clicked_item)

        target_day = self._resolve_context_menu_day(clicked_item)
        clicked_task = self._resolve_context_menu_task(clicked_item)

        menu = QMenu(self)

        add_action = QAction("Add", self)
        add_action.triggered.connect(lambda: self._open_add_dialog_for_day(target_day))
        menu.addAction(add_action)

        edit_action = QAction("Edit", self)
        edit_action.setEnabled(clicked_task is not None)
        if clicked_task is not None:
            edit_action.triggered.connect(lambda: self._open_edit_dialog_for_item(clicked_task))
        menu.addAction(edit_action)

        delete_action = QAction("Delete", self)
        delete_action.setEnabled(clicked_task is not None)
        if clicked_task is not None:
            delete_action.triggered.connect(lambda: self._delete_task_with_confirmation(clicked_task))
        menu.addAction(delete_action)

        menu.exec(self._left_tree.viewport().mapToGlobal(position))

    def _resolve_context_menu_day(self, item: Optional[QTreeWidgetItem]) -> date:
        current_item = item
        while current_item is not None:
            if current_item.data(0, ITEM_TYPE_ROLE) == ITEM_TYPE_DAY_HEADER:
                day_text = current_item.data(0, DAY_ROLE)
                if isinstance(day_text, str):
                    return date.fromisoformat(day_text)
                break
            current_item = current_item.parent()
        return datetime.now().date()

    def _resolve_context_menu_task(self, item: Optional[QTreeWidgetItem]) -> Optional[QTreeWidgetItem]:
        if item is None:
            return None
        if item.data(0, ITEM_TYPE_ROLE) == ITEM_TYPE_TASK:
            return item
        return None

    def _open_add_dialog_for_day(self, target_day: date) -> None:
        dialog = ScheduledItemDialog(
            dialog_title="Add action",
            initial_date=target_day,
            initial_title="",
            initial_time="pending",
            parent=self,
        )
        if not dialog.exec():
            return

        title = dialog.entered_title()
        time_raw = dialog.entered_time()
        if title == "":
            self._status_label.setText("Task title is empty")
            return

        if time_raw == "":
            time_raw = "pending"

        if self._add_scheduled_item_callback is None:
            self._status_label.setText("Add callback is not configured")
            return

        try:
            self._add_scheduled_item_callback(dialog.selected_python_date(), title, time_raw)
        except Exception as ex:
            self._status_label.setText(f"Add failed: {ex}")

    def _open_edit_dialog_for_item(self, task_item: QTreeWidgetItem) -> None:
        source_day_text = task_item.data(0, DAY_ROLE)
        source_time_raw = task_item.data(1, TIME_RAW_ROLE)
        source_title = task_item.data(2, TITLE_ROLE)

        if not isinstance(source_day_text, str) or not isinstance(source_time_raw, str) or not isinstance(source_title, str):
            self._status_label.setText("Could not read selected task")
            return

        dialog = ScheduledItemDialog(
            dialog_title="Edit action",
            initial_date=date.fromisoformat(source_day_text),
            initial_title=source_title,
            initial_time=source_time_raw,
            parent=self,
        )
        if not dialog.exec():
            return

        new_title = dialog.entered_title()
        new_time_raw = dialog.entered_time()
        if new_title == "":
            self._status_label.setText("Task title is empty")
            return

        if new_time_raw == "":
            new_time_raw = "pending"

        if self._edit_scheduled_item_callback is None:
            self._status_label.setText("Edit callback is not configured")
            return

        try:
            self._edit_scheduled_item_callback(
                date.fromisoformat(source_day_text),
                source_title,
                source_time_raw,
                dialog.selected_python_date(),
                new_title,
                new_time_raw,
            )
        except Exception as ex:
            self._status_label.setText(f"Edit failed: {ex}")

    def _delete_task_with_confirmation(self, task_item: QTreeWidgetItem) -> None:
        source_day_text = task_item.data(0, DAY_ROLE)
        source_time_raw = task_item.data(1, TIME_RAW_ROLE)
        source_title = task_item.data(2, TITLE_ROLE)

        if not isinstance(source_day_text, str) or not isinstance(source_time_raw, str) or not isinstance(source_title, str):
            self._status_label.setText("Could not read selected task")
            return

        answer = QMessageBox.question(
            self,
            "Delete action",
            "Are you sure you want to delete this action from the plan?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        if self._delete_scheduled_item_callback is None:
            self._status_label.setText("Delete callback is not configured")
            return

        try:
            self._delete_scheduled_item_callback(
                date.fromisoformat(source_day_text),
                source_title,
                source_time_raw,
            )
        except Exception as ex:
            self._status_label.setText(f"Delete failed: {ex}")

    def _selected_day_from_left_tree(self) -> Optional[date]:
        selected_items = self._left_tree.selectedItems()
        if len(selected_items) == 0:
            return None

        current_item = selected_items[0]
        while current_item is not None:
            if current_item.data(0, ITEM_TYPE_ROLE) == ITEM_TYPE_DAY_HEADER:
                day_text = current_item.data(0, DAY_ROLE)
                if isinstance(day_text, str):
                    return date.fromisoformat(day_text)
                return None
            current_item = current_item.parent()

        return None

    def _on_task_moved_between_days(self, source_day: date, target_day: date, time_raw: str, title: str) -> None:
        if self._move_scheduled_item_callback is None:
            self._status_label.setText(
                f"Moved in UI only: {title} | {source_day.isoformat()} -> {target_day.isoformat()}"
            )
            return

        try:
            self._move_scheduled_item_callback(source_day, target_day, time_raw, title)
            self._status_label.setText(f"Moved: {title} | {source_day.isoformat()} -> {target_day.isoformat()}")
        except Exception as ex:
            self._status_label.setText(f"Move failed: {ex}")

    def refresh_to_plan(self) -> None:
        if self._snapshot is None:
            return

        self._to_plan_tree.clear()

        data = self._snapshot.to_plan
        if data is None:
            return

        builder = ToPlanTreeBuilder()
        top_items = builder.build_top_level_items(data)

        for item in top_items:
            self._to_plan_tree.addTopLevelItem(item)

        self._to_plan_tree.collapseAll()
        for index in range(self._to_plan_tree.topLevelItemCount()):
            self._to_plan_tree.topLevelItem(index).setExpanded(False)

    def _on_to_plan_item_activated(self, item: QTreeWidgetItem, column: int) -> None:
        text = item.text(1).strip()
        if text == "":
            return

        url = self._normalize_url(text)
        if url is None:
            return

        QDesktopServices.openUrl(QUrl(url))

    def _normalize_url(self, text: str) -> Optional[str]:
        lowered = text.lower()
        if lowered.startswith("http://") or lowered.startswith("https://"):
            return text
        if lowered.startswith("www."):
            return "https://" + text
        if "amazon." in lowered and lowered.startswith("amazon."):
            return "https://" + text
        if "amazon." in lowered and lowered.startswith("www.amazon."):
            return "https://" + text
        return None

    def _open_in_pycharm(self, file_path: Optional[str]) -> None:
        if file_path is None:
            self._status_label.setText("No file path configured")
            return

        path = Path(str(file_path))
        if not path.exists():
            self._status_label.setText(f"File not found: {path}")
            return

        candidates = ["charm", "pycharm", "pycharm.sh"]
        command = None
        for candidate in candidates:
            resolved = shutil.which(candidate)
            if resolved is not None:
                command = [resolved, str(path)]
                break

        if command is None:
            resolved = shutil.which("xdg-open")
            if resolved is not None:
                command = [resolved, str(path)]

        if command is None:
            self._status_label.setText("No launcher found (charm/pycharm/xdg-open)")
            return

        try:
            subprocess.Popen(command)
            self._status_label.setText(f"Opened: {path.name}")
        except Exception as ex:
            self._status_label.setText(f"Open failed: {ex}")

    def refresh_left(self) -> None:
        if self._snapshot is None:
            return

        self._left_tree.clear()

        today = datetime.now().date()
        past_days = 15
        future_days = 16

        range_start = today - timedelta(days=past_days)
        range_end = today + timedelta(days=future_days)

        days_to_show = self._build_full_month_days(range_start, range_end)
        previous_day: Optional[date] = None

        for the_day in days_to_show:
            if previous_day is not None and previous_day.month != the_day.month:
                month_separator_item = self._create_month_separator_item(the_day)
                self._left_tree.addTopLevelItem(month_separator_item)

            day_items = self._snapshot.by_day.get(the_day, [])
            sorted_day_items = self._sort_day_items_for_display(day_items)
            current_marker = self._select_current_item_for_day(the_day, sorted_day_items)

            week_number = self._week_of_month(the_day)
            is_blue_week = week_number % 2 == 1

            displayed_week_number: Optional[str] = None
            if self._is_last_visible_day_of_week_block(the_day, days_to_show):
                displayed_week_number = str(week_number)

            header_item = self._create_day_header_item(the_day, is_blue_week, displayed_week_number)
            self._left_tree.addTopLevelItem(header_item)

            for index, item in enumerate(sorted_day_items):
                when_text = item.time_raw
                if item.time_value is None:
                    when_text = "pending"

                node = QTreeWidgetItem(["", when_text, item.title])
                self._prepare_task_item(node, the_day, when_text, item.title, is_blue_week)

                if current_marker is not None and index == current_marker:
                    self._set_item_green_bold(node)

                header_item.addChild(node)

                for child_title in item.children_titles:
                    child_node = QTreeWidgetItem(["", "", child_title])
                    self._prepare_note_item(child_node, the_day, is_blue_week)
                    node.addChild(child_node)

                if item.reminders:
                    reminders_node = QTreeWidgetItem(["", "", "reminders"])
                    self._prepare_note_item(reminders_node, the_day, is_blue_week)
                    node.addChild(reminders_node)

                    for reminder in item.reminders:
                        reminder_node = QTreeWidgetItem(["", "", str(reminder)])
                        self._prepare_note_item(reminder_node, the_day, is_blue_week)
                        reminders_node.addChild(reminder_node)

            header_item.setExpanded(True)
            previous_day = the_day

    def _build_full_month_days(self, range_start: date, range_end: date) -> List[date]:
        start_month_first_day = date(range_start.year, range_start.month, 1)
        end_month_last_day = date(
            range_end.year,
            range_end.month,
            monthrange(range_end.year, range_end.month)[1],
        )

        days: List[date] = []
        current_day = start_month_first_day
        while current_day <= end_month_last_day:
            days.append(current_day)
            current_day = current_day + timedelta(days=1)

        return sorted(days, reverse=True)

    def _is_last_visible_day_of_week_block(self, the_day: date, all_days_desc: List[date]) -> bool:
        current_key = (the_day.year, the_day.month, self._week_of_month(the_day))
        current_index = all_days_desc.index(the_day)

        if current_index == 0:
            return True

        previous_visible_day = all_days_desc[current_index - 1]
        previous_key = (previous_visible_day.year, previous_visible_day.month,
                        self._week_of_month(previous_visible_day))

        return previous_key != current_key

    def _prepare_task_item(self, item: QTreeWidgetItem, the_day: date, time_raw: str, title: str,
                           is_blue_week: bool) -> None:
        item.setData(0, ITEM_TYPE_ROLE, ITEM_TYPE_TASK)
        item.setData(0, DAY_ROLE, the_day.isoformat())
        item.setData(1, TIME_RAW_ROLE, time_raw)
        item.setData(2, TITLE_ROLE, title)
        item.setData(0, IS_BLUE_WEEK_ROLE, is_blue_week)

        flags = item.flags()
        flags = flags | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        flags = flags & ~Qt.ItemIsDropEnabled
        item.setFlags(flags)

        self._left_tree._apply_task_background(item, is_blue_week)

    def _prepare_note_item(self, item: QTreeWidgetItem, the_day: date, is_blue_week: bool) -> None:
        item.setData(0, ITEM_TYPE_ROLE, ITEM_TYPE_NOTE)
        item.setData(0, DAY_ROLE, the_day.isoformat())
        item.setData(0, IS_BLUE_WEEK_ROLE, is_blue_week)

        flags = item.flags()
        flags = flags | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        flags = flags & ~Qt.ItemIsDragEnabled
        flags = flags & ~Qt.ItemIsDropEnabled
        item.setFlags(flags)

        self._left_tree._apply_note_background(item, is_blue_week)

    def _week_of_month(self, the_day: date) -> int:
        first_day_of_month = the_day.replace(day=1)
        adjusted_day_number = the_day.day + first_day_of_month.weekday()
        return ((adjusted_day_number - 1) // 7) + 1

    def _weekday_abbreviation(self, the_day: date) -> str:
        weekday_names = {
            0: "MON",
            1: "TUE",
            2: "WED",
            3: "THU",
            4: "FRI",
            5: "SAT",
            6: "SUN",
        }
        return weekday_names[the_day.weekday()]

    def _month_abbreviation(self, month_number: int) -> str:
        month_names = {
            1: "JAN",
            2: "FEB",
            3: "MAR",
            4: "APR",
            5: "MAY",
            6: "JUN",
            7: "JUL",
            8: "AUG",
            9: "SEP",
            10: "OCT",
            11: "NOV",
            12: "DEC",
        }
        return month_names[month_number]

    def _format_day_header_title(self, the_day: date) -> str:
        return f"{the_day.isoformat()} {self._weekday_abbreviation(the_day)}"

    def _create_day_header_item(self, the_day: date, blue_week: bool,
                                displayed_week_number: Optional[str]) -> QTreeWidgetItem:
        week_text = ""
        if displayed_week_number is not None:
            week_text = f"W{displayed_week_number}"

        header_item = QTreeWidgetItem([week_text, self._format_day_header_title(the_day), ""])
        header_item.setData(0, ITEM_TYPE_ROLE, ITEM_TYPE_DAY_HEADER)
        header_item.setData(0, DAY_ROLE, the_day.isoformat())
        header_item.setData(0, IS_BLUE_WEEK_ROLE, blue_week)

        flags = header_item.flags()
        flags = flags | Qt.ItemIsEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsSelectable
        flags = flags & ~Qt.ItemIsDragEnabled
        header_item.setFlags(flags)

        font0 = header_item.font(0)
        font0.setBold(True)
        header_item.setFont(0, font0)

        font1 = header_item.font(1)
        font1.setBold(True)
        header_item.setFont(1, font1)

        header_item.setTextAlignment(0, Qt.AlignCenter)

        if blue_week:
            row_color = QBrush(QColor(223, 234, 255))
            header_item.setBackground(0, row_color)
            header_item.setBackground(1, row_color)
            header_item.setBackground(2, row_color)
        else:
            header_item.setBackground(0, QBrush())
            header_item.setBackground(1, QBrush())
            header_item.setBackground(2, QBrush())

        if week_text != "":
            if blue_week:
                header_item.setBackground(0, QBrush(QColor(75, 46, 131)))
            else:
                header_item.setBackground(0, QBrush(QColor(47, 79, 47)))
            header_item.setForeground(0, QBrush(QColor(255, 255, 255)))
        else:
            if blue_week:
                header_item.setForeground(0, QBrush(QColor(75, 46, 131)))
            else:
                header_item.setForeground(0, QBrush(QColor(47, 79, 47)))

        header_item.setForeground(1, QBrush(QColor(17, 17, 17)))
        header_item.setForeground(2, QBrush(QColor(17, 17, 17)))

        return header_item

    def _create_month_separator_item(self, the_day: date) -> QTreeWidgetItem:
        month_text = self._month_abbreviation(the_day.month)
        separator_item = QTreeWidgetItem(["", f"------------{month_text}------------", ""])
        separator_item.setData(0, ITEM_TYPE_ROLE, ITEM_TYPE_MONTH_SEPARATOR)

        flags = separator_item.flags()
        flags = flags | Qt.ItemIsEnabled
        flags = flags & ~Qt.ItemIsDragEnabled
        flags = flags & ~Qt.ItemIsDropEnabled
        separator_item.setFlags(flags)

        font1 = separator_item.font(1)
        font1.setBold(True)
        separator_item.setFont(1, font1)
        separator_item.setForeground(1, QBrush(QColor(204, 51, 51)))

        return separator_item

    def _sort_day_items_for_display(self, items: List[ScheduledItem]) -> List[ScheduledItem]:
        def key(item: ScheduledItem) -> Tuple[int, int, int, str]:
            if item.time_value is None:
                return (1, 99, 99, item.title.lower())
            return (0, item.time_value.hour, item.time_value.minute, item.title.lower())

        return sorted(items, key=key)

    def _select_current_item_for_day(self, the_day: date, items: List[ScheduledItem]) -> Optional[int]:
        if the_day != datetime.now().date():
            return None

        now = datetime.now()

        last_past_index: Optional[int] = None
        for index, item in enumerate(items):
            item_datetime = item.event_datetime()
            if item_datetime is None:
                continue
            if item_datetime <= now:
                last_past_index = index

        if last_past_index is not None:
            return last_past_index

        for index, item in enumerate(items):
            item_datetime = item.event_datetime()
            if item_datetime is None:
                continue
            if item_datetime > now:
                return index

        return None

    def refresh_right(self) -> None:
        if self._snapshot is None:
            return

        self._kinds_tree.clear()

        active_state = self._repository.get_active_state()

        current_status = self._status_label.text()
        if active_state is None:
            if current_status.startswith("Active:"):
                self._status_label.setText("MindWandering")
        else:
            self._status_label.setText(f"Active: {active_state.action_title}")

        for kind in self._snapshot.kinds:
            action_item = QTreeWidgetItem([kind.title, "", ""])
            self._kinds_tree.addTopLevelItem(action_item)
            action_item.setExpanded(True)

            action_button = QPushButton()
            self._configure_button_for_action(action_button, kind_title=kind.title, child_index=None)
            self._kinds_tree.setItemWidget(action_item, 2, action_button)

            if active_state is not None and active_state.action_title == kind.title:
                self._set_item_red_bold(action_item)
                action_item.setText(1, self._time_formatter.format_compact(active_state.remaining_seconds))

            for child_index, child in enumerate(kind.children):
                child_item = QTreeWidgetItem([child.title, "", ""])
                action_item.addChild(child_item)

                child_button = QPushButton("Start")
                self._configure_button_for_action(child_button, kind_title=kind.title, child_index=child_index)
                self._kinds_tree.setItemWidget(child_item, 2, child_button)

                if active_state is not None and active_state.action_title == kind.title and active_state.child_index == child_index:
                    self._set_item_red_bold(child_item)
                    child_item.setText(1, self._time_formatter.format_compact(active_state.remaining_seconds))

    def _configure_button_for_action(self, button: QPushButton, kind_title: str, child_index: Optional[int]) -> None:
        active = self._repository.get_active_state()

        if active is None:
            button.setText("Start")
            button.clicked.connect(
                lambda: self._repository.start_action(kind_title, 0 if child_index is None else child_index))
            return

        if active.action_title != kind_title:
            button.setText("Start")
            button.clicked.connect(
                lambda: self._repository.start_action(kind_title, 0 if child_index is None else child_index))
            return

        if child_index is None:
            if active.paused:
                button.setText("Resume")
                button.clicked.connect(self._repository.resume)
            else:
                button.setText("Pause")
                button.clicked.connect(self._repository.pause)
            return

        if active.child_index == child_index:
            if active.paused:
                button.setText("Resume")
                button.clicked.connect(self._repository.resume)
            else:
                button.setText("Pause")
                button.clicked.connect(self._repository.pause)
            return

        button.setText("Start")
        button.clicked.connect(lambda: self._repository.start_action(kind_title, child_index))

    def _set_item_red_bold(self, item: QTreeWidgetItem) -> None:
        for column_index in range(3):
            font = item.font(column_index)
            font.setBold(True)
            item.setFont(column_index, font)
            item.setForeground(column_index, QBrush(Qt.red))

    def _set_item_green_bold(self, item: QTreeWidgetItem) -> None:
        for column_index in (1, 2):
            font = item.font(column_index)
            font.setBold(True)
            item.setFont(column_index, font)

            item.setForeground(column_index, QBrush(Qt.white))
            item.setBackground(column_index, QBrush(Qt.darkGreen))