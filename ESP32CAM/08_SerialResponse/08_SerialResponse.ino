/*
*
*
Simple test of serial communication between RP Pico W (MicroPython) and ESP32CAM (Arduino).
Micropython code: 

from machine import UART, Pin
import time

#Pico UART (sends and receives)
uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

while True:
    mycommand = input("command: ")
    uart0.write(mycommand)
    print("wrote "+mycommand)
    time.sleep(1)
    
    if(uart0.any() > 0 ):
        time.sleep(1)
        print(uart0.readline())
*/

// Led pin 33 ist onboard red led, pin 4 is bright white led.
const int ledPin = 33;
byte buf[1000];

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  Serial.begin(115200);
  //Serial.setDebugOutput(true);
  Serial.println("ok");
  delay(100);

  // in bytearray schreiben noch nachsehen!!
  /*for (byte i = 0; i < 1000; i = i+1) {
    buf[i]=byte(random(0,255));
  }*/

  Serial.println("buffer");
  Serial.println(buf[1]);
}

void loop() {
  if (Serial.available() > 0) {
    String com = Serial.readString();
    com.trim();
    if (com == "hi")
      Serial.println("hello from ESP");

    else if (com == "bytes")
      Serial.write(buf, 100);

    else
      Serial.println("I dont understand");
  }

  /*String data = "hello";
  //Serial.write(data);
  Serial.println(data);
  delay(100);
  digitalWrite(ledPin, HIGH);
  delay(100);
  digitalWrite(ledPin, LOW);
  delay(2000);*/
}
