from utilityx.data.source import Source
from utilityx.data.source.type import Type
from utilityx.data.source.format import Format

class SensorSetDataFillerFromMixedYaml():
    def __init__(self, obss_source:Source):
        self._obss_source = obss_source
        if obss_source.get_format() == Format.YAML and obss_source.get_kind() == Type.FILE:
            self._obss_source

if __name__ == "__main__":
    pass
