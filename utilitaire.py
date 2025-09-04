import random
import pygame
import os

pygame.mixer.init()

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

def pixelate(img, scale=0.5):
    ver_originale = img.get_size() #récupère la taille de l'image originale
    taille_mini = int(ver_originale[0] * scale), int(ver_originale[1] * scale) # calcule la taille de l'image diminuée avec l'échelle
    ver_mini = pygame.transform.smoothscale(img, taille_mini) #réduit l'image
    ver_pixel = pygame.transform.scale(ver_mini, ver_originale) #réagrandit l'image pixelisée
    return ver_pixel


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
                print(f"Loaded: {sound_file}")
            else:
                print(f"Not found: {sound_file}")
        
        self.sound_groups[group_name] = sounds
    
    def play_random(self, group_name, volume=1.0, cooldown=0.5):
        current_time = pygame.time.get_ticks() / 1000.0
        if group_name in self.last_played:
            time_since_last = current_time - self.last_played[group_name]
            if time_since_last < cooldown:
                return False
        sound = random.choice(self.sound_groups[group_name])
        sound.set_volume(volume)
        sound.play()
        self.last_played[group_name] = current_time

    def play_music(self, music_file, volume=0.2):
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def is_playing(self):
        return pygame.mixer.music.get_busy()