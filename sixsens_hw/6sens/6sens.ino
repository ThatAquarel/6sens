#include <Adafruit_NeoPixel.h>

const int ADDR[3] = {D7, D8, D9};
const int ROW[6] = {D1, D2, D3, D4, D5, D6};
const int ENABLE = D0;

const int LED_POWER = 11;
const int LED_PIN  = 12;

Adafruit_NeoPixel pixels(1, LED_PIN, NEO_GRB + NEO_KHZ800);

#define N_COLS 8
#define N_ROWS 6

uint8_t buf[N_COLS * N_ROWS];

#define FRAME_START_FLAG 0x7E
#define FRAME_END_FLAG 0x7D

void setup() {
  Serial.begin(115200);

  pixels.begin();
  pinMode(LED_POWER, OUTPUT);
  digitalWrite(LED_POWER, HIGH);

  pixels.setPixelColor(0, pixels.Color(0, 80, 0));
  pixels.show();

  for (int i = 0; i < 3; i++) {
    pinMode(ADDR[i], OUTPUT);
    digitalWrite(ADDR[i], HIGH);
  }
  for (int i = 0; i < N_ROWS; i++) {
    pinMode(ROW[i], OUTPUT);
    digitalWrite(ROW[i], HIGH);
  }
  
  pinMode(ENABLE, OUTPUT);
}

void loop() {
  while (!Serial.available()) delay(1);

  uint8_t flag = 0;
  while (flag != FRAME_START_FLAG)
    Serial.readBytes(&flag, 1);
  Serial.readBytes(buf, N_COLS * N_ROWS);
  Serial.readBytes(&flag, 1);
  if (flag != FRAME_END_FLAG) {
    pixels.setPixelColor(0, pixels.Color(255, 0, 0));
    pixels.show();
  }

  digitalWrite(ENABLE, HIGH);
  update_matrix();
  digitalWrite(ENABLE, LOW);
}

void update_matrix() {
  for (int col = 0; col < N_COLS; col++) {
    int motor_count = 0;
    for (int row = 0; row < N_ROWS; row++) {
      int index = col * N_ROWS + row;
      motor_count += buf[index];
    }

    if (motor_count < 1) continue;

    for (int i = 0; i < 3; i++){
      digitalWrite(ADDR[i], (1 << i) & (~col));
    }

    for (int row = 0; row < N_ROWS; row++) {
      int index = col * N_ROWS + row;

      if (buf[index] == 0) continue;

      digitalWrite(ROW[row], LOW);
      delay(50);
      digitalWrite(ROW[row], HIGH);
    }
  }
}
