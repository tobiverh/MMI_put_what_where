import numpy as np
import pygame
import time
from MMI_project.audio_processing.implemented_recorder import Recorder
from MMI_project.audio_processing.implemented_speech_recognizer import  SpeechRecognizer

def on_quit(event):
    """Handles pygame's quit event (e.g. ctrl-q
    :param event: The pygame event from the main loop"""
    if event.type == pygame.QUIT:
        global running
        running = False  # Stop main loop from running (no more updates)
        pygame.display.quit()  # Quit the display
        pygame.quit()  # Quit pygame
        exit(0)  # Exit program


def draw_text(screen, text, font):
    """Draws message on the pygame display
    :param screen: the screen where the text will be displayed
    :param text: the text which is displayed on the screen
    :param font: the font type for the text"""
    col = (255, 0, 0)  # Red color for text
    img = font.render(text, True, col)  # creates a small sub-image with the provided text and color
    screen.blit(img, (screen.get_width()/2, screen.get_height() - 30))  # Adds the text in position 800, 800


def blackout(screen):
    """Fills the pygame display with black
    :param screen: the screen which is repainted"""
    screen.fill((0, 0, 0))  # Fills the screen with black
    pygame.draw.rect(screen, color=(100, 100, 100), rect=(0, screen.get_height() - 30, screen.get_width(), 30))

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


def init_font(font_name='Arial', size=24):
    """Initializes the default font to be used for relaying messages back to the user
    :param font_name: default = 'Arial'
    :param size: default = 24 is the font size to be used"""
    pygame.font.init()  # Initialize font
    text_font = pygame.font.SysFont(font_name, size=size)  # Get system font of font_name and size
    return text_font

def draw_circles(screen, original_circle_pos, new_circle_pos, flip=False):
    if flip:
        pygame.draw.circle(screen, (0, 0, 255), original_circle_pos, 75)
        pygame.draw.circle(screen, (255, 0, 0), new_circle_pos, 75)
    else:
        pygame.draw.circle(screen, (255, 0, 0), new_circle_pos, 75)
        pygame.draw.circle(screen, (0, 0, 255), original_circle_pos, 75)


def update():
    pygame.display.update()


def listening(disp_list, listening_time, screen, text_font):
    modded = (time.time() - listening_time)  # Get time since listening started
    # Emulate progress bar
    if 0.5 > modded >= 0:
        disp_list.append((draw_text, screen, 'Listening', text_font))
    elif 0.5 <= modded < 1:
        disp_list.append((draw_text, screen, 'Listening.', text_font))
    elif 1.5 > modded >= 1:
        disp_list.append((draw_text, screen, 'Listening..', text_font))
    elif 2 > modded >= 1.5:
        disp_list.append((draw_text, screen, 'Listening...', text_font))
    else:
        disp_list.append((draw_text, screen, 'Listening....', text_font))

    if modded > 2.5:  # reset timer every 2.5 seconds
        listening_time = time.time()
        disp_list.append((blackout, screen))  # clear screen
        disp_list.append((draw_text, screen, 'Listening', text_font))

    return listening_time


def dequeue(disp_list):
    if disp_list:
        for i in range(len(disp_list)):
            try:
                func, *args = disp_list[i]
            except TypeError:
                continue
            func(*args)

        disp_list = []
        update()

    return disp_list


def run():
    imp_recorder = Recorder('main_program.wav')
    imp_recognizer = SpeechRecognizer(imp_recorder.audio_file_path)

    screen = init_screen()
    text_font = init_font()

    timing = False
    start = np.inf

    original_circle_pos = new_circle_pos = (1600, 250)
    draw_circles(screen, original_circle_pos, new_circle_pos)
    update()
    item_is_selected = False

    display_item_list = []

    global running

    while running:
        for event in pygame.event.get():
            on_quit(event)  # Check if event = quit to exit program

            # Handle space key being pressed down!
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
                imp_recorder.start_listening()
                display_item_list.append((blackout, screen))  # Clear screen
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))
                recording_time = time.time()  # start timer for how long listening lasts

            # Handle space key being released!
            if event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':
                imp_recorder.stop_listening()
                
                display_item_list.append((blackout, screen))  # Clear screen
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))
                display_item_list.append((draw_text, screen, 'recognizing', text_font))  # Inform user that we are processing
                
                imp_recognizer.start_recognizing_audio()

            if imp_recognizer.has_recognized_message():
                time.sleep(0.1)
                display_item_list.append((blackout, screen))  # Queue clear screen
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))  # Queue circles

                # start message display timer
                timing = True  
                start = time.time()

                if imp_recognizer.get_message() == 'select':
                    pygame.mouse.set_pos(original_circle_pos)
                    item_is_selected = True
                elif imp_recognizer.get_message() == 'release':
                    item_is_selected = False

            if item_is_selected:  # Object selected for movement
                new_circle_pos = pygame.mouse.get_pos()  # Find mouse position to reposition circle

                display_item_list.append((blackout, screen))  # Queue screen clearing
                # Queue objects to display
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos, item_is_selected))

            # Check if recognizing audio, inform user if so
            if imp_recognizer.is_recognizing():
                display_item_list.append((draw_text, screen, 'recognizing', text_font))

            # Check if recording has started after object selection
            if imp_recorder.is_listening() and not imp_recognizer.is_recognizing(): 
                recording_time = listening(display_item_list, recording_time, screen, text_font)
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos, item_is_selected))

            # If message display timer is active
            if timing and not imp_recorder.is_listening() and not imp_recognizer.is_recognizing():
                if time.time() - start > 2:  # If longer than allotted time
                    timing = False  # Stop timing
                    display_item_list.append((blackout, screen))  # Clear screen
                    display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))
                else:
                    display_item_list.append((draw_text, screen, imp_recognizer.get_message(), text_font))  # Queue recognized message

            display_item_list = dequeue(display_item_list)  # If information to be displayed, update display


if __name__ == '__main__':
    running = True
    run()
