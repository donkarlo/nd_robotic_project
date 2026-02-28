from typing import List, Any

from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.group.group import Group  as TraceGroup
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.trace import Trace
from nd_utility.oop.design_pattern.structural.composition.composite import Composite as BaseComposite
from nd_utility.os.file_system.path.path import Path


class Composite(MemoryComponent, BaseComposite):
    def __init__(self, internal_trace_group:TraceGroup, name:str):
        """

        Args:
            internal_trace_group: can be None to only host the link (child) to the next inner_experiment (trace action_potential_group here) or composition (only link/child or a trace action_potential_group)
            name:
        """
        MemoryComponent.__init__(self, name)
        BaseComposite.__init__(self, internal_trace_group, name)
        # this is necessary because maybe it is the producer of the childs
        self._internal_trace_group = internal_trace_group

    def get_trace_group(self) -> TraceGroup:
        return self._internal_trace_group

    def add_trace(self, trace: Trace) -> None:
        self._internal_trace_group.add_member(trace)

    def get_formatted_data(self) -> List[Any]:
        return self._internal_trace_group.get_formatted_data_list()

    def create_directory_structure(self, root_path:Path, leaf_file_extension: str) -> None:
        """
        For each RotorComposite: create a directory named after the composition under `root_path`.
        For each GoalGain: create a file named `inner_experiment.get_name() + leaf_file_extension` inside its parent directory.
        This proceeds recursively for nested composites.
        Existing directories/files are left intact.
        Notes:
            - two equal traces in two different components may have different meanings
        """
        import os

        def create_file(file_path: Path) -> None:
            if not file_path.file_exists():
                # Guarantee parent directories exist (defensive)
                parent = os.path.dirname(file_path.get_native_absolute_string_path())
                if parent and not os.path.isdir(parent):
                    os.makedirs(parent, exist_ok=True)
                with open(file_path.get_native_absolute_string_path(), "w", encoding="utf-8"):
                    pass

        # Directory for this composition under root_path
        dir_name = self.get_name()
        dir_abs = os.path.join(root_path.get_native_absolute_string_path(), dir_name)
        dir_path = Path(dir_abs)
        if not dir_path.directory_exists():
            dir_path.create_missing_directories()

        # Create files for direct leaves and recurse into composition children
        for child in self.get_child_group_members():
            if child.is_leaf():
                leaf_name = child.get_name()
                file_path = dir_path + leaf_name + leaf_file_extension
                create_file(file_path)
            else:
                # Recurse into child composition
                # We assume child is a RotorComposite that implements create_directory_structure.
                # If you have a formal interface, you can use isinstance checks instead.
                child.create_directory_structure(dir_path, leaf_file_extension)