from nd_robotic.robot.robot import Collection as ActuatorCollection

class MessageSender:
    def __init__(self, actuator_collection: ActuatorCollection):
        """

        Args:
            actuator_collection:
        """
        self._actuator_collection = actuator_collection
        
    def get_action_collection(self)-> ActuatorCollection:
        return self._actuator_collection