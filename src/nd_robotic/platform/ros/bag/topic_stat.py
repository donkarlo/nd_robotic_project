from dataclasses import dataclass
from typing import Optional

@dataclass
class TopicStat:
    topic: str
    count: int
    t_min: Optional[float]  # seconds since epoch (from header.stamp) or None
    t_max: Optional[float]
    freq_avg_hz: Optional[float]  # average frequency over span; None if unknown (e.g., bag without span)
    # You can add more fields later (e.g., median), but we keep it minimal per request.