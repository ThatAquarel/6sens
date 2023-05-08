import numpy as np

from sixsens.process.process import Process


def obstruction_process(child_connection, input_queue, output_queue):
    while True:
        if input_queue.empty():
            continue

        frame = input_queue.get()
        frame = np.array(frame)
        frame = frame.reshape((-1, frame.shape[-1]))

        standard_deviations = np.std(frame, axis=0)
        obstruction = (standard_deviations <= 45).all()

        output_queue.put(obstruction)


class Obstruction(Process):
    def call(self, frame):
        self.input_queue.put(frame)

    def _get_process_function(self):
        return obstruction_process
