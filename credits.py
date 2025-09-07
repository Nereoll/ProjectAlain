import pygame
from settings import BLACK, HEIGHT
from utilitaire import pixelate, chemin_relatif


class Credits:
    """
    Classe représentant l'écran des crédits du jeu.

    Affiche :
        - Un fond personnalisé
        - Un bouton retour (Back)
        - Différentes sections : Assets, Sons, Développeurs

    Attributs :
        screen (pygame.Surface): Surface principale où tout est dessiné.
        font_title (pygame.font.Font): Police du titre.
        font_subtitle (pygame.font.Font): Police des sous-titres.
        font_text (pygame.font.Font): Police du texte classique.
        back (pygame.Surface): Image du bouton retour.
        running (bool): Indique si l'écran est actif.
        retour (bool): Indique si on doit retourner au menu précédent.
        pixel_ratio (float): Facteur de pixelisation appliqué aux textes.
    """
    FONT_TITLE = (chemin_relatif("assets/fonts/Chomsky.otf"), 52)
    FONT_SUBTITLE = (chemin_relatif("assets/fonts/Chomsky.otf"), 34)
    FONT_TEXT = (chemin_relatif("assets/fonts/GenAR102.TTF"), 18)

    BACK_IMG = chemin_relatif("assets/images/ressources/Pressed_01.png")
    BG_IMG = chemin_relatif("assets/images/background/Credit_Page.png")

    def __init__(self, screen, fullscreen):
        """
        Initialise l'écran des crédits.

        Args:
            screen (pygame.Surface): La surface principale du jeu.
        """
        self.screen = screen
        self.fullscreen = fullscreen

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
        """
        Boucle principale de l'écran des crédits.
        Gère les événements, le dessin, et met à jour l'affichage.
        """
        while self.running:
            self._handle_events()
            self._draw()
            pygame.display.flip()

    def _handle_events(self):
        """
        Gestion des événements pygame (fermeture, touches, clics).
        - Quitter : bouton X
        - Retour : touche ESC ou clic sur le bouton retour
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.retour, self.running = True, False
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back.get_rect(topleft=(10, 10)).collidepoint(pygame.mouse.get_pos()):
                    self.retour, self.running = True, False
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 1:
                    self.retour, self.running = True, False

    def _draw(self):
        """
        Dessine tous les éléments de l'écran des crédits :
        - Fond
        - Bouton retour
        - Titre
        - Sections (Assets, Sons, Développeurs)
        """
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
            pos=(240, 160),
            align="left"
        )

        self._draw_section(
            "Sons",
            [
                "musiques, de pixabay.com:",
                "musique menu :",
                "level IV, moodmode",
                "musique niveau 1 :",
                "8-bit Arcade Mode, moodmode",
                "musique niveau 2 :",
                "retro arcade game music, HitsLab",
                "musique niveau 3 et 4 :",
                "Dark game beat, Osynthw",
                "musique boss :",
                "chiptune grooving, auteur inconnu",
                "musique mode donjon infini :",
                "Kim Lightyear, Lightyeartraxx",
                "musique écran de mort :",
                "KL peach game over II, Lightyeartraxx",
            ],
            pos=(self.screen.get_width() - 340, 160),
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
        """
        Affiche le titre principal centré en haut de l'écran.

        Args:
            text (str): Texte du titre.
        """
        title_text = self.font_title.render(text, True, BLACK)
        title_rect = title_text.get_rect(midtop=(self.screen.get_width() // 2, 50))
        self.screen.blit(pixelate(title_text, self.pixel_ratio), title_rect)

    def _draw_section(self, subtitle: str, content: list[str], pos: tuple[int, int], align: str = "left"):
        """
        Affiche une section avec sous-titre et contenu.

        Args:
            subtitle (str): Nom de la section.
            content (list[str]): Lignes de texte de la section.
            pos (tuple[int, int]): Position du sous-titre.
            align (str): Alignement du texte ("left" ou "right").
        """
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
