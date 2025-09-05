import random
import pygame
import os

pygame.mixer.init()

def load_sprites(path="", num_frames=1, nopath=False, imagestring=None):
    """
    Charge un spritesheet horizontal et le découpe en plusieurs frames.

    Args:
        path (str): Chemin vers l'image.
        num_frames (int): Nombre de frames contenues dans le spritesheet.
        nopath (bool): Si True, charge à partir d'un objet `imagestring` (via PIL).
        imagestring (PIL.Image): Image PIL à convertir en surface Pygame.

    Returns:
        list[pygame.Surface]: Liste des frames découpées et recadrées.
    """
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
    """
    Charge une animation depuis un dossier contenant plusieurs fichiers PNG.

    Args:
        folder (str): Chemin vers le dossier contenant les images.

    Returns:
        list[pygame.Surface]: Liste des images triées et chargées.
    """
    sprites = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            sprites.append(img)
    return sprites


def animate(entity, sprites, loop=True, assign_to_image=True, animation_speed=None):
    """
    Anime une entité (doit avoir `current_frame`, `frame_timer` et `image`).

    Args:
        entity: Objet à animer (Player, AnimatedEntity, etc.).
        sprites (list[pygame.Surface]): Frames de l’animation.
        loop (bool): Si True, l’animation boucle, sinon elle s’arrête à la dernière frame.
        assign_to_image (bool): Si True, assigne directement la frame à `entity.image`.
        animation_speed (float|None): Vitesse d’animation (frames par tick). 
                                       Si None, utilise `entity.animation_speed`.
    """
    # Utiliser la vitesse passée en paramètre ou celle de l'entité
    speed = animation_speed if animation_speed is not None else getattr(entity, 'animation_speed', 0.15)

    # Incrément du timer
    if not hasattr(entity, 'frame_timer'):
        entity.frame_timer = 0
    if not hasattr(entity, 'current_frame'):
        entity.current_frame = 0

    entity.frame_timer += speed
    if entity.frame_timer >= 1:
        entity.frame_timer = 0
        entity.current_frame += 1
        if entity.current_frame >= len(sprites):
            if loop:
                entity.current_frame = 0
            else:
                entity.current_frame = len(sprites) - 1

    # Ensure current_frame is within bounds
    if entity.current_frame >= len(sprites):
        entity.current_frame = len(sprites) - 1
    elif entity.current_frame < 0:
        entity.current_frame = 0

    frame = sprites[entity.current_frame]
    if assign_to_image:
        entity.image = frame
    else:
        entity.current_sprite = frame

def pixelate(img, scale=0.5):
    """
    Applique un effet de pixelisation à une image.

    Args:
        img (pygame.Surface): Image originale.
        scale (float): Facteur de réduction (ex: 0.5 = réduit de moitié).

    Returns:
        pygame.Surface: Image pixelisée (agrandie après réduction).
    """
    ver_originale = img.get_size() #récupère la taille de l'image originale
    taille_mini = int(ver_originale[0] * scale), int(ver_originale[1] * scale) # calcule la taille de l'image diminuée avec l'échelle
    ver_mini = pygame.transform.smoothscale(img, taille_mini) #réduit l'image
    ver_pixel = pygame.transform.scale(ver_mini, ver_originale) #réagrandit l'image pixelisée
    return ver_pixel

def scale_sprites(sprites, scale_factor):
    """
    Redimensionne une liste de sprites.

    Args:
        sprites (list[pygame.Surface]): Liste des images.
        scale_factor (float): Facteur d’échelle (ex: 2 = double la taille).

    Returns:
        list[pygame.Surface]: Liste des sprites redimensionnés.
    """
    return [pygame.transform.scale(sprite, (int(sprite.get_width() * scale_factor), int(sprite.get_height() * scale_factor))) for sprite in sprites]


class AnimatedEntity:
    """
    Représente une entité animée simple (utile pour le menu ou le décor).

    Attributes:
        sprites (list[pygame.Surface]): Frames de l’animation.
        pos (tuple): Position (x, y) où afficher l’entité.
        animation_speed (float): Vitesse d’animation.
        loop (bool): Si True, l’animation boucle.
        current_frame (int): Frame actuelle.
        frame_timer (float): Timer pour l’animation.
        image (pygame.Surface): Frame courante affichée.
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

class SoundEffects:
    def __init__(self):
        self.sound_groups = {}
        self.last_played = {}
    
    def load_sound_group(self, group_name, sound_files):
        sounds = []
        for sound_file in sound_files:
            if os.path.exists(sound_file):
                sound = pygame.mixer.Sound(sound_file)
                sounds.append(sound)
        
        self.sound_groups[group_name] = sounds
    
    def play_group(self, group_name, volume=1.0, cooldown=0.5):
        current_time = pygame.time.get_ticks() / 1000.0
        if group_name in self.last_played:
            time_since_last = current_time - self.last_played[group_name]
            if time_since_last < cooldown:
                return False
        sound = random.choice(self.sound_groups[group_name])
        sound.set_volume(volume)
        sound.play()
        self.last_played[group_name] = current_time

    def play_one(self, music_file, volume=0.2):
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def is_playing(self):
        return pygame.mixer.music.get_busy()