import pygame
import os


class Button:
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None, sound_path=None):
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

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

    def draw(self, screen):
        current_image = self.image
        screen.bilt(current_image, self.rect.center)

