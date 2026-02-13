from nd_robotic.cognition.mind.memory.episode.episode import Episode
from nd_robotic.spa.action.action import Action
from nd_robotic.spa.action.actuator.command.command import Command
from nd_robotic.spa.plan.mission.mission import Mission
from sensorx.observation.sensor_set_obs_vals import SensorSetObsVals
from nd_math.linear_algebra.vec.vec import Vec


class SensorsetValsBetweenCommands(Episode):
    """
    multiple sensor action_potential_group between two consequent commands
    """
    def __init__(self, mission: Mission, action: Optional[Action]=None, command:Optional[Command]=None):
        self._mission = mission
        self._action = action
        self._command = command

        #init
        self._sensor_set_obs_vals = SensorSetObsVals()

    def add_sensor_set_val(self, val:Vec)->None:
        self._sensor_set_obs_vals.add_sensor_set_val(val)