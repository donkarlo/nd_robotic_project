from nd_robotic.robot.composition.composite import Composite as CompositeComponent
from nd_robotic.robot.composition.component.kind.mind.cognition.cognition import Cognition


class Mind(CompositeComponent):
    """
    Mental is the adverb for mind
    https: // en.wikipedia.org / wiki / Mental_model
        - A mind transformer_model is an internal representation of external reality — that is, a way of representing reality within the mind.

    Is all about the concepts. Whenever there is something tangiable, it should go to body>brain
    - https://en.wikipedia.org/wiki/Mind
        - The mind is that which thinks, feels, perceives, imagines, remembers, and wills. It covers the totality of mind phenomena, including both conscious processes, through which an individual is aware of external and internal circumstances, and unconscious processes, which can influence an individual without intention or awareness.
    """
    def __init__(self, cognition:Cognition):
        CompositeComponent.__init__(self)
        self.add_child(cognition)






