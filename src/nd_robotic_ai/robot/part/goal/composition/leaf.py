from nd_robotic_ai.robot.composition.leaf import Leaf as RobotLeaf
from nd_robotic_ai.robot.state.state import State
from nd_robotic_ai.robot.part.goal.acceptance.acceptance import Acceptance


class Leaf(RobotLeaf):
    def __init__(self, desired_state: State, acceptance: Acceptance):
        RobotLeaf.__init__(self, )
        self._acceptance = acceptance
        self._desired_state = desired_state

    def get_acceptance(self) -> Acceptance:
        return self._acceptance

    def get_desired_state(self) -> State:
        return self._desired_state