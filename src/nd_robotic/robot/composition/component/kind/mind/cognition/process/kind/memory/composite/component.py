from nd_utility.oop.design_pattern.structural.composition.component import Component as BaseComponent


class Component(BaseComponent):
    """
    - The component, either inner_experiment or composition can only have one internal_trace_group
    """
    def __init__(self):
        """

        Args:
            internal_trace_group: we use a action_potential_group here because in memory meaningful things should be stored and meaning arises only from a population
            title:
        """
        BaseComponent.__init__(self)

