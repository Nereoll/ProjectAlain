# player.py
import pygame
from settings import WIDTH, HEIGHT, RED

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = self.load_sprites("assets/images/Warrior_Run.png", 6) # 6 frames d'animation

        self.current_frame = 0

        self.image = self.sprites[self.current_frame]

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        self.speed = 5
        self.animation_speed = 0.15   # vitesse de défilement des frames
        self.frame_timer = 0

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


    def update(self):
            keys = pygame.key.get_pressed()
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


            if moving:
                self.frame_timer += self.animation_speed
                if self.frame_timer >= 1:
                    self.frame_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.sprites)
                    self.image = self.sprites[self.current_frame]
            else:
                # Frame "repos" = la première image
                self.current_frame = 0
                self.image = self.sprites[self.current_frame]