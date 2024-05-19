from threading import Thread

import pygame
import time
import numpy as np
import speech_recognition as sr

from MMI_project.eye_tracking.eye_meta_classes import MetaEyeTracker


def on_quit(event):
    """Handles pygame's quit event (e.g. ctrl-q
    :param event: The pygame event from the main loop"""
    if event.type == pygame.QUIT:
        global running
        running = False  # Stop main loop from running (no more updates)
        pygame.display.quit()  # Quit the display
        pygame.quit()  # Quit pygame
        exit(0)  # Exit program


def blackout(screen):
    """Fills the pygame display with black
    :param screen: the screen which is repainted"""
    screen.fill((0, 0, 0))  # Fills the screen with black
    pygame.draw.rect(screen, color=(100, 100, 100), rect=(0, screen.get_height() - 30, screen.get_width(), 30))
    # pygame.display.update()  # flips the display


def init_screen(title='Hello'):
    """Initializes the display screen of maximum size to all black with given title text
    :param title: default = 'Hello' message displayed at top of window
    :return screen: the pygame display screen"""
    pygame.init()  # Initialize pygame
    display_size = list(pygame.display.get_desktop_sizes()[0])  # Get max screen size
    display_size[1] -= 55  # Adjust to ensure window fits in screen
    screen = pygame.display.set_mode(display_size)  # Create max allowable size screen
    pygame.display.set_caption(title)  # Set caption
    blackout(screen)  # Make screen black
    pygame.display.update()  # flips the display
    return screen


def draw_text(screen, text, font):
    """Draws message on the pygame display
    :param screen: the screen where the text will be displayed
    :param text: the text which is displayed on the screen
    :param font: the font type for the text"""
    col = (255, 0, 0)  # Red color for text
    img = font.render(text, True, col)  # creates a small sub-image with the provided text and color
    screen.blit(img, (screen.get_width()/2, screen.get_height() - 30))  # Adds the text in position 800, 800
    # pygame.display.update()  # flips the display to show text on screen


def init_font(font_name='Arial', size=24):
    """Initializes the default font to be used for relaying messages back to the user
    :param font_name: default = 'Arial'
    :param size: default = 24 is the font size to be used"""
    pygame.font.init()  # Initialize font
    text_font = pygame.font.SysFont(font_name, size=size)  # Get system font of font_name and size
    return text_font


def recognize(ranger, recognizer, audio):
    """Threaded function recognizes passed in audio and stores message in global variable 'message'
    :param ranger: unused iterable argument mandated by Thread module
    :param recognizer: Speech Recognition instance
    :param audio: The audio recorded from an audio file"""
    global message, done
    # message: String where recognized audio is
    # done: bool set to True once the recognition algorithm has finished
    try:
        message = recognizer.recognize_google(audio)  # recognize audio using google's free audio recognition model
    except sr.exceptions.UnknownValueError:
        message = 'Could not recognize user input'
        print('Unknown Value, try again...')
    done = True  # Note end of recognition


def init_quadrant_matrix(screen):
    """
    This divides the provided screen into 4 equal parts in the following order: Upper-left, Upper-right, Lower-left,
    Lower-right
    :param screen: display object with get_width() and get_height() calls available
    :return: list of tuples of pygame rectangle requirements (left_x, top_y, width, height) in the following order:
           @index 0: left, up, 1: right, up, 2: left, down, 3: right, down
    """
    return [(0, 0, screen.get_width()/2, screen.get_height()/2),  # left, up
            (screen.get_width() / 2, 0, screen.get_width() / 2, screen.get_height() / 2),  # right, up
            (0, screen.get_height()/2, screen.get_width()/2, screen.get_height()/2),  # left, down
            (screen.get_width()/2, screen.get_height()/2, screen.get_width()/2, screen.get_height()/2)  # right, down
           ]  # 0: left, up, 1: right, up, 2: left, down, 3: right, down


