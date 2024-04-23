from pynput import keyboard as kb
import pyaudio
import wave


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()


class WavHandler:
    """Keyboard listener waiting for 'shift' key to be pressed to write audio to a '*.wav' file"""
    def __init__(self, wave_output_filename, channels, p, formatted, rate):
        self.key_pressed = False
        self.wf = wave.open(wave_output_filename, 'wb')  # open audio file
        self.wf.setnchannels(channels)  # Set number of audio channels
        self.wf.setsampwidth(p.get_sample_size(formatted))  # set sample size
        self.wf.setframerate(rate)  # Set frame rate

    def on_press(self):
        self.key_pressed = True

    def on_release(self):
        self.key_pressed = False