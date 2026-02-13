from nd_utility.data.kind.dic import dic
from typing import Union


class Frame:
    def __init__(self, id:Union[str,int]):
        self.__id = id
    def get_id(self):
        return self.__id