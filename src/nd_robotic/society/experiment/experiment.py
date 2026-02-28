from nd_robotic.society.composition.composite.composite import Composite  as RoboticGroupComposite


class Experiment:
    def __init__(self, robotic_group_composite: RoboticGroupComposite):
        """

        Args:
            robotic_group_composite: world is already inside this
        """
        self._robotic_group_composite = robotic_group_composite

    def get_robotic_group_composite(self)-> RoboticGroupComposite:
        return self._robotic_group_composite