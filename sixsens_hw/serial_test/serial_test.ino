#include <Adafruit_NeoPixel.h>

int POWER = 11;
int PIN  = 12;
#define NUMPIXELS 1
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

uint8_t state;

void setup() {
  Serial.begin(115200);

  pixels.begin();
  pinMode(POWER,OUTPUT);
  digitalWrite(POWER, HIGH);
}

void loop() {
  while (!Serial.available())
    delay(1);
  
  Serial.readBytes(&state, 1);

  if (state){
    pixels.setPixelColor(0, pixels.Color(255, 0, 0));
    pixels.show();
  } else {
    pixels.setPixelColor(0, pixels.Color(0, 0 ,0));
    pixels.show();
  }
}
