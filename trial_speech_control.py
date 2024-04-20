import threading

from speech_listener import MyRecognizer
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


def run():
    recognizer = MyRecognizer()

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
    while running:
        for event in pygame.event.get():
            on_quit(event)
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
                blackout(screen)
                draw_text(screen, 'Listening', text_font)
                recognizer.start_listening()
            if event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':
                recognizer.stop_listening()
                blackout(screen)
                message = recognizer.get_message()
                draw_text(screen, message, text_font)
                timing = True
                start = time.time()
            if timing:
                if time.time() - start > 2:
                    timing = False
                    blackout(screen)


            if recognizer.is_listening():
                modded = c % 5
                if modded == 0:
                    draw_text(screen, 'Listening', text_font)
                elif modded == 1:
                    draw_text(screen, 'Listening.', text_font)
                elif modded == 2:
                    draw_text(screen, 'Listening..', text_font)
                elif modded == 3:
                    draw_text(screen, 'Listening...', text_font)
                else:
                    draw_text(screen, 'Listening....', text_font)
                c += 1

                pygame.display.flip()


if __name__ == '__main__':
    display_thread = Thread(target=run)
    display_thread.daemon = True
    display_thread.start()
    display_thread.join()
    # run()
