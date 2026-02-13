from nd_robotic.robot.robot import Mind
from nd_robotic.robot.robot import Body
from nd_robotic.robot.robot import Robot


class Human(Robot):
    def __init__(self, body:Body, mind:Mind):
        super().__init__(body, mind)

    def talk(self, message):
        pass