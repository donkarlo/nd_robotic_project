from nd_robotic.mind.cognition.process.kind.thinking.decision_making.decision_making import DecisionMaking
from nd_robotic.robot.robot import Learning
from typing import List

from nd_robotic.mind.cognition.process.kind.memory.composite.composite import Composite as MemoryComposite
from nd_robotic.mind.cognition.process.kind.thinking.reasoning.reasoning import Reasoning
from nd_robotic.mind.cognition.process.kind.memory.mode.mode import Mode

from nd_robotic.robot.structure.structure import Structure


class Mind(Structure):
    """
    Mental is the adverb for mind
    https: // en.wikipedia.org / wiki / Mental_model
        - A mind transformer_model is an internal representation of external reality — that is, a way of representing reality within the mind.

    Is all about the concepts. Whenever there is something tangiable, it should go to body>brain
    - https://en.wikipedia.org/wiki/Mind
        - The mind is that which thinks, feels, perceives, imagines, remembers, and wills. It covers the totality of mind phenomena, including both conscious processes, through which an individual is aware of external and internal circumstances, and unconscious processes, which can influence an individual without intention or awareness.
    """
    def __init__(self, memory: MemoryComposite, learning:Learning, reasoning:Reasoning, decision_making:DecisionMaking):
        """

        Args:
            memory: it is the memory tree that is given to the mind
            learning: learning strategy, updating transformer_model parametes
            reasoning: reasoning strategy, how to relate new observations using learning strategy (the parameters from learning)
            decision_making: selection of a belief among several possible alternative options (planning is a part of this)
        """
        self._memory = memory
        self._reasoning = reasoning
        self._learning = learning
        self._decision_making = decision_making



    def get_learning(self)->Learning:
        return self._learning

    def get_reasoning(self)->Reasoning:
        return self._reasoning

    def get_decision_making(self)->DecisionMaking:
        return self._decision_making

    def get_memory(self)-> MemoryComposite:
        return self._memory

    def set_mental_state(self, state:Mode)->None:
        self._state = state

    def get_mental_state(self)->Mode:
        return self._state

    def reduce_suprise(self):
        """
        Somehow whenever  a new observer is noticed this must be activated to see how it is possible to reduce free energy.
        ways to reduce:
        - segregating
        - fusion
        - building new transformer_model
        - switching to apropriate transformer_model
        Returns:

        """
        pass

    def get_mind_state(self)->List:
        """
        Choices [Multiple could happen]:
        - memory:
            - remebering
                -- was I intelligently controlled?
            - recalling
            - memorizing
            - being intelligently controlled
            - autonomous with goals
        Returns:

        """
        pass






