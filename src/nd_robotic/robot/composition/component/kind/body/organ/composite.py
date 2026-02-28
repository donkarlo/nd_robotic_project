from nd_robotic.robot.composition.component.kind.body.organ.tissue.tissue import Tissue
from nd_robotic.robot.composition.composite import Composite as RoboticCompositeUnit
from nd_utility.oop.inheritance.overriding.override_from import override_from


class Composite(RoboticCompositeUnit):
    @override_from(RoboticCompositeUnit, False, False)
    def add_child(self, child: Union[Tissue, Organ]) -> None:
        if not isinstance(child, Tissue):
            raise TypeError("Organ child must be of type Tissue")
        self.add_child(child)