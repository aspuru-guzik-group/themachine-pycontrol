import modbus_tk
import modbus_tk.defines as cst
import serial
from modbus_tk import modbus_rtu
import serial
from errors import CommunicationError

# TODO: Add errors as appropriate


# controller = None
#
# #   Initialize COM port
# def PortInit(Port="com4",BaudRate=9600):
#     global controller
#     controller = modbus_rtu.RtuMaster(serial.Serial(port=Port,baudrate=BaudRate, bytesize=8, parity='N', stopbits=1))
#     controller.set_timeout(0.10)
#     controller.set_verbose(True)
#
# def set_relay(Status = 0, Channel = 0):
#     Relays = 3
#     controller.execute(Relays, function_code = cst.WRITE_SINGLE_COIL, starting_address = Channel, output_value = Status)

class RelayModule:
    """Relay module"""
    module_address = 3  # Same as Relays variable above

    def __init__(self):
        self.controller = modbus_rtu.RtuMaster(serial.Serial(port="com4", baudrate=9600, bytesize=8, parity="N", stopbits=1)) #no spaces
        self.controller.set_timeout(0.10)
        self.controller.set_verbose(True)
        self.relays: list[Relay] = [Relay(i, self.controller, self.module_address) for i in range(1, 9)]

    def relay(self, relay_num) -> Relay:
        """
        Returns the Relay object corresponding to relay_num
        """
        return self.relays[relay_num - 1]


class Relay:
    """ Relay class"""

    def __init__(self, relay_num: int, controller: Master, module_address: int):
        self.relay_num = relay_num
        self.controller = controller
        self.module_address = module_address  # ?
        self.state = False

    def set_relay(self, status: bool = False):
        self.controller.execute(self.module_address, function_code=cst.WRITE_SINGLE_COIL, starting_address=0, output_value=status)

    def read_relay(self, channel = 0) -> bool:
        relay_state = self.controller.execute(self.module_address, function_code=cst.READ_COILS, starting_address=channel, quantity_of_x=1)[0]
        self._set_state(bool(relay_state))
        return self.state

    def _set_state(self, new_state: bool):
        self.state = new_state

    def _get_state(self) -> bool:
        return self.state

    @staticmethod
    def int_to_bool(value: int) -> bool:
        assert value in range(0, 2)
        return bool(value)

    @staticmethod
    def bool_to_int(value: bool) -> int:
        # TODO: Assertion?
        return int(value)
