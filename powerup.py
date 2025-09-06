#powerup.py
import pygame
import time
from utilitaire import load_sprites, chemin_relatif, SoundEffects

class PowerUp(pygame.sprite.Sprite):
    """
    Classe représentant un power-up (bonus) que le joueur peut ramasser.

    Un power-up est un objet animé qui apparaît sur la carte et confère un effet
    temporaire ou permanent au joueur lorsqu'il est ramassé.

    Types disponibles :
    - "damageAmp" : Augmente temporairement la force d'attaque du joueur.
    - "invulnerability" : Rend le joueur invulnérable pendant un certain temps.
    - "heart" : Rend un point de vie au joueur.
    """
    def __init__(self, pos, bonus_type, player):
        super().__init__()
        self.image = pygame.Surface((64, 64))  # Taille par défaut
        self.rect = self.image.get_rect(center=pos)
        self.bonus_type = bonus_type
        self.player = player

        self.size = 50

        # Charger les sprites selon le type de bonus
        if self.bonus_type == "damageAmp":
            self.sprites = [
                pygame.transform.scale(frame, (self.size, self.size))
                for frame in load_sprites(chemin_relatif("assets/images/items/damageAmp.png"), 8)
            ]
        elif self.bonus_type == "invulnerability":
            self.sprites = [
                pygame.transform.scale(frame, (self.size, self.size))
                for frame in load_sprites(chemin_relatif("assets/images/items/invulnerability.png"), 8)
            ]
        elif self.bonus_type == "heart":
            self.sprites = [
                pygame.transform.scale(frame, (self.size, self.size))
                for frame in load_sprites(chemin_relatif("assets/images/items/heart.png"), 6)
            ]
        else:
            # Fallback : un carré rouge
            self.sprites = [pygame.Surface((32, 32))]
            self.sprites[0].fill((255, 0, 0))

        self.image = self.sprites[0]  # Première frame de l'animation
        self.current_frame = 0  # Frame actuelle
        self.frame_timer = 0  # Timer pour l'animation
        self.animationSpeed = 0.1

        self.sound = SoundEffects()

    def update(self):
        """Met à jour l'animation du power-up et vérifie la collision avec le joueur."""
        # Anime le sprite
        if self.player.invisibilityDurationLeft < 0.5 :
            self.kill()

        if hasattr(self, "sprites") and self.sprites:
            self.frame_timer += self.animationSpeed
            if self.frame_timer >= 1:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.sprites)
                self.image = self.sprites[self.current_frame]

        # Vérifie la collision avec le joueur
        # =============================
        # EQUILIBRAGE DES POWER UPS ICI
        # =============================
        if self.rect.colliderect(self.player.rect):
            self.sound.play_sound_one(chemin_relatif("assets/sounds/sound_effects/powerup.ogg"), volume=0.3)
            if self.bonus_type == "damageAmp":
                self.player.damageAmpValue = 1
                self.player.damageAmpDuration = 2 + self.player.invisibilityDurationLeft
                self.player.str += self.player.damageAmpValue
                self.player.damageAmpStart = time.time()
            elif self.bonus_type == "invulnerability":
                self.player.iframe_duration = 2 + self.player.invisibilityDurationLeft
                self.player.iframe_start_time = time.time()
                self.player.is_invulnerable = True
            elif self.bonus_type == "heart":
                self.player.hp += 1
            self.kill()  # Supprime le power-up après utilisation