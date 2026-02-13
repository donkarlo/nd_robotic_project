from typing import Any

from nd_robotic.robot.robot import Interface


class Decorator(Interface):
    __slots__ = ("_inner",)
    def __init__(self, inner:Interface):
        self._inner = inner

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")

        target: Any = self._inner
        seen = set()
        while target is not None and id(target) not in seen:
            seen.add(id(target))
            try:
                inspect.getattr_static(target, name)
                return getattr(target, name)
            except AttributeError:
                target = getattr(target, "_inner", None)
        raise AttributeError(
            f"{type(self).__name__} and its inner chain have no attribute {name!r}"
        )