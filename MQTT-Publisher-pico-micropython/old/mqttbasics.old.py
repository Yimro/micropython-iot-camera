import time #for measuring response times
#import binascii #for converting binary files and back
from dht20 import DHT20 #for reading sensor values
from umqtt.simple2 import MQTTClient 
from machine import I2C, Pin, Timer
import json
import gc
import math

# Create led object: 
led = Pin(16, Pin.OUT, value=0)

# Create Timer object:
tim = Timer()

# Define callback function timer:
def toggle_timer(t):
    led.toggle()

# Connect to wireless network:
def connect_wifi(ssid, password):
    import network
    # enable station interface and connect to WiFi access point
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    nic.connect(ssid, password) # should be changed to GGSEC:

    while not nic.isconnected():
        pass     
    print(nic.ifconfig())

# Creates a dht20 object with a I2C connection, returns temperature, humidity:
def read_dht20():
    i2c = I2C(0)
    dht20 = DHT20(i2c)
    values = {
        "tmp": dht20.dht20_temperature(),
        "hum": dht20.dht20_humidity()
        }
    return values

# MQTT connect:
def connect(server):
    # print('Connected to MQTT Broker "%s"' % (server))
    client = MQTTClient("myclient", server, 1883)
    client.connect()
    return client

# MQTT reconnect: 
def reconnect(server):
    # print('Failed to connect to MQTT broker, Reconnecting...' % (server))
    time.sleep(5)
    client.reconnect()

# MQTT subscribe to topic
def sub(client, topic, blocking_method=False):
    client.set_callback(callback_led)
    client.subscribe(topic)
    # print("Subscribed to {}".format(topic))

# MQTT publish via client
def pub(client, topic, message, qos):
    client.publish(topic, message, False, qos, False)

# MQTT publish, qos=1, callback for status, print response time broker:
def pub_status(client, topic, message):
    # print("publishing message: {}".format(message))
    start = time.ticks_ms()
    client.set_callback_status(callback_status)
    client.publish(topic, message, qos=1)
    client.wait_msg()
    delta = time.ticks_diff(time.ticks_ms(), start)
    print("respond time broker: %s ms" % delta)  

# Example callback function on received MQTT message:
def callback_led(topic, msg, retain, dup):
    print((topic, msg))
    if msg == b"on":
        led.value(1)
    elif msg == b"off":
        led.value(0)
    elif msg == b"toggle":
        led.toggle()
    elif msg == b"blinkon":
        tim.init(mode=Timer.PERIODIC, freq=10, callback=toggle_timer)
    elif msg == b"blinkoff":
        tim.deinit()

# callback function for broker response on publish
def callback_status(pid, status):
    print("Status:", end = " ") 
    if status== 1:
        print("successfully delivered")
    elif status == 0:
        print("timeout")
    elif status == 2:
        print("unknown PID")

'''
def pub_binary_file(client, filename, topic):
    f = open(filename, 'rb')
    fObj = f.read()
    msg = binascii.b2a_base64(fObj)
    # print('sending message %s on topic %s' % (msg, topic))
    pub_status(client, topic, msg)
    f.close()
'''
'''    
def pub_binary(client, topic, buffer, block_size=1024):
    
    MQTT publish a large buffer in seperate blocks.
    import: math, time, gc, micropython
    default block size 1024 bytes

    import math, time, gc
    import micropython as mp
    
    num_blocks = math.ceil(len(buffer)/block_size)
    print("Lenght of buffer in bytes: {}, block size: {}, number of blocks: {}".format(len(buffer), block_size, num_blocks))
    print("Check: buffer size  = {}".format(str(num_blocks*block_size)))
    for i in range(num_blocks):
        try:
            gc.collect() 
            time.sleep_ms(500)
            begin = i*block_size; end = begin+block_size;
            
            if i == 0:
                print("first block: {} bytes.".format(block_size))
                client.publish(topic, b'b')
            
            print(">>> Time: {}, Sending block nr. {}. Begin: {}, end: {}, size: {}".format(time.time(), str(i), begin, end, (end-begin)))
            client.publish(topic, buffer[begin:end])
            print("sent.")
            
            if i == num_blocks-1:
                if end > len(buffer):
                    end = len(buffer)
                
                client.publish(topic, b'e')
                
            # gc.collect() # ist das hier noch mal nötig? 
            # mp.mem_info() # für debugging
            # time.sleep_ms(1000) # testen ob das nötig ist
            
        except Exception as err:
            print("failed, error: {}".format(err))
            break
'''

def pub_file(client, file_name, block_size=2000):
    f = open(file_name, "rb")
    fobj = f.read()
    flen = len(fobj)
    num_blocks = math.ceil(flen/block_size)
    
    msg_info = {"file_size":flen, "num_blocks":num_blocks, "file_name":file_name}
    msg_str = json.dumps(msg_info)
    print("publishing {}.".format(msg_str))
    client.publish("proj/camera", msg_str)
    
    #print("msg_info dict: {}".format(msg_info))
    
    print("publishing file")
    for i in range(num_blocks):
        gc.collect()
        time.sleep_ms(70)
        begin = i*block_size
        end = begin + block_size
        if end >= flen:
            end = flen
        msg_binary = fobj[begin:end]
        #print("begin: {}, end: {}".format(begin, end))
        client.publish("proj/camera", msg_binary)
    f.close()
    
    
    
def main():
    server="192.168.178.36"
    topic = "proj/camera"
    ssid = 'GGSEC'
    password = 'uZQna3UipqvSYJhgkEcI'
    
    # Connect to wifi:
    connect_wifi(ssid, password)

    # Connect to MQTT broker:
    try:
        client = connect(server)
    except OSError as e:
        reconnect()

    # Subscribe to a topic:
    # sub(client, "proj/led", False)
    
    while True:
        # checking for messages in subscribed topics:
        # client.check_msg()
        
        # sending sensor data, no callback:
        env = read_dht20()
        env_dump = json.dumps(env)
        print('sending message %s on topic %s' % (env_dump, "proj/sensor"))
        pub(client, "proj/env", env_dump, 0)
        
        #gc.collect()
        #time.sleep_ms(1000)
        pub_file(client, "testfile2.jpg", 100) # block size 100 bytes 
        
        
        time.sleep(1)
        
        
        
        
        input("press Enter")
        

if __name__ == '__main__':
   main()
