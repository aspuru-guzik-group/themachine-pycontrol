
import struct
import time
import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu



master = None

def ReadFloat(*args,reverse=True):
    for n,m in args:
        n,m = '%04x'%n,'%04x'%m
    if reverse:
        v = n + m
    else:
        v = m + n
    y_bytes = bytes.fromhex(v)
    y = struct.unpack('!f',y_bytes)[0]
    y = round(y,6)
    return y

def PortInit(Port="com68",BaudRate=9600):
    # 设定串口为从站
    global master
    master = modbus_rtu.RtuMaster(serial.Serial(port=Port,baudrate=BaudRate, bytesize=8, parity='N', stopbits=1))
    master.set_timeout(1.0)
    master.set_verbose(True)

def ReadVal():
    # 读保持寄存器
    res = master.execute(1, cst.READ_HOLDING_REGISTERS, 3030, 2)  # 这里可以修改需要读取的功能码
    val=ReadFloat(res[:2])
    #print(val,end='')
    #print("uA")
    return val

if __name__ == "__main__":
    try:
        PortInit(Port="com68")
    except :
        print ("初始化端口异常")
    else:
        print ("端口初始化成功")

    r_val=0;
    while True:

        """
        r_val=ReadVal()
        print(r_val)
        time.sleep(0.5)

        """
        try:
            r_val=ReadVal()
            
        except:
            print ("SUI-903数据读取异常")
            break
        else:
            print(r_val,end='')
            print('uA')
            pass
        time.sleep(0.5)
        

        











