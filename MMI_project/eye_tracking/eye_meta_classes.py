from abc import ABC, abstractmethod

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
    def get_quadrant(self):
        """Returns the quadrant the user is looking at.\n
        Return values are ints 0,1,2,3 corresponding to top-left, top-right, bottom-left and bottom-right respectively."""

    @abstractmethod
    def start_tracking(self):
        """Sets the eye tracker in tracking mode."""

    @abstractmethod
    def finish_tracking(self):
        """Makes the eye tracker stop tracking."""

    @abstractmethod
    def is_tracking(self):
        """Boolean - True if the position is tracked"""