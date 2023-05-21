import time
import serial
import struct

import numpy as np


def main(ser):
    a = np.zeros(48, dtype=np.uint8)

    while True:
        a += 1
        ser.write(
            struct.pack(
                f"<{'x' * 4}B{len(a)}sB{'x' * 4}", 0x7E, a.tobytes(), 0x7D
            ),
        )
        ser.flush()

        time.sleep(0.025)


if __name__ == "__main__":
    # sudo chmod a+rw /dev/ttyACM0
    PORT = "/dev/ttyACM0"
    BAUD = 115200

    with serial.Serial(PORT, BAUD) as ser:
        main(ser)
