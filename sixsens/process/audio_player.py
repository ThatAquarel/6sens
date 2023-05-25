import time
import logging

from pydub import AudioSegment
from pydub.playback import play

from sixsens.process.process import Process


def audio_process(input_queue, output_queue):
    logging.info("AudioPlayer process started")

    while True:
        if input_queue.empty():
            continue

        serialized_playlist = input_queue.get()

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
        self.input_queue.put(serialized_playlist)

    def _get_process_function(self):
        return audio_process
