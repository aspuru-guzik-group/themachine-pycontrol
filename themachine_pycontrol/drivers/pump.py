import pkg_resources
from singleton_decorator import singleton
from typing import List
from errors import CommunicationError, HardwareError, RangeError

import clr
PUMP_DLL = pkg_resources.resource_filename("themachine_pycontrol", "drivers/KEMPumpDLL")
clr.AddReference(PUMP_DLL)
from KEMPumpDLL import SyringePumpDef


class Pump:
    """
    Defines a pump object.

    == Public Attributes ==
    pump_num: The number that identifies a given pump

    == Representation Invariants ==
    - pump_num must be between 1-7 inclusive
    - pump_status must be either False (inactive) or True (active)

    """
    waste_port: int = 5

    def __init__(self, pump_num: int):
        self.pump_num = pump_num
        self.controller = PumpModule()  # Singleton Object
        self.controller.initialize(pump_num)
        self.pump_port: int = self.waste_port

    def _set_current_port(self, new_pump_port: int):
        """
        Sets the value of self.current_port to new_pump_port
        """
        self.pump_port = new_pump_port

    def move(self, new_port: int, top_speed: float, volume: float, wait_ready: bool = True) -> None:
        """
        Moves a pump to the port new_port and moves the plunger of the pump to the
        position of the syringe corresponding to the volume volume at the speed top_speed.
        """
        self._move_port(new_port)
        self._move_piston(top_speed, volume, wait_ready)
        print(f"Pump is ready to dispense {volume} mL to port {new_port}.")

    def _move_port(self, new_port: int):
        """
        Moves the pump to a new port and sets the pump_port number accordingly
        """
        self.controller.set_port(self.pump_num, new_port)
        self._set_current_port(new_port)

    def _move_piston(self, top_speed: float, volume: float, wait_ready: bool = True):
        """
        Moves the pump piston accordingly to transfer the specified amount
        """
        self.controller.move_piston(self.pump_num, top_speed, volume, wait_ready)

    def dispense(self, src_port: int, dst_port: int, top_speed: float, volume: float, wait_ready: bool = True):
        """docstring"""
        self.move(src_port, top_speed, volume, wait_ready)
        self.move(dst_port, top_speed, 0, wait_ready)

    def rinse(self, soln_port: int, top_speed: float, volume: float, wait_ready: bool = True):
        """Rinse the syringe from sol to waste_port."""
        self.dispense(soln_port, self.waste_port, top_speed, volume, wait_ready)


@singleton
class PumpModule(object):
    """
    Defines a pump module, which contains all pumps.

    === Public Attributes ===
    num_pumps: The total number of pumps the module contains
    controller: The controller object used to perform all pump-related functions
    pumps: A list of all pumps contained in the pump module

    === Representation Invariants ===

    """
    steps_per_vol: int = 307200  # Steps per mL for a 10 mL syringe.
    max_num_pumps: int = 7
    waste_port: int = 5

    def __init__(self):
        """
        Initializes the pump module, which contains all pumps.

        Precondition: module must be open to communication
        """
        self.controller = SyringePumpDef()
        if not self.controller.OpenCommunications():
            # TODO: This error msg should be more specific that comm failed with pump module.
            raise CommunicationError("Communication failed.")
        self.pumps: dict = {i + 1: False for i in range(self.max_num_pumps)}

    def initialize_pump(self, pump_number: int) -> None:
        """
        Activates a pump.
        """
        if self.controller.DiscoverModule(pump_number):
            self._prime(pump_number)
        else:
            raise CommunicationError(f"Pump {pump_number} could not be discovered.")

    def _prime(self, pump_number: int) -> None:

        """
        Initializes a given pump at start of exp. This must be done at the start.
        """
        if self.controller.Initialize(pump_number, self.waste_port):
            self._set_pump_status(pump_number, True)
            print(f"Pump {pump_number} is initialized.")
        else:
            self._set_pump_status(pump_number, False)
            raise HardwareError(f"Pump {pump_number} failed to initialize while priming.")

    def _set_pump_status(self, pump_number: int, new_pump_status: bool) -> None:
        """
        Sets the value of self.pump_status to pump_status, where pump_status is True or False.
        """
        self.pumps[pump_number] = new_pump_status

    def set_port(self, pump_number: int, port_number: int) -> None:
        """
        Sets the port of a given pump to a given position
        """
        # FIXME: See same comment from hotplate.py
        try:
            assert self.pumps[pump_number]
        except AssertionError:
            raise HardwareError("Requested pump is not active.")
            # TODO: Give pump number in error msg.
        self.controller.Port(pump_number, port_number, True)

    def move_piston(self, pump_number: int, top_speed: float, volume: float, wait_ready: bool = True) -> None:
        """
        Moves the piston of a specific pump to the target position to dispense a given volume.
        """
        # FIXME: See same comment from hotplate.py
        try:
            assert self.pumps[pump_number]
        except AssertionError:
            raise HardwareError("Requested pump is not active.")
            # TODO: Give pump number in error msg.
        self.controller.Speed(pump_number, top_speed)
        position: float = volume * self.steps_per_vol
        self.controller.MoveToPosition(pump_number, position, wait_ready)

    def close(self) -> None:
        """
        Closes communication to the pump module. Only close at the end of a reaction, never during.
        """
        self.controller.CloseCommPort()
