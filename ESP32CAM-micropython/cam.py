import gc, os, math, camera, config, json, usocket as socket
from machine import reset, Pin, WDT
from time import sleep_ms, ticks_ms
from umqtt.simple2 import MQTTClient
#import camera_functions as cf
import network_functions as nf

#wdt = WDT(timeout=30000)  # enable it with a timeout of 2s

# constants
MQTT=1;
TCP=2;

#tcp settings:
hostname_tcp_server = '192.168.178.27'
#hostname_tcp_server = '192.168.1.104'
port_tcp_server = 5555

#mqtt settings
hostname_mqtt_broker ='test.mosquitto.org'
#hostname_mqtt_broker = '192.168.1.104'
sub_topic = 'iotgg-1-sub'
pub_topic = 'iotgg-1-pub'
pub_topic_img = 'iotgg-1-img-pub'
node_name = 'esp32cam-1'
client = None

#photo settings
flash = Pin(4, Pin.OUT)
current_image = None
img = None

# these settings can be changed remotely via MQTT
motion_detection = False #switch motion detection on/off
send_signal = False #send images to signal on/off
protocol = MQTT #choose protocol (MQTT/ TCP)
block_size = 2048 # set MQTT block size for binary data

       
def capture_image(save=False):
    flash.on()
    sleep_ms(80)
    ph = camera.capture()
    sleep_ms(80)
    flash.off()
    sleep_ms(200)
    print(f'capture ok, len: {len(ph)}')
    if save:
        with open('imagex.jpg', 'wb') as file:
            file.write(ph)
    return ph


def subscriber_callback(sub_topic, msg, retain, dup):
    global motion_detection
    global send_signal
    global protocol
    global block_size
    
    if msg == b'commands':
        client.publish(pub_topic,
        '''
        commands:      show list of MQTT commands \n
        photo:         take a photo and send it via signal to your phone \n
        resend:        resend last photo
        reset:         reboot ESP32-CAM \n
        motionon:      set motion detection ON \n
        motionoff:     set motion detection OFF \n
        status:        show current settings \n
        signalon:      set sending of signal message ON \n
        signaloff:     set sending of signal message OFF \n
        protocoltcp:   set transfer protocol TCP \n
        protocolmqtt:  set transfer protocol MQTT \n
        mqttbs512:     set block size 512 for MQTT image transfer \n
        mqttbs1024:    set block size 1024 for MQTT image transfer \n
        mqttbs2048:    set block size 2048 for MQTT image transfer \n
        ''', 1)
        print('sending commands')
    
                
    if msg == b'photo':
        print('photo')
        global img
        img = capture_image(True)
        #sleep_ms(2000)
        if protocol == TCP:
            try:
                send_buffer_tcp(hostname_tcp_server, port_tcp_server, img, send_signal)
                client.publish(pub_topic, 'response to photo: photo sent to signal')
            except Exception as e:
                print(f"error sending photo: {e}")
                client.publish(pub_topic, 'response to photo: error uploading')
        if protocol == MQTT:
            try:
                publish_buffer_mqtt(pub_topic_img, img)
                client.publish(pub_topic, 'response to photo: photo sent via mqtt')
            except Exception as e:
                print(f"error sending photo: {e}")
                client.publish(pub_topic, 'response to photo: error sending via mqtt')
                
    if msg == b'resend':
        global img
        if protocol == TCP:
            try:
                send_buffer_tcp(hostname_tcp_server, port_tcp_server, img, send_signal)
                client.publish(pub_topic, 'response to resend: photo resent to signal')
            except Exception as e:
                print(f"error sending photo: {e}")
                client.publish(pub_topic, 'response to resend: error uploading')
                raise
        if protocol == MQTT:
            try:
                publish_buffer_mqtt(pub_topic_img, img)
                client.publish(pub_topic, 'response to resend: photo resent via mqtt')
            except Exception as e:
                print(f"error sending photo: {e}")
                client.publish(pub_topic, 'response to resend: error sending via mqtt')
        
        
    if msg == b'reset':
        client.publish(pub_topic, 'response to reset: resetting...', 1)
        print('reset')
        reset()
        
    if msg == b'motionoff':
        client.publish(pub_topic, 'response to motionoff: motion detection OFF', 1)
        print('stop motion detection')
        motion_detection = False
        
    if msg == b'motionon':
        client.publish(pub_topic, 'response to motionon: motion detection ON', 1)
        print('start motion detection')
        motion_detection = True
            
    if msg == b'status':
        #answer = 'response to status: motion_detection: ' + str(motion_detection) + ', send_signal: '+ str(send_signal)
        if motion_detection:
            client.publish(pub_topic, 'status: motion detection ON', 1)
        else:
            client.publish(pub_topic, 'status: motion detection OFF', 1)
        if send_signal:    
            client.publish(pub_topic, 'status: signal ON', 1)
        else:
            client.publish(pub_topic, 'status: signal OFF', 1)
        if protocol == MQTT:
            client.publish(pub_topic, 'status: protocol MQTT', 1)
        if protocol == TCP:
            client.publish(pub_topic, 'status: protocol TCP', 1)
            
        client.publish(pub_topic, 'status: MQTT block size: '+str(block_size), 1)
            
        print('status')
        
    if msg == b'signalon':
        client.publish(pub_topic, 'response to signalon: signal ON', 1)
        print('signal ON')
        send_signal=True
        
    if msg == b'signaloff':
        client.publish(pub_topic, 'response to signaloff: signal OFF', 1)
        print('signal OFF')
        send_signal=False
        
    if msg == b'protocoltcp':
        client.publish(pub_topic, 'response to protocoltcp: protocol set to TCP', 1)
        print('protocol set to TCP')
        protocol = TCP
        
    if msg == b'protocolmqtt':
        client.publish(pub_topic, 'response to protocolmqtt: protocol set to MQTT', 1)
        print('protocol set to MQTT')
        protocol = MQTT
        
    if msg == b'mqttbs512':
        client.publish(pub_topic, 'response to bqttbs512: MQTT block size set to 512 bytes', 1)
        print('MQTT block size set to 512 bytes')
        block_size = 512
        
    if msg == b'mqttbs1024':
        client.publish(pub_topic, 'response to bqttbs1024: MQTT block size set to 512 bytes', 1)
        print('MQTT block size set to 1024 bytes')
        block_size = 1024
    
    if msg == b'mqttbs2048':
        client.publish(pub_topic, 'response to bqttbs1024: MQTT block size set to 2048 bytes', 1)
        print('MQTT block size set to 2048 bytes')
        block_size = 2048
        
