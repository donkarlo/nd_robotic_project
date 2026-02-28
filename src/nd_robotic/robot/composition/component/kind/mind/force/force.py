from typing import List

from nd_math.probability.bayesian.evidence import Evidence


class Force:
    """
    - similar to force=ma in physics
    - A sub sequence of sensor-role-commands-time
    from a clustering approach that has a specific meaning

    - This provoker can be a provoker to remeber other_kind things
    """
    def __init__(self, evidence:List[Evidence]):
        """
        Force is a ratio_value of evidence or how much an evidence is forceful. it ,us be a vector. So it must have both magnitude and change_direction
        """
        self._evidence = evidence

    def get_evidence(self)->Evidence:
        return self._evidence