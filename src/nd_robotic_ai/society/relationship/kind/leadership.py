from nd_robotic_ai.society.relationship.relationship import Relation
from nd_robotic_ai.society.component import Component as SocietyComponent


class Leadership(Relation):
    def __init__(self, left: SocietyComponent, right: SocietyComponent):
        Relation.__init__(self, left, right)