def init_sub_quadrant_matrix(quadrants):
    """
    This iteratively subdivides the provided quadrants into 4 equal parts in the following order: Upper-left,
    Upper-right, Lower-left, Lower-right
    :param quadrants: list of tuples with pygame rectangle requirements (left_x, top_y, width, height)
    :return: 2D list of tuples of pygame rectangle requirements (left_x, top_y, width, height) in the following order:
           @index 0: left, up, 1: right, up, 2: left, down, 3: right, down
    """
    sub_quads = []
    for left, top, width, height in quadrants:
        top_left = (left, top, width / 2, height / 2)
        top_right = (left + width / 2, top, width / 2, height / 2)
        bottom_left = (left, top + height / 2, width / 2, height / 2)
        bottom_right = (left + width / 2, top + height / 2, width / 2, height / 2)
        sub_quads.append(
            [top_left, top_right, bottom_left, bottom_right]
        )

    return sub_quads


def get_sub_quadrant_center(rectangle):
    """
    Function unpacks contents of the parameters and returns the center of the object
    :param rectangle: pygame rectangle with requirements (left_x, top_y, width, height)
    :return: tuple like: center_x, center_y
    """
    left, top, width, height = rectangle
    return left + width/2, top + height/2


def update():
    pygame.display.update()


class MyGaze(MetaEyeTracker):
    """
    This is a fake Eye Tracker, which implements the MetaEyeTracker Framework
    Returns a random integer between 0 - 3 when get_quadrant() is called
    """
    def __init__(self):
        self.started = False

    def calibrate(self):
        pass

    def get_quadrant(self):
        return np.random.randint(0, 4)  # Top right

    def start_tracking(self):
        self.started = True

    def stop_tracking(self):
        self.started = False

    def is_tracking(self):
        return self.started


