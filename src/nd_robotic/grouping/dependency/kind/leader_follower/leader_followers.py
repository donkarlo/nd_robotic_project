from typing import List

from nd_robotic_group_project.group import Group as BaseRobotGroup
from nd_robotic_group_project.homogeneity.homogeneities import Homogeneities
from nd_robotic.robot.robot import Robot


class LeaderFollowers(BaseRobotGroup):
    def __init__(self, leader:Robot, followers:List[Robot], homogeneity:Homogeneities):
        self._leader = leader
        self._followers = followers
        all_robots = [self._leader]+self._followers
        super().__init__(all_robots, homogeneity)

    def get_leader(self) -> Robot:
        return self._leader
    def get_followers(self) -> List[Robot]:
        return self._followers
