from abc import abstractmethod, ABC

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.working.part.plan.plan import \
    Plan as CurrentWorkingMemoryPlan


class Subscriber(ABC):

    @abstractmethod
    def handle_updated_plan(self, plan: CurrentWorkingMemoryPlan):
        pass
