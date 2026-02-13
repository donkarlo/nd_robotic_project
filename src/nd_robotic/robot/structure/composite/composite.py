from nd_robotic.robot.structure.composite.component import Component as StructureComponent
from nd_robotic.robot.structure.structure import Structure
from nd_utility.oop.design_pattern.structural.composite.composite import Composite as BaseComposite


class Composite(StructureComponent, BaseComposite):
    def __init__(self, structure:Structure):
        StructureComponent.__init__(self, structure)
        BaseComposite.__init__(self, structure)