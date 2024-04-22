# Taken directly from:
# https://stackoverflow.com/questions/44894796/pyaudio-and-pynput-recording-while-a-key-is-being-pressed-held-down
# on 20.04.2024

import time
import pyaudio
import sched
import sys
from MyListener import MyListener


class AudioRecorder:
    def __init__(self, filename="output.wav"):
        self.CHUNK = 8192
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = filename

        self.p_thang = pyaudio.PyAudio()
        self.frame_list = []

        self.listener = MyListener(self.WAVE_OUTPUT_FILENAME, self.CHANNELS, self.p_thang, self.FORMAT, self.RATE)
        self.listener.start()
        self.is_started = False
        self.stream_in = None

    def callback(self, in_data, frame_count, time_info, status):
        self.frame_list.append(in_data)
        return in_data, pyaudio.paContinue

    def recorder(self, started, p, stream, frames):
        # global started, p, stream, frames

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
                print("start Stream")
            except ValueError:
                print('ValueError thrown... Something seems to be off!')

        elif not self.listener.key_pressed and started:
            print("Stop recording")
            stream.stop_stream()
            stream.close()
            p.terminate()
            self.listener.wf.writeframes(b''.join(frames))
            self.listener.wf.close()
            print("You should have a wav file in the current directory")
            sys.exit()
        # Reschedule the recorder function in 100 ms.
        task.enter(0.1, 1, self.recorder, (started, p, stream, frames))


my_ar = AudioRecorder("release.wav")

print("Press and hold the 'r' key to begin recording")
print("Release the 'r' key to end recording")
task = sched.scheduler(time.time, time.sleep)
task.enter(0.1, 1, my_ar.recorder,
           (my_ar.is_started, my_ar.p_thang, my_ar.stream_in, my_ar.frame_list))
task.run()
