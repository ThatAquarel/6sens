import cv2
import time
import torch
import numpy as np

from sixsens.process.process import Process


class Profile:
    def __init__(self, t, start, dt, cuda):
        self.t = t
        self.start = start
        self.dt = dt
        self.cuda = cuda


def yolo_process(child_connection, input_queue, output_queue):
    model = torch.hub.load("ultralytics/yolov5", "yolov5n")

    while True:
        if input_queue.empty():
            continue

        frame = input_queue.get()
        results = model(frame)

        serializable = {
            "ims": results.ims,
            "pred": results.pred,
            "files": results.files,
            "times": tuple(
                [
                    Profile(t=x.t, start=x.start, dt=x.dt, cuda=x.cuda)
                    for x in results.times
                ]
            ),
            "names": results.names,
            "shape": results.s,
        }

        output_queue.put(serializable)


class Yolo(Process):
    def __init__(self):
        super().__init__()

        model = torch.hub.load("ultralytics/yolov5", "yolov5n")
        frame = cv2.imread("/home/tianyi/src/6sens/drafts/bus.jpg")
        results = model(frame)

        self.results_class = type(results)

    def call(self, frame):
        self.input_queue.put(frame)

    def latest(self):
        if not self.output_queue.empty():
            serialized = self.output_queue.get()

            self.latest_data = self.results_class(
                ims=serialized["ims"],
                pred=serialized["pred"],
                files=serialized["files"],
                times=serialized["times"],
                names=serialized["names"],
                shape=serialized["shape"],
            )

        return self.latest_data

    def _get_process_function(self):
        return yolo_process
