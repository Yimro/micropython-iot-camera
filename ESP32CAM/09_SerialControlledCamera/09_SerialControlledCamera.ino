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

/*
Extended with controlling of the OV2640 Camera that is attached to the ESP32CAM

*/


#include "esp_camera.h"

#define CAMERA_MODEL_AI_THINKER  // Has PSRAM

#include "camera_pins.h"

const int ledPin = 4;  // very bright flash LED
//int inByte = 0; // used for what?


void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);  // make sure the other device uses same Baud rate!
  //Serial.setDebugOutput(true);


  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  //  config.frame_size = FRAMESIZE_UXGA;
  config.frame_size = FRAMESIZE_VGA;
  config.pixel_format = PIXFORMAT_JPEG;  // for streaming
  config.jpeg_quality = 10;
  config.fb_count = 2;

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
}

void sendFrame() {
  camera_fb_t* fb = NULL;  // struct defined in esp_camera.h
  digitalWrite(ledPin, HIGH);
  delay(50);
  fb = esp_camera_fb_get(); // 
  delay(100);
  digitalWrite(ledPin, LOW);
  //delay(100);

  //Serial.write(*(fb->buf)); // dereference operator because we want content of pointer buf.
  /*
  Serial.print("length: ");
  Serial.print(fb->len);
  Serial.print(" bytes, width: ");
  Serial.print(fb->width);
  Serial.print(" pixels, height: ");
  Serial.print(fb->height);
  Serial.print(" pixels, format: ");
  Serial.println(fb->format);
  */
  //Serial.println(fb->timestamp->tv_sec); // problems getting timestamp, but not important.
  //Serial.println("begin transmission");
  //Serial.println("todo: writing to file..., fb size: ");
  Serial.write(fb->buf, fb->len);
  //Serial.println();
  //Serial.print("end transmission");
  digitalWrite(ledPin, HIGH);
  delay(50);
  digitalWrite(ledPin, LOW);
  // see: https://forum.arduino.cc/t/send-a-struct-to-serial-with-serial-write/400739/3
  if (!fb) {
    Serial.println("Camera capture failed");
    delay(1000);
    ESP.restart();
  }
  esp_camera_fb_return(fb);
}

void loop() {

  camera_fb_t* fb = NULL;  // struct defined in esp_camera.h

  if (Serial.available() > 0) {
    String command = Serial.readString();
    command.trim();

    if (command == "start")
      sendFrame();

    else Serial.println("I dont understand");
  }
  delay(500);
}
