import logging
import numpy as np

from sixsens.process.process import Process


def obstruction_process(input_queue, output_queue):
    logging.info("Obstruction process started")

    while True:
        if input_queue.empty():
            continue

        frame = input_queue.get()
        frame = np.array(frame)
        frame = frame.diagonal()
        frame = np.append(frame, np.fliplr(frame).diagonal())

        standard_deviations = np.std(frame, axis=0)
        obstruction = (standard_deviations <= 35).all()

        output_queue.put(obj=obstruction)


class Obstruction(Process):
    def call(self, frame):
        self.input_queue.put(frame)

    def _get_process_function(self):
        return obstruction_process
