from meta_classes import MetaSpeechRecognizer, MetaRecorder, MetaEyeTracker, MetaScreen
import speech_recognition as sr
from audio_recorder2 import AudioRecorder
from audio_recording_display import init_recorder, recognize
import time
import os
from threading import Thread



class Recorder(MetaRecorder):
    def __init__(self, audio_filename):
        self.audio_filename = audio_filename
        self.recorder = AudioRecorder(filename=self.audio_filename)

    def start_listening(self):
        init_recorder(self.recorder)
        self.recorder.listener.on_press()

    def stop_listening(self):
        self.recorder.listener.on_release()
        while (self.is_listening() or not self.has_audio()):
            time.sleep(0.05)

    def is_listening(self):
        return self.recorder.is_started
    
    def get_path(self):
        """The whole path of the the recorder's output file"""
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(root_dir, self.audio_filename)
    
    def has_audio(self):
        return os.path.exists(self.get_path())
    
    def get_audio(self):
        """Returns the filename of the stored audio clip."""
        assert self.has_audio(), "Couldn't get audio because the audio file didn't exist."
        return self.audio_filename
    
    def clear(self):
        """Removes existing file (if there is one) from the recorder's output path."""
        self.recorder.listener = None
        os.remove(self.get_path())
        self.recorder.listener = self.recorder.create_listener()

class SpeechRecognizer(MetaSpeechRecognizer):

    def __init__(self, audio_filename):
        self.recognizer = sr.Recognizer()
        with sr.AudioFile(audio_filename) as source:
            self.audio = self.recognizer.record(source)
        self.thread = None
        self.thread_started = False
        self.message = ""

    def recognize(self, ranger, recognizer, audio):
        try:
            self.message = recognizer.recognize_google(audio)  # recognize audio using google's free audio recognition model
        except sr.exceptions.UnknownValueError:
            self.message = 'Could not recognize user input'
            print('Unknown Value, try again...')  

    def start_recognizing_audio(self):
        self.thread = Thread(target=self.recognize, args=(range(10), self.recognizer, self.audio))
        self.thread.daemon = True
        self.thread.start()
        self.thread_started = True 

    def stop_recognizing_audio(self):
        print("Recognizing.", end="")
        while self.is_recognizing():
            time.sleep(0.05)   
            print(".", end="") #Print thinking dots every 0.05 seconds
        print() #Add newline after thinking
    
    def get_message(self):
        return self.message
    
    def is_recognizing(self):
        return self.thread.is_alive()
    
    def has_recognized_message(self):
        return self.thread_started and not self.thread.is_alive()
    
class PositionTracker(MetaEyeTracker):
    
    def __init__(self):
        super().__init__()

    def calibrate(self):
        return super().calibrate()

    def get_quadrant(self):
        return super().get_quadrant()

    def start_tracking(self):
        return super().start_tracking()

    def stop_tracking(self):
        return super().stop_tracking()

    def is_tracking(self):
        return super().is_tracking() 