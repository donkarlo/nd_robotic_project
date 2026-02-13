from typing import List, Any, Optional
from abc import ABC, abstractmethod
from nd_robotic.platform.ros.message.field.field import Field
from nd_utility.data.kind.dic.dic import Dic


class Message(ABC):
    """
    This is the leaf of the composite.
    - Message in ros can be formed of nested messages.
    """
    def __init__(self, fields:List[Field] = []):
        self._fields = fields

    @classmethod
    @abstractmethod
    def init_from_dic(cls, dic:Dic)->"Message": ...

    def add_field(self, field:Field)->None:
        self._fields.append(field)

    def get_field_value_by_name(self, name:str)->Optional[Any]:
        for field in self._fields:
            if field.get_name() == name:
                return field.get_value()
        raise KeyError(f"Field {name} not found")




