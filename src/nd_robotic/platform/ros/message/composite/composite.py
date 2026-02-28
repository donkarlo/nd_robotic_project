from nd_robotic.platform.ros.message.composite.component import Component
from nd_robotic.platform.ros.message.field.field import Field
from nd_robotic.platform.ros.message.message import Message
from nd_utility.data.kind.dic.dic import Dic


class Composite(Component):
    def __init__(self, name):
        self._name = name
        self._children:List[Component] = []

    def add_child(self, child: Component):
        """

        Args:
            child: is either a Message or RotorComposite

        Returns:

        """
        self._children.append(child)

    def convert_to_dic(self):
        for child in self._children:
            child.convert_to_dic()

    def init_from_dic(self, dic:Dic):
        fields: List[Field] = []
        for key, val in dic.get_raw_dict().items():
            if isinstance(val, dict):

                composite = Composite(key)
                self.init_from_dic(Dic(val))
                self.add_child(composite)

                if len(fields) > 0:
                    message = Message(fields)
                    composite.add_child(message)
            else:
                field = Field(key, val, type(val))
                fields.append(field)