from sixsens.audio.object import DistanceObject, SpeedObject, ROOT_PATH


# People


class People0(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/0_pers.mp3"


class People10(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/10_pers.mp3"


class People20(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/20_pers.mp3"


class People30(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/30_pers.mp3"


class People40(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/40_pers.mp3"


class People50(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/50_pers.mp3"


class People100(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/100_pers.mp3"


# Transportation


class Bus(SpeedObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/bus.mp3"


class Car(SpeedObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/voiture.mp3"


class Stop(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/panneau_arret.mp3"


class Lights(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/feu_circulation.mp3"


class Intersection(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/intersection.mp3"


# Objects


class Chair(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/chaise.mp3"


class Door(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/porte.mp3"


class Table(DistanceObject):
    def _get_noun_audio_file(self):
        return f"{ROOT_PATH}noun/porte.mp3"
