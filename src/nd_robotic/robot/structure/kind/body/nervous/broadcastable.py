from typing import Protocol, List


class BroadcastableProtocol(Protocol):
    load: bytes
    destinations:List[str]