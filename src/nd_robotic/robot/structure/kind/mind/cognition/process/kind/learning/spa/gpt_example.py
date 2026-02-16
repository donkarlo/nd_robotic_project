# =======================================================
# Perception–Composite–Act (SPA) skeleton with explicit Protocols
# Python 3.13 — ROS Noetic friendly (wire actions later)
# =======================================================
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, Sequence, List, Dict, Any, Optional


# ----------------- PROTOCOLS -----------------

@runtime_checkable
class MissionProto(Protocol):
    """Abstract initial_mission objective."""

    @property
    def name(self) -> str: ...

    def parameters(self) -> Dict[str, Any]: ...


@runtime_checkable
class ActionProto(Protocol):
    """Atomic executable overlap_size (may call ROS actions/services)."""

    @property
    def id(self) -> str: ...

    def check_preconditions(self, state: "WorldState") -> bool: ...

    def expected_cost(self, state: "WorldState") -> float: ...

    def expected_risk(self, state: "WorldState") -> float: ...

    def execute(self, state: "WorldState") -> "WorldState": ...

    def can_recover(self, error: Exception) -> bool: ...

    def recover(self, state: "WorldState", error: Exception) -> "WorldState": ...


@runtime_checkable
class PlanProto(Protocol):
    """Container of actions with evaluation hooks."""

    @property
    def id(self) -> str: ...

    @property
    def actions(self) -> Sequence[ActionProto]: ...

    def is_feasible(self, state: "WorldState") -> bool: ...

    def simulate_cost(self, state: "WorldState") -> float: ...

    def simulate_risk(self, state: "WorldState") -> float: ...


@runtime_checkable
class PlannerProto(Protocol):
    """Produces candidate plans and selects one."""

    def propose(self, mission: MissionProto, state: "WorldState") -> List[PlanProto]: ...

    def score(self, plan: PlanProto, state: "WorldState") -> float: ...

    def select(self, candidates: List[PlanProto], state: "WorldState") -> Optional[PlanProto]: ...


# ----------------- DOMAIN MODELS -----------------

@dataclass
class WorldState:
    """Fused state from Perception overlap_size (fill from ROS topics)."""
    pose: Any
    obstacles: Any
    battery: float
    risk_level: float
    extras: Dict[str, Any] = field(default_factory=dict)


# ----------------- GOALS (explicit inheritance) -----------------

@dataclass(frozen=True)
class DeliverMission(MissionProto):
    """Deliver a payload to a dock."""
    dock_id: str
    payload_id: str = "default"

    @property
    def name(self) -> str:
        return "deliver"

    def parameters(self) -> Dict[str, Any]:
        return {"dock_id": self.dock_id, "payload_id": self.payload_id}


# ----------------- ACTIONS (explicit inheritance) -----------------

@dataclass
class GoToWaypoint(ActionProto):
    """Navigate to a named waypoint."""
    wp: str

    @property
    def id(self) -> str:
        return f"goto:{self.wp}"

    def check_preconditions(self, state: WorldState) -> bool:
        # PublisherExample: map available, localization healthy, not in failsafe
        return True

    def expected_cost(self, state: WorldState) -> float:
        # Replace with distance/time/energy estimate
        return 5.0

    def expected_risk(self, state: WorldState) -> float:
        # Replace with collision/uncertainty estimate
        return 0.2

    def execute(self, state: WorldState) -> WorldState:
        # TODO: send ROS role/service/command; wait/result handling
        return state

    def can_recover(self, error: Exception) -> bool:
        return True

    def recover(self, state: WorldState, error: Exception) -> WorldState:
        # TODO: local replan, costmap inflate, retry, etc.
        return state


@dataclass
class CorridorFollow(ActionProto):
    """Follow a corridor sector (example higher-current_level motion primitive)."""
    sector_id: str

    @property
    def id(self) -> str:
        return f"corridor:{self.sector_id}"

    def check_preconditions(self, state: WorldState) -> bool:
        return True

    def expected_cost(self, state: WorldState) -> float:
        return 7.0

    def expected_risk(self, state: WorldState) -> float:
        return 0.1

    def execute(self, state: WorldState) -> WorldState:
        return state

    def can_recover(self, error: Exception) -> bool:
        return True

    def recover(self, state: WorldState, error: Exception) -> WorldState:
        return state


