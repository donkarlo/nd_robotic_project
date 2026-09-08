from nd_robotic_ai.robot.robot import Mind
from nd_robotic_ai.robot.robot import Body
from nd_robotic_ai.robot.robot import Robot


class Human(Robot):
    def __init__(self):
        Robot.__init__(self)

    def talk(self, message):
        pass