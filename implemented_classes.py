from meta_classes import MetaSpeechRecognizer, MetaRecorder, MetaEyeTracker, MetaScreen
import speech_recognition as sr
from audio_recorder2 import AudioRecorder
from audio_recording_display import init_recorder, recognize
import time
import os
from threading import Thread



class Recorder(MetaRecorder):
    def __init__(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.audio_file = root_dir + 'audio_recording.wav'
        self.recorder = AudioRecorder(filename=self.audio_file)

    def start_listening(self):
        init_recorder(self.recorder)
        # self.recorder.is_started = True
        #TODO: Remove print-statement ones done testing
        print("Recorder initialized")

    def stop_listening(self):
        while (self.is_listening() or not self.has_audio()):
            print()
            time.sleep(0.05)
        #TODO: Remove print-statement ones done testing
        print("Recorder stopped listening")
        

    def is_listening(self):
        return self.recorder.is_started
    
    def has_audio(self):
        return os.path.exists(self.audio_file)
    
    def get_audio(self):
        assert self.has_audio(), "Couldn't get audio because the audio file didn't exist."
        return self.audio_file
    
    def clear(self):
        """Deletes the 'audio_recording.wav' file."""
        os.remove(self.audio_file)

class SpeechRecognizer(MetaSpeechRecognizer):

    def __init__(self, audio_file):
        self.recognizer = sr.Recognizer()
        self.audio_file = audio_file
        self.audio = self.recognizer.record(self.audio_file)
        self.thread = Thread(target=recognize, args=(range(10), self, self.recognizer, self.audio), name="Recognizing audio")
        self.thread.daemon = True
        self.thread_started = False
        self.message = ""

    def start_recognizing_audio(self):
        self.thread.start()
        self.thread_started = True
    
    def recognize(ranger, self, recognizer, audio):
        try:
            self.message = recognizer.recognize_google(audio)  # recognize audio using google's free audio recognition model
        except sr.exceptions.UnknownValueError:
            self.message = 'Could not recognize user input'
            print('Unknown Value, try again...')   

    def stop_recognizing_audio(self, audio):
        while self.is_recognizing():
            time.sleep(0.05)   
        #TODO: Remove print-statement ones done testing
        print("Recognizer stopped recognizing")
    
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