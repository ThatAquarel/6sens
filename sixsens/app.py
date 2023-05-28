import cv2
import time
import ctypes
import logging
import multiprocessing
import numpy as np

from sixsens.process.audio_player import AudioPlayer
from sixsens.process.obstruction import Obstruction
from sixsens.process.matrix import Matrix
from sixsens.process.yolo import Yolo

from sixsens.reaction.audio_reaction import AudioReaction
from sixsens.reaction.matrix_reaction import MatrixReaction

from sixsens.audio.status import VisionObstructed


def run():
    audio_player = AudioPlayer()
    obstruction = Obstruction()
    matrix = Matrix()

    audio_reaction = AudioReaction()
    matrix_reaction = MatrixReaction()

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
        if i % 15 == 0:
            obstruction.call(frame)

        rendered = False
        if latest := yolo.latest(frame):
            rendered_frame = latest.render()[0]
            rendered = True

            audio_reaction.process_predictions(latest)
            matrix_reaction.process_predictions(latest)

        cv2.namedWindow("6SENS", cv2.WINDOW_NORMAL)
        cv2.moveWindow("6SENS", 1920, 0)
        cv2.setWindowProperty(
            "6SENS", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
        )
        cv2.imshow("6SENS", rendered_frame if rendered else frame)

        movements = matrix_reaction.build_reaction()
        if np.add.reduce(movements):
            matrix.call(movements)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            logging.info("Speech triggered")

            speeches = audio_reaction.build_reaction()
            # if obstruction.latest():
            #     speeches.insert(0, VisionObstructed())

            for speech in speeches:
                speech.play(audio_player)

        i += 1

        if i % 100 == 0:
            logging.debug(f"Loop time {(time.time() - past_time)/100}")
            past_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

    audio_player.stop()
    obstruction.stop()
    matrix.stop()
    yolo.stop()
