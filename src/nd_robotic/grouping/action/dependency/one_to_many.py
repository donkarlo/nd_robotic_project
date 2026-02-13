from nd_robotic.mrs.action.dependency.robot_command import RobotAction


class OneToMany:
    def __init__(self, leading_robot_command:RobotAction, follower_robot_commands:list[RobotAction]):
        '''
        One commad when performed by leader then a sequence of commands from NOT unique followers should be done
        Args:
            leading_robot_command:
            follower_robot_commands:
        '''
        self.__leading_robot_command = leading_robot_command
        self.__follower_robot_commands = follower_robot_commands
