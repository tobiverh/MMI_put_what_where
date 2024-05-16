from MMI_project.audio_processing.audio_meta_classes import MetaSpeechRecognizer
import speech_recognition as sr
import time
from threading import Thread


class SpeechRecognizer(MetaSpeechRecognizer):

    def __init__(self, audio_file_path, language="en-US", keywords=None):
        """
        Initializes the SpeechRecognizer, and the thread it will be working on.
        - `audio_file_path`: The path to the input audio file, from which to recognize speech. 
        """
        self.recognizer = sr.Recognizer()
        self.audio_file_path = audio_file_path
        self.audio = None
        self.language = language
        self.keywords = keywords
        self.thread = None
        self.thread_started = False
        self.message = ""

    # def recognize(self, ranger, recognizer: sr.Recognizer, audio, language, keywords):
    def recognize(self, ranger, recognizer: sr.Recognizer, audio):
        try:
            self.message = recognizer.recognize_google(audio)  # recognize audio using google's free audio recognition model
            # self.message = recognizer.recognize_sphinx(audio, language, keywords)
        except sr.exceptions.UnknownValueError:
            self.message = 'Could not recognize user input'
            print('Unknown Value, try again...')

    def start_recognizing_audio(self):
        with sr.AudioFile(self.audio_file_path) as source:
            self.audio = self.recognizer.record(source)
        # self.thread = Thread(target=self.recognize, args=(range(10), self.recognizer, self.audio, self.language, self.keywords))
        self.thread = Thread(target=self.recognize, args=(range(10), self.recognizer, self.audio))
        self.thread.daemon = True
        self.thread.start()
        self.thread_started = True

    def stop_recognizing_audio(self):
        print("Recognizing.", end="")
        while self.is_recognizing():
            time.sleep(0.05)
            print(".", end="")  # Print thinking dots every 0.05 seconds
        print()  # Add newline after thinking

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