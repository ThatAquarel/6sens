enum command : uint8_t
{
  NUL = 0x00,
  SYN = 0xAB,
  ACK = 0x4B,
  NAK = 0x5A,
  ERR = 0x3C,

  _MOVEMENT = 0x9F
};

#define FRAME_START_FLAG 0x7E
#define FRAME_END_FLAG 0x7D

#define COLS 8
#define ROWS 6

size_t len;
command cmd;
uint8_t buf[COLS * ROWS];

uint16_t crc16(uint8_t *data_p, size_t length)
{
  if (length == 0 || data_p == nullptr)
    return 0xFFFF;

  uint8_t x;
  uint16_t crc = 0xFFFF;

  while (length--)
  {
    x = crc >> 8 ^ *data_p++;
    x ^= x >> 4;
    crc = (crc << 8) ^ ((uint16_t)(x << 12)) ^ ((uint16_t)(x << 5)) ^ ((uint16_t)x);
  }
  return crc;
}

void recv_packet() {
  uint8_t flag = 0;
  while (flag != FRAME_START_FLAG)
    Serial.readBytes(&flag, 1);
  Serial.readBytes((uint8_t *)&cmd, 1);

  uint16_t requested_len = 0;
  Serial.readBytes((uint8_t *)&requested_len, 2);
  if (requested_len > len)
    requested_len = len;

  Serial.readBytes(buf, requested_len);
  uint16_t crc;
  Serial.readBytes((uint8_t *)&crc, 2);
  Serial.readBytes(&flag, 1);

  if (crc16(buf, requested_len) != crc)
    cmd = NAK;
  if (flag != FRAME_END_FLAG)
    cmd = ERR;
}

void send_packet() {
  uint16_t crc = crc16(buf, len);

  Serial.write(0x00000000);
  Serial.write(FRAME_START_FLAG);
  Serial.write(cmd);
  Serial.write((uint8_t *)&len, 2);
  if (buf != nullptr)
    Serial.write(buf, len);
  Serial.write((uint8_t *)&crc, 2);
  Serial.write(FRAME_END_FLAG);
  Serial.write(0x00000000);
}

void ack() {
  Serial.write(0x00000000);
  Serial.write(FRAME_START_FLAG);
  Serial.write(command::ACK);
  Serial.write(0x0000);
  Serial.write(0xFFFF);
  Serial.write(FRAME_END_FLAG);
  Serial.write(0x00000000);
}

void setup() {
  Serial.begin(115200);
  ack();

  pinMode(25, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    recv_packet();
    ack();
  } else {
    poll();
  }
}

void poll() {
  if (buf[0] > 0 ){
    digitalWrite(25, HIGH);
  } else {
    digitalWrite(25, LOW);
  }
}
