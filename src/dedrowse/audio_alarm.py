import wave

import pyaudio
from attentive import StoppableThread

from . import settings


class AudioAlarm(StoppableThread):
    def __init__(self, audio_file=settings.ALARM_SOUND()):
        super().__init__()
        self.audio_file = audio_file
        self.on = False

    def run(self):
        chunk = 1024
        p = pyaudio.PyAudio()
        wf = wave.open(self.audio_file, 'rb')

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)
        stream.start_stream()

        while not self.stopped:
            if not self.on:
                self.sleep(0.1)
                continue

            data = wf.readframes(chunk)
            while data != '':
                stream.write(data)
                data = wf.readframes(chunk)
            wf.rewind()

        stream.stop_stream()
        stream.close()
        p.terminate()
