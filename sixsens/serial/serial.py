import time
import serial
import struct
import logging
import serial.tools.list_ports
from tqdm import tqdm


class Commands:
    NUL = 0x00
    SYN = 0xAB
    ACK = 0x4B
    NAK = 0x5A
    ERR = 0x3C

    MOVEMENT = 0x9F


class Packet:
    PADDING_BYTES = 4
    FRAME_START_FLAG = 0x7E
    FRAME_END_FLAG = 0x7D

    cmd = 0
    buffer = 0

    def __init__(self, buffer=b"", cmd=Commands.NUL):
        self.buffer = buffer
        self.cmd = cmd

    def __str__(self):
        return f"cmd={self.cmd} buffer={self.buffer.hex()}"


class Serial:
    def __init__(self, ser):
        self.ser = ser

    def _crc16(self, data=b""):
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

    def send_packet(self, packet: Packet):
        packet_bytes = struct.pack(
            f"<{'x'*Packet.PADDING_BYTES}BBH{len(packet.buffer)}sHB{'x'*packet.PADDING_BYTES}",
            packet.FRAME_START_FLAG,  # U8 start of packet flag
            packet.cmd & 0xFF,  # U8 command
            len(packet.buffer) & 0xFFFF,  # U16 length of payload
            packet.buffer,  # U8 payload[len]
            self._crc16(packet.buffer),  # U16 crc
            packet.FRAME_END_FLAG,  # U8 end of packet flag
        )

        self.ser.write(packet_bytes)

    def recv_packet():
        self.ser.read_until(struct.pack("<B", Packet.FRAME_START_FLAG))

        command, length = struct.unpack("<cH", self.ser.read(3))
        payload, crc = struct.unpack(f"<{length}sH", self.ser.read(length + 2))

        if self._crc16(payload) != crc:
            command = command.NAK
            logging.warning(f"CRC mismatch {crc16(payload)} != {crc}")
        if self.ser.read(1) != struct.pack("<B", Packet.FRAME_END_FLAG):
            command = commands.ERR
            logging.warning("Frame end flag error")
        if command == commands.NUL:
            logging.warning("NULL command error")
            command = commands.ERR

        logging.debug(f"{command=} {length=} {payload=} {crc=}")
        return Packet(buffer=payload, command=ord(command))

    def acknowledge():
        resp = recv_packet()
        if resp.cmd != commands.ACK:
            logging.error(f"cmd={res.cmd} buffer={res.buffer.hex()}")
            raise Exception("SYN failed")
