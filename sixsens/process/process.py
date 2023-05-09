import queue
import multiprocessing

from abc import ABC, abstractmethod


class Process(ABC):
    def __init__(self):
        self.input_queue, self.output_queue = (
            multiprocessing.Queue(),
            multiprocessing.Queue(),
        )

        self.process = multiprocessing.Process(
            target=self._get_process_function(),
            args=(self.input_queue, self.output_queue),
        )
        self.process.start()

    @abstractmethod
    def _get_process_function(self):
        raise NotImplementedError()

    @abstractmethod
    def call(self, *args, **kwargs):
        raise NotImplementedError()

    latest_data = None

    def latest(self):
        try:
            self.latest_data = self.output_queue.get_nowait()
        except queue.Empty:
            pass

        return self.latest_data

    def stop(self):
        self.process.terminate()
        while self.process.is_alive():
            pass

        self.process.join(timeout=1.0)

        self.input_queue.close()
        self.output_queue.close()
