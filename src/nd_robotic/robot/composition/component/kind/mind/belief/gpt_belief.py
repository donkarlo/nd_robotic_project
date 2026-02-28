from typing import Protocol, Generic, TypeVar, Optional, Sequence
from nd_math.linear_algebra.vec.vec import Vec

TState = TypeVar("TState")  # could be Vec, Pose, etc.


class State(Protocol):
    """Marker protocol if you need one; your Vec/Pose already serve as concrete states."""
    ...


class Distribution(Protocol):
    """Abstracts a probability distribution."""

    def mean(self) -> Sequence[float]: ...

    def covariance(self) -> Optional[Sequence[Sequence[float]]]: ...
    # add: sample(n), log_prob(x), etc. as needed


class GaussianDistribution:
    def __init__(self, mu: Sequence[float], Sigma: Sequence[Sequence[float]]):
        self._mu = mu
        self._Sigma = Sigma

    def mean(self) -> Sequence[float]: return self._mu

    def covariance(self) -> Sequence[Sequence[float]]: return self._Sigma


class DiracDistribution:
    """Zero-uncertainty (point mass)."""

    def __init__(self, x: Sequence[float]): self._x = x

    def mean(self) -> Sequence[float]: return self._x

    def covariance(self) -> Optional[Sequence[Sequence[float]]]: return None


class Belief(Generic[TState]):
    """
    Wraps a deterministic state plus an uncertainty transformer_model.
    Keeps 'estimate' (e.g., Vec) and its distribution coherent.
    """

    def __init__(self, estimate: TState, dist: Distribution):
        self._estimate = estimate  # e.g., Vec([...])
        self._dist = dist  # e.g., Gaussian over the same space

    def estimate(self) -> TState:
        return self._estimate

    def distribution(self) -> Distribution:
        return self._dist

    def mean_as_state(self, state_ctor) -> TState:
        # Convert distribution mean back into a state using given constructor
        return state_ctor(self._dist.mean())


# Convenience creation
def lift_dirac(state: TState) -> Belief[TState]:
    # Assuming 'state' exposes its components via a method or property; adapt as needed
    comps = getattr(state, "get_components", None)
    v = comps() if callable(comps) else state  # adjust to your Vec API
    return Belief(state, DiracDistribution(v))
