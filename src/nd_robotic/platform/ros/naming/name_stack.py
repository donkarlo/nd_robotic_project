

class NameStack:
    """or namespace in ros"""
    def __init__(self, names:List[str]):
        self._names = names

    @classmethod
    def init_from_seprated_string(cls, separated_string:str, separator="/")->"NameStack":
        names = separated_string.split(separator)
        return cls(names)