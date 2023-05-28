import logging
import numpy as np

from sixsens.process.process import Process


def obstruction_process(stop_event, input_queue, output_queue):
    logging.info("Obstruction process started")

    while True:
        if stop_event.is_set():
            logging.info("Obstruction process stopped")
            break

        if input_queue.empty():
            continue

        frame = input_queue.get()
        frame = np.array(frame)

        standard_deviations = np.std(frame.reshape((-1, 3)), axis=0)
        obstruction = (standard_deviations <= 35).all()

        output_queue.put(obj=obstruction)


class Obstruction(Process):
    def call(self, frame):
        self.input_queue.put(frame)

    def _get_process_function(self):
        return obstruction_process
