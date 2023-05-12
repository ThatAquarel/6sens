import cv2
import time
import ctypes
import multiprocessing
import numpy as np

from sixsens.process.obstruction import Obstruction
from sixsens.process.audio_player import AudioPlayer

from sixsens.process.yolo import Yolo

from sixsens.audio import status
from sixsens.audio import nouns


def get_dist_string(distance_arr):
    diag = np.min(distance_arr)
    dist = -2 * diag / 125 + 9
    dist = np.round(dist / 10)

    if dist == 0:
        dist_string = "CLOSE"
    elif dist == 1:
        dist_string = "10M"
    elif dist == 2:
        dist_string = "20M"
    elif dist == 3:
        dist_string = "30M"
    elif dist == 4:
        dist_string = "40M"
    elif dist == 5:
        dist_string = "50M"
    elif dist >= 6:
        dist_string = "PERIPHERY"

    return dist_string


def run():
    audio_player = AudioPlayer()
    # c = Obstruction()

    cap = cv2.VideoCapture("/dev/video0")

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
        # if i % 5 == 0:
        #     obstruction.call(frame)

        rendered = False
        if latest := yolo.latest(frame):
            rendered_frame = latest.render()[0]
            rendered = True

        cv2.imshow("6SENS", rendered_frame if rendered else frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            speech = None

            if speech:
                speech.play(audio_player)

        i += 1

        if i % 10 == 0:
            print(f"Loop time {(time.time() - past_time)/10}")
            past_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

    audio_player.stop()
