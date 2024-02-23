import pygame
import sys
import os
import parameters as par
from panel import Button

pygame.init()

WEIGHT, HEIGHT = par.ROWS * par.TILE_SIZE, par.COLS * par.TILE_SIZE
screen_size = (WEIGHT, HEIGHT + par.LOWER_PANEL)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Menu Tower Defence (JD)')


def load_image(name, color_key=None):
    fullname = os.path.join('data/images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


background = load_image('background.jpg')
button = load_image('')


def main():
    start_button = Button(50, HEIGHT + 42, , True)


def setting():
    pass


def game():
    pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


