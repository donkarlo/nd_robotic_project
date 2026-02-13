from nd_robotic.robot.robot import Command
from nd_robotic.robot.robot import Pwm
from nd_robotic.robot.robot import Actuator
from nd_robotic.robot.robot import Status as ArmStatus
from nd_robotic.robot.robot import Arm
from nd_robotic.robot.robot import Status as DirectionStatus
from nd_robotic.robot.robot import Direction
from typing import Optional

class Rotor(Actuator):
    def __init__(self, name:Optional[str]=None):
        arm_command = Arm(ArmStatus.DISARMED)
        direction_command = Direction(DirectionStatus.CW)
        pwm_command = Pwm()
        valid_commands = [arm_command, direction_command, pwm_command]
        super().__init__(valid_commands, name)

    def _do_run_command(self, command:Command):
       if isinstance(command, Arm):
           pass
       elif isinstance(command, Direction):
           pass
       elif isinstance(command, Pwm):
           pass


