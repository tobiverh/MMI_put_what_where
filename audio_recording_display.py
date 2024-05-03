# from speech_listener import MyRecognizer
import numpy as np
import speech_recognition as sr
from threading import Thread
import pygame
import time
import sched
from audio_recorder2 import AudioRecorder


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
    # pygame.display.update()  # flips the display to show text on screen


def blackout(screen):
    """Fills the pygame display with black
    :param screen: the screen which is repainted"""
    screen.fill((0, 0, 0))  # Fills the screen with black
    pygame.draw.rect(screen, color=(100, 100, 100), rect=(0, screen.get_height() - 30, screen.get_width(), 30))
    # pygame.display.update()  # flips the display


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


def init_recorder(recorder):
    task = sched.scheduler(time.time, time.sleep)  # Start scheduler
    recorder.set_task(task)
    print('Press and hold the "space" key to begin recording')
    print('Release the "space" key to end recording')
    task.enter(0.1, 1, recorder.recorder,  # Enter the given task
               (recorder.is_started, recorder.p_thang, recorder.stream_in, recorder.frame_list))
    task_thread = Thread(target=task.run, args=())
    task_thread.daemon = True
    task_thread.start()
    # task.run()  # Run thread


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
    # recognizer = MyRecognizer()
    recognizer = sr.Recognizer()

    screen = init_screen()
    text_font = init_font()

    timing = is_listening = False
    start = np.inf
    a = True

    original_circle_pos = new_circle_pos = (1600, 250)
    draw_circles(screen, original_circle_pos, new_circle_pos)
    update()
    flip = is_recognizing = False

    display_item_list = []

    global done, running, my_recorder

    while running:
        for event in pygame.event.get():
            on_quit(event)  # Check if event = quit to exit program

            # Handle space key being pressed down!
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
                my_recorder = AudioRecorder('test.wav')
                init_recorder(my_recorder)
                my_recorder.listener.on_press()
                display_item_list.append((blackout, screen))  # Clear screen
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))
                # update()
                is_listening = True  # Set is_listening to True
                listening_time = time.time()  # start timer for how long listening lasts
                # recognizer.start_listening()

            # Handle space key being released!
            if event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':
                my_recorder.listener.on_release()
                is_listening = False  # Stop listening
                is_recognizing = True  # Start recognizing
                display_item_list.append((blackout, screen))  # Clear screen
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))
                display_item_list.append((draw_text, screen, 'recognizing', text_font))  # Inform user that we are processing
                # update()
                # if not a:
                #     with (sr.AudioFile("release.wav") as source):  # Take input file as audio source
                #         audio = recognizer.record(source)  # convert from audio file to usable
                #         # Start 'recognize' function thread
                #         a = True
                #         recognition_thread = Thread(target=recognize, args=(range(10), recognizer, audio))
                #         recognition_thread.daemon = True
                #         recognition_thread.start()
                #         # message = recognizer.recognize_google(audio)
                # else:
                #     with (sr.AudioFile("select.wav") as source):  # Take input file as audio source
                #         audio = recognizer.record(source)  # convert from audio file to usable
                #         # Start 'recognize' function thread
                #         a = False
                #         recognition_thread = Thread(target=recognize, args=(range(10), recognizer, audio))
                #         recognition_thread.daemon = True
                #         recognition_thread.start()
                #         message = recognizer.recognize_google(audio)
                while my_recorder.is_started:
                    time.sleep(0.05)
                with sr.AudioFile('test.wav') as source:
                    audio = recognizer.record(source)
                    recognition_thread = Thread(target=recognize, args=(range(10), recognizer, audio))
                    recognition_thread.daemon = True
                    recognition_thread.start()

            if done:  # indicates that the recognition_thread has finished
                time.sleep(0.1)
                display_item_list.append((blackout, screen))  # Queue clear screen
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))  # Queue circles

                done = False  # Reset done bool
                is_recognizing = False
                timing = True  # start message display timer
                start = time.time()

                if message == 'select':
                    pygame.mouse.set_pos(original_circle_pos)
                    flip = True
                elif message == 'release':
                    flip = False

            if flip:  # Object selected for movement
                new_circle_pos = pygame.mouse.get_pos()  # Find mouse position to reposition circle

                display_item_list.append((blackout, screen))  # Queue screen clearing
                # Queue objects to display
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos, flip))

            if is_recognizing:  # Check if recognizing audio, inform user if so
                display_item_list.append((draw_text, screen, 'recognizing', text_font))

            if flip and is_listening and not is_recognizing:  # Check if recording has started after object selection
                listening_time = listening(display_item_list, listening_time, screen, text_font)
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos, flip))

            if is_listening and not flip and not is_recognizing:  # Recording before object selection
                listening_time = listening(display_item_list, listening_time, screen, text_font)
                display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))

            if timing and not is_listening and not is_recognizing:  # If message display timer is active
                if time.time() - start > 2:  # If longer than allotted time
                    timing = False  # Stop timing
                    display_item_list.append((blackout, screen))  # Clear screen
                    display_item_list.append((draw_circles, screen, original_circle_pos, new_circle_pos))
                else:
                    display_item_list.append((draw_text, screen, message, text_font))  # Queue recognized message

            display_item_list = dequeue(display_item_list)  # If information to be displayed, update display


if __name__ == '__main__':
    message = ''
    done = False
    running = True
    my_recorder = None
    # display_thread = Thread(target=run)
    # display_thread.daemon = True
    # display_thread.start()
    # display_thread.join()
    run()
