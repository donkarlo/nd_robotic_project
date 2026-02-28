from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Child:
    title: str
    duration_seconds: int
