from sixsens.audio.audio import Audio, DistanceAudio, SpeedAudio, ROOT_PATH


# People


class People0(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/0_pers.wav"


class People1(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/1_pers.wav"


class People10(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/10_pers.wav"


class People20(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/20_pers.wav"


class People30(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/30_pers.wav"


class People40(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/40_pers.wav"


class People50(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/50_pers.wav"


class People100(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/100_pers.wav"


# Transportation


class Bus(SpeedAudio):
    # class Bus(SpeedAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/bus.wav"


class Car(SpeedAudio):
    # class Car(SpeedAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/voiture.wav"


class Stop(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/panneau_arret.wav"


class Lights(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/feu_circulation.wav"


class Intersection(Audio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/intersection.wav"


# Objects


class Chair(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/chaise.wav"


class Door(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/porte.wav"


class Table(DistanceAudio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}noun/porte.wav"
