from abc import ABC, abstractmethod


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

