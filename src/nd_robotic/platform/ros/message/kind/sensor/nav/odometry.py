from nd_math.probability.distribution.parametricity.kind.parametric.covariance_matrix import CovarianceMatrix
from nd_physics.quantity.kind.dynamic.kinematic.pose_twist_kinematic import PoseTwistKinematic
from nd_physics.quantity.decorator.distributed.gaussianed import Gaussianed
from nd_physics.quantity.kind.dynamic.kinematic.pose.pose import Pose
from nd_physics.quantity.kind.dynamic.kinematic.pose.position.position import Position
from nd_physics.quantity.kind.dynamic.kinematic.pose.orientation.quaternion import Quaternion
from nd_physics.quantity.kind.dynamic.kinematic.twist.angular import Angular
from nd_physics.quantity.kind.dynamic.kinematic.twist.linear import Linear
from nd_physics.quantity.kind.dynamic.kinematic.twist.twist import Twist
from nd_robotic.robot.robot import Timed
from nd_robotic.robot.robot import GaussianedQuaternionKinematic
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.trace import Trace
from nd_robotic.platform.ros.message.field.field import Field
from nd_robotic.platform.ros.message.message import Message
from nd_robotic.platform.ros.message.kind.header.time_stamp import TimeStamp
from nd_utility.data.kind.dic.dic import Dic
from typing import List
import numpy as np
from nd_utility.oop.klass.structure.kind.based_on_inheritence import BasedOnInheritence


class Odometry(Message):

    def __init__(self, fields:List):
        super().__init__(fields)
        self._time = self.get_field_value_by_name("time")

    @classmethod
    def init_from_dic(cls, dic: Dic) -> "Odometry":
        # fields
        fields:List[Field] = []

        # time
        time = TimeStamp.init_from_dic(dic).get_time()
        field = Field("time", time)
        fields.append(field)

        # pose
        ## position
        field = Field("position", Dic(dic["pose"]["pose"]["position"]))
        fields.append(field)

        ## orientation
        field = Field("orientation", Dic(dic["pose"]["pose"]["orientation"]))
        fields.append(field)

        ## orientation
        field = Field("pose_covarience", dic["pose"]["covariance"])
        fields.append(field)

        # twist
        ## linear
        field = Field("linear_twist", Dic(dic["twist"]["twist"]["linear"]))
        fields.append(field)

        ## angular
        field = Field("angular_twist", Dic(dic["twist"]["twist"]["angular"]))
        fields.append(field)

        ## orientation
        field = Field("twist_covarience", dic["twist"]["covariance"])
        fields.append(field)

        return cls(fields)



    def get_distributed_kinematic_trace(self)-> Trace:
        #pose
        position_field = self.get_field_value_by_name("position")
        position = Position(position_field["x"], position_field["y"], position_field["z"])

        orientation_field = self.get_field_value_by_name("orientation")
        orientation = Quaternion(orientation_field["x"], orientation_field["y"], orientation_field["z"],
                                 orientation_field["w"])
        pose_cov_field = self.get_field_value_by_name("pose_covarience")
        cov_pose = CovarianceMatrix(np.array(pose_cov_field).reshape(6, 6), False)

        distributed_pose = Gaussianed(Pose(position, orientation), cov_pose)

        #twist is velocity
        linear_twist_field = self.get_field_value_by_name("linear_twist")
        linear_twist = Linear(linear_twist_field["x"], linear_twist_field["y"], linear_twist_field["z"])

        angular_twist_field = self.get_field_value_by_name("angular_twist")
        angular_twist = Angular(angular_twist_field["x"], angular_twist_field["y"], angular_twist_field["z"])

        twist_cov_field = self.get_field_value_by_name("twist_covarience")
        cov_twist = CovarianceMatrix(np.array(twist_cov_field).reshape(6, 6), False)

        distributed_twist = Gaussianed(Twist(linear_twist, angular_twist), cov_twist)

        # kinematic
        trace = Trace.init_from_formatted_data_and_kind_and_name(PoseTwistKinematic(distributed_pose, distributed_twist),
                                                                 GaussianedQuaternionKinematic(), None)
        timed_trace = Timed(trace, self._time)

        kind = BasedOnInheritence(timed_trace)

        return timed_trace


