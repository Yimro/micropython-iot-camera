from machine import Pin, SPI, RTC
from ssd1306 import SSD1306_SPI
#from dht20 import DHT20
import binascii
from umqtt.simple2 import MQTTClient 
import time, random

import uartcam as ua
import mqttbasics as mq

# infrared sensor
pir = Pin(17, Pin.IN, Pin.PULL_DOWN)
        
# spi interface, display
spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
display = SSD1306_SPI(128, 64, spi, Pin(20), Pin(21), Pin(22))

# mqtt broker settings and other variables
server="192.168.178.36"
motion = False
image_count = 0
num = 0
topic = "proj/camera"
filename = ""

# wifi
mq.connect_wifi('GGSEC', 'uZQna3UipqvSYJhgkEcI')

# Connect to MQTT broker:
try:
    client = mq.connect(server)
except OSError as e:
    mq.reconnect()

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


while True:
    # motion detected:
    if motion:
        print("motion")
        display.fill(0)
        display.text(" ALARM!", 30, 9, 1)
        display.text("Taking img. {}".format(num), 3, 24, 1)
        display.show()
        filename = "file"+str(num)+".jpg"
        #ua.getAndSaveImage(filename)
        display.text("Pub.MQTT img. m{}".format(num), 3, 39, 1)
        '''with open(filename, 'rb') as f:
            obj = f.read()
            msg = binascii.b2a_base64(obj)
            mq.pub(client, topic, msg[:500], 0)
            f.close()
        '''
        msg = "Sent " + filename + " at " + str(time.time()) + " seconds since the epoch"
        mq.pub(client, topic, msg, 0)
        display.show()
        time.sleep(5)
        num +=1
        time.sleep(1)# call MQTT pub function
        motion = False
    
    # no motion detected:
    display.fill(0)
    display.rect(0,0,128,64,1)
    display.text("{} image(s)".format(num), 3,3,1)
    display.ellipse(x,y,5,5, 1)
    display.show()
    time.sleep_ms(10)        
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