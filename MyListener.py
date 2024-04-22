from pynput import keyboard as kb
import pyaudio
import wave


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()


class MyListener(kb.Listener):
    """Keyboard listener waiting for 'shift' key to be pressed to write audio to a '*.wav' file"""
    def __init__(self, wave_output_filename, channels, p, formatted, rate):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.wf = wave.open(wave_output_filename, 'wb')  # open audio file
        self.wf.setnchannels(channels)  # Set number of audio channels
        self.wf.setsampwidth(p.get_sample_size(formatted))  # set sample size
        self.wf.setframerate(rate)  # Set frame rate

    def on_press(self, key):
        """Check for 'shift' key pressed"""
        if key == key.shift:
            self.key_pressed = True
        return True

    def on_release(self, key):
        """check for 'shift' key released"""
        if key == key.shift:
            self.key_pressed = False
        return True
