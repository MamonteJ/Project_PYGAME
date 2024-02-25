import pygame
import os
import json
import sys

import parameters as par
from enemies import Enemy
from worlds import Level
from towers_arrow import Tower as Arrow
from towers_mags import Tower as Mag
from panel_buttons import Button

pygame.init()
WEIGHT, HEIGHT = par.ROWS * par.TILE_SIZE, par.COLS * par.TILE_SIZE
screen_size = (WEIGHT, HEIGHT + par.LOWER_PANEL)  # размер экрана
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Защита палаток')
FPS = 60


# ======================================================================================================================
# --- Игра -------------------------------------------------------------------------------------------------------------
# ======================================================================================================================
def main(lvl):
    pygame.mixer.music.load('data/sounds/sound_running2.mp3')
    pygame.mixer.music.play(-1)

    class SpriteGroup(pygame.sprite.Group):
        def __init__(self):
            super().__init__()

        def get_event(self, event):
            for sprite in self:
                sprite.get_event(event)

    # --------------КАРТА---------------------------------------------------
    with open(f'data/levels/level_{lvl}.txt') as file:
        world_data = json.load(file)
    Map = load_image(f'level_{lvl}.png')
    world = Level(world_data, Map, lvl)
    world.data_info()
    world.enemies_info()

    # ----------------------------------------------------------------------

    # -------------ВРАГИ----------------------------------------------------
    sprites_enemies = {
        'bleb': load_image('D_Walk2.png'),
        'wolf': load_image('D_Walk.png'),
        'ork': load_image('D_Walk_ork.png')
    }
    enemies_group = SpriteGroup()
    enemy_spawn = pygame.time.get_ticks()
    cooldown_spawn = 600
    # ----------------------------------------------------------------------

    # -----------БАШНИ------------------------------------------------------
    sprites_arrow = []
    sprites_mag = []
    for i in range(1, par.level_tower + 1):
        sprite_arrow = load_image(f"S_Attack{i}.png")
        sprite_mag = load_image(f"M_Attack{i}.png")
        sprites_arrow.append(sprite_arrow)
        sprites_mag.append(sprite_mag)

    tower_image = load_image('S_Preattack.png')
    mag_image = load_image('mag_img.png')
    towers_group_arrow = SpriteGroup()
    towers_group_mag = SpriteGroup()
    selected_tower = None
    selected_tower_m = None

    # --- Функция проверки свободного пространства для установки башни ---
    def spawn_arrow(m_pos):
        m_pos_x = m_pos[0] // par.TILE_SIZE
        m_pos_y = m_pos[1] // par.TILE_SIZE

        m_pos_number = (m_pos_y * par.COLS) + m_pos_x

        if world.tile_map[m_pos_number] == 38:
            space = True
            for a_tower in towers_group_arrow:
                if (m_pos_x, m_pos_y) == (a_tower.pos_x, a_tower.pos_y):
                    space = False
            for m_tower in towers_group_mag:
                if (m_pos_x, m_pos_y) == (m_tower.pos_x, m_tower.pos_y):
                    space = False
            if space:
                pygame.mixer.Sound('data/sounds/stand_tower.mp3').play()
                new_tower_arrow = Arrow(sprites_arrow, m_pos_x, m_pos_y)
                towers_group_arrow.add(new_tower_arrow)
                world.money -= par.price_arrow

    # --- Функция проверки свободного пространства для установки башни ---
    def spawn_mag(m_pos):
        m_pos_x = m_pos[0] // par.TILE_SIZE
        m_pos_y = m_pos[1] // par.TILE_SIZE

        m_pos_number = (m_pos_y * par.COLS) + m_pos_x

        if world.tile_map[m_pos_number] == 38:
            space = True
            for tower_a in towers_group_arrow:
                if (m_pos_x, m_pos_y) == (tower_a.pos_x, tower_a.pos_y):
                    space = False
            for tower_m in towers_group_mag:
                if (m_pos_x, m_pos_y) == (tower_m.pos_x, tower_m.pos_y):
                    space = False
            if space:
                pygame.mixer.Sound('data/sounds/stand_tower.mp3').play()
                new_tower_mag = Mag(sprites_mag, m_pos_x, m_pos_y)
                towers_group_mag.add(new_tower_mag)
                world.money -= par.price_mag

    # --- Функция отображения выбора поставленного лучника ---
    def select_tower(m_pos):
        m_pos_x = m_pos[0] // par.TILE_SIZE
        m_pos_y = m_pos[1] // par.TILE_SIZE
        for tower_a in towers_group_arrow:
            if (m_pos_x, m_pos_y) == (tower_a.pos_x, tower_a.pos_y):
                return tower_a

    # --- Функция отображения выбора поставленного мага ---
    def m_select_tower(m_pos):
        m_pos_x = m_pos[0] // par.TILE_SIZE
        m_pos_y = m_pos[1] // par.TILE_SIZE
        for tower_m in towers_group_mag:
            if (m_pos_x, m_pos_y) == (tower_m.pos_x, tower_m.pos_y):
                return tower_m

    # --- Функция отмены отображения дистанции ---
    def cancel_selected():
        for tower_a in towers_group_arrow:
            tower_a.selected = False
        for tower_m in towers_group_mag:
            tower_m.selected = False

    # -------КНОПКИ----------------------------------------------------------
    start_image = load_image('start-button.png')
    level_image = load_image('lvl_image.png')
    buy_arrow_image = load_image('arrow.png')
    buy_mag_image = load_image('mag.png')
    cancel_image = load_image('cancel_button2.png')
    restart_image = load_image('reset.png')
    repeat_image = load_image('reset2.png')
    panel_image = load_image('panel_Example2.png')
    home_image = load_image('Default_home.png')
    hover_home_image = load_image('Hover_home.png')

    buy_ar_button = Button(50, HEIGHT + 42, buy_arrow_image, True,
                           None, 'data/sounds/sound_arrow.mp3')
    buy_mag_button = Button(150, HEIGHT + 40, buy_mag_image, True,
                            None, 'data/sounds/sound_mag.mp3')
    cancel_button = Button(95, HEIGHT + 100, cancel_image, True,
                           None, 'data/sounds/click_button.mp3')
    level_up_button = Button(102, HEIGHT + 40, level_image, True,
                             None, 'data/sounds/click_button.mp3')
    start_wave_button = Button(300, HEIGHT + 40, start_image, True,
                               None, 'data/sounds/sound_wave.mp3')
    restart_button = Button(350, 380, restart_image, True,
                            None, 'data/sounds/click_button.mp3')
    repeat_button = Button(WEIGHT - 150, HEIGHT + 105, repeat_image,
                           True, None, 'data/sounds/click_button.mp3')
    home_button = Button(WEIGHT - 80, HEIGHT + 105, home_image,
                         True, None, 'data/sounds/click_button.mp3', hover_home_image)
    home_button_game_over = Button(250, 390, home_image,
                                   True, None, 'data/sounds/click_button.mp3', hover_home_image)

    level_start = False
    placing_arrow = False
    placing_mag = False

    param_font = pygame.font.SysFont('Copyright', 60, bold=True)
    text_font = pygame.font.SysFont('Copyright', 20)

    # --- Функция для отображения текста ---
    def draw_text(text, font, col, x, y):
        image = font.render(text, True, col)
        screen.blit(image, (x, y))

    game_over = False
    game_outcome = 0
    placement = 0
    clock = pygame.time.Clock()
    running = True
    # =================================================================================================================
    # ------Запуск игры------------------------------------------------------------------------------------------------
    # =================================================================================================================
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < WEIGHT and mouse_pos[1] < HEIGHT:
                    selected_tower = None
                    selected_tower_m = None
                    cancel_selected()
                    if placing_arrow:
                        if world.money >= par.price_arrow:
                            spawn_arrow(mouse_pos)
                    elif placing_mag:
                        if world.money >= par.price_mag:
                            spawn_mag(mouse_pos)
                    else:
                        selected_tower = select_tower(mouse_pos)
                        selected_tower_m = m_select_tower(mouse_pos)

        screen.fill(pygame.Color("#a6b04f"))
        world.draw(screen)
        enemies_group.draw(screen)
        for a_tower in towers_group_arrow:
            a_tower.draw(screen)
        for m_tower in towers_group_mag:
            m_tower.draw(screen)
        # --- Панель, где расположены кнопки ---
        screen.blit(panel_image, (0, HEIGHT, WEIGHT, HEIGHT + par.LOWER_PANEL))
        # --- Отображаем жизни, деньги и текущую волну врагов ---
        draw_text(str(world.health), param_font, 'crimson', WEIGHT - 90, HEIGHT + 30)
        draw_text('жизни', text_font, 'crimson', WEIGHT - 135, HEIGHT + 30)
        draw_text(str(world.money), param_font, 'gold3', WEIGHT - 90, HEIGHT + 65)
        draw_text('деньги', text_font, 'gold3', WEIGHT - 135, HEIGHT + 65)
        draw_text(str(f'Волна{world.level}'), param_font, 'black', 255, HEIGHT + 115)

        # --- Проверка победы игрока ---
        if game_over is False:
            if world.health <= 0:
                game_over = True
                game_outcome = -1
                pygame.mixer.music.load('data/sounds/defeat.mp3')
                pygame.mixer.music.play()
            if world.level >= par.wave + 1:
                game_over = True
                game_outcome = 1
                world.level = par.wave
                pygame.mixer.music.load('data/sounds/victory.mp3')
                pygame.mixer.music.play()
            # --- Обновление групп объектов ---
            enemies_group.update(world)
            towers_group_arrow.update(enemies_group)
            towers_group_mag.update(enemies_group)
            # --- Выбор уже поставленной башни ---
            if selected_tower:
                selected_tower.selected = True
            if selected_tower_m:
                selected_tower_m.selected = True

        # --- Начало игрового процесса ---
        if game_over is False:
            # --- Запуск волны врагов ---
            if level_start is False:
                if start_wave_button.draw(screen):
                    level_start = True
            else:
                if pygame.time.get_ticks() - enemy_spawn > cooldown_spawn:
                    if world.spawned < len(world.list_enemies):
                        type_enemy = world.list_enemies[world.spawned]
                        enemy = Enemy(type_enemy, world.waypoints, sprites_enemies)
                        enemies_group.add(enemy)
                        world.spawned += 1
                        enemy_spawn = pygame.time.get_ticks()
            # --- Обновление волны врагов ---
            if world.wave_end() is True:
                world.level += 1
                world.money += par.wave_money
                level_start = False
                enemy_spawn = pygame.time.get_ticks()
                world.new_wave()
                world.enemies_info()

            # --- Рисуем кнопки ----------------------------------------------------------------------------------------
            # --- Кнопка покупки лучника ---
            if buy_ar_button.draw(screen):
                placing_arrow = True
                placing_mag = False
                placement = 1

            if placing_arrow is True and placement == 1:
                # --- Отображение досягаемости при установке башни---
                renge_area = pygame.Surface((90 * 2, 90 * 2))
                renge_area.fill((0, 0, 0))
                renge_area.set_colorkey((0, 0, 0))
                pygame.draw.circle(renge_area, 'white', (90, 90), 90)
                renge_area.set_alpha(70)
                renge_rect = renge_area.get_rect()
                cursor_rect = tower_image.get_rect()
                cursor_pos = pygame.mouse.get_pos()
                cursor_rect.center = cursor_pos
                renge_rect.center = cursor_rect.center
                if cursor_pos[1] <= HEIGHT and (cursor_pos[1] > 0):
                    screen.blit(tower_image, cursor_rect)
                    screen.blit(renge_area, renge_rect)
                if cancel_button.draw(screen):
                    placing_arrow = False
                    placing_mag = False
                    placement = 0
            if selected_tower:
                if selected_tower.level < par.level_tower:
                    if level_up_button.draw(screen):
                        if world.money >= par.price_update_ar:
                            selected_tower.upgrade()
                            world.money -= par.price_update_ar
            # --- Кнопка покупки мага ---
            if buy_mag_button.draw(screen):
                placing_mag = True
                placing_arrow = False
                placement = -1
            if placing_mag is True and placement == -1:
                # --- Отображение досягаемости при установке башни ---
                renge_area = pygame.Surface((60 * 2, 60 * 2))
                renge_area.fill((0, 0, 0))
                renge_area.set_colorkey((0, 0, 0))
                pygame.draw.circle(renge_area, 'white', (60, 60), 60)
                renge_area.set_alpha(70)
                renge_rect = renge_area.get_rect()
                cursor_rect = mag_image.get_rect()
                cursor_pos = pygame.mouse.get_pos()
                cursor_rect.center = cursor_pos
                renge_rect.center = cursor_rect.center
                if cursor_pos[1] <= HEIGHT and (cursor_pos[1] > 0):
                    screen.blit(mag_image, cursor_rect)
                    screen.blit(renge_area, renge_rect)
                if cancel_button.draw(screen):
                    placing_arrow = False
                    placing_mag = False
                    placement = 0
            if selected_tower_m:
                if selected_tower_m.level < par.level_tower:
                    if level_up_button.draw(screen):
                        if world.money >= par.price_update_mag:
                            selected_tower_m.upgrade()
                            world.money -= par.price_update_mag
            # --- Кнопка рестарта ---
            if repeat_button.draw(screen):
                game_over = False
                level_start = False
                placing_arrow = False
                placing_mag = False
                selected_tower = None
                selected_tower_m = None
                enemy_spawn = pygame.time.get_ticks()
                world = Level(world_data, Map, lvl)
                world.data_info()
                world.enemies_info()
                enemies_group.empty()
                towers_group_arrow.empty()
                towers_group_mag.empty()
            # --- Кнопка меню ---
            if home_button.draw(screen):
                levels_menu()
            # --- Отображение цен ---
            draw_text(f'цена {par.price_arrow}', text_font, 'gold3', 42, HEIGHT + 110)
            draw_text(f'цена {par.price_mag}', text_font, 'gold3', 150, HEIGHT + 110)
            draw_text(f'лвл+ {par.price_update_ar}', text_font, 'gold3', 42, HEIGHT + 130)
            draw_text(f'лвл+ {par.price_update_mag}', text_font, 'gold3', 150, HEIGHT + 130)
            # ----------------------------------------------------------------------------------------------------------
        else:
            # --- Поражение, рестарт игры ---
            pygame.draw.rect(screen, 'cornsilk', (100, 240, 450, 240), border_radius=60)
            if game_outcome == -1:
                draw_text('ПОРАЖЕНИЕ...(',
                          pygame.font.SysFont('Copyright', 60), 'black', 175, 300)
            elif game_outcome == 1:
                draw_text('ЭТО ПОБЕДА!',
                          pygame.font.SysFont('Copyright', 60), 'black', 180, 300)
            # --- Сброс уровня ---
            if restart_button.draw(screen):
                game_over = False
                level_start = False
                placing_arrow = False
                placing_mag = False
                selected_tower = None
                selected_tower_m = None
                enemy_spawn = pygame.time.get_ticks()
                world = Level(world_data, Map, lvl)
                world.data_info()
                world.enemies_info()
                enemies_group.empty()
                towers_group_arrow.empty()
                towers_group_mag.empty()
                pygame.mixer.music.load('data/sounds/sound_running2.mp3')
                pygame.mixer.music.play(-1)
            if home_button_game_over.draw(screen):
                levels_menu()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


