from pyvisa import ResourceManager
import time
from typing import Union
from errors import CommunicationError, HardwareError

COM_LIST = [10, 7, 11, 10, 5, 9, 8]
rm = ResourceManager()

# TODO: use a decorator to wrap all functions with open and close valve
# close.controller() still has to be written above all raise Exceptions


def close(func):
    def wrapper(self, *args, **kwargs):
        controller = rm.open_resource(self.com_port_cmd)
        func(self, *args, **kwargs)
        controller.close()
    return wrapper


class Valve:
    """
    Describes one of the four valves on each valve module.
    Valves should only be instantiated through the ValveModule class.

    === Public Attributes ===
    valve_num: Identifies the valve number of a given valve in a module
    module_num: Identifies the module to which the valve belongs
    current_port: Identifies the current port a valve is open to

    === Private Attributes ===

    == Representation Invariants ===
    - valve_module must be a number between 1-6 inclusive
    - valve_num must be a number between 1-4 inclusive
    - valve_port is between 1 and 8 inclusive
    """
    num_ports = 8

    def __init__(
        self, valve_num: int, com_num: int
    ):  # Should we allow init w/ current_port != 8?
        """
        Initialize a new controller. Default port is port 8.
        """
        self.valve_num = valve_num
        # self.module_num = module_num
        self.current_port: int = 8
        # com_num = COM_LIST[module_num - 1]
        self.com_num = com_num
        self.com_port_cmd = f"ASRL{self.com_num}::INSTR"

    def _set_current_port(self, new_port: int):
        """
        Sets the value of self.current_port to valve_port.
        """
        self.current_port: int = new_port

    @close
    def get_current_port(self) -> int:
        """
        Returns the current valve position or port number.
        """
        controller = rm.open_resource(self.com_port_cmd)
        for _ in range(10):
            command = f"/{self.valve_num}?8"
            controller.write(command)
            time.sleep(1)
            returned_bytes: bytes = controller.read_bytes(4)
            try:
                last_byte: str = returned_bytes.decode()[-1]
                returned_port: int = int(last_byte)
                if returned_port in range(1, self.num_ports+1):
                    self._set_current_port(returned_port)
                    #controller.close()
                    return returned_port
            except ValueError:
                continue
        controller.close()
        raise CommunicationError("Querying port failed.")

    @close
    def move(self, valve_port: int):
        """
        Moves a given valve to a selected port.

        Precondition: Valve port is between 1 and 8 inclusive
        """
        assert valve_port in range(1, 9), f"Submitted {valve_port}"
        controller = rm.open_resource(self.com_port_cmd)
        command = f"/{self.valve_num}o{valve_port}R"
        for _ in range(10):
            controller.write(command)
            time.sleep(2)
            if self.get_current_port() == valve_port:
                print(
                    # f"Valve {self.valve_num} of module {self.module_num} has been moved to port {self.current_port}."
                    f"Valve {self.valve_num} has been moved to port {self.current_port}."
                )
                #controller.close()
                return
        controller.close()
        raise HardwareError(f"Moving valve {self.valve_num} to port {valve_port} failed.")




# class ValveModule:
#     """
#     Describes a module, each of which contains four valves.
#
#     === Public Attributes ===
#     module_num: Identifies the given module by a number 1-6
#     valves:
#
#     === Private Attributes ===
#
#     === Representation Invariants ===
#     - module_num is between 1 and 6 inclusive
#
#
#     """
#     def __init__(self, module_num: int):
#         """
#         Initialize a valve module.
#
#         """
#         self.module_num = module_num - 1
#         #com_num = COM_LIST[module_num]
#         #self.com_port = f'ASRL{com_num}::INSTR' #are this and valves private?
#         self.valves: list[Valve] = [Valve(i, self.module_num) for i in range(1, 5)]
#
#     def valve(self, valve_num: int) -> Valve:
#         """function that returns valve instance"""
#         return self.valves[valve_num - 1]


def cli_main():



if __name__ == "__main__":
    cli_main()
