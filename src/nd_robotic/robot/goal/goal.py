from nd_robotic.robot.goal.acceptance.acceptance import Acceptance
from nd_robotic.robot.goal.composite.component import Component as ComponentGoal
from nd_utility.oop.design_pattern.structural.composition.leaf import Leaf as BaseLeaf
from nd_robotic.robot.state.state import State


class Goal(ComponentGoal, BaseLeaf):
    '''
    TODO: should be replaced with a higher level composite_goal and
    it is formed of a state for example for a quad it can be 3d position, pitch, yaw role
    This is a single role
    - GoalGain is not a tangibeable concept. GoalGain is tangeable. DeliverMission or CorridorInspectionMission. But GoalGain needs tangeable points and in the world such as GoTo point.
    - if an role is breakable to smaller actions then it is actually a initial_mission
    '''

    def __init__(self, desired_state:State, acceptance: Acceptance):
        ComponentGoal.__init__(self, None)
        BaseLeaf.__init__(self, None)
        self._acceptance = acceptance
        self._desired_state = desired_state


    def get_name(self) -> str:
        return self._name

    def get_acceptance(self) -> Acceptance:
        return self._acceptance

    def get_desired_state(self)->State:
        return self._desired_state
