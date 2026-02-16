from nd_utility.oop.design_pattern.structural.composite.composite import Composite as BaseComposite
from ./component import Component
from ./leaf import Leaf
from typing import Optional

class Composite(Component, BaseComposite):
    """
    Composite node that can hold other Components.
    """

    def __init__(self, leaf: Leaf, name: Optional[str]):
        BaseComposite.__init__(self, leaf, name)
        Component.__init__(self, name)