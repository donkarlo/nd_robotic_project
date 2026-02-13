class OneToMany:
    '''
    ROS 2 breaks complex systems down into many modular nodes.
    Topics are a vital element of the ROS graph that role as a bus for nodes to exchange messages.
    A Topic is a bus/tunnel through which messages move
    '''
    def __init__(self, publisher:Node, subscribers:list[Node,...]):
        self._publisher = publisher
        self._subscribers = subscribers