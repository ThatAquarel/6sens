void init(unsigned long baud) {
  Serial.begin(baud);
}

packet_t recv_packet(packet_t *packet) {
    while (Serial.available() < 1)
        ;

    uint8_t flag = 0;
    while (flag != pyserial::comm::FRAME_START_FLAG)
        Serial.readBytes(&flag, 1);
    Serial.readBytes((uint8_t *)&packet->cmd, 1);

    uint16_t requested_len = 0;
    Serial.readBytes((uint8_t *)&requested_len, 2);
    if (requested_len > packet->len)
        requested_len = packet->len;

    Serial.readBytes(packet->buf, requested_len);
    uint16_t crc;
    Serial.readBytes((uint8_t *)&crc, 2);
    Serial.readBytes(&flag, 1);

    if (pyserial::comm::crc16(packet->buf, requested_len) != crc)
        packet->cmd = pyserial::NAK;
    if (flag != pyserial::comm::FRAME_END_FLAG)
        packet->cmd = pyserial::ERR;

    return packet;
}

void send_packet(packet_t *packet)
{
    uint16_t crc = pyserial::comm::crc16(packet->buf, packet->len);

    Serial.write(0x00000000);
    Serial.write(pyserial::comm::FRAME_START_FLAG);
    Serial.write(packet->cmd);
    Serial.write((uint8_t *)&(packet->len), 2);
    if (packet->buf != nullptr)
        Serial.write(packet->buf, packet->len);
    Serial.write((uint8_t *)&crc, 2);
    Serial.write(pyserial::comm::FRAME_END_FLAG);
    Serial.write(0x00000000);
}

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

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
