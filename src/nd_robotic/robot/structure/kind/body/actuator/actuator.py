from nd_robotic.robot.robot import Command
from abc import abstractmethod, ABC

class Actuator(ABC):
    def __init__(self, valid_commands:tuple[Command], name:str=None):
        self._valid_commands = valid_commands
        self.__name = name

    def run_command(self, command:Command)->None:
        if command not in self._valid_commands:
            raise ValueError("Invalid command")
        self._do_run_command()

    @abstractmethod
    def _do_run_command(self, command:Command)->None:
        pass
