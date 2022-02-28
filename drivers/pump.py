import sys
import clr
clr.AddReference(r"C:\Users\AAG Group\Dropbox (Aspuru-Guzik Lab)\TheMachine\Python Code\drivers\KEMPumpDLL")
#print(os.getcwd())
#DLL_Address = os.getcwd()+'\KEMPumpDLL'
#clr.AddReference(DLL_Address)

from KEMPumpDLL import SyringePumpDef


class PumpModule:
    """
    Defines a pump module, which contains all pumps.

    === Public Attributes ===
    num_pumps: The total number of pumps the module contains

    === Representation Invariants ===


    """
    num_pumps: int = 8

    def __init__(self):
        """
        Initializes the pump module, which contains all pumps.

        Precondition: module must be open to communication
        """
        self.controller = SyringePumpDef()
        if not self.controller.OpenCommunications():
            raise Exception("Communication failed.")
        self.pumps = [Pump(i, self.controller) for i in range(1, self.num_pumps + 1)]

    def get_status_list(self):
        return [self.pumps[i].pump_status for i in range(0, self.num_pumps)]

    def close(self):
        """
        Closes communication to the pump. Only close at the end of a reaction, never during.
        """
        self.controller.CloseCommPort()


class Pump:
    """
    Defines a pump, where all pumps are part of a pump module in the PumpModule class.

    == Public Attributes ==
    pump_num: The number that identifies a given pump

    == Representation Invariants ==
    - pump_num must be between 1-7 inclusive
    - pump_status must be either False (inactive) or True (active)

    """
    waste_port: int = 5

    def __init__(self, pump_num: int, controller: SyringePumpDef, pump_port: int = waste_port, pump_status: bool = False):
        self.pump_num = pump_num
        self._set_current_port(pump_port)
        self._set_pump_status(pump_status)
        self.controller = controller
        if self.controller.DiscoverModule(pump_num):
            self.controller.priming()
        else:
            raise Exception(f"Module {self.pump_num} failed to be discovered.")

    def _set_pump_status(self, new_pump_status: bool):
        """
        Sets the value of self.pump_status to pump_status, where pump_status is True or False.
        """
        self.pump_status = new_pump_status

    def _set_current_port(self, new_pump_port: int):
        """
        Sets the value of self.current_port to new_pump_port
        """
        self.pump_port = new_pump_port

    def priming(self):
        """
        Initializes a given pump at start of exp. This must be done at the start. Do NOT reinitialize
        (call only once).
        """
        # waste_port = 5
        if self.controller.Initialize(self.pump_num, self.waste_port):
            self._set_pump_status(True)
            print(f"Pump {self.pump_num} is initialized.")
        else:
            self._set_pump_status(False)
            raise Exception(f"Pump number {self.pump_num} failed to initialize.")

    def move(self, new_port, topspeed, volume, wait_ready: bool = True): #lowercase
        """
        Moves a pump to the port new_port and moves the plunger of the pump to the
        position of the syringe corresponding to the volume volume at the speed topspeed.

        Precondition: Pump must be active, ie pump_status == True
        """
        if self.pump_status:
            self._move_port(new_port)
            self._move_piston(topspeed, volume, wait_ready)
            print(f"Pump is ready to dispense {volume} mL to port {new_port}.") #unsure if it actually dispenses
        else:
            raise Exception("Pump is not active.")

    def _move_port(self, new_port):
        """
        Sets the port of a given pump to new_port.

        Precondition: Pump is active, ie pump_status == True
        """
        if self.pump_status:
            self.controller.Port(self.pump_num, new_port, True)
            self._set_current_port(new_port)
        else:
            raise Exception("Pump not active.")

    def _move_piston(self, topspeed: int, volume: int, wait_ready: bool = True):
        """
        Sets piston speed to topseed, then moves piston to the position corresponding to volume volume.

        Precondition: pump is active, ie pump_status == True
        """
        if self.pump_status:
            self.controller.Speed(self.pump_num, topspeed)
            position = volume * 307200
            self.controller.MoveToPosition(self.pump_num, position, wait_ready)
        else:
            raise Exception("Pump is not active.")

    def dispense(self, src_port: int, dst_port: int, ...): #same args as Pump.move()
        """docstring"""
        # self.move(src_port, ..., volume = volume, ...)
        # self.move(dst_port, ..., volume = 0, ...)

    def rinse(self, soln_port, ...):
        """Rinse the syringe from sol to waste_port."""
        # self.dispense(soln_port, waste_port, ...)






