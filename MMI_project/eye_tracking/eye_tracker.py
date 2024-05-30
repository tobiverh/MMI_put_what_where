from threading import Thread
import time
import cv2
from MMI_project.eye_tracking.GazeTracking.gaze_tracking.gaze_tracking import GazeTracking
from MMI_project.eye_tracking.meta_class import MetaEyeTracker


class EyeTracker(MetaEyeTracker):
    """
    EyeTracker that tracks the position of the user's eye gaze, assigning it a quadrant on the screen (top-left, top-right, bottom-left, bottom-right).
    For the EyeTracker to work, the device needs to have a camera that is not currently used by any other software.
    """
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        self.thread_started = False
        self.quadrant = None
        self.thread = None
        self.thread_started = False
    
    def get_quadrant(self):
        return self.quadrant if self.quadrant in range(4) else -1

    def start_tracking(self):
        """
        Starts the job of tracking eye gaze, as a quadrant-value from 0 to 3.
        """
        self.thread = Thread(target=self.face2quadrant_update)
        self.thread.daemon = True
        self.thread_started = True
        self.thread.start()

    def finish_tracking(self, freq = 0.01):
        """
        Waits for EyeTracker to finish the job of tracking user's eye gaze.
        """
        self.thread.join()

    def terminate(self):
        """
        Terminates the EyeTracker. That is, the video capture is closed down.
        """
        self.webcam.release()
        cv2.destroyAllWindows()

    def is_tracking(self):
        return self.thread_started and self.thread.is_alive()
    
    def read_face(self):
        # We get a new frame from the webcam
        _, frame = self.webcam.read()
        # We send this frame to GazeTracking to analyze it
        self.gaze.refresh(frame)

    def face2quadrant_update(self):
        assert self.thread_started, "The PositionTracker should be started before looking for eye positions."
        self.read_face()
        #Wait for user to stop blinking
        while self.gaze.is_blinking() or not self.gaze.pupils_located:
            time.sleep(0.01)
            self.read_face()
        #Check where user is looking
        self.gaze.set_right()
        self.gaze.set_up()
        #Update chosen quadrant
        up = self.gaze.is_up()
        down = not up
        right = self.gaze.is_right()
        left = not right

        if up and left:
            self.quadrant = 0
        elif up and right:
            self.quadrant = 1
        elif down and left:
            self.quadrant = 2
        elif down and right:
            self.quadrant = 3

def test():
    print("Tracking eyes...")
    print("""
    0 --> Top-left
    1 --> Top-right
    2 --> Bottom-left
    3 --> Bottom-right
    """)
    tracker = EyeTracker()
    tracker.start_tracking()
    tracker.finish_tracking()
    print(f"Tracked quadrant: {tracker.get_quadrant()}")


if __name__ == "__main__":
    test()