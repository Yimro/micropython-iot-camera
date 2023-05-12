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
    with open(filename, 'wb') as f:
        f.write(buffer)
        print('Image written into {}'.format(filename))
        f.close()

def getAndSaveImage(filename):
    uart0.write("start")
    time.sleep(2)
    
    #rxData = readBytesUart()
    rxData = bytes()
    while(uart0.any() > 0):
       rxData += uart0.read(1)
    #writeToFile(filename, rxData)
    with open(filename, 'wb') as f:
        f.write(rxData)
        print('Image written into {}'.format(filename))
        f.close()
    
def main():
    #time.sleep(20)
    num = 0
    while True:    
        '''
        Add here sensor trigger code:
        '''
        pir = Pin(17, Pin.IN, Pin.PULL_DOWN)
        led = Pin(16, Pin.OUT, value=0)
        
        if (pir.value()):
            led.value(1)
            filename = "file"+str(num)+".jpg"
            print('getting image, please wait'.format(filename))
            getAndSaveImage(filename)
            
            num = (num + 1)%3
        
        ''' remove manual break below and add time.sleep() instead:'''
        #input("Press Enter to continue...")
        time.sleep(1)
        
if __name__ == '__main__':
   main()
