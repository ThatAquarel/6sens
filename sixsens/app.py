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

from sixsens.reaction.audio_reaction import AudioReaction
from sixsens.reaction.matrix_reaction import MatrixReaction
from sixsens.process.serial import Matrix


def run():
    audio_player = AudioPlayer()
    audio_reaction = AudioReaction()
    matrix_reaction = MatrixReaction()
    matrix = Matrix()

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

        rendered = False
        if latest := yolo.latest(frame):
            rendered_frame = latest.render()[0]
            rendered = True

            audio_reaction.process_predictions(latest)
            matrix_reaction.process_predictions(latest)
        cv2.imshow("6SENS", rendered_frame if rendered else frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            print("key")
            speeches = audio_reaction.build_reaction()

            for speech in speeches:
                speech.play(audio_player)

        i += 1

        if i % 10 == 0:
            print(f"Loop time {(time.time() - past_time)/10}")
            past_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

    audio_player.stop()
    yolo.stop()
