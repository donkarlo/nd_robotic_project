from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.thinking.concept_formation.concept_formation import \
    ConceptFormation
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.thinking.decision_making.decision_making import \
    DecisionMaking
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.thinking.problem_soving.problem_solving import \
    ProblemSolving
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.thinking.reasoning.reasoning import \
    Reasoning
from nd_robotic.robot.composition.composite import Composite


class Thinking(Composite):
    def __init__(self, decision_making:DecisionMaking, concept_formation:ConceptFormation, problem_solvoing:ProblemSolving, reasoning:Reasoning):
        pass