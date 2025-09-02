# enemie.py
import pygame
import random
import math
import time

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, player, pos=(0, 0)):
        super().__init__()
        self.enemy_type = enemy_type
        self.player = player
        self.last_attack_time = 0

        # Stats selon le type
        if enemy_type == "squelette":
            self.hp = 60
            self.speed = 2
            self.attack_points = 8
            color = (200, 200, 200)
        elif enemy_type == "goblin":
            self.hp = 40
            self.speed = 3
            self.attack_points = 5
            color = (0, 200, 0)
        elif enemy_type == "lancier":
            self.hp = 80
            self.speed = 1.5
            self.attack_points = 12
            color = (150, 150, 255)
        else:
            raise ValueError("Type d’ennemi inconnu")

        # Sprite A REMPLACER PAR LES VRAIS SPRITES
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        """Déplacement vers le joueur + attaque si proche"""
        # Position du joueur
        player_x, player_y = self.player.rect.center
        enemy_x, enemy_y = self.rect.center

        # Calcul du vecteur direction
        dx, dy = player_x - enemy_x, player_y - enemy_y
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx, dy = dx / distance, dy / distance  # normalisation
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # Vérifie si assez proche pour attaquer
        if distance < 50:  # rayon d’attaque
            current_time = time.time()
            if current_time - self.last_attack_time >= 1:  # attaque toutes les secondes
                self.attack()
                self.last_attack_time = current_time

    def attack(self):
        """Inflige des dégâts au joueur"""
        self.player.take_damage(self.attack_points)

    def take_damage(self, amount):
        """Le joueur ou d’autres entités peuvent attaquer l’ennemi"""
        self.hp -= amount
        if self.hp <= 0:
            self.kill()  # supprime l’ennemi du groupe
