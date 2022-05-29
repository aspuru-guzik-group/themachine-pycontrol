from typing import Union
from themachine_pycontrol.drivers.errors import CommunicationError, RangeError, HardwareError


class Vessel:
    """
    Defines a vessel, which may be a solution container, a reaction vial, a N2 tank, or a waste bottle.

    == Public Attributes ==
    max_volume: The maximum volume in mL a vessel can contain
    current_volume: The current volume occupied in a vessel
    min_volume: The minimum volume that can be withdrawn from a vessel

    """

    def __init__(self, max_volume: Union[float, int], current_volume: Union[float, int], addable: bool, removable: bool):
        """
        Initializes a container object
        """
        self.max_volume = max_volume
        self.min_volume = self.max_volume * 0.1
        self._set_volume(current_volume)
        self.addable = addable
        self.removable = removable

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

    def update_volume(self, vol_change: float, direction: bool):
        """
        Sets an updated volume by adding volume_change to old_volume 
        """
        prev_volume: float = self._get_volume()
        self._check_transfer_volume(vol_change)
        self._check_transfer_possible(direction)
        self._set_volume(prev_volume + vol_change)
        print(f"The volume of this vessel is now {self.current_volume}")

    def _check_transfer_volume(self, vol_change: float) -> bool:
        """
        Returns remaining volume in a container.value

        vol_to_add: positive or negative
        """    
        check_vol: float = self.current_volume + vol_change
        if check_vol > self.max_volume:
            raise RangeError(f"The resulting volume {check_vol} from this transfer would exceed"
                             f" the vessel's max volume of {self.max_volume}")
        elif check_vol < self.min_volume:
            raise RangeError(f"The resulting volume {check_vol} from this transfer would be below"
                             f" the vessel's minimum volume of {self.min_volume}")
        else:
            return True

    def _check_transfer_possible(self, direction: bool) -> bool:
        """


        """
        if direction:
            if self.removable:
                return True
            else:
                raise HardwareError("This vessel cannot be drawn from.")
        else:
            if self.addable:
                return True
            else:
                raise HardwareError("This vessel cannot be added to.")


def main():
    sln1 = Vessel(200, 150, False, True)
    sln1.update_volume(-20, True)


if __name__ == "__main__":
    main()
