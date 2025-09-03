import pygame
import os

def load_sprites(path = "", num_frames = 1 , nopath = False , imagestring = None):
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
    Anime un spritesheet générique pour un sprite.
    """
    # Sécurité : si l'entité change de spritesheet, recaler current_frame
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


