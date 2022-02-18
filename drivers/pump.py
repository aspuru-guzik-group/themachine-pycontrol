import sys
import clr
import os

#load DLL file
clr.AddReference(r"C:\Users\AAG Group\Dropbox (Aspuru-Guzik Lab)\TheMachine\Python Code\drivers\KEMPumpDLL")
#print(os.getcwd())
#DLL_Address = os.getcwd()+'\KEMPumpDLL'
#clr.AddReference(DLL_Address)

#load syringe pump control commands
from KEMPumpDLL import SyringePumpDef
pump = SyringePumpDef()
JKPump_List = [0,0,0,0,0,0,0]
JKPump_Active = JKPump_List
Err = ""

#initialize pump,out put online pump to JKPump_List as 1
def pump_initialize():
    #open communication
    if pump.OpenCommunications():
        #print("Communication Open")
        
        #discover module
        for i in range (0,7):
            if pump.DiscoverModule(i+1):
                #print("Pump Found No.",(i+1))
                JKPump_List[i] = 1
        #print(JKPump_List)        
        #initialize pump
        for j in range (0,7):
            if JKPump_List[j] == 1:
                if pump.Initialize((j+1),5):
                    JKPump_Active[j] =1
                    #print("Pump Initialized No.",(j+1))
                else:
                    JKPump_Active[j] =0
                    print("Pump Initialize Failed No.",(j+1))
        return True
        
    else:
        print("Communication failed")
        #return False

#set pump X to access port Y and move to volumn Z, Wait_Ready=False only for moving two pump simultaneously (BE CAREFUL!)
def pump_move(Pump_No,Pump_Port,Topspeed,Volume,Wait_Ready=True):
    if JKPump_Active[(Pump_No-1)] == 0:
        Err = "Pump not active"
        print(Err)
    else:
        pump.Port(Pump_No,Pump_Port,True)
        pump.Speed(Pump_No,Topspeed)
        Position = Volume*307200
        pump.MoveToPosition(Pump_No,Position,Wait_Ready)
        
def pump_port(Pump_No,Pump_Port):
    if JKPump_Active[(Pump_No-1)] == 0:
        Err = "Pump not active"
        print(Err)
    else:
        pump.Port(Pump_No,Pump_Port,True)

def pump_position(Pump_No):
    if JKPump_Active[(Pump_No-1)] == 0:
        Err = "Pump not active"
        print(Err)
    else:
        Position = pump.SyringePosition(Pump_No)
        return Position
        
#close control
def pump_close():
    pump.CloseCommPort()

#pump_initialize()
#print(JKPump_List)
#print(JKPump_Active)

'''
pump_move(1,5,20,2)
pump_move(1,5,20,0)

print(pump_position(1))
pump_move(1,1,20,1)
print(pump_position(1))
pump_move(1,1,20,0)
pump_close()
'''
