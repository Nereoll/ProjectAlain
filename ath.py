import pygame
import os
from settings import WIDTH, ATH_HEIGHT, BLACK

class Ath(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        # === Player ===
        self.player = player
        
        # === Polygone ===
        self.image = pygame.Surface((WIDTH, ATH_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(0, 0))
        
        # === Sprites ===
        self.fullLife = self.load_sprites("assets/images/ath/fulllife")
        self.almostHalfLife = self.load_sprites("assets/images/ath/almosthalflife")
        self.halflife = self.load_sprites("assets/images/ath/halflife")
        self.onelife = self.load_sprites("assets/images/ath/onelife")
        self.death = self.load_sprites("assets/images/ath/death")

        # === Animation ===
        self.current_frame = 0
        self.animation_speed = 0.15   # vitesse de défilement des frames de mouvement
        self.frame_timer = 0 #Compte le temps pour passer à la frame suivante.

        self.current_sprite = None
        
    def load_sprites(self, folder):
        sprites = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                sprites.append(img)
        return sprites
    
    def animate(self, sprites, loop=True):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(sprites):
                if loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(sprites) - 1
            self.current_sprite = sprites[self.current_frame]

    def update(self):
        player_hp = self.player.hp
        
        if player_hp == 4:
            self.animate(self.fullLife)
        elif player_hp == 3:
            self.animate(self.almostHalfLife)
        elif player_hp == 2:
            self.animate(self.halflife)
        elif player_hp == 1:
            self.animate(self.onelife)
        elif player_hp <= 0:
            self.animate(self.death)
            
        self.image.fill(BLACK)
        if self.current_sprite:
            # Centrer le cœur dans la barre ATH
            rect = self.current_sprite.get_rect(center=self.image.get_rect().center - pygame.Vector2(80, 0))
            self.image.blit(self.current_sprite, rect)