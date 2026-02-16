from typing import Any

from nd_robotic.robot.structure.kind.mind.process.kind.memory.action.kind.intra.segregation.segregator.kind.slicer.feature.feature_slicer import \
    FeatureSlicer
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.composite import Composite as MemoryComposite
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.action.kind.intra.segregating.segregating import Segregating
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.group.decorator.storaged import Storaged
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.group.group import Group as TraceGroup
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.kind.core.kind import Kind as TraceGroupKind
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.group.kind.core.kind import Kind as TraceGroupKinds
from nd_robotic.platform.ros.message.kind.sensor.lidar.scan.scan import Scan as RosScanMessage
from nd_robotic.platform.ros.message.kind.sensor.nav.odometry import Odometry as RosOdometryMessage
from nd_utility.data.kind.dic.dic import Dic
from nd_utility.data.kind.sliceix.sliceix import Sliceix
from nd_utility.data.storage.decorator.multi_valued.decorator.sliced.sliced import Sliced
from nd_utility.data.storage.decorator.multi_valued.observer.add_to_ram_values_subscriber import \
    AddToRamValuesSubscriber as TraceAddValueSubscriber
from nd_utility.data.storage.decorator.multi_valued.observer.group_ram_values_addition_finished_subscriber import \
    GroupRamValuesAdditionFinishedSubscriber
from nd_utility.data.storage.decorator.multi_valued.decorator.uni_kinded import UniKinded
from nd_utility.data.storage.factory.uni_kinded_multi_valued_yaml_file import UniKindedMultiValuedYamlFile
from nd_utility.data.storage.kind.file.pkl.pkl import Pkl as PklDataStorage
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator as BaseDecorator
from nd_utility.oop.inheritance.overriding.override_from import override_from
from nd_utility.os.file_system.file.file import File as OsFile
from nd_utility.os.file_system.path.file import File as FilePath
from nd_utility.os.file_system.path.directory import Directory as DirPath
from nd_utility.os.file_system.path.path import Path


class RosBagYamlMessageSegragating(FeatureSlicer, TraceAddValueSubscriber, GroupRamValuesAdditionFinishedSubscriber):
    """
    Represents the modality action_potential_group for one event_specific_knowledge_forcasting_model_config
    """

    def __init__(self, source_memory_component: MemoryComponent, slc: slice):
        self._storage_type_after_segregation = "pkl"
        self._slice = slc
        Segregating.__init__(self, source_memory_component)

        if not BaseDecorator.has_decorator(self._source_memory_component.get_trace_group(), Storaged):
            raise TypeError("Working component's trace action_potential_group must be decorated with Storage")
        if not isinstance(self._source_memory_component.get_trace_group().get_storage(),
                          UniKindedMultiValuedYamlFile):
            raise TypeError("Working component's trace action_potential_group internal_storage must be a UniKindedMultiValuedYamlFile")

        # umvyf stand for UniKindedMultiValuedYamlFile internal_storage
        self._current_uni_formted_multi_value_storage:UniKindedMultiValuedYamlFile = self._source_memory_component.get_trace_group().get_storage()

        # observer subscriptions
        self._current_uni_formted_multi_value_storage.attach_add_to_ram_values_subscriber(self)
        self._current_uni_formted_multi_value_storage.attach_group_ram_values_addition_finished_subscriber(self)

        # helpers, this will be filled when self.do_when_a_new_value_is_added_to_ram is called from uniformated_multi_valued_yaml_file.add_value
        self._trace_groups_dic = Dic({})

    @override_from(Segregating)
    def _build_segregated_components(self) -> None:
        # this envokes TraceAddValueSubscriber.do_when_a_new_value_is_added_to_ram
        self._current_uni_formted_multi_value_storage.load()
        # when finished GroupRamValuesAdditionFinishedSubscriber.do_when_group_ram_values_addition_is_finished

    @override_from(TraceAddValueSubscriber)
    def do_when_a_new_value_is_added_to_ram(self, value: Any) -> None:
        """
        Is called from SlicedValues internal_storage decorator
        """
        if isinstance(value, Dic):
            # if it is a ros message
            if value.has_nested_keys(["header", "frame_id"]):
                # if it is a ROS odom message
                if value.has_nested_keys(["pose"]):
                    # then its is a ROS odometry trace
                    new_trace = RosOdometryMessage.init_from_dic(value).get_distributed_kinematic_trace()
                elif value.has_nested_keys(["ranges"]):
                    # then it is a ROS scan trace
                    new_trace = RosScanMessage.init_from_dic(value).get_scan_ranges_trace()

            # note that trace kind name is the same as trace action_potential_group kind name in this case

            if new_trace.get_kind().get_name() not in self._trace_groups_dic.get_keys():
                new_trace_group_kind: TraceGroupKind = None

                for existing_trace_group_kind in TraceGroupKinds().get_kind_list():
                    if existing_trace_group_kind.get_name() == new_trace.get_kind().get_name():
                        new_trace_group_kind = existing_trace_group_kind

                # setting trace groupe name to be used as the file name too
                slice_name = Sliceix(self._slice).get_name()
                trace_group_name = new_trace_group_kind.get_name() + slice_name

                # init the trace action_potential_group now
                new_trace_group = TraceGroup.init_by_traces_and_kind_and_name(None, new_trace_group_kind,
                                                                              trace_group_name)

                # adding it to the dictionary
                self._trace_groups_dic.add_key_value(new_trace_group.get_kind().get_name(), new_trace_group, True)

            for trace_group_kind_name, trace_group in self._trace_groups_dic.get_keys_values():
                # we use starts with here because trace action_potential_group kind name is has a slice string in the end
                if trace_group_kind_name==new_trace.get_kind().get_name():
                    trace_group.add_member(new_trace)

    @override_from(GroupRamValuesAdditionFinishedSubscriber)
    def do_when_group_ram_values_addition_is_finished(self) -> None:
        os_sep = Path.get_os_path_separator()

        for trace_kind_name, trace_group in self._trace_groups_dic.get_keys_values():
            # Buiding the path for ne File storages
            current_umvyf_storage_str_path = self._current_uni_formted_multi_value_storage.get_native_absolute_string_path()

            current_uni_format_yaml_file_parent_storage_str_path = Path(current_umvyf_storage_str_path).get_parent_directory_string_path()

            segregated_storage_dir_path = DirPath(current_uni_format_yaml_file_parent_storage_str_path + os_sep + trace_group.get_name() + os_sep + trace_group.get_name())

            segregated_storage_file_path = FilePath(segregated_storage_dir_path.get_native_os_string_path_with_trailing_slash() + "." + self._storage_type_after_segregation)

            os_file = OsFile(segregated_storage_file_path, None, None)
            #TODO here multi valued must be replaced with Sliced
            trace_group_storage = UniKinded(Sliced(PklDataStorage(os_file, create_directory_structure=True), self._slice , None), trace_kind_name, False)

            storaged_traced_group = Storaged(trace_group, trace_group_storage)
            # TODO saving must NOT be done here, later I should talk to Memory component for saving. This is just for test
            storaged_traced_group.save()

            segregated_component = MemoryComposite(storaged_traced_group, trace_kind_name)

            self._segregated_components.append(segregated_component)


