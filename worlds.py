import csv
import random
import parameters as par


# Класс карты уровня ---
class Level:
    def __init__(self, data, map_image, lvl):
        self.res = []
        with open(f'data/csv_files/spawner{lvl}.csv', encoding='utf-8') as file:
            fieldnames = ['bleb', 'wolf', 'ork']
            file_reader = csv.DictReader(file, fieldnames=fieldnames)
            for row in file_reader:
                self.res.append(row)

        self.level = 1
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.list_enemies = []
        self.spawned = 0
        self.killed_enemies = 0
        self.missing_enemies = 0
        self.health = par.health
        self.money = par.money

    # --- Информация об карте уровня из txt файла ---
    def data_info(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "level":
                self.tile_map = layer["data"]
            if layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoints_date = obj["polyline"]
                    self.waypoints_info(waypoints_date)

    # --- Информация о пути перемещения врагов ---
    def waypoints_info(self, date):
        for pos in date:
            pos_x = pos.get("x")
            pos_y = pos.get("y")
            self.waypoints.append((pos_x, pos_y))

    # --- Информация о врагах на уровне --
    def enemies_info(self):
        enemies = self.res[self.level]
        for enemy_type in enemies:
            enemies_spawn = enemies[enemy_type]
            for enemy in range(int(enemies_spawn)):
                self.list_enemies.append(enemy_type)
        random.shuffle(self.list_enemies)

    # --- Завершение волны ---
    def wave_end(self):
        if (self.killed_enemies + self.missing_enemies) == len(self.list_enemies):
            return True

    # --- Новая волна ---
    def new_wave(self):
        self.list_enemies = []
        self.spawned = 0
        self.killed_enemies = 0
        self.missing_enemies = 0

    # --- Отрисовка изображения уровня ---
    def draw(self, surface):
        surface.blit(self.image, (0, 0))
