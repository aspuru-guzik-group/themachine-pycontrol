import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


# master = None
#
# #   Initialize COM port
# def PortInit(Port="com4",BaudRate=9600):
#     global master
#     master = modbus_rtu.RtuMaster(serial.Serial(port=Port,baudrate=BaudRate, bytesize=8, parity='N', stopbits=1))
#     master.set_timeout(0.10)
#     master.set_verbose(True)
#
# def set_relay(Status = 0, Channel = 0):
#     Relays = 3
#     master.execute(Relays, function_code = cst.WRITE_SINGLE_COIL, starting_address = Channel, output_value = Status)

class RelayModule:
    """Relay module"""
    module_address = 3 # Same as Relays variable above

    def __init__(self):
        #TODO: Put PortInit functionality in here.
        #TODO: Create list of 8 Relay objects, passing modbus_rtu.RtuMaster object to each.

    def relay(self):
        #TODO: Return Relay in list from 1-indexed counting. (see valve.py)

class Relay:
    """ Relay class"""

    def __init__(self):
        #TODO: Accept RtuMaster object as argument.
        #TODO: Accept arg for mod_address
        #TODO: arg: relay number (from 1)
        self.state = 0

    def set_relay(self, state: bool):
        #TODO: Adapt from Han's set_relay() above.
        #TODO: convert from bool to int

    def read_relay(self) -> bool:
        #TODO: Reads returns relay state.
        #TODO: convert into to bool
        #TODO: Update self.state with _set_state()
        return ...

    def _set_state(self):
        #TODO: Update self.state

    def _get_state(self):
        #TODO: Return self.state

    @staticmethod
    def int_to_bool(value: int) -> bool:
        #TODO: assert value is 0 or 1
        return bool(value)

    @staticmethod
    def bool_to_int(value: bool) -> int:
        #TODO: Assertion
        return int(value)


