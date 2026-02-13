from nd_robotic.mind.cognition.process.kind.memory.kind.long_term.explicit.episodic.experience.experience import Experience
from typing import List, Optional

from nd_robotic.mind.cognition.process.kind.memory.stack.stack import Stack


class Group:
    def __init__(self, shared_stack:Stack, members:Optional[List[Experience]]=None):
        """
        in an experiment, on action_potential_group can be considered as learning[normal] and testing[follow, next_to]
        Args:
            members:
        """
        self._shared_stack = shared_stack
        if members is not None:
            self._members = members
        else:
            self._members = []

    def get_members(self)->List[Experience]:
        return self._members

    def __getitem__(self, index:int)->Experience:
        return self._members[index]

    def add_experience(self, experience:Experience)->None:
        for existing_experience in self._members:
            if existing_experience.get_name() == experience.get_name():
                raise ValueError (f"Exprience with name {experience.get_name()} already exists")

        self._members.append(experience)

    def get_experience_by_name(self, name:str)->Optional[Experience]:
        for experience in self._members:
            if experience.get_name() == name:
                return experience
        raise ValueError (f"Experience with name {name} does not exist")