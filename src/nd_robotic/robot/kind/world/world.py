from nd_robotic.robot.composition.component.kind.body.body import Body
from nd_robotic.robot.composition.component.kind.mind.mind import Mind
from nd_robotic.robot.robot import Robot


class World(Robot):
    """
    World is a composition of robot that we study its intraction with other robots and vise versa
    - this robot should include the obstacles
    - the mind of this robot is mostely formed of physics rules
    """
    def __init__(self, body:Body, mind:Mind):
        """

        Args:
            body: Body contains the walls etc. Body most probably is defined by a map such as occupancy grid map
            mind: mind contains the physical ruls of the world, such as earth
        """
        Robot.__init__(self, body, mind)
