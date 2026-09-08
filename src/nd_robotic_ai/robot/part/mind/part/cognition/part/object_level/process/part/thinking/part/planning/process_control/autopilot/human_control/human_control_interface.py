from typing import Protocol, runtime_checkable

@runtime_checkable
class HumanControlInterface(Protocol):
    """
    Human process_control role is to give a new initial_mission to 'RotorComposite'
    """
    pass