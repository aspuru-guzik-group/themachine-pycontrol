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
    module_address = 3  # Same as Relays variable above

    def __init__(self, master):
        # FIXME: Change 'master' var name to 'controller' for consistency across code.
        self.master = modbus_rtu.RtuMaster(serial.Serial(port = "com4", baudrate=9600, bytesize=8, parity='N', stopbits=1))
        # FIXME: No spaces between arg, = and value in function call.
        # This is probably causing a PEP 8: E251 error for you (warning or weak warning)
        self.master.set_timeout(0.10)
        self.master.set_verbose(True)
        self.relays: list[Relay] = [Relay(i, self.master, self.module_address) for i in range(1,9)]
        # FIXME: Space after comma when entering multiple args (PEP8: E231 for range)

    def relay(self, relay_num) -> Relay:
        # FIXME: No docstring
        return self.relays[relay_num - 1]


class Relay:
    """ Relay class"""

    def __init__(self, relay_num: int, master: Master, module_address):
        self.relay_num = relay_num
        self.master = master
        self.module_address = module_address  # ?
        self.state = False

    def set_relay(self, status: bool = False):
        # FIXME: master reference is unresolved
        # FIXME: spaces before/after variable assignment in func call
        master.execute(self.module_address, function_code = cst.WRITE_SINGLE_COIL, starting_address = 0, output_value = status)

    def read_relay(self, channel = 0) -> bool:
        # FIXME: master reference is unresolved
        # FIXME: Relays reference is unresolved (leftover var name from Han's code)
        # FIXME: spaces before/after variable assignment in func call
        # FIXME: res var name is unclear. Change to smth more informative
        res = master.execute(Relays, function_code = cst.READ_COILS, starting_address = channel, quantity_of_x = 1)[0]
        self._set_state(bool(res))
        return self.state

    def _set_state(self, new_state: bool):
        self.state = new_state

    def _get_state(self):  # FIXME: Typehint return!
        return self.state

    @staticmethod
    def int_to_bool(value: int) -> bool:
        assert value in range(0,2)
        # FIXME: Space after comma when entering multiple args (PEP8: E231 for range)
        return bool(value)

    @staticmethod
    def bool_to_int(value: bool) -> int:
        # TODO: Assertion?
        return int(value)


