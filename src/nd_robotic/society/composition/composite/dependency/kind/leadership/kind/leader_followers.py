from typing import List
from nd_robotic.robot.robot import Robot
from nd_robotic.society.composition.composite.composite import Composite


class LeaderFollowers(Composite):
    def __init__(self, leader:Robot, followers:List[Robot]):
        self._leader = leader
        self._followers = followers
        self.add_child(self._leader)
        for follower in self._followers:
            self.add_child(follower)


    def get_leader(self) -> Robot:
        return self._leader
    def get_followers(self) -> List[Robot]:
        return self._followers
