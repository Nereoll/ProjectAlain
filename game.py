# game.py
import pygame
import random
import time
from settings import WIDTH, HEIGHT, ATH_HEIGHT, FPS, TITLE
from player import Player
from enemy import Enemy
from ath import Ath
from shadow import Shadow


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Groupes de sprites
        # Groupes de sprites avec gestion de layers
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.Group()

        # Joueur
        self.player = Player()
        self.all_sprites.add(self.player, layer=2)

        # Ath
        self.ath = Ath(self.player)

        # Timer de spawn
        self.start_time = time.time()
        self.last_spawn = 0
        self.spawn_delay = 3  # premier ennemi toutes les 3 sec
        # Score
        self.score = 0

        # Load images once during initialization
        self.shadow1 = pygame.image.load("assets/images/Shadow1.png").convert_alpha()
        self.shadow2 = pygame.image.load("assets/images/Shadow2.png").convert_alpha()
        self.shadow3 = pygame.image.load("assets/images/Shadow3.png").convert_alpha()
        self.background = pygame.image.load("assets/images/Base_Stage.png").convert()
        
        # On garde un seul sprite shadow et on change son image selon le HP
        self.shadow_sprite = Shadow(self.shadow1, (0, 80))
        self.shadow_sprites = pygame.sprite.LayeredUpdates()
        self.shadow_sprites.add(self.shadow_sprite, layer=4)



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

        # Mise à jour explicite de l'ATH
        self.ath.update()

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
        self.all_sprites.add(enemy, layer=1)
        self.enemies.add(enemy)

    def draw(self):
        """Affichage"""

        #DEBUG fps dans la console
        print(int(self.clock.get_fps()))

        self.screen.blit(self.background, (0, 0))

        # Dessiner tous les sprites (ennemis + joueur + ATH)
        self.all_sprites.draw(self.screen)

        # Choisir l'image selon l' HP
        if self.player.hp == 3:
            self.shadow_sprite.image = self.shadow1
        elif self.player.hp == 2:
            self.shadow_sprite.image = self.shadow2
        elif self.player.hp <= 1:
            self.shadow_sprite.image = self.shadow3

        # Dessiner le sprite shadow
        self.shadow_sprites.draw(self.screen)

        self.ath.draw(self.screen)

        pygame.display.flip()
