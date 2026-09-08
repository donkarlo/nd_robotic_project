from nd_physics.quantity.decorator.united import United
from nd_physics.quantity.kind.time.time import Time

from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator


class Periodic:
    def __init__(self, period_length: Time):
        if not Decorator.has_decorator(period_length, United):
            raise TypeError("I need a United(Time())")
        self._period_length = period_length