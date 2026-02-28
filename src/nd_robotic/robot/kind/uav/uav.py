from nd_robotic.robot.composition.component.kind.body.body import Body
from nd_robotic.robot.composition.component.kind.mind.mind import Mind
from nd_robotic.robot.robot import Robot


class Uav(Robot):
    def __init__(self):
        self.add_child(Mind())
        self.add_child(Body())
