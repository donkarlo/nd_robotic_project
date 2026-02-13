from typing import Generic, TypeVar

# to cover both state and composite_goal
VecType = TypeVar("VecType", bound=Vec)

class CollectionGenerator(Generic[VecType]):
    @staticmethod
    def clone_from_states_list(states_list:List[Type[VecType]]) -> List[Action]:
        path = Path(vecs_file_path)
        vecs_text = File(path).get_ram().strip()
        actions: List[Action] = []

        vec_class = sample_action.get_goal().get_desired_state().__class__
        # to support position
        vec_factory = getattr(vec_class, "init_from_components", None)
        vec_lines = vecs_text.split(vec_sep)
        for vec_line in vec_lines:
            vec_line = vec_line.strip()
            # if the vec_line is empty
            if not vec_line:
                continue
            vec_components = []
            for component in vec_line.split(component_sep):
                vec_components.append(float(component))
            vec: Vec = vec_factory(vec_components) if callable(vec_factory) else vec_class(vec_components)
            goal_acceptance = copy.deepcopy(sample_action.get_goal().get_acceptance())
            goal = Goal(vec, goal_acceptance)
            action = sample_action.__class__(goal)
            actions.append(action)
        return actions