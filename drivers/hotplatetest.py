from visa import ResourceManager as rm
import time


#communicate to devices and list them
# rm = visa.ResourceManager()

#output COM ports connected
res = rm.list_resources()
print(res)



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

    def __init__(self, com_no, heat_switch=False, stir_switch=False, temp=20, rpm=0, hotplate) -> None:
        """
        Initialize a new hotplate with heating and stirring switches set to off.
        """
        com_no: int
        heat_switch: bool
        stir_switch: bool
        temp: float
        rpm: int

        # connect to desired COM port device and open remote control
        COM_Port = f'ASRL{com_no}::INSTR'
        self.hotplate = rm.open_resource(COM_Port)
        self.hotplate = hotplate
        self.heat_switch = heat_switch
        self.stir_switch = stir_switch
        self.temp = temp
        self.rpm = rpm

    def heat(self, heat_switch_status=False, new_temp=20) -> None:
        """
        Sets the temperature the hotplate should heat up to if heat_switch is True (or "on").
        If it is off, the hotplate stops heating.

        Precondition: Max value is 340 degrees C, but safe limit should be >25deg lower than flash
        point of material

        """
        heat_switch_status: bool
        new_temp: float
        self.heat_switch = heat_switch_status
        if self.heat_switch:
            # set temp
            self.temp = new_temp
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

    def read_temp(self):
        """
        Returns temperature of hotplate

        """
        print(f"The hotplate is currently {self.temp} degrees Celsius.")
        return self.temp

    def stir(self, stir_switch_status=False,new_rpm=0) -> None:
        """
        Sets the rpm the hotplate should stir at if stir_switch is true ("on").
        If it is off, the hotplate stops stirring.

        Precondition: max rpm is 1700
        """
        new_rpm: int
        stir_switch_status: bool

        self.stir_switch = stir_switch_status
        if self.stir_switch:
            # set rpm
            self.rpm = new_rpm
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
        Weighs an amount. If tare_switch is True, the weight recorded iwll be set to 0.
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

#hotplate.write('START_1')
#hotplate.write('START_90')
#time.sleep(10)
#hotplate.write('STATUS_90')
#hotplate.write('IN_PV_90')

#print(hotplate.read())
#hotplate_temp(False,25)
#hotplate_stir(False,0)
#print(hotplate_weigh(True))
