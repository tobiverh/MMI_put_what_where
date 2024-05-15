"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
https://github.com/antoinelame/GazeTracking
"""
from threading import Thread

import cv2
from MMI_project.eye_tracking.GazeTracking.gaze_tracking import GazeTracking
import time


class MyGazeTracker:
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)

        self.is_started = False

    def start_tracking(self):
        self.is_started = True
        print('started!')
        while self.is_started:
            # We get a new frame from the webcam
            _, frame = self.webcam.read()

            # We send this frame to GazeTracking to analyze it
            self.gaze.refresh(frame)

            frame = self.gaze.annotated_frame()
            text = ""

            if self.gaze.is_blinking():
                text = "Blinking"
            else:
                text = "Not Blinking"

            if self.gaze.pupils_located:
                self.gaze.set_right()
                self.gaze.set_up()

                if self.gaze.is_right():
                    text1 = "Looking right"
                else:
                    text1 = "Looking Left"
                if self.gaze.is_up():
                    text2 = "Looking up"
                else:
                    text2 = "Looking down"

                print("is_blinking?", text)
                print("is_right?", text1)
                print("is_up?", text2)

                time.sleep(0.5)
                # if time.time() - start > 15:
                #     break

    def stop_tracking(self):
        self.is_started = False
        self.webcam.release()
        cv2.destroyAllWindows()

    def get_gaze(self):
        side = int(self.gaze.is_right())
        up = int(self.gaze.is_up())
        return side, up


if __name__ == '__main__':
    my_tracker = MyGazeTracker()

    tracking_thread = Thread(target=my_tracker.start_tracking)
    tracking_thread.daemon = True
    tracking_thread.start()
    # tracking_thread.run()

    time.sleep(3)
    if tracking_thread.is_alive():
        # tracking_thread.join()
        my_tracker.stop_tracking()
    print('uh oh')
    # my_tracker.stop_tracking()
