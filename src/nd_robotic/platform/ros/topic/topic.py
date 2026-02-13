from nd_robotic.platforms.ros.message.message import Message
from rosx.topic.one_to_many import OneToMany


class Topic:
    def __init__(self, message_type:):
        pass

    def add_publisher(self, publisher:Node):
        pass

    def add_subscriber(self, subscriber:Node):
        pass

    def publish_message(self, publisher:Node , message:Message):
        if publisher in self._publishers:
            self._add_to_published_messages()