from nd_robotic.robot.robot import Component
from nd_robotic.robot.robot import Decorator
from nd_robotic.robot.robot import Segregator


class Segregatored(Decorator):
    """
    A segregating must be provoked when the system can not predict. maybe, some how, that I dont know at the moment of writing this. I mean it must happen on observing high anomary

    # Automatic triggers cases:
        - To try to reduce suprise

    """
    def __init__(self, inner: Component, segregator:Segregator)->None:
        Decorator.__init__(self, inner)
        self._segregator = segregator

    def get_segregator(self)->Segregator:
        return self._segregator

    def create_segregated_componnets_as_children(self) -> None:
        segregated_components = self._segregator.get_segregated_components()
        for segregated_component in segregated_components:
            self.add_child(segregated_component)

    def stringify(self) -> str:
        return self._inner.stringify()



