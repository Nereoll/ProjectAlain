# player.py
import pygame
import time
from settings import WIDTH, HEIGHT, ATH_HEIGHT
from PIL import Image , ImageOps

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Miror srite
        imageLwalk = ImageOps.mirror(Image.open("assets/images/Warrior_Run.png"))
        imageLattack = ImageOps.mirror(Image.open("assets/images/Warrior_Attack2.png"))

        # === Sprites ===
        self.walkRSprites = self.load_sprites("assets/images/Warrior_Run.png", 6) # 6 frames d'animation
        self.walkLSprites = self.load_sprites(imagestring= imageLwalk,num_frames=6, nopath =True)
        self.attackRSprites = self.load_sprites("assets/images/Warrior_Attack2.png", 4)
        self.attackLSprites = self.load_sprites(imagestring= imageLattack, num_frames= 4, nopath =True)

        # Animation courante
        self.current_frame = 0 #Index de la frame actuelle dans la liste de sprites.
        self.image = self.walkLSprites[self.current_frame] #Image actuelle du sprite affichée à l’écran.
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2)) #Rectangle qui définit la position et la taille du sprite.
        self.original_rect = self.rect.copy()

        # Pixel perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        # Cooldown d'attaque
        self.last_attack_time = 0  # Temps de la dernière attaque
        self.attack_cooldown = 1  # Cooldown en secondes

        # Variables de déplacement
        self.speed = 10

        # Animation
        self.animation_speed = 0.15   # vitesse de défilement des frames de mouvement
        self.frame_timer = 0 #Compte le temps pour passer à la frame suivante.

        # États possibles : "idleR", "idleL", "walkR", "walkL", "attackR", "attackL", "invisible"
        self.state = "idleR" #État actuel du joueur (idle, walk, attack, invisible).
        self.attacking = False
        self.invisible = False
        self.invisible_start_time = 0
        self.invisible_duration = 2  # secondes

        # Stats
        self.hp = 4
        self.mana = 0
        
        self.score = 0

        # Direction face
        self.faceRorL = "R"

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

    def handle_keys(self):
            keys = pygame.key.get_pressed()
            moving = False

            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.rect.x -= self.speed
                moving = True
                self.faceRorL = "L"
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += self.speed
                moving = True
                self.faceRorL = "R"
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.rect.y -= self.speed
                moving = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += self.speed
                moving = True

            # Empêche le joueur de sortir de la fenêtre
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.top < ATH_HEIGHT:
                self.rect.top = ATH_HEIGHT
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

            # === Déclenchement invisibilité ===
            if keys[pygame.K_i] and not self.invisible and self.mana == 5:
                self.state = "invisible"
                self.invisible = True
                self.invisible_start_time = time.time()
                self.mana = 0

            # === Déclenchement attaque ===
            if keys[pygame.K_SPACE] and not self.attacking and not self.invisible and self.faceRorL == "L":
                current_time = time.time()
                if current_time - self.last_attack_time >= self.attack_cooldown:  # Vérifie le cooldown
                    self.state = "attackL"
                    self.attacking = True
                    self.current_frame = 0
                    self.frame_timer = 0
                    self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque
            elif keys[pygame.K_SPACE] and not self.attacking and not self.invisible and self.faceRorL == "R":
                current_time = time.time()
                if current_time - self.last_attack_time >= self.attack_cooldown:  # Vérifie le cooldown
                    self.state = "attackR"
                    self.attacking = True
                    self.current_frame = 0
                    self.frame_timer = 0
                    self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque

            if not moving and not self.attacking and not self.invisible and self.faceRorL == "L":
                self.state = "idleL"
            elif not moving and not self.attacking and not self.invisible and self.faceRorL == "R":
                self.state = "idleR"
            elif moving and not self.attacking and not self.invisible and self.faceRorL == "L":
                self.state = "walkL"
            elif moving and not self.attacking and not self.invisible and self.faceRorL == "R":
                self.state = "walkR"


    def update(self):
        """Mets à jour le joueur

        - update est appelée à chaque frame du jeu.
        - Elle traite l'input, met à jour l'état et l'animation.

        - Walk : animation en boucle.
        - Attack : animation non bouclée. Quand l'attaque finit, on revient à idle.
        - Idle : on prend juste la première frame de marche.
        - Invisible : on prend la frame d'invisibilité.
        """
        self.handle_keys()

        # Vérifie si l’invisibilité est terminée
        if self.invisible and (time.time() - self.invisible_start_time >= self.invisible_duration):
            self.invisible = False
            self.state = "idleR"

        # Animation selon l’état
        if self.state == "walkR":
            self.animate(self.walkRSprites, loop=True)
            self.image.set_alpha(255)  # normal
        elif self.state == "walkL" :
            self.animate(self.walkLSprites, loop=True)
            self.image.set_alpha(255)  # normal
        elif self.state == "attackR":

            # Étend temporairement le rectangle autour du joueur
            # A faire/corriger
            #self.rect = self.original_rect.inflate_ip(40, 40)  # Augmente toutes les directions

            self.animate(self.attackRSprites, loop=False)
            self.image.set_alpha(255)  # normal
            # Quand l'animation d'attaque est terminée
            if self.current_frame == len(self.attackRSprites) - 1 and self.frame_timer == 0:
                self.state = "idleR"
                self.attacking = False
                self.current_frame = 0
        elif self.state == "attackL":

            # Étend temporairement le rectangle autour du joueur
            # A faire/corriger
            #self.rect = self.original_rect.inflate_ip(40, 40)  # Augmente toutes les directions

            self.animate(self.attackLSprites, loop=False)
            self.image.set_alpha(255)  # normal
            # Quand l'animation d'attaque est terminée
            if self.current_frame == len(self.attackLSprites) - 1 and self.frame_timer == 0:
                self.state = "idleL"
                self.attacking = False
                self.current_frame = 0
        elif self.state == "invisible":
            self.image.set_alpha(0)  # invisible
        elif self.state == "idleR" :
            self.image = self.walkRSprites[0]
        elif self.state == "idleL" :
            self.image = self.walkLSprites[0]

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            print("Game Over")

    def enemy_killed(self, points):
        self.score += points
        if self.mana < 5:
            self.mana += 1
