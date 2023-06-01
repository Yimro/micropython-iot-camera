from machine import Pin, I2C, RTC, UART
from umqtt.simple2 import MQTTClient 
import time, random, math, gc, json, network


i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)

'''
def get_image_size_I2C(i2c, addr):
    #returns bytearray with length of image in bytes
    b = i2c.readfrom(addr, 4)
    #convert bytearray into int:
    return int.from_bytes(b, True)
    #another way to convert bytearray into int:
'''    



def main():
    #n = get_image_size_I2C(i2c, 85)
    #print(n)
    
    # reading data:
    i2c.writeto(85, "get")
    time.sleep(1)
    i2c.writeto(85, "x")
    b = i2c.readfrom(85, 4)
    b_int = int.from_bytes(b[0:4], True)
    print(b_int)
    time.sleep(1)
    i2c.writeto(85, "y")
    b = i2c.readfrom(85, 4)
    print(b)
    #important when handling binary data!
    #convert bytearray to int, so we know length of buffer
    b_int = int.from_bytes(b[0:4], True)
    print(b_int) # length of buffer
    #######time.sleep(1)    
    #write some string to i2c bus:
    

    
    
if __name__ == '__main__':
   main()