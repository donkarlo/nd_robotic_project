from __future__ import annotations

from dataclasses import dataclass
from typing import List

from nd_robotic.robot.action.kind.core.kinds.children import Child


@dataclass(frozen=True)
class Kind:
    title: str
    children: List[Child]
