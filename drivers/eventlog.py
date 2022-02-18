from datetime import datetime, date
import os

def new_log(Rxn_Name):
    Date_Tag = str(date.today())
    New_Name = os.getcwd() + '\\log_file\\' + Rxn_Name + '_' + Date_Tag + '.log'
    with open(New_Name,'w') as New_Log:
        Time_Tag = str(datetime.now())
        First_Line = Time_Tag + '\t' + Rxn_Name + ' Start Run\n'
        New_Log.write(First_Line)
    return New_Name

def write_log(File,Event):
    #get starting time in ms
    
    #open log file as append
    with open(File,'a') as Log:
        Time_Tag = str(datetime.now())
        To_Write = Time_Tag + '\t' + Event + '\n'
        Log.write(To_Write)

