import pygame
from pygame.locals import *
import numpy as np
import math


class Colors:
    def __init__(self):
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.dark_blue = (0, 0, 155)
        self.brown = (155, 75, 0)
        self.cyan = (0, 255, 255)
        self.white = (255, 255, 255)
        self.grey = (189, 189, 189)
        self.light_grey = (244, 244, 244)
        self.dark_grey = (120, 120, 120)


def on_quit(event):
    if event.type == pygame.QUIT:
        global run
        run = False
        pygame.display.quit()
        pygame.quit()
        exit(0)


# def get_pos():
#     pos = pygame.mouse.get_pos()
#     cur_cell = [math.floor(pos[i] / self.cell_size) for i in range(len(pos))]
#     return cur_cell[0], cur_cell[1]


def distance(vec1, vec2):
    a = vec1[0] - vec2[0]
    b = vec1[1] - vec2[1]
    return math.sqrt(a * a + b * b)
    # return np.linalg.norm(vec1 - vec2)


colors = Colors()
pygame.init()
# sweep = Sweep(cell_size, cell_count_x, cell_count_y, num_mines)
# print(pygame.display.get_desktop_sizes()[0])
screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0])
pygame.display.set_caption("Hello")

screen.fill(colors.black)
center = og_center = (1600, 250)
circle_centers = [og_center]
dist = []
radius = 50
pygame.draw.circle(screen, colors.blue, og_center, radius)
pygame.display.flip()

cols = [colors.white, colors.dark_blue, colors.dark_grey, colors.green, colors.brown, colors.cyan,
        colors.grey, colors.light_grey]

run = True
flip = False
while run:
    for event in pygame.event.get():
        on_quit(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
            pos = pygame.mouse.get_pos()
            i, j = pos[0], pos[1]
            for center in circle_centers:
                dist.append(distance(pos, center))
                # print(pos, center)
            if flip:
                flip = False
                circle_centers.append(pygame.mouse.get_pos())
                pygame.draw.circle(screen, cols[len(circle_centers) - 2 % len(cols)], circle_centers[-1], radius)
                pygame.display.flip()
                # print(circle_centers)
                break
            if len(np.where(np.array(dist) < radius)[0]):
                flip = True
        if flip:
            center = pygame.mouse.get_pos()
            screen.fill(colors.black)
            pygame.draw.circle(screen, colors.blue, circle_centers[0], radius)
            if len(circle_centers) > 1:
                for i, circle in enumerate(circle_centers[1:]):
                    pygame.draw.circle(screen, cols[i - 1 % len(cols)], circle, radius)

            pygame.draw.circle(screen, colors.red, center, radius)

            pygame.display.flip()
