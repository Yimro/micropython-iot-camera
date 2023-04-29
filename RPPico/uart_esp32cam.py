from machine import UART, Pin
import time

# Pico UART (sends and receives)
# Important: set txbuf and rxbuf large enough to fit a vga image.
uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1), rxbuf=25000)

def readBytesUart():
    buf = bytes()
    while(uart0.any() > 0):
       buf += uart0.read(1)
    return buf

def writeToFile(filename, buffer):
    with open('file.jpg', 'wb') as f:
        f.write(buffer)
        print('written into file.jpg')
        f.close()

def getAndSaveImage(filename):
    uart0.write("start")
    time.sleep(2)
    rxData = readBytesUart()
    writeToFile(filename, rxData)
    
while True:    
    '''
    Add her sensor trigger code:
    '''
    getAndSaveImage("file.jpg")
    
    ''' remove manual break below and add time.sleep() instead:'''
    input("Press Enter to continue...")
