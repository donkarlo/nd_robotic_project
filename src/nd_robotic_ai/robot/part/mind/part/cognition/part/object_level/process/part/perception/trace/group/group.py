from nd_utility.data.kind.dic.dic import Dic


class Group:
    """
    Modality is one branch of a dic with its sequential data. time should not be considered  as an independent modality. Either the order of data represents the time or the time lable
    """

    def __init__(self, dic: Dic):
        self._dic = dic