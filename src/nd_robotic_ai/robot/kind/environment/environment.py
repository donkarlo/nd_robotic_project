from nd_robotic_ai.robot.robot import Robot


class Environment(Robot):
    """
    Environment is a classification of robot that we study its intraction with other robots and vise versa
    - this robot should include the obstacles
    - the mind of this robot is mostely formed of physics rules
    """
    def __init__(self):
        """

        Args:
            body: Body contains the walls etc. Body most probably is defined by a map such as occupancy grid map
            mind: mind contains the physical ruls of the environment, such as earth
        """
        Robot.__init__(self)
