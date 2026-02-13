from typing import List
from nd_utility.data.kind.dic.dic import Dic


class FrameSequence:
    def __init__(self, frame_list: List[str]):
        """

        Args:
            frame_list: from parent to _children
        """
        self._frame_list = frame_list

    def get_frame_list(self) -> List[str]:
        return self._frame_list

    @classmethod
    def init_from_message_dic(cls, dic:Dic)->"FrameIdStack":
        frames_seq_ids_str:str = dic["header"]["frame_id"]
        frames_seq_ids = frames_seq_ids_str.split("/")
        frame_seq = []
        for frame_id in frames_seq_ids:
            frame_seq.append(Frame(frame_id))