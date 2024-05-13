"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
https://github.com/antoinelame/GazeTracking
"""

import cv2
from gaze_tracking import GazeTracking
import time

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    gaze.set_right()
    gaze.set_up()
    # print('horiz:', gaze.horizontal_ratio())
    # print('vertic:', gaze.vertical_ratio())

    if gaze.is_blinking():
        text = "Blinking"
    else:
        text = "Not Blinking"

    if gaze.is_right():
        text1 = "Looking right"
    else:
        text1 = "Looking Left"
    if gaze.is_up():
        text2 = "Looking up"
    else:
        text2 = "Looking down"
    # elif gaze.is_left():
    #     text = "Looking left"
    # elif gaze.is_center():
    #     text = "Looking center"

    frame_shape = frame.shape
    width = frame_shape[1]
    height = frame_shape[0]
    # if gaze.pupils_located:
    #     hor_ratio = gaze.horizontal_ratio()
    #     vert_ratio = gaze.vertical_ratio()
    #     if hor_ratio > 0.75:
    #         hor_ratio = 1.
    #     elif hor_ratio < 0.25:
    #         hor_ratio = 0.
    #     else:
    #         # 0.25 = 0, 0.75 = 1,
    #         hor_ratio -= 0.5
    #         hor_ratio *= 2.
    #         hor_ratio += 0.5
    #     # print(gaze.horizontal_ratio())
    #     position = (int(hor_ratio * width), int(gaze.vertical_ratio() * height))
    #     # print(position, gaze.horizontal_ratio(), width, gaze.vertical_ratio(), height)
    #
    #     frame = cv2.circle(frame, center=position, radius=3, color=(0, 0, 255), thickness=-1)

    cv2.putText(frame, text, (90, 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, (147, 58, 31))
    cv2.putText(frame, text1, (90, 70), cv2.FONT_HERSHEY_DUPLEX, 1.0, (147, 58, 31))
    cv2.putText(frame, text2, (90, 90), cv2.FONT_HERSHEY_DUPLEX, 1.0, (147, 58, 31))

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # cv2.imshow("Demo", frame)
    print("is_blinking?", text)
    print("is_right?", text1)
    print("is_up?", text2)

    time.sleep(1)
    if cv2.waitKey(1) == 27:  # Escape key
        break
   
webcam.release()
cv2.destroyAllWindows()
