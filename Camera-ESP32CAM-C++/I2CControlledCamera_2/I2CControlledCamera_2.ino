/*
Controlling the OV2640 Camera of the ESP32CAM (Model AI-Thinker) over I2C
*/

#include "esp_camera.h"
#define CAMERA_MODEL_AI_THINKER  // Has PSRAM
#include "camera_pins.h"
#include "Wire.h"

#define I2C_DEV_ADDR 0x55
#define I2C_SDA 14
#define I2C_SCL 15

uint32_t i = 0;
const int ledPin = 4;    // very bright flash LED
camera_fb_t* fb = NULL;  // struct defined in esp_camera.h
unsigned char bytes[4];
uint len = 0;

void createByteArray(uint num) {
  Serial.print("createByteArray : ");
  Serial.print(num);
  Serial.println(" bytes");
  unsigned char mask = 0xff;
  bytes[0] = (num >> 24) & mask;
  Serial.println(bytes[0]);
  bytes[1] = (num >> 16) & mask;
  Serial.println(bytes[1]);
  bytes[2] = (num >> 8) & mask;
  Serial.println(bytes[2]);
  bytes[3] = num & mask;
  Serial.println(bytes[3]);
}

void getFrame() {
  esp_camera_fb_return(fb);
  digitalWrite(ledPin, HIGH);
  delay(50);
  fb = esp_camera_fb_get();  // saving frame to buffer
  delay(50);
  digitalWrite(ledPin, LOW);
  
  if (!fb) {
    Serial.println("Camera capture failed");
    delay(1000);
    ESP.restart();
  }
}

void onRequest() {
  
  
  Wire.write(bytes, sizeof(bytes));


 /* if (fb != NULL) {
    //Wire.write(fb->buf, 31);
    Serial.print("onRequest: fb len: ");
    Serial.println(fb -> len);
    createByteArray(fb-> len);
    Wire.write(bytes, 4);
   
    //Wire.write(fb->buf, 31);
  }
  else {
    Wire.write("nothing to send");
    
  }
  */
}

void onReceive(int len) {
  char com[len];
  int i = 0;
  Serial.printf("Received %d bytes: ", len);

  while (Wire.available()) {
    char c = Wire.read();
    Serial.print(c);
    com[i] = c;
    i++;
  }

  com[i] = '\0';
  Serial.println();

  String str2 = String(com);
  Serial.println(str2);
  if (str2.equals("get")) {
    
    Serial.print("onReceive: getting frame, len: ");
    getFrame();
    Serial.println(fb -> len);   
    createByteArray(fb-> len);
    
    //Wire.write(bytes, 4);
    
  } 
  if (str2.equals("x")){
    Wire.write(bytes, 4);

  }

  if (str2.equals("y")){
    Wire.write(fb->buf, 32);

  }
  else {
    Serial.println("nothing");
    
  }

  //sendFrame();
}

void config_init_camera() {
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

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Wire.onReceive(onReceive);
  Wire.onRequest(onRequest);
  Wire.begin(I2C_DEV_ADDR, I2C_SDA, I2C_SCL, 100000);
  Wire.flush();
  config_init_camera();



  /*#if CONFIG_IDF_TARGET_ESP32
  char message[64];
  snprintf(message, 64, "%u Packets.", i++);
  Wire.slaveWrite((uint8_t *)message, strlen(message));
  #endif*/
}

void loop() {
    



}
