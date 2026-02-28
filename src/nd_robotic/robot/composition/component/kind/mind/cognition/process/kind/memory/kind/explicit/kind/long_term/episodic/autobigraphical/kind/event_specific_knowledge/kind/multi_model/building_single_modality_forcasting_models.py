from nd_datascience.machine_learning.model.application.sequence_to_sequence.kind.time_series.kind.transformer.kind.uncertainty.gaussian.predicting.predicting import \
    Predicting
from nd_datascience.machine_learning.model.application.sequence_to_sequence.kind.time_series.kind.transformer.kind.uncertainty.gaussian.training.training import \
    Training
from nd_math.probability.distribution.discrepancy.kind.distance.kind.mahalanobis import Mahalanobis
from nd_math.probability.statistic.population.sampling.kind.countable.finite.members_mentioned.numbered.sequence.sliding_window.generator import \
    Generator as SlidingWindowGenerator
from nd_math.probability.statistic.population.sampling.kind.countable.finite.members_mentioned.numbered.sequence.sliding_window.sliding_window import \
    SlidingWindow
from nd_robotic.robot.action.action import Action
from nd_robotic.robot.action.kind.suprise_reducing.suprise_reducing import SupriseReducingAction
from nd_robotic.robot.goal.acceptance.kind.suprise.suprise import Suprise as SupriseAcceptance
from nd_robotic.robot.goal.kind.suprise_poise.suprise_poise import SurprisePoise
from nd_robotic.robot.robot import Robot
from nd_robotic.robot.state.kind.suprise import Suprise as SupriseState
from nd_utility.oop.inheritance.overriding.override_from import override_from
from typing import List

class BuildingSingleModalityForcastingModels(SupriseReducingAction):
    """
    By building suprise reduction model
    """
    def __init__(self) -> None:
        acceptance_threshold = self._compute_acceptance_threshold()

        # KL produces a scalar and when you give to scalars to Mahalonobis, it gives the absolute value of them
        acceptance_discrepancy_method = Mahalanobis()

        acceptance = SupriseAcceptance(acceptance_discrepancy_method, acceptance_threshold)

        #TODO, this must be determined by sigma+-mean of running on training set, or using the improvemnt methods so long that each for spliting the periods  we reach this confidence interval. Methods such as clustering and KF
        desired_suprise_state_value = 0.1
        desired_suprise_state = SupriseState(desired_suprise_state_value)
        goal = SurprisePoise(desired_suprise_state, acceptance)

        SupriseReducingAction.__init__(self, goal)

    def build_forcasting_modalities(self)->None:
        esps = Robot().get_event_specific_knowledge_episodes()
        forcasting_model_architecture = Robot().get_priming_forcasting_event
        forcasting_model_configs = Robot().get_priming_forcasting_models_training_configs()

        for esp in esps:
            mixed_traces = esp.get_trace_group().get_members()
            episode_modalities = mixed_traces.get_child_group_members()

            # here we are at either GPS or LIDAR (this can happen to a segregatable data)
            for modality in episode_modalities:
                # the difference between desired KL of prior and posterior and expected KL of prior and posterior
                modality_trace_group = modality.get_trace_group()
                sliding_window = SlidingWindow()
                input_target_train_sequences = SlidingWindowGenerator(modality_trace_group)

                priming_memory = Robot().get_priming_memory()
                forcasting_model_architecture = priming_memory.get_forcating_model_architecture()
                training_config = priming_memory.get_training_config()
                Training(forcasting_model_architecture, training_config, input_target_train_sequences)
                learned_parameters = Training.get_learned_parameters()



    def _build_sequence_to_sequence_model(self)-> Predicting:
        pass

    def _compute_acceptance_threshold(self)-> float:
        return 0.5

    def _compute_anomaly_values_by_test_episodes(self, test_episode:List[Episode])->List:
        return []

    @override_from(Action)
    def run(self):
        traces = self._learning_episodes.get_trace_group().get_members()
        # Phase 1: learn
        model_training_config = ...
        model_architecture = ...

        # Phase 2: test

        # Phase 3: test online



