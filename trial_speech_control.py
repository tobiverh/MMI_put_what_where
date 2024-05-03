# from speech_listener import MyRecognizer
import speech_recognition as sr
from threading import Thread
import pygame
import time


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
    screen.blit(img, (800, 800))  # Adds the text in position 800, 800
    pygame.display.flip()  # flips the display to show text on screen


def blackout(screen):
    """Fills the pygame display with black
    :param screen: the screen which is repainted"""
    screen.fill((0, 0, 0))  # Fills the screen with black
    pygame.display.flip()  # flips the display to show text on screen


def recognize(ranger, recognizer, audio):
    """Threaded function recognizes passed in audio and stores message in global variable 'message'
    :param ranger: unused iterable argument mandated by Thread module
    :param recognizer: Speech Recognition instance
    :param audio: The audio recorded from an audio file"""
    global message, done
    # message: String where recognized audio is
    # done: bool set to True once the recognition algorithm has finished
    message = recognizer.recognize_google(audio)  # recognize audio using google's free audio recognition model
    done = True  # Note end of recognition


def init_screen(title='Hello'):
    """Initializes the display screen of maximum size to all black with given title text
    :param title: default = 'Hello' message displayed at top of window
    :return screen: the pygame display screen"""
    pygame.init()  # Initialize pygame
    screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])  # Create max size screen
    pygame.display.set_caption(title)  # Set caption
    blackout(screen)  # Make screen black
    return screen


def init_font(font_name='Arial', size=24):
    """Initializes the default font to be used for relaying messages back to the user
    :param font_name: default = 'Arial'
    :param size: default = 24 is the font size to be used"""
    pygame.font.init()  # Initialize font
    text_font = pygame.font.SysFont(font_name, size=size)  # Get system font of font_name and size
    return text_font


def run():
    # recognizer = MyRecognizer()
    recognizer = sr.Recognizer()

    screen = init_screen()
    text_font = init_font()

    timing = is_listening = False
    start = -1
    global done, running

    while running:
        for event in pygame.event.get():
            on_quit(event)  # Check if event = quit to exit program

            # Handle space key being pressed down!
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
                blackout(screen)  # Clear screen
                draw_text(screen, 'Listening', text_font)  # Inform user that they are being recorded
                is_listening = True  # Set is_listening to True
                listening_time = time.time()  # start timer for how long listening lasts
                # recognizer.start_listening()

            # Handle space key being released!
            if event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':
                is_listening = False  # Stop listening
                blackout(screen)  # Clear screen
                draw_text(screen, 'recognizing', text_font)  # Inform user that we are processing
                with (sr.AudioFile("release.wav") as source):  # Take input file as audio source
                    audio = recognizer.record(source)  # convert from audio file to usable
                    # Start 'recognize' function thread
                    recognition_thread = Thread(target=recognize, args=(range(10), recognizer, audio))
                    recognition_thread.daemon = True
                    recognition_thread.start()
                    # message = recognizer.recognize_google(audio)

            if done:  # indicates that the recognition_thread has finished
                blackout(screen)  # clear screen
                draw_text(screen, message, text_font)  # Draw the recognized message
                done = False  # Reset done bool
                timing = True  # start message display timer
                start = time.time()

            if timing:  # If message display timer is started
                if time.time() - start > 2:  # Check if more than 2 seconds
                    timing = False  # Stop timing
                    blackout(screen)  # Clear screen

            if is_listening:  # If recording has started
                modded = (time.time() - listening_time)  # Get time since listening started
                # Emulate progress bar
                if 0.5 > modded >= 0:
                    draw_text(screen, 'Listening', text_font)
                elif 0.5 <= modded < 1:
                    draw_text(screen, 'Listening.', text_font)
                elif 1.5 > modded >= 1:
                    draw_text(screen, 'Listening..', text_font)
                elif 2 > modded >= 1.5:
                    draw_text(screen, 'Listening...', text_font)
                else:
                    draw_text(screen, 'Listening....', text_font)

                if modded > 2.5:  # reset timer every 2.5 seconds
                    listening_time = time.time()
                    blackout(screen)  # clear screen


if __name__ == '__main__':
    message = ''
    done = False
    running = True
    # display_thread = Thread(target=run)
    # display_thread.daemon = True
    # display_thread.start()
    # display_thread.join()
    run()
