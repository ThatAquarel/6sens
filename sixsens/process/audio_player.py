from pydub import AudioSegment
from pydub.playback import play

from sixsens.process.process import Process


def audio_process(child_connection, *args):
    while True:
        serialized_playlist = child_connection.recv()
        if len(serialized_playlist) < 1:
            break

        audios = []
        for key, value in serialized_playlist.items():
            audio = AudioSegment.from_file(key, format="mp3")

            a = value[0]
            b = len(audio) + value[0]

            audios.append(audio[a:b])

        for audio in audios:
            play(audio)


class AudioPlayer(Process):
    def call(self, serialized_playlist):
        self.child_connection.send(serialized_playlist)

    def _get_process_function(self):
        return audio_process
