import math
from nd_robotic.robot.robot import AcceptanceCriterion
from nd_physics.quantity.kind.dynamic.kinematic.pose.position.position import Position


class PositionToleranceCriterion(AcceptanceCriterion):
    """
    GoalGain is satisfied if the Euclidean distance between
    current and desired positions is below a threshold.
    """

    def __init__(self, tolerance: float):
        self._tolerance = tolerance

    def is_satisfied(self, desired_position: Position, current_position: Position) -> bool:
        dx = current_position.x - desired_position.x
        dy = current_position.y - desired_position.y
        dz = current_position.z - desired_position.z
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)
        return distance <= self._tolerance
