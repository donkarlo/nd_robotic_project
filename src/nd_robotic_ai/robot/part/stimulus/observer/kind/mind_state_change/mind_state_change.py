from nd_robotic_ai.robot.part.mind.state.state import State as MentalState
from nd_robotic_ai.robot.part.stimulus.stimulus import Stimulus


class MindStateChange(Stimulus):
    def __init__(self, start_state: MentalState, end_state: MentalState):
        self._state_state = start_state
        self._end_state = end_state

    def get_start_mental_state(self) -> MentalState:
        return self._start_mental_state

    def get_end_mind_state(self) -> MentalState:
        return self._end_mental_state
