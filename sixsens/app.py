import cv2
import time
import numpy as np

from sixsens.process.audio_player import AudioPlayer
from sixsens.process.obstruction import Obstruction

from sixsens.model.yolo import YoloNode


def run():
    audio_player = AudioPlayer()
    obstruction = Obstruction()

    yolo_node = YoloNode()

    cap = cv2.VideoCapture("/dev/video2")

    i = 0
    past_time = time.time()
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        if i % 5 == 0:
            obstruction.call(frame)
        if not obstruction.output_queue.empty():
            print(obstruction.output_queue.get())

        cv2.imshow("6SENS", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        i += 1

        if i % 10 == 0:
            print(f"Loop time {(time.time() - past_time)/10}")
            past_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

    audio_player.stop()
    obstruction.stop()
