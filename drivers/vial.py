# imports

class Container:
    """container class"""
    max_volume: float
    current_volume: float
    add: bool
    remove: bool
    inert: bool

    def _get_volume(self):

    def _set_volume(self):

    def update_volume(self):

    # Is full decorator (eventually)

    # Is empty decorator (eventually)

class StockVial(Container):
    """stock vial class"""
    #TODO: Set values for add, remove and inert variable
    def __init__(self):
        #TODO: Set values for max_volume and current_volume


class ReactionVial(Container):
    """reaction vial class"""
    # TODO: Set values for add, remove and inert variable
    def __init__(self):
        # TODO: Set values for max_volume and current_volume

class Waste(Container):
    """wate container class"""
    # TODO: Set values for add, remove and inert variable
    def __init__(self):
        # TODO: Set values for max_volume and current_volume

