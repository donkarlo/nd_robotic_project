from __future__ import annotations

from typing import List

from PySide6.QtWidgets import QTreeWidgetItem


class ToPlanTreeBuilder:
    """
    Builds a QTreeWidgetItem tree from YAML-loaded python objects.
    """

    def build_top_level_items(self, data) -> List[QTreeWidgetItem]:
        if isinstance(data, dict):
            items: List[QTreeWidgetItem] = []
            for key, value in data.items():
                node = QTreeWidgetItem([str(key), self._format_scalar_if_scalar(value)])
                self._fill_children(node, value)
                items.append(node)
            return items

        root = QTreeWidgetItem(["root", self._format_scalar_if_scalar(data)])
        self._fill_children(root, data)
        return [root]

    def _fill_children(self, parent: QTreeWidgetItem, value) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                child = QTreeWidgetItem([str(k), self._format_scalar_if_scalar(v)])
                parent.addChild(child)
                self._fill_children(child, v)
            return

        if isinstance(value, list):
            for index, v in enumerate(value):
                child = QTreeWidgetItem([f"[{index}]", self._format_scalar_if_scalar(v)])
                parent.addChild(child)
                self._fill_children(child, v)
            return

    def _format_scalar_if_scalar(self, value) -> str:
        if isinstance(value, dict):
            if len(value) == 0:
                return "{}"
            return ""
        if isinstance(value, list):
            if len(value) == 0:
                return "[]"
            return ""
        if value is None:
            return "null"
        return str(value)