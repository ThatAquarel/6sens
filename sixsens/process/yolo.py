import cv2
import time
import torch
import queue
import logging
import numpy as np

from sixsens.process.process import Process


class Profile:
    def __init__(self, t, start, dt, cuda):
        self.t = t
        self.start = start
        self.dt = dt
        self.cuda = cuda


def yolo_process(
    stop_event, input_queue, output_queue, shared_buffer, frame_shape
):
    logging.info("Yolo process started")

    buffer = np.frombuffer(shared_buffer.get_obj(), np.uint8)
    frame = np.empty(frame_shape, np.uint8)
    model = torch.hub.load("ultralytics/yolov5", "yolov5n")

    while True:
        if stop_event.is_set():
            logging.info("Yolo process stopped")
            break

        if input_queue.empty():
            continue

        frame_shape_ = input_queue.get()
        frame[:] = buffer.reshape(frame_shape_)

        results = model(frame)

        serializable = {
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

        output_queue.put(obj=serializable)


class Yolo(Process):
    def __init__(self, shared_buffer, frame_shape):
        self.shared_buffer = shared_buffer
        super().__init__(self.shared_buffer, frame_shape)

        model = torch.hub.load("ultralytics/yolov5", "yolov5n")
        frame = cv2.imread("C:\\Users\\xia_t\\Desktop\\Projects\\6thsense\\drafts\\bus.jpg")
        results = model(frame)

        self.results_class = type(results)

    def call(self, frame_shape):
        self.input_queue.put(frame_shape)

    def latest(self, frame):
        if not self.output_queue.empty():
            serialized = self.output_queue.get()

            self.latest_data = self.results_class(
                ims=[frame],
                pred=serialized["pred"],
                files=serialized["files"],
                times=serialized["times"],
                names=serialized["names"],
                shape=serialized["shape"],
            )

        return self.latest_data

    def _get_process_function(self):
        return yolo_process
