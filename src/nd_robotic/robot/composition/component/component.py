from nd_utility.oop.design_pattern.structural.composition.component import Component as BaseComponent

class Component(BaseComponent):
    def __init__(self):
        BaseComponent.__init__(self)

    def evolve(self):
        """
        for example build more memory nodes
        Returns:

        """
        pass