def run():
    screen = init_screen()

    # Return values are ints 0, 1, 2, 3 corresponding to:
    # top - left, top - right, bottom - left and bottom - right respectively
    quadrant_rectangles = init_quadrant_matrix(screen=screen)
    sub_quadrant_rectangles = init_sub_quadrant_matrix(quadrants=quadrant_rectangles)

    # INITIALIZE OLD RECOGNIZER
    recognizer = sr.Recognizer()

    # Set a random seed for our random quadrant generator
    np.random.seed(0)
    gazer = MyGaze()

    # Choose placement of starting object
    original_circle_pos = new_circle_pos = get_sub_quadrant_center(sub_quadrant_rectangles[1][1])

    global running, done, message
    # Set quadrant indices to default values
    quadrant_idx = -1
    sub_quadrant_idx = -1
    selected = False
    n_quad_idx = -1
    n_sub_quad_idx = -1

    # Main pygame event loop
    while running:
        for event in pygame.event.get():
            # Here we are checking to see if the 's' key was pressed. This chunk of code queues the 'select.wav' file to
            # The OLD VERSION of the Audio recognizer.
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 's':
                gazer.start_tracking()
                with sr.AudioFile('../audio_files/select.wav') as source:
                    audio = recognizer.record(source)
                    recognition_thread = Thread(target=recognize, args=(range(10), recognizer, audio))
                    recognition_thread.daemon = True
                    recognition_thread.start()

            # Here we are checking to see if the 'r' key was pressed. This chunk of code queues the 'release.wav' file
            # to the OLD VERSION of the Audio recognizer.
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'r':
                gazer.start_tracking()
                with sr.AudioFile('../audio_files/release.wav') as source:
                    audio = recognizer.record(source)
                    recognizer.adjust_for_ambient_noise(source)
                    recognition_thread = Thread(target=recognize, args=(range(10), recognizer, audio))
                    recognition_thread.daemon = True
                    recognition_thread.start()

            # This marks the OLD VERSION of the Audio Recognizer finishing its recognition task. The Value of 'done'
            # Is changed in the 'recognize' function on line 64 of this script. This means that a message has been
            # interpreted and is ready for inference
            if done:
                # Stop eye tracking, it holds the previous position in memory
                gazer.stop_tracking()
                done = False

                # If the message reads 'select', we select the quadrant or sub quadrant returned by the 'gaze tracker'
                if message == 'select':
                    # Clear the screen
                    blackout(screen)
                    # Checks to see if a shape object is selected or not. If it hasn't been, update the original
                    # Quadrant index using the 'gaze tracker'
                    if not selected:
                        # This means that the outer quadrant hasn't been selected yet.
                        if quadrant_idx == -1:
                            quadrant_idx = gazer.get_quadrant()
                        # This means that the sub quadrant hasn't been selected yet
                        else:
                            sub_quadrant_idx = gazer.get_quadrant()
                    # If a shape IS selected, then update the new quadrant indices! These can be merged with some clever
                    # thinking which I didn't have time for...
                    else:
                        # Same as above comment on line 195
                        if n_quad_idx == -1:
                            n_quad_idx = gazer.get_quadrant()
                        # Same as above comment on line 198
                        else:
                            n_sub_quad_idx = gazer.get_quadrant()

                # If the message reads 'release', we drop/release the quadrant or sub-quadrant which is currently
                # selected
                elif message == 'release':
                    # Clear the screen
                    blackout(screen)
                    # If a shape is selected and a sub-quadrant has been chosen, then change the shape's location to the
                    # center of the desired sub quadrant.
                    if selected and n_sub_quad_idx != -1:
                        # New circle position is defined further down
                        original_circle_pos = new_circle_pos
                        # Reset the new quadrant indices!
                        n_quad_idx = -1
                        n_sub_quad_idx = -1
                        # Release shape object!
                        selected = False
                    # If a shape is selected and an outer quadrant hasn't been chosen yet, update the outer quadrant
                    elif selected and n_quad_idx != -1:
                        n_quad_idx = -1
                    # If a shape has not been selected, 'go back/cancel' ONE step, so if you chose the wrong
                    # sub-quadrant you don't need to redo everything, just the sub quadrant selection process
                    elif not selected:
                        if sub_quadrant_idx == -1:
                            quadrant_idx = -1
                        else:
                            sub_quadrant_idx = -1

            # If an outer quadrant HAS been selected, draw the outer quadrant
            if quadrant_idx != -1:
                pygame.draw.rect(screen, (50, 50, 50), quadrant_rectangles[quadrant_idx])
                # If a sub-quadrant HAS been selected, draw the sub quadrant as well
                if sub_quadrant_idx != -1:
                    pygame.draw.rect(screen, (100, 50, 50), sub_quadrant_rectangles[quadrant_idx][sub_quadrant_idx])

                    # Get the center of the selected sub-quadrant
                    new_circle_pos = get_sub_quadrant_center(sub_quadrant_rectangles[quadrant_idx][sub_quadrant_idx])
                    # If the center of the sub-quadrant is the same as the center of the original shape position
                    if new_circle_pos == original_circle_pos:
                        # Select shape and reset indices
                        selected = True
                        quadrant_idx = -1
                        sub_quadrant_idx = -1

            # If the new outer quadrant HAS been selected, draw the outer quadrant
            if n_quad_idx != -1:
                pygame.draw.rect(screen, (50, 50, 50), quadrant_rectangles[n_quad_idx])
                # If a new sub-quadrant HAS been selected, draw the sub-quadrant, and reassign shape position to the
                # center of the sub-quadrant
                if n_sub_quad_idx != -1:
                    pygame.draw.rect(screen, (100, 50, 50), sub_quadrant_rectangles[n_quad_idx][n_sub_quad_idx])
                    new_circle_pos = get_sub_quadrant_center(sub_quadrant_rectangles[n_quad_idx][n_sub_quad_idx])
                    pygame.draw.circle(screen, (50, 150, 50), new_circle_pos, radius=50)

            # If an object IS selected, draw a RED circle behind the original circle to make it look like the edge of
            # the object is highlighted to indicate to the user which shape is currently selected
            if selected:
                pygame.draw.circle(screen, (255, 0, 0), original_circle_pos, radius=52)

            # Draw the original circle position (this auto-updates after a new position is assigned)!
            pygame.draw.circle(screen, (50, 50, 150), original_circle_pos, radius=50)

            # Update the screen with all the new shapes and things
            update()

            on_quit(event)  # Check if event = quit to exit program


if __name__ == '__main__':
    running = True
    message = ''
    done = False
    run()
