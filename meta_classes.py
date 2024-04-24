from abc import ABC, abstractmethod

class MetaSpeechRecognizer(ABC):
    """Meta class for speech recognizers.\n
    Methods:
    - __init__()
    - start_listening()
    - stop_listening()
    - get_message()
    - is_listening()"""

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

class MetaEyeTracker(ABC):
    """Meta class for eye trackers.\n
    Methods:
    - __init__()
    - calibrate()
    - get_pos()
    - start_tracking()
    - stop_tracking()
    - is_tracking()"""

    @abstractmethod
    def __init__():
        """Initializes the eye tracker."""

    @abstractmethod
    def calibrate():
        """Calibrates the eye tracker."""

    @abstractmethod
    def get_pos():
        """Returns the position of the eye gaze."""

    @abstractmethod
    def start_tracking():
        """Should set the eye tracker in tracking mode."""

    @abstractmethod
    def stop_tracking():
        """Should make the eye tracker stop tracking."""

    @abstractmethod
    def is_tracking():
        """Boolean - True if the position is tracked"""

class MetaScreen(ABC):
    """Meta class for screens, on which objects can be drawn and moved.\n
    Methods:
    - __init__()
    - get_objects()
    - draw_object()
    - show()
    - terminate()"""

    @abstractmethod
    def __init__():
        """Initializes the eye gazer."""

    @abstractmethod
    def get_objects():
        """Returns a list of tuples, containing all drawn objects, together with their current location.\n
        Example:
        - [ ('red circle', (x, y)) , ('green square', (32, 45)) ]"""

    @abstractmethod
    def draw_object(shape, color):
        """Draws an object with the given shape and color.\n
        The new object should be added to the screen's register of drawn objects,\n
        so that it can be found by calling get_objects()."""

    @abstractmethod
    def show():
        """Updates the display of the screen."""
        
    @abstractmethod
    def terminate():
        """Stop displaying the screen."""

