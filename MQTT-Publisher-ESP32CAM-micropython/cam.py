from machine import Pin, RTC, reset, SDCard
from umqtt.simple2 import MQTTClient
from time import sleep, sleep_ms, localtime
import camera, math, network, config, json, os, gc, wifi

AP = wifi.AP
PWD = wifi.PWD
flash = Pin(4, Pin.OUT)
client = None
current_image = None
rtc = RTC()

def error_flash():
    while True:
        try:
            flash.on()
            sleep_ms(1)
            flash.off()
            sleep_ms(1000)
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break

def wlan():    
    # wlan settings
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(AP, PWD)

    while not wlan.isconnected():
        pass
    print(f"wlan connected: {wlan.isconnected()}")
    print(f"ifconfig: {wlan.ifconfig()}")

# camera settings + init
def cam_init():
    config.configure(camera, config.ai_thinker)
    try:
        camera.deinit()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        error_flash()
        raise

    for i in range(5):
        cam_ready = camera.init()
        if cam_ready:
            print(f"Camera ready:{cam_ready}")
            break
        else: sleep(2)
    else:
        print(f"Timeout init camera")
        

def mqtt_client_init():
    global client
    client = MQTTClient("ESP32-CAM1", "192.168.178.36", 1883)
    try:
        client.connect()
    except Exception:
        print("mqtt_client_init: not able to connect")  
        raise
    
def sd_card_init():
    sdc=SDCard()
    try:
        os.mkdir('/sd')
    except:
        print("dir exists")
    os.mount(sdc, '/sd')
    os.chdir('/sd')
    print(f"SD card mounted")

def get_datetime_string():
    t = localtime()
    year = str(t[0])
    month = "{:02d}".format(t[1])
    day = "{:02d}".format(t[2])
    hour = "{:02d}".format(t[3])
    minute = "{:02d}".format(t[4])
    second = "{:02d}".format(t[5])
    datetime = year + month + day +"-" + hour + minute + second
    return datetime
            
def pub_buf(img, topic, fileName, bs=2000):
    
    li = len(img)
    try:         
        numBlocks = math.ceil((len(img)/bs))
        msgInfo = {'type':'mqtt_camera_image', 'file_name':fileName, 'file_size':li, 'block_size':bs, 'num_blocks':numBlocks }
        msgStr = json.dumps(msgInfo, separators=(',', ':'))
        print(f"pub_buf: {msgStr}")
        # publishing info msg 
        client.publish(topic, msgStr)
        # publishing buffer in chunks:
        for i in range (numBlocks):
            
            begin = i*bs
            end = begin+bs
            if end >= len(img):
                end = len(img)
            block = img[begin:end]
            client.publish(topic, block)
            print(f"pub_buf: published block {i}")
        print("pub_buf: done")
    except Exception as err:
        print(f"pub_buf: Exc: {err=}, {type(err)=}")
        
def detect_motion_simple():
    motion = False
    try:
        len(current_image)
    except:
        current_image = camera.capture()
        print("detect_motion: capturing first image")
        print(f"length current image: {len(current_image)}")
    
        while motion == False:
            try:
                print("\n")
                sleep_ms(1000)
                new_image = camera.capture()
                abs_diff_curr_new = math.fabs(len(new_image) - len(current_image))
                rel_diff_curr_new = abs_diff_curr_new/len(current_image)
                print("detect_motion: capturing image")
                print(f"length new image: {len(new_image)}")
                print("absolute difference:", abs_diff_curr_new)
                print("relative difference:", rel_diff_curr_new)
                
                if rel_diff_curr_new > 0.05:
                    print("detected motion!")
                    motion = True
                    break
                
                current_image=new_image
            
            except KeyboardInterrupt:
                print("Keyboard Interrupt")
                break
        
    return motion
    

def loop():
    num = 0
    current_size = -1
    limit = 0.05
    
    
    while True:
        try:
            
            #if motion detected:
            if  detect_motion_simple():
                flash.on()
                sleep_ms(10)
                img = camera.capture()
                sleep_ms(10)
                flash.off()
                
                #Save image to file
                fileName = f"IMG{get_datetime_string()}.jpg"
                print(f"saving image {fileName}")
                
                fs = open(fileName, "wb")
                sleep_ms(200)
                fs.write(img)
                fs.close()
                sleep_ms(200)
                #Publish MQTT text message
                client.publish('proj/motion', f"motion detected: file name: {fileName}")
                print("sent MQTT text message.")
                
                #Publish MQTT binary message(S)
                pub_buf(img, 'proj/images', fileName, 1000)
                num = 0        
            
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break

wlan()
mqtt_client_init()
sd_card_init()
cam_init()
loop()