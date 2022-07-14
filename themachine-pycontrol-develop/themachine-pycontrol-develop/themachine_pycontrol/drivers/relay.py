import modbus_tk
import modbus_tk.defines as cst
import serial
from modbus_tk import modbus_rtu
import serial
from themachine_pycontrol.drivers.errors import CommunicationError
from singleton_decorator import singleton

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
    """
    Defines a relay module, each of which contains 8 relays.

    === Public Attributes ===
    controller: the controller object used to perform all relay-related functions.

    === Representation Invariants ===

    """
    #module_address = 3  # Same as Relays variable above

    def __init__(self):
        """
        Initializes an object of the relay module singleton class.
        """
        self.controller = None

    @property
    def controller(self):
        """
        Getter function that returns the controller object.
        """
        return self.controller

    @controller.setter
    def controller(self, com_num):
        """
        Setter function that sets the content of self.controller.
        """
        ser = serial.Serial(port=com_num, baudrate=9600, bytesize=8, parity="N", stopbits=1)
        self.controller = modbus_rtu.RtuMaster(ser)
        self.controller.set_timeout(0.10)
        self.controller.set_verbose(True)

    @controller.deleter
    def controller(self):
        """
        Deleter function that deletes the controller object.
        """
        ser.close()
        del self.controller

    @ctrl_decorator
    def relay_control(self, com_num, module_address, channel, bool_status):
        # NOTE: com_num is unused -> This is required for the decorator!
        """
        Changes the relay status of the relay corresponding to the channel number to bool_status.
        """
        # with serial.Serial(port=com_num, baudrate=9600, bytesize=8, parity="N", stopbits=1) as ser:
        #     self.controller = modbus_rtu.RtuMaster(ser)
        #     self.controller.set_timeout(0.10)
        #     self.controller.set_verbose(True)
        status = int(bool_status)
        self.controller.execute(module_address, function_code=cst.READ_COILS, starting_address=channel, output_value=status)
        print(f"Relay number {channel+1} has been set to {status}.")
        
    @ctrl_decorator
    def relay_read(self, com_num, channel):
        # NOTE: com_num is unused -> Same as above!
        """
        Queries and returns the current relay status of the relay corresponding to channel.
        """
        # with serial.Serial(port=com_num, baudrate=9600, bytesize=8, parity="N", stopbits=1) as ser:
        #     self.controller = modbus_rtu.RtuMaster(ser)
        #     self.controller.set_timeout(0.10)
        #     self.controller.set_verbose(True)
        relay_state = self.controller.execute(self.module_address, function_code=cst.READ_COILS, starting_address=channel, quantity_of_x=1)[0]
        return relay_state


class Relay:
    """
    Defines a relay object, which controls a solenoid.

    === Public Attributes ===
    relay_num: the number identifying each relay
    com_num: the COM port number for communicating to a given relay
    module: the relay module to which a given relay belongs
    module_address: the address of the given relay's relay module
    state: the on vs. off state 
    channel: the number on the relay hardware corresponding to a given relay channel
    

    === Representation Invariants ===


    """

    def __init__(self, relay_num: int, com_num: int, module_address: int):
        """
        Instantiates a relay object.
        """
        self.relay_num = relay_num
        self.com_num = com_num
        self.module = RelayModule()
        self.module_address = module_address
        self.state: bool = False
        self.channel = self.relay_num - 1

    def set_relay(self, status: bool = False):
        """
        Sets the relay's on/off state to status.
        """
        self.module.relay_control(self.com_num, self.module_address, self.channel, status)
        self._set_state(status)

    def read_relay(self) -> bool:
        """
        Queries then returns the relay's current on/off state.
        """
        #relay_state = self.controller.execute(self.module_address, function_code=cst.READ_COILS, starting_address=self.channel, quantity_of_x=1)[0]
        relay_state = self.module.relay_read(self.com_num, self.channel)
        self._set_state(bool(relay_state))
        return self.state

    def _set_state(self, new_state: bool):
        """
        Sets self.state to new_state.
        """
        self.state = new_state

    def _get_state(self) -> bool:
        """
        Returns self.state.
        """
        return self.state
