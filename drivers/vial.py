# imports

class Container:
    """container class"""
    min_volume: float  # TODO: Add to subclasses
    max_volume: float
    current_volume: float

    def _get_volume(self) -> float:
        """
        Returns the current volume of a container.
        """
        return self.current_volume

    def _set_volume(self, new_volume: float):
        """
        Sets the current volume of a container to current_volume
        """
        self.current_volume = new_volume

    def _update_volume(self, volume_change: float):
        """
        Sets an updated volume by adding volume_change to old_volume 
        """
        prev_volume: float = self._get_volume()
        self._set_volume(prev_volume + volume_change)

    def check_transfer(self, vol_change: float) -> bool:
        """
        Returns remaining volume in a container.value

        vol_to_add: positive or negative
        """    
        check_vol: float = self.current_volume + vol_change
        if (check_vol > self.max_volume) or (check_vol < self.min_volume):
            return False
        else:
            return True
