# enemie.py
import pygame
import random
import math
import time
from settings import WIDTH, HEIGHT
from PIL import Image , ImageOps


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, player, pos=(0, 0)):
        super().__init__()
        self.enemy_type = enemy_type
        self.player = player
        self.last_attack_time = 0
        

        # Stats selon le type
        if enemy_type == "pawn":
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
            raise ValueError("Type d'ennemi inconnu")

        # === Sprites ===
        # Miror srite pawn
        imageLwalkpawn = ImageOps.mirror(Image.open("assets/images/Pawn_Run.png"))
        # Miror srite goblin
        imageLwalkgoblin = ImageOps.mirror(Image.open("assets/images/Goblin_Run.png"))
        # Miror srite lancier
        imageLwalklancier = ImageOps.mirror(Image.open("assets/images/Lancier_Run.png"))

        if self.enemy_type == "pawn":
            self.walkRSprites = self.load_sprites("assets/images/Pawn_Run.png", 6)
            self.attackRSprites = self.load_sprites("assets/images/Pawn_Attack.png", 6)
            self.walkLSprites = self.load_sprites(imagestring= imageLwalkpawn, num_frames=6, nopath =True)
            self.attackLSprites = self.load_sprites("assets/images/Pawn_Attack_reversed.png", 6)
        elif self.enemy_type == "goblin":
            self.walkRSprites = self.load_sprites("assets/images/Goblin_Run.png", 6)
            self.attackRSprites = self.load_sprites("assets/images/Goblin_Attack.png", 6)
            self.walkLSprites = self.load_sprites(imagestring= imageLwalkgoblin, num_frames=6, nopath =True)
            self.attackLSprites = self.load_sprites("assets/images/Goblin_Attack_reversed.png", 6)
        elif self.enemy_type == "lancier":
            self.walkRSprites = self.load_sprites("assets/images/Lancier_Run.png", 6)
            self.attackRSprites = self.load_sprites("assets/images/Lancier_Attack.png", 3)
            self.walkLSprites = self.load_sprites(imagestring= imageLwalklancier, num_frames=6, nopath =True)
            self.attackLSprites = self.load_sprites("assets/images/Lancier_Attack_reversed.png", 3)
        else:
            # fallback : un carré rouge
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))


        # Animation courante
        self.current_frame = 0 #Index de la frame actuelle dans la liste de sprites.
        self.image = self.walkRSprites[self.current_frame] #Image actuelle du sprite affichée à l’écran.
        self.rect = self.image.get_rect(center=pos)

        # Animation
        self.animation_speed = 0.15   # vitesse de défilement des frames de mouvement
        self.frame_timer = 0 #Compte le temps pour passer à la frame suivante.

        # États possibles : "idleR", "idleL", "walkR", "walkL", "attackR", "attackL"
        self.state = "idleR" #État actuel de l'ennemi (idleR, walk, attack).
        self.attacking = False

        """
        # Sprite (à remplacer par les vrais sprites)
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        """
        # Distance minimale entre joueur et ennemi
        self.stop_distance = 35

    def load_sprites(self, path = "", num_frames = 1 , nopath = False , imagestring = None):
        if nopath :
            mode = imagestring.mode
            size = imagestring.size
            data = imagestring.tobytes()

            sheet = pygame.image.fromstring(data, size, mode).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()
        else :
            sheet = pygame.image.load(path).convert_alpha()
            sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // num_frames
        sprites = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))

            # === Recadrage automatique sur la zone utile ===
            # Garder la zone non transparente
            rect = frame.get_bounding_rect()
            cropped = frame.subsurface(rect).copy()
            sprites.append(cropped)
        return sprites

    def animate(self, sprites, loop=True):
        """Anime un spritesheet"""
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(sprites):
                if loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(sprites) - 1  # rester sur la dernière frame
            self.image = sprites[self.current_frame]


    def handle_state(self):
        """Gère l'état actuel de l'ennemi"""
        if self.state == "walkR":
            self.animate(self.walkRSprites, loop=True)
        elif self.state == "walkL":
            self.animate(self.walkLSprites, loop=True)
        elif self.state == "attackR":
            self.animate(self.attackRSprites, loop=False)
            if self.current_frame == len(self.attackRSprites) - 1 and self.frame_timer == 0:
                self.state = "idleR"
                self.attacking = False
                self.current_frame = 0
        elif self.state == "attackL":
            self.animate(self.attackLSprites, loop=False)
            if self.current_frame == len(self.attackLSprites) - 1 and self.frame_timer == 0:
                self.state = "idleL"
                self.attacking = False
                self.current_frame = 0
        elif self.state == "idleR":
            self.image = self.walkRSprites[0]
        elif self.state == "idleL":
            self.image = self.walkLSprites[0]


    def update(self):
        """Déplacement vers le joueur + attaque si proche"""
        # Position du joueur
        player_x, player_y = self.player.rect.center
        enemy_x, enemy_y = self.rect.center
        moving = False

        # Face direction
        if player_x < enemy_x :
            faceRorL = "L" 
        else : 
            faceRorL = "R"


        # Calcul du vecteur direction
        dx, dy = player_x - enemy_x, player_y - enemy_y
        distance = math.hypot(dx, dy)

        # Déplacement seulement si trop loin
        if distance > self.stop_distance:
            dx, dy = dx / distance, dy / distance  # normalisation
            moving=True
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        # Vérifie si assez proche pour attaquer
        if distance <= 50 and not self.attacking:  # rayon d'attaque
            current_time = time.time()
            if current_time - self.last_attack_time >= 1:  # attaque toutes les secondes
                self.attacking = True
                if faceRorL == "R":
                    self.state = "attackR"
                else :
                    self.state = "attackL"
                self.current_frame = 0
                self.frame_timer = 0
                self.attack()
                self.last_attack_time = current_time

        # Si pas en attaque, choisir l'état
        if not self.attacking:
            if moving and faceRorL == "R":
                self.state = "walkR"
            elif moving and faceRorL == "L":
                self.state = "walkL"
            elif faceRorL == "R":
                self.state = "idleR"
            elif faceRorL == "L":
                self.state = "idleL"

        # Toujours gérer l'animation selon l'état
        self.handle_state()

    def attack(self):
        """Inflige des dégâts au joueur"""
        self.player.take_damage(self.attack_points)

    def take_damage(self, amount):
        """Le joueur ou d'autres entités peuvent attaquer l'ennemi"""
        self.hp -= amount
        if self.hp <= 0:
            self.kill()  # supprime l'ennemi du groupe
