from meta_classes import MetaSpeechRecognizer
import speech_recognition


class MyRecognizer(MetaSpeechRecognizer):
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()
        self.audio = ''
        self.listening = False

    def start_listening(self):
        self.listening = True
        with self.microphone as source:
            try:
                self.audio = self.recognizer.listen(source)
            except KeyboardInterrupt:
                pass

    def stop_listening(self):
        self.listening = False

    def get_message(self):
        try:
            return self.recognizer.recognize_whisper(self.audio)
        except speech_recognition.UnknownValueError:
            return 'Recognizer could not interpret your audio'

    def is_listening(self):
        return self.listening
