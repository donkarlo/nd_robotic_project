from typing import List
from nd_utility.data.kind.dic.dic import Dic


class FrameIdStack:
    def __init__(self, frame_id_list: List[str]):
        """

        Args:
            frame_id_list: from parent to _children
        """
        self._frame_id_list = frame_id_list

    def get_frame_list(self) -> List[str]:
        return self._frame_id_list

    @classmethod
    def init_from_message_dic(cls, dic:Dic)-> "FrameIdStack":
        frame_id_seq_str:str = dic["header"]["frame_id"]
        frames_id_seq_splitted = frame_id_seq_str.split("/")
        return cls(frames_id_seq_splitted)