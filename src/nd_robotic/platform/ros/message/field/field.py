from typing import Any, Union


class Field:
    def __init__(self, name:str, value:Any):
        """

        Args:
            name:
            value:
            kind:
        """
        self._name = name
        self._value = value

    def get_value(self)->Any:
        return self._value

    def get_name(self)->str:
        return self._name