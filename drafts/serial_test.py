import time
import serial
import struct

import numpy as np


def main(ser):
    while True:
        ser.write(b"\xff")
        ser.flush()
        time.sleep(0.5)
        ser.write(b"\x00")
        ser.flush()
        time.sleep(0.5)


if __name__ == "__main__":
    PORT = "/dev/ttyACM0"
    BAUD = 115200

    with serial.Serial(PORT, BAUD) as ser:
        main(ser)
