from nd_math.linear_algebra.tensor.vector.operation.many_operanded import ManyOperanded
from nd_math.linear_algebra.tensor.vector.vector_representable import VectorRepresentable
from typing import List

class State(VectorRepresentable):
    """
    Mode is a set of vectors as variables which are contributing to the Predicting the next state of a system.
    for example in a body system
    """
    def __init__(self, vec_representables:List[VectorRepresentable]):
        self._vector_representables = vec_representables
        super().__init__(ManyOperanded(self._vector_representables).get_concated())

    def get_vec(self)-> List[VectorRepresentable]:
        return self._vector_representables