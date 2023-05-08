import torch

from sixsens.process.process import Process


def yolo_process(child_connection, input_queue, output_queue):
    model = torch.hub.load("ultralytics/yolov5", "yolov5n")

    while True:
        if input_queue.empty():
            continue

        frame = input_queue.get()
        results = model(frame)

        output_queue.put(results)


class Yolo(Process):
    def call(self, frame):
        self.input_queue.put(frame)

    def _get_process_function(self):
        return yolo_process
