import cv2
import time
import ctypes
import multiprocessing
import numpy as np

from sixsens.process.audio_player import AudioPlayer
from sixsens.process.obstruction import Obstruction

from sixsens.process.yolo import Yolo

from sixsens.audio import status


def run():
    audio_player = AudioPlayer()
    obstruction = Obstruction()

    cap = cv2.VideoCapture("/dev/video2")

    i = 0

    shared_buffer = None
    buffer = None
    yolo = None

    past_time = time.time()
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        if i == 0:
            shared_buffer = multiprocessing.Array(
                ctypes.c_uint8, int(np.multiply.reduce(frame.shape))
            )
            buffer = np.frombuffer(shared_buffer.get_obj(), np.uint8)
            yolo = Yolo(shared_buffer, frame.shape)

        buffer[:] = frame.flatten()

        if i % 2 == 0:
            yolo.call(frame.shape)
        if i % 5 == 0:
            obstruction.call(frame)

        if latest := yolo.latest(frame):
            frame = latest.render()[0]

        cv2.imshow("6SENS", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            speech = None
            if obstruction.latest():
                speech = status.VisionObstructed()

            if speech:
                speech.play(audio_player)
        print(obstruction.latest())

        i += 1

        if i % 10 == 0:
            print(f"Loop time {(time.time() - past_time)/10}")
            past_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

    audio_player.stop()
    obstruction.stop()
