import pygame
from settings import TITLE, BLACK, HEIGHT
from utilitaire import pixelate


class Credits:
    FONT_TITLE = ("assets/fonts/Chomsky.otf", 52)
    FONT_SUBTITLE = ("assets/fonts/Chomsky.otf", 34)
    FONT_TEXT = ("assets/fonts/GenAR102.TTF", 18)

    BACK_IMG = "assets/images/ressources/Pressed_01.png"
    BG_IMG = "assets/images/background/Credit_Page.png"

    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption(TITLE)

        # Fonts
        self.font_title = pygame.font.Font(*self.FONT_TITLE)
        self.font_subtitle = pygame.font.Font(*self.FONT_SUBTITLE)
        self.font_text = pygame.font.Font(*self.FONT_TEXT)

        # Back button
        self.back = pygame.image.load(self.BACK_IMG)

        # State
        self.running = True
        self.retour = False
        self.pixel_ratio = 0.8

    def run(self):
        while self.running:
            self._handle_events()
            self._draw()
            pygame.display.flip()

    def _handle_events(self):
        """Gestion des événements pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.retour, self.running = True, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back.get_rect(topleft=(10, 10)).collidepoint(pygame.mouse.get_pos()):
                    self.retour, self.running = True, False

    def _draw(self):
        """Dessine l’écran des crédits."""
        # Fond
        background = pygame.image.load(self.BG_IMG).convert_alpha()
        self.screen.blit(background, (0, 0))

        # Bouton retour
        self.screen.blit(self.back, (10, 10))

        # Titre
        self._draw_title("Crédits")

        # Sections
        self._draw_section(
            "Assets",
            ["Tiny Sword Pack by Pixel Frog on itch.io"],
            pos=(240, 180),
            align="left"
        )

        self._draw_section(
            "Sounds",
            [
                "Medieval Battle by SoundBible.com",
                "Sword Clash by SoundBible.com",
                "Magic Spell by SoundBible.com",
                "Monster Roar by SoundBible.com",
                "Footsteps on Grass by SoundBible.com",
                "Player Hurt by SoundBible.com",
                "Enemy Hurt by SoundBible.com",
                "Player Death by SoundBible.com",
                "Enemy Death by SoundBible.com",
                "Door Open by SoundBible.com"
            ],
            pos=(self.screen.get_width() - 300, 280),
            align="right"
        )

        self._draw_section(
            "Développeurs",
            [
                "Bastien ALLEGRE / Hugo BARBIERI",
                "Emeric DIEUDONNE / Vianney MIQUEL",
                "Cyrian TORREJON"
            ],
            pos=(220, HEIGHT - 420),
            align="left"
        )

    def _draw_title(self, text: str):
        """Affiche le titre principal centré en haut."""
        title_text = self.font_title.render(text, True, BLACK)
        title_rect = title_text.get_rect(midtop=(self.screen.get_width() // 2, 50))
        self.screen.blit(pixelate(title_text, self.pixel_ratio), title_rect)

    def _draw_section(self, subtitle: str, content: list[str], pos: tuple[int, int], align: str = "left"):
        """Affiche une section avec un sous-titre et des lignes de texte."""
        # Sous-titre
        subtitle_surf = self.font_subtitle.render(subtitle, True, BLACK)
        subtitle_rect = subtitle_surf.get_rect(**{f"top{align}": pos})
        self.screen.blit(pixelate(subtitle_surf, self.pixel_ratio), subtitle_rect)

        # Contenu
        for i, line in enumerate(content):
            line_text = self.font_text.render(line, True, BLACK)
            x, y = pos
            y_offset = y + 40 + i * 30
            if align == "left":
                self.screen.blit(line_text, (x - 20, y_offset))
            elif align == "right":
                self.screen.blit(line_text, (self.screen.get_width() - 500, y_offset))
