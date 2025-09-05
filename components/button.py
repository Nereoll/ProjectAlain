import pygame
from settings import WHITE

class Button:
    def __init__(self, text, font, x, y, padding=10, color=WHITE):
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.padding = padding
        self.color = color
        self.text_surface = self.font.render(text, True, color)
        self.rect = self.text_surface.get_rect(topleft=(x, y))
        self.box_rect = pygame.Rect(
            self.rect.left - padding,
            self.rect.top - padding,
            self.rect.width + 2 * padding,
            self.rect.height + 2 * padding
        )

    def draw(self, screen):
        screen.blit(self.text_surface, (self.x, self.y))

    def collidepoint(self, point):
        return self.box_rect.collidepoint(point)