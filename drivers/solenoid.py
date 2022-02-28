import nidaqmx

Task_DO_Chan = nidaqmx.Task()
DO_Chan = 'Dev1/port0/line0:7'
Task_DO_Chan.do_channels.add_do_chan(DO_Chan)


#better to make nidaq class THEN solenoid class? one isntance of nidaq will have array of solenoid and solenoid list

class Solenoid:
    """

    """
    def __init__(self, solen_num: int, solen_status: int):
        """
        solen_status is an integer equal to 0 or 1.
        """
        self.solen_num = solen_num
        self.solen_status = solen_status

    def _set_solen_status(self, new_solen_status: int):
        """
        Sets self.solen_status to be new_solen_status which is an integer equal to 0 or 1
        """
        self.solen_status = new_solen_status

    def read_solen_status(self):
        """
        Returns binary status for a given solenoid where 1 = active and 0 = inactive.
        """
        decimal_status = Task_DO_Chan.read()
        binary_status = f'{decimal_status:08b}'  # 08 means fill 0 at begin to make it at least 8 digits
        return binary_status


    #write status of solenoids, start from 0, operation 1 = high
    def solen_operation(self, solen_num = 0, operation = 0,solen_status_list=[0,0,0,0,0,0,0,0]):
        solen_status = self.read_solen_status



        solen_status_list = solen_list_read()
        #overwrites w output of solen_list_read() basically in case of error
        solen_status_list[Solen_No] = Operation
        #reset status of a certain solenoid
        #for given solen_no (channel) this operatiion fn changes it to operation = true or false
        solen_status = 0
        for i in range (0,8):
             solen_status += solen_status_list[i]*pow(2,i)
        Task_DO_Chan.start() #tell the nidaq we r gonna do smth, initiate action?
        Task_DO_Chan.write(solen_status) #write the decimal u got to the device
        Task_DO_Chan.stop()
        #now go from binary to decimal
        #nidaq only takes dec integer as input

    #close control of nidaqmx and solenoids
    def solen_close(self):
        #for safety? close device
        #write 0 = set all solenoid to close
        #close whole device
        Task_DO_Chan.start()
        Task_DO_Chan.write(0)
        Task_DO_Chan.stop()
        Task_DO_Chan.close() #after closing need to redo the initialization


#solen_operation(1,0)


#solenoid = a switch/ a relay better, w current, lifts small thing up = allows current to flow