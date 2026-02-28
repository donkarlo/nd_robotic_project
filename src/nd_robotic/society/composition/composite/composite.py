from typing import Optional

from nd_robotic.society.composition.component.component import Component
from nd_robotic.society.composition.composite.dependency.dependency import Dependency
from nd_robotic.society.composition.composite.homogeneity.homogeneity import Homogeneity
from nd_utility.data.kind.group.group import Group
from nd_utility.oop.design_pattern.structural.composition.composite import Composite as BaseComposite


class Composite(Component, BaseComposite):
    """
    The leaf here is a Group
    """

    def __init__(self, children: Group, dependency: Optional[Dependency], homogeneity: Optional[Homogeneity]):
        """

        Args:
            children:
            dependency:
        """
        BaseComposite.__init__(self, children)
        self._dependency = dependency
        self._homogeneity = homogeneity

    def get_dependency(self) -> Dependency:
        return self._dependency
