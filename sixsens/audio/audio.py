import time

from abc import ABC, abstractmethod

from pydub import AudioSegment
from pydub.playback import play


# ROOT_PATH = "/home/tianyi/src/6sens/sixsens/audio/"
ROOT_PATH = "C:\\Users\\xia_t\\Desktop\\Projects\\6thsense\\sixsens\\audio\\"


class Audio(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def _get_audio_file(self):
        raise NotImplementedError()

    def _load_audio(self):
        self.serialized_playlist = {self._get_audio_file(): [0, 0]}

    def play(self, audio_player):
        self._load_audio()
        audio_player.call(self.serialized_playlist)


class DistanceAudio(Audio):
    DISTANCES = {
        "10M": f"{ROOT_PATH}distance/10m.wav",
        "20M": f"{ROOT_PATH}distance/20m.wav",
        "30M": f"{ROOT_PATH}distance/30m.wav",
        "40M": f"{ROOT_PATH}distance/40m.wav",
        "50M": f"{ROOT_PATH}distance/50m.wav",
        "PERIPHERY": f"{ROOT_PATH}distance/en_peripherie.wav",
        "CLOSE": f"{ROOT_PATH}distance/tres_proche.wav",
    }

    def __init__(self, distance):
        super().__init__()
        self.distance = distance

    def _get_distance_audio_file(self):
        return self.DISTANCES[self.distance]

    def _load_audio(self):
        self.serialized_playlist = {
            self._get_audio_file(): [500, -75],
            self._get_distance_audio_file(): [350, 0],
        }


class SpeedAudio(DistanceAudio):
    SPEEDS = {
        "NONE": f"{ROOT_PATH}speed/immobile.wav",
        "SLOW": f"{ROOT_PATH}speed/lente.wav",
        "FAST": f"{ROOT_PATH}speed/exces_vitesse.wav",
    }

    def __init__(self, distance, speed):
        super().__init__(distance)
        self.speed = speed

    def _get_speed_audio_file(self):
        return self.SPEEDS[self.speed]

    def _load_audio(self):
        self.serialized_playlist = {
            self._get_audio_file(): [500, -75],
            self._get_speed_audio_file(): [400, 0],
            self._get_distance_audio_file(): [350, 0],
        }
