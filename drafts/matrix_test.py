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


def main(ser):
    for i in range(47):
        a = np.zeros(48, dtype=np.uint8)
        a[i] = 255

        write(a)
        print(i)
        time.sleep(0.025)


if __name__ == "__main__":
    # sudo chmod a+rw /dev/ttyACM0
    PORT = "/dev/ttyACM0"
    BAUD = 115200

    with serial.Serial(PORT, BAUD) as ser:
        main(ser)
