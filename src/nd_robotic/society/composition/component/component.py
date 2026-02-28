from nd_utility.oop.design_pattern.structural.composition.component import Component as BaseComponent

class Component(BaseComponent):
    """
    This component is shared by both the grouping and the composition
    """

    def __init__(self):
        BaseComponent.__init__(self)

