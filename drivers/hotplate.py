from visa import ResourceManager
import time


COM_LIST = [4, 6]
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

    def __init__(self, hotplate_num: int): # Change to hotplate_num
        """
        Initialize a new hotplate with heating and stirring switches set to off.
        """
        # connect to desired COM port device and open remote control
        #TODO: read com_num value from COM_LIST (see valve.py)
        com_port = f'ASRL{com_num}::INSTR'
        self.hotplate = rm.open_resource(com_port)
        self.heat_switch: bool = False
        self.stir_switch: bool = False
        self.temp: int = 20
        self.rpm: int = 0

    def heat(self, heat_switch_status: bool = False, new_temp: int = 20):
        """
        Sets the temperature the hotplate should heat up to if heat_switch is True (or "on").
        If it is off, the hotplate stops heating.

        Precondition: Max value is 340 degrees C, but safe limit should be >25deg lower than flash
        point of material

        """

        # TODO: Add assertions for temp.

        self.heat_switch = heat_switch_status # replace
        if self.heat_switch:
            # set temp
            self.temp = new_temp # replace
            self.hotplate.write(f'OUT_SP_1 {new_temp}')
            time.sleep(1)
            # start heating
            self.hotplate.write('START_1')
            time.sleep(1)
            print(f"Hotplate is now heating to {new_temp}.")
        else:
            # stop heating
            self.hotplate.write('STOP_1')
            time.sleep(1)
            print("Hotplate is no longer heating.")

    #TODO: Create funcs that _set (and _get?) heat and stir statuses, as well as temp and rpm. Replace as appropriate.

    def stir(self, stir_switch_status=False,new_rpm=0):
        #TODO: Correct type hinting.
        """
        Sets the rpm the hotplate should stir at if stir_switch is true ("on").
        If it is off, the hotplate stops stirring.

        Precondition: max rpm is 1700
        """
        new_rpm: int
        stir_switch_status: bool

        #TODO: Add assertions for rpm.

        self.stir_switch = stir_switch_status # replace
        if self.stir_switch:
            # set rpm
            self.rpm = new_rpm # replace
            self.hotplate.write(f'OUT_SP_4 {new_rpm}')
            time.sleep(1)
            # start stirring
            self.hotplate.write('START_4')
            time.sleep(1)
            print(f"The hotplate is now stirring at {new_rpm} rpm")
        else:
            # stop stirring
            self.hotplate.write('STOP_4')
            time.sleep(1)
            print("The hotplate has stopped stirring.")

    def weigh(self, tare_switch):
        """
        Placeholder function. Not currently in use!

        Weighs an amount. If tare_switch is True, the weight recorded will be set to 0.
        """
        if tare_switch:
            # reset taring value
            self.hotplate.write('STOP_90')
            self.hotplate.write('START_90')
            time.sleep(10)
            self.hotplate.write('STATUS_90')
            print(self.hotplate.read())
            print("The hotplate has been tared.")
            return 0
        else:
            # check stability
            for i in range(0, 6):
                self.hotplate.write('STATUS_90')
                hotplate_reading = self.hotplate.read()
                hotplate_reading = hotplate_reading.strip()
                if hotplate_reading == '1041 90':
                    #    print('y')
                    break
                else:
                    #   print('n')
                    time.sleep(10)
                # out put error here?
            # measure weight
            self.hotplate.write('IN_PV_90')
            time.sleep(1)
            weight = self.hotplate.read()
            print(f"A weight of {weight} has been obtained.")
            return weight


#close control, do NOT shut down hotplate!!!
    def hotplate_close(self):
        self.hotplate.close()

