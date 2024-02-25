import pygame


# --- Класс кнопок ---
class Button:
    def __init__(self, x, y, image, click, text=None, sound=None, image_hover=None):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.single_click = click
        self.text = text
        self.sound = None
        self.image_hover = None
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        if image_hover:
            self.image_hover = image_hover
        self.hovered = False

    # --- Отрисовка кнопок ---
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.image_hover:
                self.hovered = self.rect.collidepoint(pos)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                action = True
                if self.sound:
                    self.sound.play()

                if self.single_click:
                    self.clicked = True
        else:
            self.hovered = False

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        current_image = self.image
        if self.hovered:
            current_image = self.image_hover
        surface.blit(current_image, self.rect)

        if self.text:
            text_button = pygame.font.SysFont('Copyright', 50, bold=True)
            text_image = text_button.render(self.text, True, 'black')
            text_rect = text_image.get_rect(center=self.rect.center)
            surface.blit(text_image, text_rect)

        return action
