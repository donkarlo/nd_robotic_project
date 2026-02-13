from abc import ABC, abstractmethod

from nd_utility.data.kind.dic.dic import Dic


class Kind(ABC):
    def __init__(self, name: str):
        self._name = name

        #lazy loading
        self._schema = None

    def get_name(self) -> str:
        return self._name

    @abstractmethod
    def get_schema(self)->Dic:
        ...

    def __eq__(self, other_kind: "Kinds")->bool:
        return self.is_equal_to(other_kind)

    def is_equal_to(self, kind:"Kinds")->bool:
        if self.get_schema() == kind.get_schema():
            pass