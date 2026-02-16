from nd_data_science.machine_learning.model.application.sequence_to_sequence.kind.time_series.kind.transformer.kind.uncertainty.gaussian.architecture.architecture import \
    Architecture as BaseArchitecture
from nd_utility.data.kind.dic.dic import Dic


class Architecture(BaseArchitecture):
    def __init__(self, overriding_architecture_dic: Dic):
        required_to_override = ["input_feature_dimension"] #must be 3 for example for the position - its not the tarining sequence
        for key in required_to_override:
            if key not in overriding_architecture_dic:
                raise KeyError(f"overriding_architecture must provide {key!r}.")
            if overriding_architecture_dic[key] is None:
                raise ValueError(f"overriding_architecture must provide a non-None value for {key!r}.")

        self._overriding_architecture_dic = overriding_architecture_dic
        self._base_architecture_dic = Dic({
            "model_dimension": 64,
            "number_of_attention_heads": 8,
            "feed_forward_dimension": 128,
            "input_feature_dimension": self._overriding_architecture_dic["input_feature_dimension"],
            "output_sequence_size": 100,
            "output_feature_dimension": self._overriding_architecture_dic["output_feature_dimension"],
            "maximum_time_steps": 2048,
            "dropout_rate": 0.1
        })
        self._architecture_dic = Dic({}).merge_dic(self._base_architecture_dic).merge_dic(self._overriding_architecture_dic)
        BaseArchitecture.__init__(self, **self._architecture_dic)

    def get_architecture_dic(self) -> Dic:
        return self._architecture_dic

    def get_base_architecture_dic(self) -> Dic:
        return self._base_architecture_dic

    def get_overriding_architecture_dic(self) -> Dic:
        return self._overriding_architecture_dic
