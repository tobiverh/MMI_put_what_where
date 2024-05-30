import os
from MMI_project.audio_processing.meta_classes import MetaSpeechRecognizer
import speech_recognition as sr
import time
from threading import Thread


class SpeechRecognizer(MetaSpeechRecognizer):

    def __init__(self, audio_file_path):
        """
        Initializes the SpeechRecognizer, and the thread it will be working on.
        - `audio_file_path`: The path to the input audio file, from which to recognize speech. 
        """
        self.recognizer = sr.Recognizer()
        self.audio_file_path = audio_file_path
        self.audio = None
        self.thread = None
        self.thread_started = False
        self.message = ""

    def recognize(self, recognizer: sr.Recognizer, audio: sr.AudioData):
        try:
            self.message = recognizer.recognize_google(audio) # recognize audio using google's free audio recognition model
        except sr.exceptions.UnknownValueError:
            self.message = None # Could not recognize audio input...

    def start_recognizing_audio(self):
        if not self.has_audio():
            raise Exception("Cannot start recognizing, because there is no audio file.")
        with sr.AudioFile(self.audio_file_path) as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.audio = self.recognizer.record(source)
        self.thread = Thread(target=self.recognize, args=(self.recognizer, self.audio))
        self.thread.daemon = True
        self.thread.start()
        self.thread_started = True

    def has_audio(self):
        return os.path.exists(self.audio_file_path)

    def finish_recognizing_audio(self):
        """Finnishing the recognizing process"""
        self.thread.join()

    def get_message(self):
        return self.message

    def is_recognizing(self):
        if self.thread_started:
            return self.thread.is_alive() # True if thread was started AND is still alive
        else:
            return False    # Thread was never started

    def has_recognized_message(self):
        if self.thread_started:
            return not self.thread.is_alive() # True is thread was started AND terminated
        else:
            return False    # Thread was never started
        

def test():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir, 'audio_files'))
    select = os.path.abspath(os.path.join(path, 'select.wav'))
    release = os.path.abspath(os.path.join(path, 'release.wav'))
    rec = SpeechRecognizer(select)
    rec.start_recognizing_audio()
    rec.finish_recognizing_audio()
    print(f"Recognized 'select' as : {rec.get_message()}")
    rec = SpeechRecognizer(release)
    rec.start_recognizing_audio()
    rec.finish_recognizing_audio()
    print(f"Recognized 'release' as : {rec.get_message()}")

if __name__ == "__main__":
    test()