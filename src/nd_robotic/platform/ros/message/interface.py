from nd_robotic.platform.ros.message.field.field import Field
from typing import Protocol, List, Any
from nd_utility.data.kind.dic.dic import Dic

class Interface(Protocol):
    _fileds:List[Field]
    def __init__(self, fields:List[Field]): ...
    def get_fields(self) -> List[Field]: ...