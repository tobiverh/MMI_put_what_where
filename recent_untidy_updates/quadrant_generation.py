import pygame
import time
import numpy as np


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


def init_quadrant_matrix(screen):
    return [(0, 0, screen.get_width()/2, screen.get_height()/2),  # left, up
            (screen.get_width() / 2, 0, screen.get_width() / 2, screen.get_height() / 2),  # right, up
            (0, screen.get_height()/2, screen.get_width()/2, screen.get_height()/2),  # left, down
            (screen.get_width()/2, screen.get_height()/2, screen.get_width()/2, screen.get_height()/2)
           ]  # 0: left, up, 1: right, up, 2: left, down, 3: right, down


def init_sub_quadrant_matrix(quadrants):
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


def update():
    pygame.display.update()


def run():

    screen = init_screen()
    text_font = init_font()

    start = np.inf

    # Return values are ints 0, 1, 2, 3 corresponding to top - left, top - right, bottom - left and bottom - right respectively
    quadrant_rectangles = init_quadrant_matrix(screen=screen)
    sub_quadrant_rectangles = init_sub_quadrant_matrix(quadrants=quadrant_rectangles)

    # update()
    # time.sleep(5)
    # return
    # print(positions[right][up])
    # return

    original_circle_pos = new_circle_pos = (1600, 250)
    # draw_circles(screen, original_circle_pos, new_circle_pos)
    # update()
    flip = is_recognizing = False

    display_item_list = []

    global running

    while running:
        for event in pygame.event.get():
            for quad_idx in range(len(quadrant_rectangles)):
                for sub_quad_idx in range(len(sub_quadrant_rectangles)):
                    blackout(screen)
                    pygame.draw.rect(screen, (50, 50, 50), quadrant_rectangles[quad_idx])
                    pygame.draw.rect(screen, (100, 50, 50), sub_quadrant_rectangles[quad_idx][sub_quad_idx])
                    update()
                    time.sleep(2)

            return
            # on_quit(event)  # Check if event = quit to exit program


if __name__ == '__main__':
    running = True
    run()