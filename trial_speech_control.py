from speech_listener import MyRecognizer
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


def draw_text(text, font):
    col = (255, 0, 0)
    img = font.render(text, True, col)
    global screen
    screen.blit(img, (800, 800))


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
    while running:
        for event in pygame.event.get():
            on_quit(event)
            if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'space':
                recognizer.start_listening()
            if recognizer.is_listening():
                draw_text('Listening', text_font)
            if event.type == pygame.KEYUP and pygame.key.name(event.key) == 'space':
                recognizer.stop_listening()
                # raise KeyboardInterrupt
                message = recognizer.get_message()
                print(message)


if __name__ == '__main__':
    run()
