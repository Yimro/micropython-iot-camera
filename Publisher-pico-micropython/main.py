from machine import Pin, I2C, RTC, UART
from umqtt.simple2 import MQTTClient 
import time, random, math, gc, json, network

#import mqttbasics as mq
import wificred as wf

# infrared sensor
pir = Pin(17, Pin.IN, Pin.PULL_DOWN)

# display
display = None
display_available = False

# mqtt settings
server="192.168.178.36"
topic = "proj/camera"

motion = False
image_count = 0
num = 0

# irq handler for PIR Sensor
def irq_handler(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin
    
# set interrupt on PIR sensor
pir.irq(handler=irq_handler, trigger=Pin.IRQ_RISING)

def get_image_UART(filename, baudrate):
    uart0 = UART(0, baudrate=baudrate, tx=Pin(0), rx=Pin(1), rxbuf=28000)
    time.sleep(1)
    uart0.write("start")
    time.sleep(1)
    
    rxData = bytes()
    n  = 0
    while(uart0.any() > 0):
       rxData += uart0.read(1)
       n +=1 
       if (n % 1024 == 0):
           print(str(math.floor((n/1024)) + " kbytes -"))
    print("get_image_UART: File size: {} bytes".format(str(n)))
    #writeToFile(filename, rxData)
    with open(filename, 'wb') as f:
        f.write(rxData)
        print('get_image_UART: Image written into {}'.format(filename))
        f.close()
    uart0.deinit()
    return n

def get_img(baudrate):
    uart0 = UART(0, baudrate=baudrate, tx=Pin(0), rx=Pin(1), rxbuf=28000)
    
    uart0.write("start")
    time.sleep(3)
    start_time = time.ticks_ms()
    file_size = uart0.any()
    
    #while(uart0.any() > 0):
    #   rx += uart0.read(1)
    if file_size > 0:
        rx = bytes()
        for n in range(file_size-1):
            rx += uart0.read(1)
            if n % 1024 == 0 and n > 0:
                print(n)
    
    end_time = time.ticks_ms()
    diff_time = end_time-start_time
    speed = file_size/diff_time*1000
    
    print("file size: {} bytes, transfer time: {} ms, speed: {} bytes/second".format(file_size, diff_time, math.floor(speed)))        
    
    
    '''with open(filename, 'wb') as f:
        f.write(rx)
        print('get_image_UART: Image ({} bytes) written into {}'.format(len, filename))
        f.close()
    '''
    uart0.deinit()
    return rx


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
        time.sleep_ms(150)
        begin = i*block_size
        end = begin + block_size
        if end >= flen:
            end = flen
        block = fobj[begin:end]
        #print("begin: {}, end: {}".format(begin, end))
        client.publish("proj/camera", block)
    f.close()


def main():
    
    global motion, filename, num, x, y, xdir, ydir, display_available
    num = 0
    
    #connect to wifi
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    nic.connect(wf.ssid, wf.password) 
    while not nic.isconnected():
        pass     
    print(nic.ifconfig())
    
    try:
        print("main: connecting to {} ...".format(server))
        client = MQTTClient("myclient", server, 1883)
        client.connect()
        print("main: connected")
    except:
        print("main: no connection to broker")
        
    while True:        
        filename = "file"+str(num)+".jpg"
        # motion detected:
        if motion:
            print("main: motion")
            
            print("main: Getting image from camera over UART/I2C")
            start_time = time.ticks_ms()
            
            # request image from ESP32CAM:
            size = get_img(filename, 2000000)
            # size = get_image_I2C(i2c, 85)

            end_time = time.ticks_ms()
            diff_time = end_time-start_time
            speed = size/diff_time*1000
            print("main: Finished transferring image over UART")
            print("main: UART transfer time: {} ms; bytes transferred: {}; transfer speed: {}"
                  .format(str(diff_time), str(size), str(speed)))
            
            # publish image via mqtt
            print("main: Start publishing to MQTT broker")
            
            pub_file(client, filename, 500)
            start_pub = time.ticks_ms()
            print("main: Done publishing {} to MQTT broker".format(filename))
            end_pub = time.ticks_ms()
            diff_pub = end_pub-start_pub
            
            #print("main: MQTT publish time: {} ms; bytes transferred: {}".format(str(diff_uart), str(size), str(speed)))
                
            #msg0 = "Sent " + filename + " at " + str(time.time()) + " seconds since the epoch"
                        
            time.sleep(5)
            num = (num+1)%10
            motion = False       
        
#if __name__ == '__main__':
#   main()

buf = get_img(2000000)

time.sleep(2)

with open("filen.jpg", 'wb') as f:
    f.write(buf)
    #print('get_image_UART: Image ({} bytes) written into {}'.format(len, filename))
    print("file written")
    f.close()
