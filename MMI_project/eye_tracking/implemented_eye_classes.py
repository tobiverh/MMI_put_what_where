import time
import cv2
from MMI_project.eye_tracking.GazeTracking.gaze_tracking.gaze_tracking import GazeTracking
from MMI_project.eye_tracking.eye_meta_classes import MetaEyeTracker


class EyeTracker(MetaEyeTracker):

    def __init__(self):
        self.gaze = None
        self.webcam = None
        self.is_started = False
        self.quadrant = None

    def calibrate(self):
        return super().calibrate()
    
    def get_quadrant(self):
        self.face2quadrant_update()
        return self.quadrant if self.quadrant in range(4) else -1

    def start_tracking(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        self.is_started = True

    def stop_tracking(self):
        self.is_started = False
        self.webcam.release()
        cv2.destroyAllWindows()

    def is_tracking(self):
        return self.is_started
    
    def read_face(self):
        # We get a new frame from the webcam
        _, frame = self.webcam.read()
        # We send this frame to GazeTracking to analyze it
        self.gaze.refresh(frame)

    def face2quadrant_update(self):
        assert self.is_started, "The PositionTracker should be started before looking for eye positions."
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
        else:
            print("It should be impossible to get here.")

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
    print(f"Tracked quadrant: {tracker.get_quadrant()}")

    tracker.stop_tracking()

test()