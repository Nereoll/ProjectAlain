# enemie.py
import pygame
import math
import time
from settings import WIDTH, HEIGHT, ATH_HEIGHT
from PIL import Image , ImageOps


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, player, screen, pos=(0, 0)):
        super().__init__()
        self.enemy_type = enemy_type
        self.player = player
        self.screen = screen
        self.last_attack_time = 0
        

        # Stats selon le type
        if enemy_type == "pawn":
            self.hp = 1
            self.speed = 2
            self.attack_points = 1
            self.stagger_timer = 0.3
            self.knockback_distance = 50  # Distance du knockback
            self.knockback_speed = 5
            color = (200, 200, 200)
        elif enemy_type == "goblin":
            self.hp = 2
            self.speed = 4
            self.attack_points = 1
            self.stagger_timer = 0.5
            self.knockback_distance = 100  # Distance du knockback
            self.knockback_speed = 5
            color = (0, 200, 0)
        elif enemy_type == "lancier":
            self.hp = 3
            self.speed = 1.5
            self.attack_points = 1
            self.stagger_timer = 0.2
            self.knockback_distance = 10  # Distance du knockback
            self.knockback_speed = 5
            color = (150, 150, 255)
        else:
            raise ValueError("Type d'ennemi inconnu")
        
        self.currentKB = self.knockback_distance
        self.default_speed = self.speed  # Sauvegarde de la vitesse initiale

        self.question_mark = pygame.image.load("assets/images/question_mark.png").convert_alpha()
        self.question_mark = pygame.transform.scale(self.question_mark, (30, 30))  # Redimensionne à 20x20 pixels
        self.question_mark_rect = self.question_mark.get_rect()

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
        self.default_animation_speed = self.animation_speed  # Sauvegarde de la vitesse d'animation initiale (pour le stagger)
        self.frame_timer = 0 #Compte le temps pour passer à la frame suivante.

        # États possibles : "idleR", "idleL", "walkR", "walkL", "attackR", "attackL"
        self.state = "idleR" #État actuel de l'ennemi (idleR, walk, attack).
        self.attacking = False

        self.last_damage_time = 0

        self.faceRorL= "R"

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
        self.handle_state()
        if self.state == "staggered":
            if self.is_knockback:
                dx, dy = self.knockback_direction
                self.rect.x += dx * self.knockback_speed
                self.rect.y += dy * self.knockback_speed
                self.currentKB -= self.knockback_speed
                if self.currentKB <= 0:  # Fin du knockback
                    self.is_knockback = False
                    self.currentKB = self.knockback_distance
            current_time = time.time()  # Obtenir le temps actuel
            # Vérifie si le temps de stagger est écoulé
            if current_time - self.stagger_start_time >= self.stagger_timer:
                # Fin du stagger, réinitialise les vitesses
                if self.faceRorL == "L":
                    self.state = "idleL" 
                else:
                    self.state = "idleR" 
                self.speed = self.default_speed
                self.animation_speed = self.default_animation_speed

                # Vérifie si l'ennemi doit marcher ou rester idle
                player_x, player_y = self.player.rect.center
                enemy_x, enemy_y = self.rect.center
                distance = math.hypot(player_x - enemy_x, player_y - enemy_y)

                if distance > self.stop_distance and self.faceRorL =="L":
                    self.state = "walkL"  # Passe à l'état "walk" si trop loin
                if distance > self.stop_distance and self.faceRorL =="R":
                    self.state = "walkR"  # Passe à l'état "walk" si trop loin

        elif (self.player.state == "attackR" or self.player.state == "attackL") and self.player.rect.colliderect(self.rect):
            current_time = time.time()
            # Vérifie si l'ennemi peut prendre des dégâts (délai entre deux dégâts)
            if current_time - self.last_damage_time >= 0.5:  # Délai de 0.5 seconde
                if self.state != "staggered":
                    self.take_damage(1)
                    self.last_damage_time = current_time  # Met à jour le temps du dernier dégât
        else :
            if self.player.state == "invisible":
                if self.faceRorL == "L":
                    self.state = "idleL"
                else:
                    self.state = "idleR"
                self.question_mark_rect.center = (self.rect.centerx, self.rect.top -20)  # Position au-dessus de l'ennemi
                self.screen.blit(self.question_mark, self.question_mark_rect)
            else :
                # Position du joueur
                player_x, player_y = self.player.rect.center
                enemy_x, enemy_y = self.rect.center
                moving = False
                # Calcul du vecteur direction
                dx, dy = player_x - enemy_x, player_y - enemy_y
                distance = math.hypot(dx, dy)
                # Face direction
                if player_x < enemy_x :
                    self.faceRorL = "L" 
                else : 
                    self.faceRorL = "R"

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
                        if self.faceRorL == "R":
                            self.state = "attackR"
                        else :
                            self.state = "attackL"
                        self.current_frame = 0
                        self.frame_timer = 0
                        self.attack()
                        self.last_attack_time = current_time

                # Si pas en attaque, choisir l'état
                if not self.attacking:
                    if moving and self.faceRorL == "R":
                        self.state = "walkR"
                    elif moving and self.faceRorL == "L":
                        self.state = "walkL"
                    elif self.faceRorL == "R":
                        self.state = "idleR"
                    elif self.faceRorL == "L":
                        self.state = "idleL"

        # Toujours gérer l'animation selon l'état
        self.handle_state()

    def attack(self):
        """Inflige des dégâts au joueur"""
        self.player.take_damage(self.attack_points)

    def take_damage(self, amount):
        """Le joueur ou d'autres entités peuvent attaquer l'ennemi"""

        self.state = "staggered"
        self.speed = 0
        self.animation_speed = 0
        self.stagger_start_time = time.time() # Enregistre le début du stagger

        player_x, player_y = self.player.rect.center
        enemy_x, enemy_y = self.rect.center
        dx, dy = enemy_x - player_x, enemy_y - player_y  # Direction opposée au joueur
        distance = math.hypot(dx, dy)
        if distance != 0:  # Normalisation
            dx, dy = dx / distance, dy / distance
        self.knockback_direction = (dx, dy)
        self.is_knockback = True

        self.hp -= amount
        if self.hp <= 0:
            if self.enemy_type == "pawn":
                self.player.enemy_killed(100)
            if self.enemy_type == "goblin":
                self.player.enemy_killed(150)
            if self.enemy_type == "lancier":
                self.player.enemy_killed(200)
            self.kill()
