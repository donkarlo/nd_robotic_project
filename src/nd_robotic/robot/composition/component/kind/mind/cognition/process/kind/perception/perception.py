class Perception:
    def __init__(self):
        """
        https://en.wikipedia.org/wiki/Perception
        """
        obss = self._sense.get_obss()
        pp_obss = self._preprocessing.preprocess(obss)
        states = self._odometry_and_state_estimation.estimate(pp_obss)


