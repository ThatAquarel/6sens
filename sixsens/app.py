import cv2

from sixsens.audio.audio_process import AudioPlayerManager
from sixsens.audio.nouns import Intersection

from sixsens.model.yolo import YoloNode


def run():
    audio_player = AudioPlayerManager()

    yolo_node = YoloNode()

    cap = cv2.VideoCapture("/dev/video0")
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        yolo_results, annotated_frame = yolo_node.process(frame)

        cv2.imshow("6SENS", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    audio_player.stop()
