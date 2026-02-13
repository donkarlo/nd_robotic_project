from typing import Tuple

from nd_math.physics.unit.unit import Unit
from sensorx.observation.sensor_set_obss import SensorSetObss

from nd_robotic.spa.action.action import Action
from nd_robotic.spa.action.actuator.command.command import Command
from nd_robotic.spa.plan.mission.mission import Mission


class SensoriMotor(Unit):
    """
    This unit episodic says each memory unit is formed of a initial_mission for which multiple actions should be performed so that acc
    - The main probllem here is that we dont know after a set of commands in the meiddle how long should we expecting the forthcomming sensory observations are related. maybe clustering can do this
    """
    def __init__(self, mission:Mission, action:Action, prv_obss:SensorSetObss, commands:Tuple[Command,...], next_obss:SensorSetObss):
        self._mission = mission
        self._action = action
        self._prv_obss = prv_obss
        self._commands = commands
        self._next_obss = next_obss