def publish_buffer_mqtt(topic, buf, bs=None):
    global block_size
    if bs == None:
        bs = block_size
        
    try:         
        numBlocks = math.ceil((len(buf)/bs))
        msgInfo = {'type':'mqtt_camera_image', 'file_size':len(buf), 'block_size':bs,
                   'num_blocks':numBlocks, 'signal':send_signal }
        msgStr = json.dumps(msgInfo, separators=(',', ':'))
        print(f"pub_buf: {msgStr}")
        # publishing info msg 
        client.publish(topic, msgStr)
        # publishing buffer in chunks:
        for i in range (numBlocks):
            
            begin = i*bs
            end = begin+bs
            if end >= len(buf):
                end = len(buf)
            block = buf[begin:end]
            client.publish(topic, block)
            print(f"publish_buffer_mqtt: published block {i} of {numBlocks}")
        print("publish_buffer_mqtt: publishing finished")
    except Exception as err:
        print(f"publish_buffer_mqtt: Exc: {err=}, {type(err)=}")
        raise


def send_buffer_tcp(ip, port, buf, send_signal=False):
    '''
    this function sends a bytes object via a socket connection.
    ip: ip-address of the server
    port: port of the server
    buf: bytes object
    send_signal: sends a command if file should be uploaded to messenger
    '''
    gc.collect()
    sleep_ms(10)

    s = socket.socket()
    s.settimeout(10)
    s.connect((ip, port))
    print(f"send_buffer_tcp: connected to {ip} on port {port}")
    if send_signal == False:
        s.send(str.encode('local'))
    if send_signal == True:        
        s.send(str.encode('remot'))    
        
    print(f"send_buffer_tcp: sending image")
    
    totalsent = 0
    while totalsent < len(buf):
        sent = s.send(buf[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
        
    print("send_buffer_tcp: sending finished")
    s.close()       
    print("send_buffer_tcp: connection closed")

def loop():
    global motion_detection
    global send_signal
    global protocol
    global img
    client.publish(pub_topic, 'boot/reset: starting loop', 1)
    motion = False
    
    #measure time for taking scheduled photos, every 1 hour
    start_time = ticks_ms()
    #sleep_time=200
    
    #relative difference between last 2 image sizes, used as a simple motion detection
    diff = 0.08
    
    while True:
        wdt.feed()
        try:
            client.check_msg()
            sleep_ms(200)
            
            if motion_detection:      
                
                current_image = camera.capture()
                sleep_ms(200)
                new_image = camera.capture()
                
                abs_diff_curr_new = math.fabs(len(new_image) - len(current_image))
                rel_diff_curr_new = abs_diff_curr_new/len(current_image)
                
                
                if rel_diff_curr_new > diff: 
                    print(f"loop: MOTION DETECTED, difference: {rel_diff_curr_new}")
                    #print(rel_diff_curr_new)
                    client.publish(pub_topic, 'motion detected', 1)
                    motion=True
            
            #print(ticks_ms()-start_time)
            #print('.')
            if (ticks_ms()-start_time)>30000:
                start_time=ticks_ms()
                print("loop: SCHEDULED IMAGE")
                client.publish(pub_topic, 'scheduled photo', 1)
                motion=True
            
            if motion:
                img = capture_image()
                sleep_ms(100)
                if protocol == TCP:
                    try:
                        send_buffer_tcp(hostname_tcp_server, port_tcp_server, img, send_signal)
                    except OSError:
                        print("could not connect to file server")
                        client.publish(pub_topic, "could not connect to file server")
                if protocol == MQTT:
                    print("TODO publishing via MQTT")
                    publish_buffer_mqtt('iotgg-1-img-pub', img, 512)
                motion=False
                
            sleep_ms(200)
            #sleep_time=1000

        except KeyboardInterrupt:
            print("loop: Keyboard Interrupt")
            break

#connect to wlan
nf.wlan()

#create mqtt client
client=MQTTClient(node_name, 'test.mosquitto.org', 1883)

client.set_callback(subscriber_callback)
client.connect()
client.subscribe(sub_topic)
    
try:
    camera.deinit()
except:
    pass
assert camera.init()
#camera.init()
#sleep_ms(100)
loop()
    

