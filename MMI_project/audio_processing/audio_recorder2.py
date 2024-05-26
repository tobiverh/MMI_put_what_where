# Taken (almost) directly from:
# https://stackoverflow.com/questions/44894796/pyaudio-and-pynput-recording-while-a-key-is-being-pressed-held-down
# on 20.04.2024

import pyaudio
import sys
# from MyListener import MyListener
from MMI_project.audio_processing.wav_handler import WavHandler


class AudioRecorder:
    """AudioRecorder starts a keyboard listener to listen for key-key
     presses to start recording to a given audio file."""
    def __init__(self, filename="output.wav"):
        self.CHUNK = 8192
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = filename

        self.p_thang = pyaudio.PyAudio()
        self.frame_list = []
        self.listener = self.create_listener()

        # self.listener.start()
        self.is_started = False
        self.stream_in = None
        self.task = None

    def set_task(self, task):
        self.task = task

    def create_listener(self):
        return WavHandler(self.WAVE_OUTPUT_FILENAME, self.CHANNELS, self.p_thang, self.FORMAT, self.RATE)

    def new_file(self, new_filename):
        self.WAVE_OUTPUT_FILENAME = new_filename
        self.listener = self.create_listener()

    def callback(self, in_data, frame_count, time_info, status):
        """Refer to
        https://stackoverflow.com/questions/44894796/pyaudio-and-pynput-recording-while-a-key-is-being-pressed-held-down
        """
        self.frame_list.append(in_data)
        return in_data, pyaudio.paContinue

    def recorder(self, started, p, stream, frames):
        """Refer to
        https://stackoverflow.com/questions/44894796/pyaudio-and-pynput-recording-while-a-key-is-being-pressed-held-down
        """

        if self.listener.key_pressed and not started:
            # Start the recording
            try:
                stream = p.open(format=self.FORMAT,
                                channels=self.CHANNELS,
                                rate=self.RATE,
                                input=True,
                                frames_per_buffer=self.CHUNK,
                                stream_callback=self.callback)
                print("Stream active:", stream.is_active())
                started = True
                self.is_started = True
            except ValueError:
                print('ValueError thrown... Something seems to be off!')

        elif not self.listener.key_pressed and started:
            # Stop the recording
            stream.stop_stream()
            stream.close()
            p.terminate()
            self.listener.wf.writeframes(b''.join(frames))
            self.listener.wf.close()
            print("You should have a wav file in the current directory")
            self.is_started = False
            sys.exit()
        # Reschedule the recorder function in 100 ms.
        self.task.enter(0.1, 1, self.recorder, (started, p, stream, frames))
