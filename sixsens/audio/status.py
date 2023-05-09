from sixsens.audio.audio import Audio, ROOT_PATH

# Status


class Attention(Audio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}status/attention.mp3"


class VisionObstructed(Audio):
    def _get_audio_file(self):
        return f"{ROOT_PATH}status/champ_vision.mp3"
