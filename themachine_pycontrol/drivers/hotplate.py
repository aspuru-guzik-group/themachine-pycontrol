from pyvisa import ResourceManager
from pyvisa.resources import Resource
import time
from themachine_pycontrol.drivers.errors import CommunicationError, RangeError

rm = ResourceManager()


class Hotplate:
    """
    A hotplate with functions that can heat to a given temperature, stir at a given speed,
    and weigh materials

    === Public Attributes ==
    heat_switch: Indicates if heating function is on or off
    stir_switch: Indicates if stirring function is on or off
    temp: temperature of hotplate
    rpm: rpm of hotplate


    === Representation Invariants ===
    - temp must be <340 degrees C
    - rpm must be <1700 rpm
    """

    def __init__(self, com_num: int):
        """
        Initialize a new hotplate with heating and stirring switches set to off.
        """
        self.com_num = com_num
        com_port: str = f"ASRL{self.com_num}::INSTR"
        try:
            self.controller: Resource = rm.open_resource(com_port)
        except MissingManifestResourceException:
            raise CommunicationError(f"Hotplate at COM {com_num} not found.")
        self._set_heat_switch(False)
        self._set_stir_switch(False)
        self._set_temp(20)
        self._set_rpm(0)

    def heat(self, heat_switch_state: bool, new_temp: int = 20):
        """
        Sets the temperature the hotplate should heat up to if heat_switch is True (or "on").
        If it is off, the hotplate stops heating.

        Precondition: Max value is 340 degrees C, but safe limit should be >25deg lower than flash
        point of material

        """
        self._set_heat_switch(heat_switch_state)
        if self.heat_switch:
            self._set_temp(new_temp)
            self.controller.write(f"OUT_SP_1 {new_temp}")
            time.sleep(1)
            # start heating
            self.controller.write("START_1")
            time.sleep(1)
            print(f"Hotplate is now heating to {new_temp}.")
        else:
            # stop heating
            self.controller.write("STOP_1")
            time.sleep(1)
            print("Hotplate is no longer heating.")

    def _set_temp(self, new_temp: int = 20):
        """
        Sets self.temp to new_temp
        """
        # TODO: This does nothing!
        if new_temp not in range(20, 341):
            raise RangeError(f"New temperature of {new_temp} is not within the range of 20-341 degrees Celsius.")

    def _get_temp(self) -> int:
        """
        Returns current temp status
        """
        return self.temp

    def _set_heat_switch(self, new_heat_switch: bool = False):
        """
        Sets self.heat_switch to new_heat_switch_state
        """
        self.heat_switch = new_heat_switch

    def _get_heat_switch(self) -> bool:
        """
        Returns current heat switch status
        """
        return self.heat_switch

    def _set_stir_switch(self, new_stir_switch: bool):
        """
        Sets self.stir_switch to new_heat_switch_state
        """
        self.stir_switch = new_stir_switch

    def _get_stir_switch(self) -> bool:
        """
        Returns current stir switch status
        """
        return self.stir_switch

    def _set_rpm(self, new_rpm: int = 0):
        """
        Sets self.rpm to be new_rpm, which must be <1700 rpm
        """
        if new_rpm not in range(0, 1701):
            raise RangeError(f"Desired stir speed of {new_rpm} is not under 1700 rpm")

    def _get_rpm(self) -> int:
        """
        Returns current rpm
        """
        return self.rpm

    def stir(self, stir_switch_state: bool = False, new_rpm: int = 0):
        """
        Sets the rpm the hotplate should stir at if stir_switch is true ("on").
        If it is off, the hotplate stops stirring.

        Precondition: max rpm is 1700
        """

        self._set_stir_switch(stir_switch_state)
        if self.stir_switch:
            self._set_rpm(new_rpm)
            self.controller.write(f"OUT_SP_4 {new_rpm}")
            time.sleep(1)
            # start stirring
            self.controller.write("START_4")
            time.sleep(1)
            print(f"The hotplate is now stirring at {new_rpm} rpm")
        else:
            # stop stirring
            self.controller.write("STOP_4")
            time.sleep(1)
            print("The hotplate has stopped stirring.")

    # def weigh(self, tare_switch):
    #     """
    #     Placeholder function. Not currently in use!
    # 
    #     Weighs an amount. If tare_switch is True, the weight recorded will be set to 0.
    #     """
    #     if tare_switch:
    #         # reset taring value
    #         self.controller.write("STOP_90")
    #         self.controller.write("START_90")
    #         time.sleep(10)
    #         self.controller.write("STATUS_90")
    #         print(self.controller.read())
    #         print("The hotplate has been tared.")
    #         return 0
    #     else:
    #         # check stability
    #         for i in range(0, 6):
    #             self.controller.write("STATUS_90")
    #             hotplate_reading = self.controller.read()
    #             hotplate_reading = hotplate_reading.strip()
    #             if hotplate_reading == "1041 90":
    #                 #    print('y')
    #                 break
    #             else:
    #                 #   print('n')
    #                 time.sleep(10)
    #             # out put error here?
    #         # measure weight
    #         self.controller.write("IN_PV_90")
    #         time.sleep(1)
    #         weight = self.controller.read()
    #         print(f"A weight of {weight} has been obtained.")
    #         return weight

    def close(self):
        # close control, do NOT shut down hotplate!!!
        self.controller.close()


def main():
    hp = Hotplate(4)
    hp.heat(True, 25)
    hp.stir(True, 100)


if __name__ == "__main__":
    main()
