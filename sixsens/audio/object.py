import time

from abc import ABC, abstractmethod

from pydub import AudioSegment
from pydub.playback import play


ROOT_PATH = "/home/tianyi/src/6sens/sixsens/audio/"


class DistanceObject(ABC):
    DISTANCES = {
        "10M": f"{ROOT_PATH}distance/10m.mp3",
        "20M": f"{ROOT_PATH}distance/20m.mp3",
        "30M": f"{ROOT_PATH}distance/30m.mp3",
        "40M": f"{ROOT_PATH}distance/40m.mp3",
        "50M": f"{ROOT_PATH}distance/50m.mp3",
        "PERIPHERY": f"{ROOT_PATH}distance/en_peripherie.mp3",
        "CLOSE": f"{ROOT_PATH}distance/tres_proche.mp3",
    }

    def __init__(self, distance):
        super().__init__()
        self.distance = distance

    @abstractmethod
    def _get_noun_audio_file(self):
        raise NotImplementedError()

    def _get_distance_audio_file(self):
        return self.DISTANCES[self.distance]

    def _load_audio(self):
        self.serialized_playlist = {
            self._get_noun_audio_file(): [500, -75],
            self._get_distance_audio_file(): [350, 0],
        }

    def play(self, audio_player):
        self._load_audio()
        audio_player.play(self.serialized_playlist)


class SpeedObject(DistanceObject):
    SPEEDS = {
        "NONE": f"{ROOT_PATH}speed/immobile.mp3",
        "SLOW": f"{ROOT_PATH}speed/lente.mp3",
        "FAST": f"{ROOT_PATH}speed/exces_vitesse.mp3",
    }

    def __init__(self, distance, speed):
        super().__init__(distance)
        self.speed = speed

    def _get_speed_audio_file(self):
        return self.SPEEDS[self.speed]

    def _load_audio(self):
        self.serialized_playlist = {
            self._get_noun_audio_file(): [500, -75],
            self._get_speed_audio_file(): [400, 0],
            self._get_distance_audio_file(): [350, 0],
        }
