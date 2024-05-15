from MMI_project.audio_processing.audio_meta_classes import MetaSpeechRecognizer
import speech_recognition as sr
import time
from threading import Thread


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
            self.message = recognizer.recognize_google(
                audio)  # recognize audio using google's free audio recognition model
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
            print(".", end="")  # Print thinking dots every 0.05 seconds
        print()  # Add newline after thinking

    def get_message(self):
        return self.message

    def is_recognizing(self):
        return self.thread.is_alive()

    def has_recognized_message(self):
        return self.thread_started and not self.thread.is_alive()