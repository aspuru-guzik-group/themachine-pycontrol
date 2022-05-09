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

def ctrl_decorator(func):
    def wrapper(self, com_num, *args, **kwargs):
        self.controller(com_num)
        output = func(self, com_num, *args, **kwargs)
        del self.controller
        return output
    return wrapper


@singleton
class RelayModule:
    """Relay module"""
    #module_address = 3  # Same as Relays variable above

    def __init__(self):
        self.controller = None

    @property
    def controller(self):
        return self.controller

    @controller.setter
    def controller(self, com_num):
        ser = serial.Serial(port=com_num, baudrate=9600, bytesize=8, parity="N", stopbits=1)
        self.controller = modbus_rtu.RtuMaster(ser)
        self.controller.set_timeout(0.10)
        self.controller.set_verbose(True)

    @controller.deleter
    def controller(self):
        ser.close()
        del self.controller

    @ctrl_decorator
    def relay_control(self, com_num, module_address, channel, status):
        # with serial.Serial(port=com_num, baudrate=9600, bytesize=8, parity="N", stopbits=1) as ser:
        #     self.controller = modbus_rtu.RtuMaster(ser)
        #     self.controller.set_timeout(0.10)
        #     self.controller.set_verbose(True)
        self.controller.execute(module_address, function_code=cst.READ_COILS, starting_address=channel, output_value=status)
        print(f"Relay number {channel+1} has been set to {status}.")
        
    @controller
    def relay_read(self, com_num, module_address, channel, status=None):
        # with serial.Serial(port=com_num, baudrate=9600, bytesize=8, parity="N", stopbits=1) as ser:
        #     self.controller = modbus_rtu.RtuMaster(ser)
        #     self.controller.set_timeout(0.10)
        #     self.controller.set_verbose(True)
        relay_state = self.controller.execute(self.module_address, function_code=cst.READ_COILS, starting_address=channel, quantity_of_x=1)[0]
        return relay_state


class Relay:
    """ Relay class"""

    def __init__(self, relay_num: int, com_num: int, module_address: int):
        self.relay_num = relay_num
        self.module = RelayModule()
        self.module_address = module_address
        self.state = False
        self.channel = self.relay_num - 1

    def set_relay(self, status: bool = False):
        self.module.relay_control(self.com_num, self.module_address, self.channel, status)
        self._set_state(status)

    def read_relay(self) -> bool:
        #relay_state = self.controller.execute(self.module_address, function_code=cst.READ_COILS, starting_address=self.channel, quantity_of_x=1)[0]
        relay_state = self.module.relay_read(self.com_num, self.module_address, self.channel)
        self._set_state(bool(relay_state))
        return self.state

    def _set_state(self, new_state: bool):
        self.state = new_state

    def _get_state(self) -> bool:
        return self.state
