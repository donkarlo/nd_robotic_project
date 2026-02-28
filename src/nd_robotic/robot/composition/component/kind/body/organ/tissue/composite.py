from nd_robotic.robot.composition.component.kind.body.organ.tissue.tissue import Tissue
from nd_robotic.robot.composition.composite import Composite as RoboticComposite


class Composite(RoboticComposite):
    def add_child(self, child: Tissue) -> None:
        if not isinstance(child, Tissue):
            raise TypeError("Composite Tissue child must be of type Tissue")
        self.add_child(child)