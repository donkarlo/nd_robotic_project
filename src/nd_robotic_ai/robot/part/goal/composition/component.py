from nd_utility.oop.design_pattern.structural.composition.component import Component as BaseComponent


class Component(BaseComponent):
    def __init__(self, name: str):
        BaseComponent.__init__(self, name)

