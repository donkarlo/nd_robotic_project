from nd_robotic.robot.robot import Actuator
from typing import List
from typing import Optional


class Collection:
    def __init__(self, actuators:List[Actuator], parent_name:Optional[str]=None, name:Optional[str] = None):
        self.__name = name
        self._parent_name = parent_name
        self._actuators = actuators

    def get_name(self)->Optional[str]:
        return self.__name

    def get_parent_name(self)->Optional[str]:
        return self._parent_name

    def get_actuators(self)->List[Actuator]:
        return self._actuators