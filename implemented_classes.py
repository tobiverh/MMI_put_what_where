from meta_classes import MetaSpeechRecognizer, MetaRecorder, MetaEyeTracker, MetaScreen
import speech_recognition as sr
from audio_recorder2 import AudioRecorder
from audio_recording_display import init_recorder, recognize
import time
import os



class Recorder(MetaRecorder):
    def __init__(self):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.audio_file = root_dir + 'audio_recording.wav'
        self.recorder = AudioRecorder(self.audio_file)

    def start_listening(self):
        init_recorder(self.recorder)
        self.is_listening = True
        #TODO: Remove print-statement ones done testing
        print("Recorder initialized")

    def stop_listening(self):
        while (self.is_listening):
            time.sleep(0.05)
        #TODO: Remove print-statement ones done testing
        print("Recorder stopped listening")
        

    def is_listening(self):
        return self.recorder.is_started
    
    def has_audio(self):
        return os.path.exists(self.audio_file)
    
    def get_audio(self):
        assert self.has_audio(), "Couldn't get audio because the audio file didn't exist."
        pass
    
    def clear(self):
        """Deletes the 'audio_recording.wav' file."""
        os.remove(self.audio_file)


class SpeechRecognizer(MetaSpeechRecognizer):

    def __init__(self):
        self.recorder = AudioRecorder()
        self.recognizer = sr.Recognizer()
        self.message

    def start_listening(self):
        init_recorder(self.recorder)
        #TODO: Remove print-statement ones done testing
        print("Recorder initialized")

    def stop_listening():
        pass

    def get_message(self):
        return self.message

    def is_listening():
        pass

class PositionTracker(MetaEyeTracker):
    pass