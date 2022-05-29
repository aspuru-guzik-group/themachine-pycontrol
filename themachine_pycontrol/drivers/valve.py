from pyvisa import ResourceManager
from pyvisa.resources import Resource
import time
from typing import Union
from themachine_pycontrol.drivers.errors import CommunicationError, HardwareError, RangeError

RM = ResourceManager()


def open_close_controller(func):
    def wrapper(self, *args, **kwargs):
        controller: Resource = RM.open_resource(self.com_port_cmd)
        output = func(self, *args, controller=controller, **kwargs)
        controller.close()
        return output
    return wrapper


def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        function = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time() - start} seconds")
        return function
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

    # NOTE: The Valve class doesn't support multiple valve modules anymore. Should we add that capability?
    def __init__(self, valve_num: int, com_num: int):
        # Should we allow init w/ current_port != 8?
        """
        Initialize a new controller. Default port is port 8.
        """
        self.valve_num = valve_num
        # TODO: Move to port 8 instead of just setting value.
        self.current_port: int = 8
        self.com_num = com_num
        self.com_port_cmd = f"ASRL{self.com_num}::INSTR"

    def _set_current_port(self, new_port: int):
        """
        Sets the value of self.current_port to valve_port.
        """
        self.current_port: int = new_port

    def get_current_port(self) -> int:
        """
        Returns the current valve position or port number.
        """
        command = f"/{self.valve_num}?8"
        for _ in range(10):
            returned_bytes: bytes = self._write_read(command)
            # print(returned_bytes, end='  ')
            try:
                last_byte: str = returned_bytes.decode()[-1]
                returned_port: int = int(last_byte)
                if returned_port in range(1, self.num_ports+1):
                    self._set_current_port(returned_port)
                    return returned_port
            except ValueError:
                continue

        raise CommunicationError("Querying port failed.")

    @open_close_controller
    def _write_read(self, command, controller: Resource = None) -> bytes:
        controller.write(command)
        time.sleep(1)
        read = controller.read_bytes(4)
        return read

    def move(self, valve_port: int):
        """
        Moves a given valve to a selected port.

        Precondition: Valve port is between 1 and 8 inclusive
        """
        if valve_port not in range(1, 9):
            raise RangeError(f"Valve port number {valve_port} is not within 1-8")
        command = f"/{self.valve_num}o{valve_port}R"
        for _ in range(10):
            self._write(command)
            if self.get_current_port() == valve_port:
                print(
                    f"Valve {self.valve_num} has been moved to port {self.current_port}."
                )
                return True
            else:
                print(f"Move to port {valve_port} failed.")
        raise HardwareError(f"Moving valve {self.valve_num} to port {valve_port} failed.")

    @open_close_controller
    def _write(self, command, controller: Resource = None) -> None:
        controller.write("Fuck")  # Blank command to wake up the valve module.
        time.sleep(0.01)  # Some minimal time is needed between writes to work correctly. Determined empirically.
        controller.write(command)


def main():
    v1 = Valve(1, 9)
    current = v1.get_current_port()
    moved = v1.move(5)
    current = v1.current_port
    pass


if __name__ == "__main__":
    main()
