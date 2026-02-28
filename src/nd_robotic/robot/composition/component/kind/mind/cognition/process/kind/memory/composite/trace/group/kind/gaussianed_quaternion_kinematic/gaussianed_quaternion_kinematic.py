from functools import cache

import numpy as np

from nd_robotic.robot.robot import Storaged
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.group.group import Group as TraceGroup
from nd_robotic.robot.robot import Kind as TraceGroupKind
from nd_robotic.robot.robot import TimePosition
from nd_robotic.robot.robot import GaussianedQuaternionKinematic as GaussianedQuaternionKinematicTraceKind
from nd_utility.data.kind.dic.dic import Dic
from nd_utility.data.storage.decorator.multi_valued.multi_valued import MultiValued
from nd_utility.data.storage.kind.file.numpi.multi_valued import MultiValued as MultiValuedNumPi

from nd_utility.data.storage.kind.file.pkl.pkl import Pkl
from nd_utility.os.file_system.file.file import File as OsFile
from nd_utility.os.file_system.path.file import File as FilePath


class  GaussianedQuaternionKinematic(TraceGroup, TraceGroupKind):
    """
    """

    def __init__(self):
        self._trace_kind = GaussianedQuaternionKinematicTraceKind()
        TraceGroup.__init__(self, None, self._trace_kind.get_name())
        TraceGroupKind.__init__(self, self._trace_kind.get_name())

    @cache
    def get_schema(self) -> Dic:
        return self._trace_kind.get_schema()

    def get_time_position_sequence_trace_group(self) -> np.ndarray:
        """
        TODO: This is a composition of action
        Returns:

        """
        parent_trace_dir_str_path = "/home/donkarlo/Dropbox/phd/data/experiements/oldest/robots/uav1/structure/mind/memory/explicit/long_term/episodic/normal/gaussianed_quaternion_kinematic_sliced_from_1_to_300000/"
        parent_file_name = "gaussianed_quaternion_kinematic_sliced_from_1_to_300000.pkl"
        parent_trace_file_str_path = parent_trace_dir_str_path+parent_file_name

        file_path = FilePath(parent_trace_file_str_path)
        os_file = OsFile(file_path, None, None)

        storage = MultiValued(Pkl(os_file, False), None)

        trace_group = TraceGroup(None, self.get_name())

        storaged_trace_group = Storaged(trace_group, storage)

        traces = storaged_trace_group.get_traces()

        time_position_seq = []
        for trace in traces:
            position_component = trace.get_formatted_data().get_pose().get_position().get_vector_representation().get_components()
            time = [trace.get_time().get_value()]
            time_position_seq.append(time+position_component.tolist())

        time_position_seq = np.array(time_position_seq)
        file_path = FilePath(parent_trace_dir_str_path+"time_position_sequence_sliced_from_1_to_300000.npz")
        os_file = OsFile(file_path, None, None)
        position_trace_group_storage = MultiValuedNumPi(os_file, True)
        position_trace_group_storage.set_ram(time_position_seq)

        # TODO: must be removed and add a segrgated memory composition in all_modalities.schema.yaml
        position_trace_group_storage.save()


        # Build the memory component for time position trace action_potential_group
        #position_sequence_trace_group = StoragedTraceGroup.init_by_traces_and_kind_and_name(time_position_seq, TimePosition,                                                                                    TimePosition.__name__)
        # position_sequence_storaged_trace_group = Storage(position_sequence_trace_group, position_trace_group_storage)
        # stroraged_trace_group = Storage(StoragedTraceGroup.init_by_traces_and_kind_and_name(time_position_sequence, None, None))
        # stroraged_trace_group.save()
        # print(time_position_sequence)


if __name__ == "__main__":
    o = GaussianedQuaternionKinematic()
    print(o.get_time_position_sequence_trace_group())
    #
    # path = Path(self._str_path)
    #
    # os_file = File.init_from_path(path)
    # pickle = Pkl(os_file, False)
    # position_sliced_values = pickle.load()
    # scan_values = position_sliced_values.get_values()
    #
    # positions_sequence = []
    # for scan_value in scan_values:
    #     positions_sequence.append(
    #         scan_value
    #         .get_formatted_data()
    #         .get_pose()
    #         .get_position()
    #         .get_vector_representation()
    #         .get_components()
    #     )
    #
    # positions_sequence = np.array(positions_sequence, dtype=np.float64)

    # return positions_sequence
