import pygame
import os

def load_sprites(path="", num_frames=1, nopath=False, imagestring=None):
    """Charge un spritesheet horizontal découpé en plusieurs frames."""
    if nopath:
        mode = imagestring.mode
        size = imagestring.size
        data = imagestring.tobytes()
        sheet = pygame.image.fromstring(data, size, mode).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
    else:
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()

    frame_width = sheet_width // num_frames
    sprites = []
    for i in range(num_frames):
        frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))

        # Recadrage automatique sur la zone utile (non transparente)
        rect = frame.get_bounding_rect()
        cropped = frame.subsurface(rect).copy()
        sprites.append(cropped)
    return sprites


def load_sprites_from_folder(folder):
    """Charge une animation depuis un dossier contenant plusieurs PNG."""
    sprites = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            sprites.append(img)
    return sprites


def animate(entity, sprites, loop=True, assign_to_image=True):
    """
    Anime un spritesheet générique pour un sprite-like (entité ayant
    current_frame, frame_timer, animation_speed).
    """
    if entity.current_frame >= len(sprites):
        entity.current_frame = 0

    entity.frame_timer += entity.animation_speed
    if entity.frame_timer >= 1:
        entity.frame_timer = 0
        entity.current_frame += 1
        if entity.current_frame >= len(sprites):
            if loop:
                entity.current_frame = 0
            else:
                entity.current_frame = len(sprites) - 1

    frame = sprites[entity.current_frame]
    if assign_to_image:
        entity.image = frame
    else:
        entity.current_sprite = frame


class AnimatedEntity:
    """
    Petit helper pour gérer une animation simple (idle, walk, etc.)
    dans le menu ou le jeu, sans devoir créer un sprite complet.
    """
    def __init__(self, sprites, pos, animation_speed=0.15, loop=True):
        self.sprites = sprites
        self.pos = pos
        self.animation_speed = animation_speed
        self.loop = loop

        # Attributs utilisés par animate()
        self.current_frame = 0
        self.frame_timer = 0
        self.image = sprites[0]

    def update(self):
        """Avance l'animation."""
        animate(self, self.sprites, loop=self.loop)

    def draw(self, screen):
        """Affiche l'entité sur l'écran."""
        screen.blit(self.image, self.pos)
