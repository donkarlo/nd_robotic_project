from dataclasses import dataclass

from nd_robotic.robot.robot import \
    Chunk


@dataclass(frozen=True)
class RetrievalHit:
    score: float
    chunk: Chunk