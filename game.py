# game.py
import pygame
import random
import time
from settings import WIDTH, HEIGHT, ATH_HEIGHT, FPS, TITLE, WHITE
from player import Player
from enemy import Enemy
from ath import Ath


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

        # Ath
        self.ath = Ath(self.player)
        self.all_sprites.add(self.ath)

        # Timer de spawn
        self.start_time = time.time()
        self.last_spawn = 0
        self.spawn_delay = 3  # premier ennemi toutes les 3 sec
        
        # Score
        self.score = 0

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
            if self.spawn_delay > 0.8:
                self.spawn_delay -= 0.1
        oldLength = self.enemies.__len__()
        self.all_sprites.update()
        if oldLength > self.enemies.__len__():
            self.score += 100

    def spawn_enemy(self):
        """Crée un ennemi aléatoire et l'ajoute au jeu"""
        enemy_type = random.choice(["pawn", "goblin", "lancier"])

        # Spawn autour de la zone de jeu (hors écran)
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            pos = (random.randint(0, WIDTH), ATH_HEIGHT)
        elif side == "bottom":
            pos = (random.randint(0, WIDTH), HEIGHT + 20)
        elif side == "left":
            pos = (-20, random.randint(ATH_HEIGHT, HEIGHT))
        else:  # right
            pos = (WIDTH + 20, random.randint(ATH_HEIGHT, HEIGHT))

        enemy = Enemy(enemy_type, self.player, pos)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def draw(self):
        """Affichage"""
        shadow1 = pygame.image.load("assets/images/Shadow1.png").convert_alpha()
        shadow2 = pygame.image.load("assets/images/Shadow2.png").convert_alpha()
        shadow3 = pygame.image.load("assets/images/Shadow3.png").convert_alpha()

        #DEBUG fps dans la console
        #print(int(self.clock.get_fps()))

        background = pygame.image.load("assets/images/Base_Stage.png").convert()
        self.screen.blit(background, (0, 0))

        self.all_sprites.draw(self.screen)

        if self.player.hp == 3:
            self.screen.blit(shadow1, (0, 80))
        elif self.player.hp == 2:
            self.screen.blit(shadow2, (0, 80))
        elif self.player.hp <= 1:
            self.screen.blit(shadow3, (0, 80))


        pygame.display.flip()
