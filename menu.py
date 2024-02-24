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


background = load_image('background1.png')
level_background = load_image('levels_background.png')
button = load_image('Default.png')
button_hover = load_image('Hover.png')
button_mini = load_image('Default_mini.png')
button_mini_hover = load_image('Hover_mini.png')
sound_click = 'data/sounds/click_button.mp3'


def main():
    start_button = Button(WEIGHT / 2.5 - 5, HEIGHT / 2, button, True, 'Играть', sound_click, button_hover)
    exit_button = Button(WEIGHT / 2.5 - 5, (HEIGHT / 2) + 150, button, True, 'Выйти', sound_click, button_hover)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # --- Рисуем кнопки ---
        screen.fill(pygame.Color('white'))
        screen.blit(background, (0, 0, WEIGHT, HEIGHT))
        pygame.draw.rect(screen, 'gold', (105, 95, 450, 110), border_radius=60)
        pygame.draw.rect(screen, 'cornsilk', (110, 100, 440, 100), border_radius=60)
        font = pygame.font.SysFont('Copyright', 80, bold=True)
        text = font.render('Tower Defense', True, '#C7A01F')
        text_rect = text.get_rect(center=(WEIGHT / 2 + 10, 150))
        if start_button.draw(screen):
            levels_menu()
        if exit_button.draw(screen):
            running = False
        screen.blit(text, text_rect)
        pygame.display.flip()
    pygame.quit()


def levels_menu():
    lvl = 0
    level_1 = Button(WEIGHT / 2 - 30, 110, button_mini,
                     True, '1', sound_click, button_mini_hover)
    level_2 = Button(WEIGHT / 2 - 30, 210, button_mini,
                     True, '2', sound_click, button_mini_hover)
    level_3 = Button(WEIGHT / 2 - 30, 310, button_mini,
                     True, '3', sound_click, button_mini_hover)
    level_4 = Button(WEIGHT / 2 - 30, 410, button_mini,
                     True, '4', sound_click, button_mini_hover)
    level_5 = Button(WEIGHT / 2 - 30, 510, button_mini,
                     True, '5', sound_click, button_mini_hover)
    exit_button = Button(WEIGHT / 2.5 - 5, HEIGHT - 30, button,
                         True, 'Назад', sound_click, button_hover)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color('#92834E'))
        screen.blit(level_background, (0, 0, WEIGHT, HEIGHT))
        if level_1.draw(screen):
            lvl = 1
        if level_2.draw(screen):
            lvl = 2
        level_3.draw(screen)
        level_4.draw(screen)
        level_5.draw(screen)
        if exit_button.draw(screen):
            main()
        pygame.display.flip()
    pygame.quit()
    return lvl


