import visa
import time
com_list = [10,7,11,10,5,9,8]
rm = visa.ResourceManager()


class Valve:
    """
    Description

    === Public Attributes ===
    valve_module: Describes the module in which a given valve is located
    valve_no: Identifies the valve number of a given valve in a module

    == Representation Invariants ===
    - valve_module must be a number between 0-5 inclusive
    - valve_no must be a number between 1-4 inclusive
    """

    def __init__(self, valve_module, valve_no, valve, current_port) -> None:
        """
        Initialize a new valve.

        """
        valve_module: int
        valve_no: int
        valve: rm
        current_port: int

        com_no = com_list[valve_module]
        com_port = f'ASRL{com_no}::INSTR'
        self.valve = rm.open_resource(com_port)
        self.valve = valve
        self.valve_module = valve_module
        self.valve_no = valve_no
        self.current_port = current_port

    def move(self, valve_port):
        """
        Moves a given valve to a selected port.

        Precondition: Valve port is between 1 and 8 inclusive

        """
        valve_port: int

        command = f'/{self.valve_no}o{valve_port}R'
        valve_port = self.current_port
        self.valve.write(command)
        time.sleep(2)
        self.valve.write(command)
        time.sleep(2)
        self.valve.close()
        print(f"Valve {self.valve_no} in module {self.valve_module }has been moved to port {self.current_port}.")

    def locate(self):
        """
        Returns the current port of a given valve.
        """
        return self.current_port



