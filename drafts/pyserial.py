import time
import serial
import struct
import logging
import serial.tools.list_ports
from tqdm import tqdm

import numpy as np


class commands:
    NUL = 0x00
    SYN = 0xAB
    ACK = 0x4B
    NAK = 0x5A
    ERR = 0x3C

    MOVEMENT = 0x9F


class packet_t:
    PADDING_BYTES = 4
    FRAME_START_FLAG = 0x7E
    FRAME_END_FLAG = 0x7D

    cmd = 0
    buffer = 0

    def __init__(self, buffer=b"", cmd=commands.NUL):
        self.buffer = buffer
        self.cmd = cmd

    def __str__(self):
        return f"cmd={self.cmd} buffer={self.buffer.hex()}"


def crc16(data=b""):
    m = 0xFFFF

    if data == b"":
        return m

    x = 0
    crc = m

    for i in range(len(data)):
        x = (crc >> 8) ^ data[i]
        x &= 0xFF
        x ^= x >> 4
        x &= 0xFF
        crc = (crc << 8) ^ (m & (x << 12)) ^ (m & (x << 5)) ^ (m & x)
        crc &= m

        i -= 1

    return crc


def send_packet(packet: packet_t):
    packet_bytes = struct.pack(
        f"<{'x'*packet_t.PADDING_BYTES}BBH{len(packet.buffer)}sHB{'x'*packet_t.PADDING_BYTES}",
        packet_t.FRAME_START_FLAG,  # U8 start of packet flag
        packet.cmd & 0xFF,  # U8 command
        len(packet.buffer) & 0xFFFF,  # U16 length of payload
        packet.buffer,  # U8 payload[len]
        crc16(packet.buffer),  # U16 crc
        packet_t.FRAME_END_FLAG,  # U8 end of packet flag
    )

    ser.write(packet_bytes)


def recv_packet():
    ser.read_until(struct.pack("<B", packet_t.FRAME_START_FLAG))

    command, length = struct.unpack("<cH", ser.read(3))
    payload, crc = struct.unpack(f"<{length}sH", ser.read(length + 2))

    if crc16(payload) != crc:
        command = command.NAK
        logging.warning(f"CRC mismatch {crc16(payload)} != {crc}")
    if ser.read(1) != struct.pack("<B", packet_t.FRAME_END_FLAG):
        command = commands.ERR
        logging.warning("Frame end flag error")
    if command == commands.NUL:
        logging.warning("NULL command error")
        command = commands.ERR

    logging.debug(f"{command=} {length=} {payload=} {crc=}")
    return packet_t(payload, ord(command))


def acknowledge():
    resp = recv_packet()
    if resp.cmd != commands.ACK:
        logging.error(f"cmd={res.cmd} buffer={res.buffer.hex()}")
        raise Exception("SYN failed")


def main(ser):
    logging.info("Init serial communications")
    acknowledge()

    a = np.zeros(48, dtype=np.uint8)
    packet = packet_t(buffer=a.tobytes(), cmd=commands.MOVEMENT)
    send_packet(packet)

    acknowledge()


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)

    ports = serial.tools.list_ports.comports()
    for i, port in enumerate(ports):
        print(f"{i} - {port.device}")

    COM = len(ports) - 1
    BAUD = 115200

    com = ""
    while com == "":
        com_in = input(f"Input COM port (default: {COM}): ")

        if com_in == "":
            com = ports[COM].device
            break
        try:
            j = int(com_in)
            com = ports[j].device
        except (ValueError, IndexError()):
            continue
    logging.info(f"Using {com}")

    baud = 0
    while baud < 9600:
        baud_in = input(f"Input baud rate (default: {BAUD}): ")
        if baud_in == "":
            baud = BAUD
            break
        try:
            baud = int(baud_in)
        except ValueError:
            continue
    logging.info(f"Using {baud}")

    with serial.Serial(com, baud) as ser:
        main(ser, buffers)
