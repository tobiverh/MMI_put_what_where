from abc import ABC, abstractmethod

class MetaSpeechRec(ABC):
    """Meta class for speech recognizers.\n
    Holds both an AudioRecorder and a SpeechRecognizer.\n
    Methods:
    - __init__()
    - start_listening()
    - stop_listening()
    - get_message()
    - is_listening()"""

    @abstractmethod
    def __init__(self):
        """Initializes the speech recognizer."""

    @abstractmethod
    def start_listening(self):
        """Sets the speech recognizer in listening mode."""

    @abstractmethod
    def stop_listening(self):
        """Makes the speech recognizer stop listening."""

    @abstractmethod
    def get_message(self):
        """Returns the recognized message."""

    @abstractmethod
    def is_listening(self):
        """Boolean - True if recognizer is listening."""

class MetaRecorder(ABC):
    """Abstract class for audio recorders.\n
    A MetaRecorder should be able to record an audio message, and store it as an audio file.\n
    Methods:
    - __init__()
    - start_listening()
    - stop_listening()
    - is_listening()
    - get_audio()
    - has_audio()"""

    @abstractmethod
    def __init__(self):
        """Initializes the audio recoder."""

    @abstractmethod
    def start_listening(self):
        """Sets the audio recorder in listening mode."""

    @abstractmethod
    def stop_listening(self):
        """Makes the audio recorder stop listening."""

    @abstractmethod
    def is_listening(self):
        """Boolean - True if recorder is listening."""
        
    @abstractmethod
    def get_audio(self):
        """Returns the recorded message."""

    @abstractmethod
    def has_audio(self):
        """Boolean - True if the recorder has stored an audio file."""

class MetaSpeechRecognizer(ABC):
    """Meta class for speech recognizers.\n
    A MetaSpeechRecognizer should be able to recognize speech from audio files.\n
    Methods:
    - __init__()
    - recognize_audio()
    - get_message()
    - is_recognizing()
    - has_recognized_message()"""

    @abstractmethod
    def __init__(self):
        """Initializes the speech recognizer."""

    @abstractmethod
    def start_recognizing_audio(self, audio):
        """Starts recognizing speech from the given audio file."""

    @abstractmethod
    def stop_recognizing_audio(self, audio):
        """Stops recognizing speech from the given audio file."""
    

    @abstractmethod
    def get_message(self):
        """Returns the recognized message."""

    @abstractmethod
    def is_recognizing(self):
        """Boolean - True if recognizer is in the process of recognizing."""

    @abstractmethod
    def has_recognized_message(self):
        """Boolean - True if recognizer has recognized a spoken message."""
