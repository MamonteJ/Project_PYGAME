import pygame
import parameters as siz
import math
import csv

ANIMATION_STEPS = 6
ANIMATION_DELAY = 100


class Tower(pygame.sprite.Sprite):
    def __init__(self, sprites_tower, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.results = []
        with open('data/stats_arrows.csv', encoding='utf-8') as file:
            fieldnames = ['range', 'cooldown', 'damage']
            file_reader = csv.DictReader(file, fieldnames=fieldnames)
            for row in file_reader:
                self.results.append(row)

        self.level = 1
        self.damage = int(self.results[self.level].get('damage'))
        self.cooldown = int(self.results[self.level].get('cooldown'))
        self.renge = int(self.results[self.level].get('range'))
        self.selected = False
        self.target = None
        self.flip = False
        self.last_shot = pygame.time.get_ticks()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = (self.pos_x + 0.5) * siz.TILE_SIZE
        self.y = (self.pos_y + 0.5) * siz.TILE_SIZE

        self.sprite_sheets = sprites_tower
        self.frames = self.cut_sheet(self.sprite_sheets[self.level - 1])
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.renge_area = pygame.Surface((self.renge * 2, self.renge * 2))
        self.renge_area.fill((0, 0, 0))
        self.renge_area.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.renge_area, 'white', (self.renge, self.renge), self.renge)
        self.renge_area.set_alpha(70)
        self.renge_rect = self.renge_area.get_rect()
        self.renge_rect.center = self.rect.center

    def cut_sheet(self, sprite_sheet):
        size = sprite_sheet.get_height()
        frames = []
        for x in range(ANIMATION_STEPS):
            temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
            frames.append(temp_img)
        return frames

    def update(self, enemies_group):
        if self.target:
            self.animation()
        else:
            if pygame.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemies_group)

    def pick_target(self, enemies_group):
        for enemy in enemies_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                distance = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if distance < self.renge:
                    self.target = enemy
                    if enemy.pos[0] > self.x:
                        self.flip = True
                    else:
                        self.flip = False
                    self.target.health -= self.damage
                    pygame.mixer.Sound('data/sounds/strelba1.mp3').play()
                    break

    def animation(self):
        self.image = self.frames[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
                self.last_shot = pygame.time.get_ticks()
                self.target = None

    def upgrade(self):
        pygame.mixer.Sound('data/sounds/sound_level_up.mp3').play()
        self.level += 1
        self.cooldown = int(self.results[self.level].get('cooldown'))
        self.renge = int(self.results[self.level].get('range'))
        self.damage = int(self.results[self.level].get('damage'))
        self.frames = self.cut_sheet(self.sprite_sheets[self.level - 1])
        self.image = self.frames[self.frame_index]

        self.renge_area = pygame.Surface((self.renge * 2, self.renge * 2))
        self.renge_area.fill((0, 0, 0))
        self.renge_area.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.renge_area, 'white', (self.renge, self.renge), self.renge)
        self.renge_area.set_alpha(70)
        self.renge_rect = self.renge_area.get_rect()
        self.renge_rect.center = self.rect.center

    def draw(self, surface):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(image_flip, self.rect)
        if self.selected:
            surface.blit(self.renge_area, self.renge_rect)
