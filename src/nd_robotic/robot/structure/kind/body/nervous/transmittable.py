from typing import Protocol,List

class Transmittable(Protocol):
    source:str
    destination:str
    supporting_channels:List[str]