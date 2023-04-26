from machine import UART, Pin
import time

#Pico UART (sends and receives)
uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

def readBytes():
    buf = bytes()
    while(uart0.any() > 0):
       buf += uart0.read(1)
    return buf

while True:
    mycommand = input("command: ")
    uart0.write(mycommand)
    print("wrote "+mycommand)
    time.sleep(10)
    
    if(uart0.any() > 0 ):
        #time.sleep(1)
        #print(uart0.readline())
        print(readBytes())

    

#buffer1 = bytearray(b'1234',  'utf-8')
#buffer0 = bytearray(10)

"""
uart1.write(buffer1)
time.sleep(1)
uart0.readinto(buffer0, 10)
print(buffer1)
print(buffer0)
"""