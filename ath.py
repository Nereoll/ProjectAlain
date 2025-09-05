import pygame
from settings import WIDTH, ATH_HEIGHT, BLACK, WHITE
from utilitaire import load_sprites, load_sprites_from_folder, animate


class Ath(pygame.sprite.Sprite):
    SCALE_FACTOR = 2
    FONT_PATH = "assets/fonts/GenAR102.TTF"
    FONT_SIZE = 40

    LIFE_PATHS = {
        4: "assets/images/ath/fulllife",
        3: "assets/images/ath/almosthalflife",
        2: "assets/images/ath/halflife",
        1: "assets/images/ath/onelife",
        0: "assets/images/ath/death",
    }

    MANA_PATHS = {
        0: "assets/images/ath/noMana.png",
        1: "assets/images/ath/oneMana.png",
        2: "assets/images/ath/halfMana.png",
        3: "assets/images/ath/almostHalfMana.png",
        4: "assets/images/ath/fullMana.png",
    }

    def __init__(self, player):
        super().__init__()
        self.player = player

        # === Font ===
        self.font_title = pygame.font.Font(self.FONT_PATH, self.FONT_SIZE)

        # === Surface principale ===
        self.image = pygame.Surface((WIDTH, ATH_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))

        # === Sprites ===
        self.life_sprites = {
            hp: self._load_and_scale(load_sprites_from_folder(path))
            for hp, path in self.LIFE_PATHS.items()
        }
        self.mana_sprites = {
            mana: self._load_and_scale(load_sprites(path, 1))
            for mana, path in self.MANA_PATHS.items()
        }

        # === Animation ===
        self.current_sprite = None
        self.current_frame = 0
        self.animation_speed = 0.15
        self.frame_timer = 0

    def _load_and_scale(self, sprites):
        """Charge et redimensionne une liste de sprites."""
        return [
            pygame.transform.scale(
                img,
                (img.get_width() * self.SCALE_FACTOR, img.get_height() * self.SCALE_FACTOR),
            )
            for img in sprites
        ]

    def update(self):
        # === Gestion des HP ===
        player_hp = max(0, min(4, self.player.hp))  # clamp entre 0 et 4
        animate(self, self.life_sprites[player_hp], loop=True, assign_to_image=False)

        # === Gestion du Mana ===
        player_mana = max(0, min(4, self.player.mana))  # clamp entre 0 et 4
        mana_sprite = self.mana_sprites[player_mana][0]

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

        # Mana - à droite
        if mana_sprite:
            rect_mana = mana_sprite.get_rect(midright=(self.rect.width - 40, self.rect.centery))
            self.image.blit(mana_sprite, rect_mana)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
