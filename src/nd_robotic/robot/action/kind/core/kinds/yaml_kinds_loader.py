from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

import yaml

from nd_robotic.robot.action.kind.core.kinds.children import Child
from nd_robotic.robot.action.kind.core.kinds.duration_parser import DurationParser
from nd_robotic.robot.action.kind.core.kinds.kind import Kind


@dataclass(frozen=True)
class LoadedKinds:
    # Preserve YAML order by storing a list
    plans: List[Kind]


class YamlKindsLoader:
    """Loads kinds.yaml.

    This loader is intentionally permissive because the user maintains the YAML manually.

    Supported root formats:
        - dict: {ActionTitle: <children_def>, ...}
        - list: [{title: ActionTitle, children: <children_def>}, ...]

    Supported children formats (per action):
        - dict: {ChildTitle: "10min", ...}
        - list of dicts:
            - {title: ChildTitle, duration: "10min"}
            - {name: ChildTitle, duration: "10min"}
            - {ChildTitle: "10min"}  (single-key dict)
        - list of strings:
            - "ChildTitle"  (treated as 0 seconds)

    Missing durations are treated as 0 seconds.
    Invalid child entries are ignored.
    """

    def __init__(self, duration_parser: DurationParser) -> None:
        self._duration_parser = duration_parser

    def load(self, yaml_file_path: str) -> LoadedKinds:
        path = Path(yaml_file_path)
        if not path.exists():
            raise FileNotFoundError(str(path))

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        plans = self._parse_root(data)
        return LoadedKinds(plans=plans)

    def _parse_root(self, data: Any) -> List[Kind]:
        if isinstance(data, list):
            return self._parse_list_root(data)

        if isinstance(data, dict):
            plans: List[Kind] = []
            for action_title, children_raw in data.items():
                plans.append(self._parse_action(title=str(action_title), children_raw=children_raw))
            return plans

        raise ValueError("kinds.yaml must be a dict or list")

    def _parse_list_root(self, data: List[Any]) -> List[Kind]:
        plans: List[Kind] = []
        for item in data:
            if not isinstance(item, dict):
                continue

            title = str(item.get("title", "")).strip()
            if not title:
                continue

            children_raw = item.get("children", [])
            plans.append(self._parse_action(title=title, children_raw=children_raw))
        return plans

    def _parse_action(self, title: str, children_raw: Any) -> Kind:
        children: List[Child] = []

        if isinstance(children_raw, dict):
            for child_title, duration_raw in children_raw.items():
                child_title_text = str(child_title).strip()
                if not child_title_text:
                    continue
                seconds = self._safe_parse_seconds(duration_raw)
                children.append(Child(title=child_title_text, duration_seconds=seconds))
            return Kind(title=title, children=children)

        if isinstance(children_raw, list):
            for child in children_raw:
                if isinstance(child, str):
                    child_title_text = child.strip()
                    if child_title_text:
                        children.append(Child(title=child_title_text, duration_seconds=0))
                    continue

                if not isinstance(child, dict):
                    continue

                child_title_text = str(child.get("title", child.get("name", ""))).strip()
                duration_raw = child.get("duration", child.get("time", None))

                if not child_title_text:
                    # Single-key dict fallback: {"Sprechen": "10min"}
                    if len(child) == 1:
                        only_key = next(iter(child.keys()))
                        child_title_text = str(only_key).strip()
                        duration_raw = child[only_key]

                if not child_title_text:
                    continue

                seconds = self._safe_parse_seconds(duration_raw)
                children.append(Child(title=child_title_text, duration_seconds=seconds))

            return Kind(title=title, children=children)

        # None or unsupported types
        return Kind(title=title, children=children)

    def _safe_parse_seconds(self, duration_raw: Any) -> int:
        if duration_raw is None:
            return 0

        duration_text = str(duration_raw).strip()
        if not duration_text:
            return 0

        try:
            return self._duration_parser.parse_to_seconds(duration_text)
        except Exception:
            return 0