# --- Загрузка изображений ---
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


# ======================================================================================================================
# --- Меню игры --------------------------------------------------------------------------------------------------------
# ======================================================================================================================
# --- Главное меню -----------------------------------------------------------------------------------------------------
def main_menu():
    start_button = Button(WEIGHT / 2.5 - 5, HEIGHT / 2 + 100, button, True,
                          'Играть', sound_click, button_hover)
    exit_button = Button(WEIGHT / 2.5 - 5, HEIGHT + 50, button, True,
                         'Выйти', sound_click, button_hover)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # --- Рисуем кнопки ---
        screen.fill(pygame.Color('white'))
        screen.blit(background, (0, 0, WEIGHT, HEIGHT))
        pygame.draw.rect(screen, 'gold2', (105, 95, 450, 110), border_radius=60)
        pygame.draw.rect(screen, 'cornsilk', (110, 100, 440, 100), border_radius=60)
        font = pygame.font.SysFont('Copyright', 70, bold=True)
        text = font.render('Защита палаток', True, '#C7A01F')
        text_rect = text.get_rect(center=(WEIGHT / 2 + 10, 150))
        if start_button.draw(screen):
            levels_menu()
        if exit_button.draw(screen):
            running = False
        screen.blit(text, text_rect)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


# --- Меню выбора уровня -----------------------------------------------------------------------------------------------
def levels_menu():
    pygame.mixer.music.stop()
    level_1 = Button(WEIGHT / 2 - 30, 110, button_mini,
                     True, '1', sound_click, button_mini_hover)
    level_2 = Button(WEIGHT / 2 - 30, 210, button_mini,
                     True, '2', sound_click, button_mini_hover)
    level_3 = Button(WEIGHT / 2 - 30, 310, button_mini,
                     True, '3', sound_click, button_mini_hover)
    # level_4 = Button(WEIGHT / 2 - 30, 410, button_mini,
    #                  True, '4', sound_click, button_mini_hover)
    # level_5 = Button(WEIGHT / 2 - 30, 510, button_mini,
    #                  True, '5', sound_click, button_mini_hover)
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
            main(lvl)
        if level_2.draw(screen):
            lvl = 2
            main(lvl)
        if level_3.draw(screen):
            lvl = 3
            main(lvl)
        # level_4.draw(screen)
        # level_5.draw(screen)
        if exit_button.draw(screen):
            main_menu()
        pygame.display.flip()
    pygame.quit()
    sys.exit()


# --- Иконка приложения ---
icon = load_image('icon.png')
pygame.display.set_icon(icon)

# -- Запуск ---
if __name__ == '__main__':
    main_menu()
