from ./component import Component
from nd_utility.oop.design_pattern.structural.composite.leaf import Leaf as BaseLeaf
from typing import Optional

class Leaf(Component, BaseLeaf):
    def __init__(self, name:Optional[str]):
        BaseLeaf.__init__(self, name)