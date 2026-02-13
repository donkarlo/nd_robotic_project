from typing import Protocol, runtime_checkable

from nd_utility.data.kind.group.interface import Interface as GroupInterface

@runtime_checkable
class Interface(GroupInterface, Protocol):
    """
    
    """
    pass
