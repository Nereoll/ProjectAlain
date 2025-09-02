# game.py
import pygame 
import random
import time
from settings import WIDTH, HEIGHT, FPS, TITLE, WHITE
from player import Player
from enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Joueur
        self.player = Player()
        self.all_sprites.add(self.player)

        # Timer de spawn
        self.start_time = time.time()
        self.last_spawn = 0
        self.spawn_delay = 3  # premier ennemi toutes les 3 sec

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
        current_time = time.time() - self.start_time

        # Spawner des ennemis au fil du temps
        if current_time - self.last_spawn >= self.spawn_delay:
            self.spawn_enemy()
            self.last_spawn = current_time
            # Exemple : réduire le délai de spawn petit à petit (jusqu’à un minimum)
            if self.spawn_delay > 0.8:
                self.spawn_delay -= 0.1

        self.all_sprites.update()

    def spawn_enemy(self):
        """Crée un ennemi aléatoire et l'ajoute au jeu"""
        enemy_type = random.choice(["pawn", "goblin", "lancier"])

        # Spawn autour de la zone de jeu (hors écran)
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            pos = (random.randint(0, WIDTH), -20)
        elif side == "bottom":
            pos = (random.randint(0, WIDTH), HEIGHT + 20)
        elif side == "left":
            pos = (-20, random.randint(0, HEIGHT))
        else:  # right
            pos = (WIDTH + 20, random.randint(0, HEIGHT))

        enemy = Enemy(enemy_type, self.player, pos)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def draw(self):
        """Affichage"""
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        # Debug : affichage des hitbox
        for sprite in self.all_sprites:
            pygame.draw.rect(self.screen, (0, 255, 0), sprite.rect, 2)

        pygame.display.flip()

