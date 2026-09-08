from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.working.part.plan.plan import \
    Plan as CurrentWorkingMemoryPlan


class Publisher:
    def __init__(self):
        self._subscribers = []

    def notify(self, current_working_plan: CurrentWorkingMemoryPlan):
        for subscriber in self._subscribers:
            subscriber.notify(current_working_plan)
