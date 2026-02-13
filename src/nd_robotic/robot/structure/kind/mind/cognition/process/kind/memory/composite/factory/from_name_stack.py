from typing import List
from nd_robotic.mind.cognition.process.kind.memory.composite.composite import Composite as CompositeMemory


class FromNameStack:
    def __init__(self, names:List[str]):
        self._names = names
        compit_mems: List[CompositeMemory] = []
        for compit_counter, name in enumerate(names):
            cur_comp = CompositeMemory(None, name)
            compit_mems.append(cur_comp)
            if compit_counter > 0:
                compit_mems[-2].add_child(cur_comp)

        self._root_composite = compit_mems[0]
        self._deepest_composite = compit_mems[-1]

    def get_root_composite(self) -> CompositeMemory:
        return self._root_composite

    def get_deepest_composite(self) -> CompositeMemory:
        return self._deepest_composite
