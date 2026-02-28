from nd_robotic.robot.state.state import State
from nd_physics.quantity.kind.dynamic.kinematic.pose.position.position import Position as PhysicsQuantityPosition


class Position(State, PhysicsQuantityPosition):
    """
    """

    def __init__(self, x: float, y: float, z: float):
        PhysicsQuantityPosition.__init__(self, x, y, z)
        State.__init__(self)