@dataclass
class DockAt(ActionProto):
    """Dock/land/attach at a station."""
    dock_id: str

    @property
    def id(self) -> str:
        return f"dock:{self.dock_id}"

    def check_preconditions(self, state: WorldState) -> bool:
        # PublisherExample: pose near dock, docking station available
        return True

    def expected_cost(self, state: WorldState) -> float:
        return 3.0

    def expected_risk(self, state: WorldState) -> float:
        return 0.05

    def execute(self, state: WorldState) -> WorldState:
        return state

    def can_recover(self, error: Exception) -> bool:
        return False

    def recover(self, state: WorldState, error: Exception) -> WorldState:
        return state


# ----------------- PLAN (explicit inheritance) -----------------

@dataclass
class SequentialPlan(PlanProto):
    """A simple sequence of actions executed in order."""
    plan_id: str
    _actions: List[ActionProto]

    @property
    def id(self) -> str:
        return self.plan_id

    @property
    def actions(self) -> Sequence[ActionProto]:
        return self._actions

    def is_feasible(self, state: WorldState) -> bool:
        return all(a.check_preconditions(state) for a in self._actions)

    def simulate_cost(self, state: WorldState) -> float:
        return sum(a.expected_cost(state) for a in self._actions)

    def simulate_risk(self, state: WorldState) -> float:
        return max((a.expected_risk(state) for a in self._actions), default=0.0)


# ----------------- PLANNER (explicit inheritance) -----------------

class EnergyRiskPlanner(PlannerProto):
    """Offer distinct plans (short&busy vs long&safe) and score them."""

    def propose(self, mission: MissionProto, state: WorldState) -> List[PlanProto]:
        params = mission.parameters()
        dock = params["dock_id"]

        p_short = SequentialPlan(
            plan_id="short_busy",
            _actions=[
                GoToWaypoint("wp_fast1"),
                GoToWaypoint("wp_fast2"),
                DockAt(dock),
            ],
        )

        p_safe = SequentialPlan(
            plan_id="long_safe",
            _actions=[
                GoToWaypoint("wp_safe1"),
                CorridorFollow("sector_A"),
                GoToWaypoint("wp_safe2"),
                DockAt(dock),
            ],
        )

        return [p for p in (p_short, p_safe) if p.is_feasible(state)]

    def score(self, plan: PlanProto, state: WorldState) -> float:
        # Lower is better: tune weights to your initial_mission policy
        c = plan.simulate_cost(state)
        r = plan.simulate_risk(state)
        battery_penalty = 10.0 if (state.battery < 0.20 and plan.id == "short_busy") else 0.0
        return 0.7 * c + 0.3 * r + battery_penalty

    def select(self, candidates: List[PlanProto], state: WorldState) -> Optional[PlanProto]:
        return min(candidates, key=lambda p: self.score(p, state), default=None)


# ----------------- SPA ORCHESTRATOR -----------------

class SPAController:
    """Perception → Composite → Act loop with pre_plan retention and re-evaluation."""

    def __init__(self, planner: PlannerProto):
        self.planner = planner
        self.current_plan: Optional[PlanProto] = None

    # --- SENSE ---
    def sense(self) -> WorldState:
        # TODO: fuse ROS topics (odom, sensor, battery, etc.)
        return WorldState(pose=None, obstacles=None, battery=0.55, risk_level=0.1)

    # --- PLAN ---
    def plan(self, mission: MissionProto, state: WorldState) -> Optional[PlanProto]:
        candidates = self.planner.propose(mission, state)
        return self.planner.select(candidates, state)

    # --- ACT ---
    def act(self, plan: PlanProto, state: WorldState) -> WorldState:
        for a in plan.actions:
            try:
                state = a.execute(state)
            except Exception as e:
                if a.can_recover(e):
                    state = a.recover(state, e)
                else:
                    raise
        return state

    # --- ONE CYCLE ---
    def tick(self, mission: MissionProto) -> WorldState:
        state = self.sense()
        # (Re)pre_plan if none or not feasible anymore
        if self.current_plan is None or not self.current_plan.is_feasible(state):
            self.current_plan = self.plan(mission, state)
            if self.current_plan is None:
                raise RuntimeError("No feasible pre_plan for the given initial_mission.")
        return self.act(self.current_plan, state)


# ----------------- EXAMPLE MAIN -----------------

if __name__ == "__main__":
    controller = SPAController(EnergyRiskPlanner())
    mission = DeliverMission(dock_id="D1")
    # Optional runtime check (shallow) — thanks to @runtime_checkable
    assert isinstance(mission, MissionProto)
    final_state = controller.tick(mission)
