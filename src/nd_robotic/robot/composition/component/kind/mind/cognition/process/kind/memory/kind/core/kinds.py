from enum import Enum, auto


class Kinds(Enum):
    EXPERIENCE = auto()
    #such as sensors action_potential_group
    MODALITY = auto()
    #partitioned by clustering for example
    CLASSIFIED = auto()
    SEMANTIC = auto()
    # formed of episodes that answer the question
    EPISODIC = auto()

