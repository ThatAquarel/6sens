import time
import serial
import struct
import logging

import numpy as np

from sixsens.process.process import Process


PORT = "/dev/ttyACM0"
BAUD = 115200
# ON_TIME = 2


def matrix_process(stop_event, input_queue, output_queue):
    logging.info("Matrix process started")

    try:
        ser = serial.Serial(PORT, BAUD)
        logging.info("Matrix connected")
    except serial.SerialException:
        ser = None
        logging.warning("Failed to connect to serial matrix")

    while True:
        if stop_event.is_set():
            logging.info("Matrix process stopped")
            break

        if input_queue.empty():
            continue

        serialized_array = input_queue.get()
        serialized_array[-1] = 0
        serialized_array = serialized_array.astype(np.uint8)

        try:
            if ser:
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
            logging.error(f"Failed to write to {PORT}")


class Matrix(Process):
    def call(self, serialized_array):
        self.input_queue.put(serialized_array)

    def _get_process_function(self):
        return matrix_process
