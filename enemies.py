import pygame
from pygame.math import Vector2
import math
import csv
import parameters as par

ANIMATION_STEPS = 6
ANIMATION_DELAY = 100


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type_enemy, waypoints, sprites_enemies):
        pygame.sprite.Sprite.__init__(self)
        self.res = {}
        with open('data/enemies_stats.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                sl_stats = {row[0]: {'health': row[1], 'speed': row[2], 'money': row[3]}}
                self.res.update(sl_stats)

        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.money = int(self.res.get(type_enemy)['money'])
        self.speed = float(self.res.get(type_enemy)['speed'])
        self.health = float(self.res.get(type_enemy)['health'])
        self.angle = 90
        self.cooldown = 10
        self.last_shot = pygame.time.get_ticks()
        self.type = type_enemy

        self.sprite_sheet = sprites_enemies.get(type_enemy)
        self.frames = self.cut_sheet()
        self.frame_index = 5
        self.update_time = pygame.time.get_ticks()
        self.start_image = self.frames[self.frame_index]
        self.image = pygame.transform.rotate(self.start_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def cut_sheet(self):
        size = self.sprite_sheet.get_height()
        frames = []
        for x in range(ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            frames.append(temp_img)
        return frames

    def update(self, world):
        self.move(world)
        self.rotate()
        self.enemy_alive(world)
        if pygame.time.get_ticks() - self.last_shot > self.cooldown:
            self.animation()

    def animation(self):
        self.image = self.frames[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
                self.last_shot = pygame.time.get_ticks()

    def move(self, world):
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
            world.health -= 1
            world.missing_enemies += 1
            pygame.mixer.Sound('data/sounds/bonk.mp3').play()

        dist = self.movement.length()
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

        self.image = pygame.transform.rotate(self.image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def enemy_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += self.money
            self.kill()
            if self.type == 'wolf':
                pygame.mixer.Sound('data/sounds/death_wolf.mp3').play()
            if self.type == 'bleb':
                pygame.mixer.Sound('data/sounds/death_bleb.mp3').play()
