from typing import List

from nd_robotic.robot.robot import Component
from nd_utility.data.kind.group.group import Group as BaseGroup


class Group(BaseGroup):
    def __init__(self, members:List[Component]):
        BaseGroup.__init__(self, members)