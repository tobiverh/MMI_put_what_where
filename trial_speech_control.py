import threading

import speech_recognition
# from speech_listener import MyRecognizer
import speech_recognition as sr
# from MyListener import MyListener
from threading import Thread
import pygame
from pygame.locals import *
import time


def on_quit(event):
    if event.type == pygame.QUIT:
        global running
        running = False
        pygame.display.quit()
        pygame.quit()
        exit(0)


def draw_text(screen, text, font):
    col = (255, 0, 0)
    img = font.render(text, True, col)
    screen.blit(img, (800, 800))
    pygame.display.flip()


def blackout(screen):
    screen.fill((0, 0, 0))
    pygame.display.flip()


def recognize(ranger, recognizer, audio, screen, text_font):
    global message, recognizing, done
    recognizing = True
    done = False
    message = recognizer.recognize_google(audio)
    # draw_text(screen, message, text_font)
    recognizing = False
    done = True
    # return message


def run():
    # recognizer = MyRecognizer()
    recognizer = sr.Recognizer()

    pygame.init()
    screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
    pygame.display.set_caption("Hello")

    pygame.font.init()
    text_font = pygame.font.SysFont('Arial', size=24)

    screen.fill((0, 0, 0))
    pygame.display.flip()
    running = True
    timing = False
    start = -1
    c = 0
    is_listening = False
    global done
    while running:
        for event in pygame.event.get():
            on_quit(event)
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
                blackout(screen)
                draw_text(screen, 'Listening', text_font)
                is_listening = True
                listening_time = time.time()
                # recognizer.start_listening()

            if event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':
                is_listening = False
                with sr.AudioFile("release.wav") as source:
                    audio = recognizer.record(source)
                    display_thread = Thread(target=recognize, args=(range(10), recognizer, audio, screen, text_font))
                    display_thread.daemon = True
                    display_thread.start()
                    # message = recognizer.recognize_google(audio)

                # recognizer.stop_listening()
                blackout(screen)
                # message = recognizer.get_message()

            if timing:
                if time.time() - start > 2:
                    timing = False
                    blackout(screen)

            if recognizing and not done:
                draw_text(screen, 'recognizing', text_font)

            if done and not recognizing:
                blackout(screen)
                draw_text(screen, message, text_font)
                done = False
                timing = True
                start = time.time()

            if is_listening:
                modded = (time.time() - listening_time)
                if 0.5 > modded >= 0:
                    draw_text(screen, 'Listening', text_font)
                elif 1 > modded >= 0.5:
                    draw_text(screen, 'Listening.', text_font)
                elif 1.5 > modded >= 1:
                    draw_text(screen, 'Listening..', text_font)
                elif 2 > modded >= 1.5:
                    draw_text(screen, 'Listening...', text_font)
                else:
                    draw_text(screen, 'Listening....', text_font)
                # c += 1

                if modded > 2.5:
                    listening_time = time.time()
                    blackout(screen)

                # pygame.display.flip()


if __name__ == '__main__':
    message = ''
    recognizing = False
    done = False
    # display_thread = Thread(target=run)
    # display_thread.daemon = True
    # display_thread.start()
    # display_thread.join()
    run()
