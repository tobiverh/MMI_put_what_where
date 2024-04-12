from abc import ABC, abstractmethod

class MetaSpeechRecognizer(ABC):
    """Meta class for speech recognizers"""

    @abstractmethod
    def __init__():
        """Initializes the speech recognizer."""

    @abstractmethod
    def start_listening():
        """Should set the speech recognizer in listening mode."""

    @abstractmethod
    def stop_listening():
        """Should make the speech recognizer stop listening."""

    @abstractmethod
    def get_message():
        """Should return the recognized message."""

    @abstractmethod
    def is_listening():
        """Boolean - True if recognizer is listening."""

class MetaEyeGazer(ABC):
    """Meta class for eye gazers."""

    @abstractmethod
    def __init__():
        """Initializes the eye gazer."""

    @abstractmethod
    def calibrate():
        """Calibrates the eye gazer."""

    @abstractmethod
    def get_pos():
        """Returns the position of the eye gaze."""

    @abstractmethod
    def start_tracking():
        """Should set the eye gazer in tracking mode."""

    @abstractmethod
    def stop_tracking():
        """Should make the eye gazer stop tracking."""

    @abstractmethod
    def is_tracking():
        """Boolean - True if the position is tracked"""
