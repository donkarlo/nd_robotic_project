from typing import Protocol, runtime_checkable, Any, Optional

from nd_robotic.robot.structure.kind.body.nervous.neuron.action_potential.group.group import Group as ActionPotentialGroup


@runtime_checkable
class Interface(Protocol):
    _population_activity_field: Optional[ActionPotentialGroup]
    _formatted_data: Any

    def __init__(self, population_activity_field: ActionPotentialGroup):
        ...

    def get_population_activity_field(self) -> ActionPotentialGroup:
        ...

    def convert_formatted_data_to_population_activity_field(self) -> ActionPotentialGroup:
        ...
