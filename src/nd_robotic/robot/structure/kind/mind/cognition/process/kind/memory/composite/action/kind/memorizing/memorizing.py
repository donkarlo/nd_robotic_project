class Memorizing:
    """
    - The _layers place will be detrmined
    - memory can not memorize unless it is given a meaningful action_potential_group of trace such as Working/Composite/Componnet
    """
    def __init__(self):
        #should be set by calling set _layers from Working class
        self._experience_group = None

    def memorize(self)->None:
        """
        What entities exist to memorize

        """
        pass

    def set_memory_tree(self, experience_group: ExperienceGroup) -> None:
        self._experience_group = experience_group