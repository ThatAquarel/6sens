import multiprocessing

from pydub import AudioSegment
from pydub.playback import play


def audio_process(child_connection):
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


class AudioPlayerManager:
    def __init__(self):
        self.parent_connection, self.child_connection = multiprocessing.Pipe()

        self.audio_process = multiprocessing.Process(
            target=audio_process, args=(self.child_connection,)
        )
        self.audio_process.start()

    def play(self, serialized_playlist):
        self.parent_connection.send(serialized_playlist)

    def stop(self):
        self.parent_connection.send({})
