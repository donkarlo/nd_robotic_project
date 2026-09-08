from typing import Union

from nd_robotic_ai.robot.composition.kind.body.organ.organ import Organ
from nd_robotic_ai.robot.composition.kind.body.organ.tissue.tissue import Tissue
from nd_robotic_ai.robot.composition.composite import Composite as RobotCompositeUnit


class Limb(RobotCompositeUnit):
    """
    Limb = موتور/عملگر داخل مفصل
    In persian it is azoleh, in english it is muscle.
    It is whatever that can convert a control signal to a movement
    """
    def __init__(self):
        pass

    def add_child(self, child: Union[Tissue, Organ]) -> None:
        if not isinstance(child, (Organ, Tissue)):
            raise TypeError("Limb classification must be of type Organ or Tissue")


