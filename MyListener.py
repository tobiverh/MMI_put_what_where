from pynput import keyboard
import pyaudio
import wave


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()


class MyListener(keyboard.Listener):
    def __init__(self, wave_output_filename, channels, p, formatted, rate):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None
        self.wf = wave.open(wave_output_filename, 'wb')
        self.wf.setnchannels(channels)
        self.wf.setsampwidth(p.get_sample_size(formatted))
        self.wf.setframerate(rate)

    def on_press(self, key):
        if key.char == 'r':
            self.key_pressed = True
        return True

    def on_release(self, key):
        if key.char == 'r':
            self.key_pressed = False
        return True
