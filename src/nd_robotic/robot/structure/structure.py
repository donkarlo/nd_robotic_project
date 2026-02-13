from nd_utility.data.kind.dic.dic import Dic
from nd_utility.data.storage.kind.file.yaml.yaml import Yaml as YamlStorage
from nd_utility.oop.design_pattern.structural.composite.leaf import Leaf
from nd_utility.os.file_system.file.file import File as OsFile
from nd_utility.os.file_system.path.file import File as FilePath
from typing import Optional

class Structure(Leaf):
    """
    Stryctuure is the joint to exchange messages in for of traces to action. it can be considerer spinal cord + brain
    TODO: This structure must be made of composite pattern
    TODO: rename to embodyment as it represents both mind and body
    """
    def __init__(self, name: Optional[str]):
        Leaf.__init__(self, name)


        self._schema = None

    def get_schema(self) -> Dic:
        if self._schema is None:
            # it is in current folder
            current_dir_path = FilePath(__file__).get_containing_abolute_directory_path()
            current_file_path = current_dir_path + "structure.yaml"
            yaml_os_file = OsFile(FilePath(current_file_path), None, None)
            yaml = YamlStorage(yaml_os_file, None)
            self._schema = yaml.get_ram()
        return self._schema

    def draw(self):
        self.get_schema().draw()


if __name__ == "__main__":
    schema = Structure().draw()
