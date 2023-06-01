from machine import UART, Pin
import time

# Important: set txbuf and rxbuf large enough to fit a vga image.
# uart0 = UART(0, baudrate=921600, tx=Pin(0), rx=Pin(1), rxbuf=50000)

def getAndSaveImage(filename):
    uart0 = UART(0, baudrate=921600, tx=Pin(0), rx=Pin(1), rxbuf=28000)
    #time.sleep(1)
    uart0.write("start")
    time.sleep(2)
    
    #rxData = readBytesUart()
    rxData = bytes()
    n  = 0
    while(uart0.any() > 0):
       rxData += uart0.read(1)
       n +=1 
       if (n % 1024 == 0):
           print(str(n/1024) + " kbytes -")
    print("uartcam: file size: {} bytes".format(str(n)))
    #writeToFile(filename, rxData)
    with open(filename, 'wb') as f:
        f.write(rxData)
        print('uartcam: Image written into {}'.format(filename))
        f.close()
    uart0.deinit()
    
def main():
    #time.sleep(20)
    num = 0
    while True:    
        filename = "file"+str(num)+".jpg"
        print('getting image, please wait'.format(filename))
        getAndSaveImage(filename)        
        print('finished')
        num = (num + 1)%3
        
        #input("Press Enter to continue...")
        time.sleep(1)
        
if __name__ == '__main__':
    main()
