

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.component import Component as MemoryComponent
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.decorator.decorator import \
    Decorator
from nd_utility.data.storage.decorator.multi_valued.decorator.sliced.cashed.interface import Interface as MultiValuedStorageInterface
from nd_utility.data.storage.interface import Interface as StorageInterface


class Storaged(Decorator, StorageInterface):
    """
    -
    """
    def __init__(self, inner: MemoryComponent, storage: MultiValuedStorageInterface):
        """
        The internal_storage in storaged is brain or body parts of the mind
        """
        Decorator.__init__(self, inner)
        self._storage = storage

    def get_storage(self) -> MultiValuedStorageInterface:
        return self._storage

    def save(self)->None:
        self._storage.save()

    def load(self)->None:
        self._storage.load()

    def stringify(self) -> str:
        return self._inner.stringify()

