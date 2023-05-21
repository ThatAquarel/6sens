#include <Adafruit_NeoPixel.h>

int POWER = 11;
int PIN  = 12;
#define NUMPIXELS 1
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define COLS 8
#define ROWS 6

uint8_t buf[COLS * ROWS];
#define FRAME_START_FLAG 0x7E
#define FRAME_END_FLAG 0x7D

void setup() {
  Serial.begin(115200);

  pixels.begin();
  pinMode(POWER,OUTPUT);
  digitalWrite(POWER, HIGH);
}

void loop() {
  while (!Serial.available())
    delay(1);

  uint8_t flag = 0;
  while (flag != FRAME_START_FLAG)
    Serial.readBytes(&flag, 1);
  Serial.readBytes(buf, COLS * ROWS);
  Serial.readBytes(&flag, 1);
  if (flag != FRAME_END_FLAG) {
    pixels.setPixelColor(0, pixels.Color(255, 255, 255));
    pixels.show();
  }

  poll();
}

void poll() {
  pixels.setPixelColor(0, pixels.Color(buf[0], 0 ,0));
  pixels.show();
}
