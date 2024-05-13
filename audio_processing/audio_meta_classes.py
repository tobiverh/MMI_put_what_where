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

    
class MetaEyeTracker(ABC):
    """Meta class for eye trackers.\n
    Methods:
    - __init__()
    - calibrate()
    - get_quadrant()
    - start_tracking()
    - stop_tracking()
    - is_tracking()"""

    @abstractmethod
    def __init__(self):
        """Initializes the eye tracker."""

    @abstractmethod
    def calibrate(self):
        """Calibrates the eye tracker."""

    @abstractmethod
    def get_quadrant(self):
        """Returns the quadrant the user is looking at.\n
        Return values are ints 0,1,2,3 corresponding to top-left, top-right, bottom-left and bottom-right respectively."""

    @abstractmethod
    def start_tracking(self):
        """Sets the eye tracker in tracking mode."""

    @abstractmethod
    def stop_tracking(self):
        """Makes the eye tracker stop tracking."""

    @abstractmethod
    def is_tracking(self):
        """Boolean - True if the position is tracked"""

class MetaScreen(ABC):
    """Meta class for screens, on which objects can be drawn and moved.\n
    Methods:
    - __init__()
    - get_objects()
    - draw_object()
    - display_quadrants()
    - highlight_quadrant()
    - show()
    - terminate()"""

    @abstractmethod
    def __init__(self):
        """Initializes the eye gazer."""

    @abstractmethod
    def get_objects(self):
        """Returns a list of tuples, containing all drawn objects, together with their current location.\n
        Example:
        - [ ('red circle', (x, y)) , ('green square', (32, 45)) ]"""

    @abstractmethod
    def draw_object(self, shape, color):
        """Draws an object with the given shape and color.\n
        The new object is added to the screen's register of drawn objects,\n
        so that it can be found by calling get_objects()."""

    @abstractmethod
    def display_quadrants(self):
        """Displays a two by two grid, dividing the screen into four quadrants."""

    @abstractmethod
    def highlight_quadrant(self, quadrant):
        """Highlights the given quadrant on the screen.
        - quadrant is a tuple (i,j), indicating the quadrant's coordinates"""

    @abstractmethod
    def show(self):
        """Updates the display of the screen."""
        
    @abstractmethod
    def terminate(self):
        """Stop displaying the screen."""
