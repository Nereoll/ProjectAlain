import pygame
import os
from settings import WIDTH, ATH_HEIGHT, BLACK, WHITE

class Ath(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        
        # === Font ===
        self.font_title = pygame.font.SysFont("gentiumalt", 36)

        # === Player ===
        self.player = player
        
        # === Surface principale ===
        self.image = pygame.Surface((WIDTH, ATH_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))

        # === Sprites ===
        # Life
        self.fullLife = self.load_sprites("assets/images/ath/fulllife")
        self.almostHalfLife = self.load_sprites("assets/images/ath/almosthalflife")
        self.halflife = self.load_sprites("assets/images/ath/halflife")
        self.onelife = self.load_sprites("assets/images/ath/onelife")
        self.death = self.load_sprites("assets/images/ath/death")
        
        # Mana (une seule image par état)
        self.noMana = self.load_sprites_from_one_image("assets/images/ath/noMana.png", 1)
        self.oneMana = self.load_sprites_from_one_image("assets/images/ath/oneMana.png", 1)
        self.halfMana = self.load_sprites_from_one_image("assets/images/ath/halfMana.png", 1)
        self.almostHalfMana = self.load_sprites_from_one_image("assets/images/ath/almostHalfMana.png", 1)
        self.fullMana = self.load_sprites_from_one_image("assets/images/ath/fullMana.png", 1)

        # augmenter les tailles des spirites
        self.fullLife = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.fullLife]
        self.almostHalfLife = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.almostHalfLife]
        self.halflife = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.halflife]
        self.onelife = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.onelife]
        self.death = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.death]
        #/////
        self.noMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.noMana]
        self.oneMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.oneMana]
        self.halfMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.halfMana]
        self.almostHalfMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.almostHalfMana]
        self.fullMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.fullMana]

        # === Animation ===
        self.current_frame = 0
        self.animation_speed = 0.15
        self.frame_timer = 0
        self.current_sprite = None  # frame courante

    def load_sprites(self, folder):
        """Charge une animation depuis un dossier contenant plusieurs PNG."""
        sprites = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                sprites.append(img)
        return sprites

    def load_sprites_from_one_image(self, path, num_frames):
        """Découpe une spritesheet simple (ou juste un PNG unique)."""
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // num_frames
        sprites = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
            rect = frame.get_bounding_rect()
            cropped = frame.subsurface(rect).copy()
            sprites.append(cropped)
        return sprites
    
    def animate(self, sprites, loop=True):
        """Fait défiler une animation."""
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(sprites):
                if loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(sprites) - 1
            self.current_sprite = sprites[self.current_frame]

    def update(self):
        # === Gestion des HP ===
        player_hp = self.player.hp
        if player_hp == 4:
            self.animate(self.fullLife)
        elif player_hp == 3:
            self.animate(self.almostHalfLife)
        elif player_hp == 2:
            self.animate(self.halflife)
        elif player_hp == 1:
            self.animate(self.onelife)
        elif player_hp <= 0:
            self.animate(self.death, loop=False)
        
        # === Gestion du Mana ===
        player_mana = self.player.mana 
        if player_mana == 0:
            mana_sprite = self.noMana[0]
        elif player_mana == 1:
            mana_sprite = self.oneMana[0]
        elif player_mana == 2:
            mana_sprite = self.halfMana[0]
        elif player_mana == 3:
            mana_sprite = self.almostHalfMana[0]
        else:
            mana_sprite = self.fullMana[0]

        

        # === Redessiner l'ATH ===
        self.image.fill(BLACK)

        # HP - à gauche
        if self.current_sprite:
            rect_hp = self.current_sprite.get_rect(midleft=(40, self.rect.centery))
            self.image.blit(self.current_sprite, rect_hp)
            
        # Score - au milieu
        score_text = self.font_title.render(f"Score: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.rect.width // 2, 40))
        self.image.blit(score_text, score_rect)

        # Mana → à droite
        if mana_sprite:
            rect_mana = mana_sprite.get_rect(midright=(self.rect.width - 40, self.rect.centery))
            self.image.blit(mana_sprite, rect_mana)
