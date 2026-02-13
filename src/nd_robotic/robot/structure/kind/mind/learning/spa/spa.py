from nd_robotic.spa.plan.mission.mission import Mission


class Spa:
    """
    - Stands for perception-pre_plan-role
    - implements perception(perception), reasoning(pre_plan), control(role)
    """
    def __init__(self, mission:Mission):
        while True:
            self.sense()
            self.plan()
            self.act()
