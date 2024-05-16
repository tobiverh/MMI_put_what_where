import numpy as np
import pygame
import time
import math
from MMI_project.audio_processing.implemented_recorder import Recorder
from MMI_project.audio_processing.implemented_speech_recognizer import  SpeechRecognizer

def on_quit(event):
    """Handles pygame's quit event (e.g. ctrl-q
    :param event: The pygame event from the main loop"""
    if event.type == pygame.QUIT:
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
    screen = pygame.display.set_mode(display_size, pygame.RESIZABLE)  # Create max allowable size screen
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

def draw_circles(screen: pygame.Surface, original_circle_pos, new_circle_pos, flip=False):
    if flip:
        pygame.draw.circle(screen, (0, 0, 255), original_circle_pos, 75)
        pygame.draw.circle(screen, (255, 0, 0), new_circle_pos, 75)
    else:
        pygame.draw.circle(screen, (255, 0, 0), new_circle_pos, 75)
        pygame.draw.circle(screen, (0, 0, 255), original_circle_pos, 75)


def update():
    pygame.display.update()


def display_thinking(process_str, start_time, screen, text_font):
    """
    Takes a `process_str`, describing what the program is doing.\n
    The `process_str` is displayed on the `screen` followed by thinking dots, 
    depending on how much time has passed since the process started (`start_time`).
    The appropriate displaying actions are appended to the `disp_list`.
    \n
    Returns `start_time`.
    """
    thinking_time = (time.time() - start_time)  # Get time since listening started
    n_dots = math.floor(thinking_time / 0.5) % 5
    (blackout, screen)  # clear screen
    (draw_text, screen, process_str + '.' * n_dots, text_font)
    return start_time

def run():
    imp_recorder = Recorder('main_program.wav')                           
    imp_recognizer = SpeechRecognizer(imp_recorder.audio_file_path)

    screen = init_screen()
    text_font = init_font()

    old_item_pos = new_item_pos = (screen.get_width()/2, screen.get_height()/2)
    draw_circles(screen, old_item_pos, new_item_pos)
    update()

    item_is_selected = False
    message = ""

    while True:
        for event in pygame.event.get():
            on_quit(event)  # Check if event = quit to exit program

            # Handle space key being pressed down!
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
                imp_recorder.start_listening()
                listened_since = time.time()  # start timer for how long listening lasts

            # Handle space key being released!
            elif event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':
                imp_recorder.stop_listening()
                imp_recognizer.start_recognizing_audio()
                imp_recognizer.stop_recognizing_audio()

            # Handle recognized speech command
            if imp_recognizer.has_recognized_message():
                message = imp_recognizer.get_message()
                if message == 'select':
                    pygame.mouse.set_pos(old_item_pos)
                    item_is_selected = True
                elif message == 'release':
                    item_is_selected = False

            # Handle movement of selected object
            if item_is_selected:  # Object selected for movement
                new_item_pos = pygame.mouse.get_pos()  # Find mouse position to reposition circle
                draw_circles(screen, old_item_pos, new_item_pos, item_is_selected)

            # Display to user what the program is doing.
            if imp_recorder.is_listening(): 
                display_thinking('Listening', listened_since, screen, text_font)
            else:
                draw_text(screen, message, text_font)
            
            #Reset screen
            blackout(screen) #TODO: This should be specific for text and image, and be integrated into draw_text and draw_circles
            update()

if __name__ == '__main__':
    run()
