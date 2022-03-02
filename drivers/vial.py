# imports

class Container:
    """container class"""
    max_volume: float
    current_volume: float
    add: bool
    remove: bool
    inert: bool

    def _get_volume(self):
        """
        Returns the current volume of a container.
        """
        return self.current_volume

    def _set_volume(self, current_volume):
        """
        Sets the current volume of a container to current_volume
        """
        self.current_volume = current_volume

    def update_volume(self):
        """

        """

    # Is full decorator (eventually)

    # Is empty decorator (eventually)

class StockVial(Container):
    """stock vial class"""
    add: bool = False
    remove: bool = True
    inert: bool = True

    def __init__(self, max_volume: float, current_volume: float):
        self.max_volume = max_volume
        self._set_volume(current_volume)

class ReactionVial(Container):
    """reaction vial class"""
    add: bool = True
    remove: bool = False
    inert: bool = True

    def __init__(self, max_volume: float, current_volume: float = 0): #set to 0?
        self.max_volume = max_volume
        self._set_volume(current_volume)

class Waste(Container):
    """waste container class"""
    add: bool = True
    remove: bool = False
    inert: bool = False

    def __init__(self, max_volume: float, current_volume: float):
        self.max_volume = max_volume
        self._set_volume(current_volume)

