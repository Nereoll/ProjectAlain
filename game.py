# game.py
import pygame 
from settings import WIDTH, HEIGHT, FPS, TITLE, WHITE
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

    def new(self):
        """Nouvelle partie"""
        self.run()

    def run(self):
        """Boucle principale"""
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Gestion des événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Mise à jour des objets"""
        self.all_sprites.update()

    def draw(self):
        """Affichage"""
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        for sprite in self.all_sprites:
            pygame.draw.rect(self.screen, (0, 255, 0), sprite.rect, 2)  
        pygame.display.flip()

