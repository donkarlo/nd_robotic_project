from nd_robotic.robot.robot import Storaged
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.group.group import Group as TraceGroup
from nd_robotic.robot.robot import \
    GaussianedQuaternionKinematic
from nd_utility.data.storage.decorator.multi_valued.multi_valued import MultiValued
from nd_utility.data.storage.kind.file.pkl.pkl import Pkl
from nd_utility.os.file_system.file.file import File as OsFile
from nd_utility.os.file_system.path.file import File as FilePath


class TestInteraction:
    def setup_method(self) -> None:
        pass

    def test_segregation(self):
        str_path = "/home/donkarlo/Dropbox/phd/data/experiements/oldest/robots/uav1/structure/mind/memory/explicit/long_term/episodic/normal/gaussianed_quaternion_kinematic_sliced_from_1_to_300000/gaussianed_quaternion_kinematic_sliced_from_1_to_300000.pkl"

        file_path = FilePath(str_path)
        os_file = OsFile(file_path, None, None)

        storage= MultiValued(Pkl(os_file, False), None)

        trace_group = TraceGroup(None, GaussianedQuaternionKinematic)


        storaged_trace_group = Storaged(trace_group, storage)

        traces = storaged_trace_group.get_traces()

        print(traces)