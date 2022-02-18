import nidaqmx

#initialize nidaqmx as controller of solenoids
Task_DO_Chan = nidaqmx.Task()
DO_Chan = 'Dev1/port0/line0:7'
Task_DO_Chan.do_channels.add_do_chan(DO_Chan)

#read current status of solenoids, return list of status
def solen_list_read ():
    Solen_Status = Task_DO_Chan.read()
    Solen_Status_Process = Solen_Status
    Solen_Status_List = [0,0,0,0,0,0,0,0]
    for i in range (0,8):
        Solen_Status_List[i] = Solen_Status_Process % 2
        Solen_Status_Process = Solen_Status_Process // 2
    return Solen_Status_List

#write status of solenoids, start from 0, operation 1 = high
def solen_operation(Solen_No=0, Operation=0,Solen_Status_List=[0,0,0,0,0,0,0,0]):
    Solen_Status_List=solen_list_read()
    Solen_Status_List[Solen_No] = Operation
    Solen_Status = 0
    for i in range (0,8):
         Solen_Status += Solen_Status_List[i]*pow(2,i)
    Task_DO_Chan.start()
    Task_DO_Chan.write(Solen_Status)
    Task_DO_Chan.stop()

#close control of nidaqmx and solenoids
def solen_close():
    Task_DO_Chan.start()
    Task_DO_Chan.write(0)
    Task_DO_Chan.stop()
    Task_DO_Chan.close()
    

#solen_operation(1,0)
