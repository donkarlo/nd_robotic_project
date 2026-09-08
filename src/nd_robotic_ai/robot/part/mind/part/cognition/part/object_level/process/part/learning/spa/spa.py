from nd_robotic_ai.spa.plan.mission.mission import Mission


class Spa:
    """
    - Stands for percepting-pre_plan-role
    - implements percepting(percepting), reasoning(pre_plan), process_control(role)
    """
    def __init__(self, mission:Mission):
        while True:
            self.sense()
            self.plan()
            self.act()
