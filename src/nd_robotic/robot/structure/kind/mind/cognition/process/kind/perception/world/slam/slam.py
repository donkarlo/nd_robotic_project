from nd_robotic.mind.cognition.process.kind.perception.world.occupancy_grid_map import OccupancyGridMap


class Slam:
    """
    Simulatnious localization and mapping
    it has two outputs
    - Occupancy grid map
    -
    """

    def __init__(self):
        pass

    def get_occupancy_grid(self)->OccupancyGridMap:
        """the map"""
        pass

    def get_pose_estimation(self):
        pass

    def get_trajectory(self):
        pass

    def get_uncertainty_estimates(self):
        """
        uncertainty for pose or map
        :return:
        """
        pass