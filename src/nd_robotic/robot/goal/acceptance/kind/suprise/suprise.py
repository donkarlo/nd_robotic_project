from nd_robotic.robot.goal.acceptance.acceptance import Acceptance


class Suprise(Acceptance):
    """
    - This can be used as the tolerence line for novelty detection
    if x the probability of state x happing then suprise is -log(p(x)), this is usually not possible. FOr example it is not possible to directly compute the the probability of a wall existance in  the sky
    """
    def __init__(self, discrepancy_method, threshold):
        Acceptance.__init__(self, discrepancy_method, threshold)


