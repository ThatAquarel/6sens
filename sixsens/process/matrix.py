import time
import serial
import struct
import logging

import numpy as np

from sixsens.process.process import Process


PORT = "/dev/ttyACM0"
BAUD = 115200
# ON_TIME = 2


def matrix_process(input_queue, output_queue):
    logging.info("Matrix process started")

    try:
        ser = serial.Serial(PORT, BAUD)
    except serial.SerialException:
        ser = None
        logging.warning("Failed to connect to serial matrix")

    while True:
        if input_queue.empty():
            continue

        serialized_array = input_queue.get()
        try:
            if ser:
                # while (time.time())
                ser.write(
                    struct.pack(
                        f"<{'x' * 4}B{len(serialized_array)}sB{'x' * 4}",
                        0x7E,
                        serialized_array.tobytes(),
                        0x7D,
                    ),
                )
                ser.flush()
        except serial.SerialException:
            logging.error(f"Failed to write to {self.port}")
        logging.debug(f"Write {serialized_array.reshape((8, 6)).T}")


class Matrix(Process):
    def call(self, serialized_array):
        self.input_queue.put(serialized_array)

    def _get_process_function(self):
        return matrix_process