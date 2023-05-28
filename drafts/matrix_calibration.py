import time
import serial
import struct

import numpy as np


def write(arr):
    ser.write(
        struct.pack(
            f"<{'x' * 4}B{len(arr)}sB{'x' * 4}", 0x7E, arr.tobytes(), 0x7D
        ),
    )
    ser.flush()


ROWS = 6
COLS = 8


def main(ser):
    matrix = np.zeros((COLS, ROWS), dtype=np.uint8)
    matrix[4, 4] = 255

    while True:
        a = matrix.flatten()
        write(a)
        time.sleep(0.025)


if __name__ == "__main__":
    # sudo chmod a+rw /dev/ttyACM0
    PORT = "/dev/ttyACM0"
    BAUD = 115200

    with serial.Serial(PORT, BAUD) as ser:
        main(ser)
