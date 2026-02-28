from nd_utility.oop.design_pattern.structural.composition.component import Component as BaseComponent
from typing import Optional

class Component(BaseComponent):
    def __init__(self, name: Optional[str]):
        BaseComponent.__init__(self, name)