# player.py
import pygame
from settings import WIDTH, HEIGHT, RED

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # === Sprites ===
        self.walkSprites = self.load_sprites("assets/images/Warrior_Run.png", 6) # 6 frames d'animation
        self.attackSprites = self.load_sprites("assets/images/Warrior_Attack2.png", 4)


        # Animation courante
        self.current_frame = 0 #Index de la frame actuelle dans la liste de sprites.
        self.image = self.walkSprites[self.current_frame] #Image actuelle du sprite affichée à l’écran.
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2)) #Rectangle qui définit la position et la taille du sprite.

        # Variables de déplacement
        self.speed = 5

        # Animation
        self.animation_speed = 0.15   # vitesse de défilement des frames de mouvement
        self.frame_timer = 0 #Compte le temps pour passer à la frame suivante.

        # États possibles : "idle", "walk", "attack"
        self.state = "idle" #État actuel du joueur (idle, walk, attack).
        self.attacking = False

    def load_sprites(self, path, num_frames):
        """Découpe le spritesheet en images"""
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // num_frames
        sprites = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
            sprites.append(frame)
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
            # === Mouvement ===
            moving = False

            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
                moving = True
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
                moving = True
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
                moving = True
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
                moving = True

            # === Déclenchement attaque ===
            if keys[pygame.K_SPACE] and not self.attacking and not moving:
                self.state = "attack"
                self.attacking = True
                self.current_frame = 0
                self.frame_timer = 0

            if not moving and not self.attacking:
                self.state = "idle"
            elif moving and not self.attacking:
                self.state = "walk"

    def update(self):
        """Mets à jour le joueur

        - update est appelée à chaque frame du jeu.
        - Elle traite l'input, met à jour l'état et l'animation.

        - Walk : animation en boucle.
        - Attack : animation non bouclée. Quand l'attaque finit, on revient à idle.
        - Idle : on prend juste la première frame de marche.
        """
        self.handle_keys()

        # Animation selon l’état
        if self.state == "walk":
            self.animate(self.walkSprites, loop=True)
        elif self.state == "attack":
            self.animate(self.attackSprites, loop=False)
            # Quand on arrive à la fin de l'animation d'attaque (len()-1), retour à l'état idle
            if self.current_frame == len(self.attackSprites) - 1 and self.frame_timer == 0:
                self.state = "idle"
                self.attacking = False
                self.current_frame = 0
        else:
            # Idle = première frame du walk
            self.image = self.walkSprites[0]

