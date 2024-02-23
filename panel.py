import pygame


class Button:
    def __init__(self, x, y, image, click, text=None, sound=None):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.single_click = click
        self.text = text
        self.sound = None
        if sound:
            self.sound = pygame.mixer.Sound(sound)

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                if self.sound:
                    self.sound.play()

                if self.single_click:
                    self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, self.rect)

        if self.text:
            text_button = pygame.font.SysFont('Copyright', 50, bold=True)
            text_image = text_button.render(self.text, True, 'black')
            text_rect = text_image.get_rect(center=self.rect.center)
            surface.blit(text_image, (self.x, self.y))

        return action
