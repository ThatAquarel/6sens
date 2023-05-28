from sixsens.audio.audio import Audio, DistanceAudio, SpeedAudio, ROOT_PATH


# People


class People0(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/0_pers.mp3"


class People1(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/1_pers.mp3"


class People10(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/10_pers.mp3"


class People20(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/20_pers.mp3"


class People30(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/30_pers.mp3"


class People40(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/40_pers.mp3"


class People50(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/50_pers.mp3"


class People100(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/100_pers.mp3"


# Transportation


class Bus(SpeedAudio):
    # class Bus(SpeedAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/bus.mp3"


class Car(SpeedAudio):
    # class Car(SpeedAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/voiture.mp3"


class Stop(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/panneau_arret.mp3"


class Lights(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/feu_circulation.mp3"


class Intersection(Audio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/intersection.mp3"


# Objects


class Chair(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/chaise.mp3"


class Door(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/porte.mp3"


class Table(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/porte.mp3"
