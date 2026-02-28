from typing import Dict, Any
from nd_robotic.robot.robot import Composite as CompositeMemory
from nd_utility.data.kind.dic.dic import Dic


class FromNameDictionary:
    def __init__(self, raw_dic: Dic) -> None:
        """
        Expects a nested dict of the form:
            {
                "root_name": {
                    "child_1": {},
                    "child_2": {
                        "grand_child": {}
                    }
                }
            }
        """
        raw_dict = raw_dic.get_raw_dict()
        keys = list(raw_dict.keys())
        if len(keys) == 0:
            raise ValueError("Dictionary must contain at least one root node.")

        root_name = keys[0]
        root_children = raw_dict[root_name]
        if not isinstance(root_children, dict):
            raise TypeError("Root value must be a dict mapping child names to subtrees.")

        root = CompositeMemory(None, root_name)
        self._root_composite: CompositeMemory = root

        self._build_subtree(root, root_children)

    def _build_subtree(
            self,
            parent: CompositeMemory,
            subtree: Dict[str, Any],
    ) -> None:
        """
        Recursively builds CompositeMemory children from a nested dict.
        """
        for child_name, child_subtree in subtree.items():
            child = CompositeMemory(parent, child_name)
            parent.add_child(child)

            if isinstance(child_subtree, dict) and len(child_subtree) > 0:
                self._build_subtree(child, child_subtree)

    def get_root_composite(self) -> CompositeMemory:
        return self._root_composite
