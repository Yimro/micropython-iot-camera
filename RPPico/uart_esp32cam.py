from machine import UART, Pin
import time

# Pico UART (sends and receives)
# Important: set txbuf and rxbuf large enough to fit a vga image (30000 bytes).
uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1), rxbuf=25000)

def readBytesUart():
    buf = bytes()
    while(uart0.any() > 0):
       buf += uart0.read(1)
    return buf

def writeFile(filename, buffer):
    with open('file.jpg', 'wb') as f:
        f.write(buffer)
        print('written into file.jpg')
        f.close()

def saveImage(filename):
    uart0.write("start")
    time.sleep(2)
    rxData = readBytesUart()
    writeFile(filename, rxData)
    
while True:    
    saveImage("file.jpg")    
    input("Press Enter to continue...")
