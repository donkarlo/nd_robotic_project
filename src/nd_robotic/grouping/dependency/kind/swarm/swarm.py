from nd_robotic_group_project.decorator.homogeneoused import Homogeneous
from nd_robotic_group_project.group import Group


class Swarm(Group):
    """Ever lasting swarm that tries to keep homostatis situation from sun can be used for gardeh afshani"""
    def __init__(self):
        super().__init__(self, Homogeneous.homogeneous)