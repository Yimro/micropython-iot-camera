import gc, os, math, camera, config
from machine import reset, Pin
from time import sleep_ms, ticks_ms
from umqtt.simple2 import MQTTClient
#import camera_functions as cf
import file_upload_client as upload
import network_functions as nf


# def sd_card_init():
#     sdc=SDCard()
#     try:
#         os.mkdir('/sd')
#     except:
#         print("sd_card_init: dir exists")
#     os.mount(sdc, '/sd')
#     os.chdir('/sd')
#     print("sd_card_init: SD card mounted")
    

client = None
motion_detection = False
send_signal = False
current_image = None
flash = Pin(4, Pin.OUT)
sub_topic = 'iotgg-1-sub'
pub_topic = 'iotgg-1-pub'
name = 'esp32cam-1'

# camera settings + init
# def cam_init():
#     config.configure(camera, config.ai_thinker)
#     try:
#         camera.deinit()
#     except Exception as err:
#         print(f"cam_init: Unexpected {err=}, {type(err)=}")
#         raise
# 
#     for i in range(5):
#         cam_ready = camera.init()
#         if cam_ready:
#             print(f"cam_init: Camera ready:{cam_ready}")
#             break
#         else: sleep_ms(2000)
#     #else:
#     #    print(f"cam_init: Timeout init camera")
#     assert cam_ready, 'Camera init failure'
        
def capture_and_save_image():
    flash.on()
    sleep_ms(80)
    img = camera.capture()
    sleep_ms(80)
    flash.off()
    print('capture ok')
    
    # write to file:
    fs = open('image.jpg', "wb")
    sleep_ms(200)
    fs.write(img)
    sleep_ms(200)
    fs.close()
    sleep_ms(200)
    gc.collect()


def subscriber_cb(sub_topic, msg, retain, dup):
    global motion_detection
    global send_signal
    
    if msg == b'photo':
        print('photo')
        capture_and_save_image()
        sleep_ms(100)
        try:
            upload.send_file('192.168.178.49', 5555, 'image.jpg', True)
        except Exception as e:
            raise
        client.publish(pub_topic, 'response to photo: photo sent to signal')
        
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
        print('status')
        
    if msg == b'signalon':
        client.publish(pub_topic, 'response to signalon: signal ON', 1)
        print('signal ON')
        send_signal=True
        
    if msg == b'signaloff':
        client.publish(pub_topic, 'response to signaloff: signal OFF', 1)
        print('signal OFF')
        send_signal=False
        
    if msg == b'commands':
        client.publish(pub_topic, 'photo reset motionon motionoff status signalon signaloff', 1)
        print('send commands')
        send_signal=False

def loop():
    global motion_detection
    global send_signal
    client.publish(pub_topic, 'boot/reset: starting loop', 1)
    motion = False
    start_time = ticks_ms()
    sleep_time=200
    diff = 0.08
    
    
    while True:
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
            if (ticks_ms()-start_time)>3600000:
                start_time=ticks_ms()
                print("loop: SCHEDULED IMAGE")
                client.publish(pub_topic, 'scheduled photo', 1)
                motion=True
            
            if motion:
                capture_and_save_image()
                sleep_ms(100)
                upload.send_file('192.168.178.49', 5555, 'image.jpg', send_signal)
                client.publish(pub_topic, 'transferred image to RPZero', 1)
                motion=False
                
            sleep_ms(sleep_time)
            sleep_time=1000

        except KeyboardInterrupt:
            print("loop: Keyboard Interrupt")
            break

try:
    nf.wlan()
    
    client=MQTTClient(name, 'test.mosquitto.org', 1883)
    try:
        client.set_callback(subscriber_cb)
        client.connect()
        client.subscribe(sub_topic)
        
    except Exception:
        raise
    try:
        camera.deinit()
    except:
        pass
    assert camera.init()
    
    sleep_ms(100)
    loop()
except Exception as e:
    
    #print(e, type(e))
    reset()
