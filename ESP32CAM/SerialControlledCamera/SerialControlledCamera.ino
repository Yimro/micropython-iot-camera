/*
Controlling the OV2640 Camera of the ESP32CAM (Model AI-Thinker) over UART
*/

#include "esp_camera.h"
#define CAMERA_MODEL_AI_THINKER  // Has PSRAM
#include "camera_pins.h"

const int ledPin = 4;  // very bright flash LED

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(2000000);  // 115200 make sure the other device uses same Baud rate!
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
  fb = esp_camera_fb_get(); // saving frame to buffer
  delay(50);
  digitalWrite(ledPin, LOW);
  Serial.write(fb->buf, fb->len); // writing image buffer to uart
  
  if (!fb) {
    Serial.println("Camera capture failed");
    delay(1000);
    ESP.restart();
  }
  esp_camera_fb_return(fb); 
}

void loop() {

  if (Serial.available() > 0) {
    String command = Serial.readString();
    command.trim();
    /*
    * Here will be added more commands for different resolutions, etc.
    */
    if (command == "start")
      sendFrame();

    else Serial.println("I dont understand");
  }
  delay(100);
}
