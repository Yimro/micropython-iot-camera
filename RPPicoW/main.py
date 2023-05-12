from machine import Pin, SPI, RTC
from ssd1306 import SSD1306_SPI
#from dht20 import DHT20
from umqtt.simple2 import MQTTClient 
import time, random, math, gc, json

import uartcam as ua
import mqttbasics as mq
import wificred as wf

# infrared sensor
pir = Pin(17, Pin.IN, Pin.PULL_DOWN)
        
# spi interface, display
spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
display = SSD1306_SPI(128, 64, spi, Pin(20), Pin(21), Pin(22))

# mqtt settings
server="192.168.178.36"
topic = "proj/camera"

# wifi
mq.connect_wifi(wf.ssid, wf.password)

# Connect to MQTT broker:
try:
    client = mq.connect(server)
except OSError as e:
    mq.reconnect()

motion = False
image_count = 0
num = 0

# animation values
x = random.randint(5,123)
y = random.randint(5,59)
xdir = random.randrange(-1,1,2)
ydir = random.randrange(-1,1,2)

# irq handler for PIR Sensor
def irq_handler(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin
    
# set interrupt on PIR sensor
pir.irq(handler=irq_handler, trigger=Pin.IRQ_RISING)

# publishing files over mqtt
def pub_file(client, file_name, block_size=2000):
    f = open(file_name, "rb")
    fobj = f.read()
    flen = len(fobj)
    num_blocks = math.ceil(flen/block_size)
    
    msg_info = {"file_size":flen, "block_size":block_size, "num_blocks":num_blocks, "file_name":file_name}
    msg_str = json.dumps(msg_info)
    print("pub_file: publishing {}.".format(msg_str))
    client.publish("proj/camera", msg_str)
    
    print("pub_file: publishing file")
    for i in range(num_blocks):
        gc.collect()
        time.sleep_ms(100)
        begin = i*block_size
        end = begin + block_size
        if end >= flen:
            end = flen
        block = fobj[begin:end]
        #print("begin: {}, end: {}".format(begin, end))
        client.publish("proj/camera", block)
    f.close()


def main():
    global motion, filename, num, x, y, xdir, ydir
    num = 0
    while True:
        filename = "file"+str(num)+".jpg"
        # motion detected:
        if motion:
            print("motion")
            display.fill(0)
            display.text(" ALARM!", 30, 9, 1)
            display.text("saving {}".format(filename), 0, 20, 1)
            display.show()
            
            ua.getAndSaveImage(filename)
            
            
            display.text(" done ", 30, 30, 1)
            display.show()
            print("main: publishing")
            pub_file(client, filename, 1000)
            print("main: done publishing")
            display.text("Published: {}".format(filename), 3, 55, 1)
            
            #msg0 = "Sent " + filename + " at " + str(time.time()) + " seconds since the epoch"
                        
            time.sleep(5)
            num +=1
            
            motion = False
        
        # show animation while no motion detected:
        display.fill(0)
        display.rect(0,0,128,64,1)
        display.text("{} image(s)".format(num), 3,3,1)
        display.ellipse(x,y,5,5, 1)
        display.show()
        time.sleep_ms(20)        
        x += xdir
        y += ydir
        if (x == 123):
            xdir = -1
        if (x == 5):
            xdir = 1
        if (y == 59):
            ydir = -1
        if (y == 5):
            ydir = 1

if __name__ == '__main__':
   main()