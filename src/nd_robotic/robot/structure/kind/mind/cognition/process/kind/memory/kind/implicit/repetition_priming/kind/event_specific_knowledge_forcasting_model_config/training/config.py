from nd_data_science.machine_learning.model.application.sequence_to_sequence.kind.time_series.kind.transformer.kind.uncertainty.gaussian.training.config import \
    Config as BaseTrainingConfig
from nd_utility.data.kind.dic.dic import Dic


class Config(BaseTrainingConfig):
    def __init__(self, overriding_config: Dic):
        self._overriding_config_dic = overriding_config
        self._base_config_dic = Dic({
            "training_sequence_size": None,
            "input_sequence_size": 100,
            "output_sequence_size": 100,
            "sequence_overlap_size": 10,
            "epochs": 10,
            "batch_size": 4,
            "learning_rate": 1e-3,
            "shuffle": True
        })
        self._config_dic = Dic({}).merge_dic(self._base_config_dic).merge_dic(self._overriding_config_dic)
        BaseTrainingConfig.__init__(self, **self._config_dic)

    def get_overriding_config_dic(self) -> Dic:
        return self._overriding_config_dic

    def get_base_config_dic(self) -> Dic:
        return self._base_config_dic

    def get_config_dic(self) -> Dic:
        return self._config_dic
