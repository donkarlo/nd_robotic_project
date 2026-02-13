from nd_math.linear_algebra.tensor.vector.vector import Vector
from nd_robotic.robot.robot import Group


class Group:
    def __init__(self, sensor_set: Group):
        """
        Storing observer vectors for the same sensor set
        Args:
            sensor_set:
        """
        self._sensor_set: Group = sensor_set
        # it will hold sensor id as key and a single_sensor_time_val_seq
        # as the action_potential_group for that in a heirarchical order
        self._all_nested_sensor_set_vals = {}
        self._time_seq = {}
        self._val_seq = {}
        self._time_vec_seq = {}

    def add_sensor_obs(self, sensor_ids_path:str, val:Vector)->None:
        # Split the str_path by "/" (e.g., "uav1/lidar" → ["uav1", "lidar"])
        keys = sensor_ids_path.split("/")
        d = self._all_nested_sensor_set_vals
        for k in keys[:-1]:
            # If intermediate key does not exist, create a new dictionary
            d = d.setdefault(k, {})

        # Handle the last key
        last_key = keys[-1]
        if last_key not in d:
            d[last_key] = []

        # Append the value to the list at the last key
        d[last_key].append(val)