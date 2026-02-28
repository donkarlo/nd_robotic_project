from nd_physics.quantity.kind.dynamic.kinematic.pose.pose import Pose
from nd_robotic.robot.state.state import State


class FullPose(State):
    def __init__(self, pos:Pose):
        '''
        Fill in with best estimation which is done out of here.
        it is not a place for estimation. it is just to hold separated action_potential_group.
        '''
        pass
