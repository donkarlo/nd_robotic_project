from typing import List


class Learning:
    """
    Learning is either discovering more enteties (relation or clusters) or making more abstract entities from a lower memory current_level to a higher one
    - learning is the matter of updating a models parameter according to new eveidences(Observation)
    """
    def __init__(self, model):
        self._model = model

    def update_model_parameters(self, model_parameters:List) -> None:
        pass

    def learn(self):
        pass
