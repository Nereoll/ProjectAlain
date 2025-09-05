# end.py
import pygame
from settings import TITLE, WHITE, WIDTH, HEIGHT
from utilitaire import load_sprites, animate, SoundEffects, scale_sprites
from audio import SoundMeter

import threading

class End:
    """
    Classe représentant l'écran de fin de partie (Game Over).

    Affiche :
        - Le titre "Game Over"
        - Une animation de mort du joueur
        - Deux boutons (respawn par cri, retour menu principal)

    Attributs :
        screen (pygame.Surface): Surface principale pour l'affichage.
        player (Player): Référence au joueur pour gérer respawn et stats.
        game (Game): Référence au jeu pour modifier son état.
        font_title (pygame.font.Font): Police pour le titre.
        font_button (pygame.font.Font): Police pour les boutons.
        death_sprite (list[pygame.Surface]): Frames de l'animation de mort.
        current_frame (int): Frame actuelle de l'animation.
        animation_speed (float): Vitesse d'animation.
        frame_timer (float): Timer interne pour l'animation.
        retry_button (pygame.Rect): Zone du bouton "Scream to continue".
        menu_button (pygame.Rect): Zone du bouton "Main Menu".
        sound (SoundEffects): Gestionnaire des sons et musiques.
        meters (SoundMeter): Microphone pour mesurer le volume du joueur.
    """
    FONT_TITLE = ("assets/fonts/Chomsky.otf", 64)
    FONT_BUTTON = ("assets/fonts/GenAR102.TTF", 32)
    DEATH_SPRITE_PATH = "assets/images/player/Dead.png"
    DEATH_FRAMES = 14

    def __init__(self, screen, player, game):
        """
        Initialise l'écran de fin de partie.

        Args:
            screen (pygame.Surface): Surface du jeu.
            player (Player): Objet joueur.
            game (Game): Instance du jeu.
        """
        self.screen = screen
        self.player = player
        self.game = game
        pygame.display.set_caption(TITLE)

        # Fonts
        self.font_title = pygame.font.Font(*self.FONT_TITLE)
        self.font_button = pygame.font.Font(*self.FONT_BUTTON)

        # Sprites & Animation
        self.death_sprite = load_sprites(self.DEATH_SPRITE_PATH, self.DEATH_FRAMES)
        self.current_frame = 0
        self.animation_speed = 0.2
        self.frame_timer = 0

        # Boutons
        self.retry_button_image = pygame.image.load("assets/images/ui/retry_button.png").convert_alpha()
        self.retry_button_pressed_image = pygame.image.load("assets/images/ui/retry_button_pressed.png").convert_alpha()
        self.menu_button_image = pygame.image.load("assets/images/ui/menu_button.png").convert_alpha()
        self.retry_button = pygame.Rect(WIDTH // 2 - 310, HEIGHT // 4, 300, 200)
        self.menu_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 4, 300, 200)
        self.retry_clicked = False

        #microphone
        self.micro= pygame.image.load("assets/images/ui/micro.png").convert_alpha()
        self.microRect=self.micro.get_rect(center=(WIDTH//2,HEIGHT-200))

        # Audio
        self.sound = SoundEffects()
        self.meters = SoundMeter()

        # Timer
        self.timer = 1
        self.timer_active = False
        self.last_tick = pygame.time.get_ticks()

    # ---------------------------
    # Logic
    # ---------------------------
    def handle_event(self, event):
        """
        Gère les événements utilisateur (clics souris).

        Args:
            event (pygame.event.Event): Événement pygame.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.retry_button.collidepoint(event.pos) and (self.player.nb_rea < 3):
                # Lancer l'écoute micro dans un thread
                self.timer_active = True
                self.timer = 0
                self.last_tick = pygame.time.get_ticks()
                threading.Thread(target=self._try_respawn).start()
            elif self.menu_button.collidepoint(event.pos):
                self._go_to_menu()
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 4 and (self.player.nb_rea < 3):
                # Lancer l'écoute micro dans un thread
                self.timer_active = True
                self.timer = 0
                self.last_tick = pygame.time.get_ticks()
                threading.Thread(target=self._try_respawn).start()
            elif event.button == 5:
                self._go_to_menu()

    def _try_respawn(self):
        """
        Vérifie si le joueur crie assez fort pour continuer.
        Seuil fixé à 100 dB (valeur simulée via SoundMeter).
        """
        max_value = self.meters.get_max_db(3)
        if max_value >= 100:
            self.respawn_player()

    def _go_to_menu(self):
        """
        Retourne au menu principal.
        Stoppe la musique et modifie l'état du jeu.
        """
        self.sound.stop_music()
        self.game.running = False
        self.game.game_over = True

    def respawn_player(self):
        """
        Ramène le joueur à la vie.
        - Redonne ses HP
        - Change son état
        - Autorise respawn si pas au stage final
        """
        self.game.spawnable = (self.game.stage != 5)
        self.player.hp = 4
        self.player.nb_rea += 1
        self.player.state = "idleR"
        self.timer = 0  # reset timer quand le joueur respawn
        self.last_tick = pygame.time.get_ticks()


    def update(self):
        """Met à jour l'animation de mort."""
        # Timer incrémenté toutes les 1000ms
        if self.timer_active:
            now = pygame.time.get_ticks()
            if now - self.last_tick >= 1000:
                self.timer += 1
                self.last_tick = now

        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.retry_clicked = self.retry_button.collidepoint(mouse_pos) and mouse_pressed[0]
        animate(self, self.death_sprite, loop=True)

    # ---------------------------
    # Rendering
    # ---------------------------

    def draw(self):
        """
        Affiche l'écran de fin :
        - Titre
        - Animation de mort
        - Boutons
        """
        self._draw_title("Game Over")
        self._draw_death_animation()
        if (self.player.nb_rea < 3):
            self._draw_button(self.retry_button, self.retry_button_image)
            if self.retry_clicked:
                self._draw_button(self.retry_button, self.retry_button_pressed_image)
        self._draw_button(self.menu_button, self.menu_button_image)

        if self.timer_active:
            timer_text = self.font_button.render(f"{self.timer}s", True, WHITE)
            timer_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            self.screen.blit(timer_text, timer_rect)
            # Microphone
            self._draw_button(self.microRect, self.micro)



    def _draw_title(self, text: str):
        """
        Affiche le titre centré en haut de l'écran.

        Args:
            text (str): Texte du titre.
        """
        surf = self.font_title.render(text, True, WHITE)
        rect = surf.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(surf, rect)

    def _draw_death_animation(self):
        """
        Affiche l'animation de mort du joueur
        au centre de l'écran.
        """
        if self.current_frame < len(self.death_sprite):
            img = self.death_sprite[self.current_frame]
            rect = img.get_rect(center=(self.screen.get_width() // 2,
                                        self.screen.get_height() // 2))
            self.screen.blit(img, rect)

    def _draw_button(self, rect: pygame.Rect, image):
        """
        Affiche un bouton avec texte centré.

        Args:
            rect (pygame.Rect): Zone du bouton.
            iamge (pygame.Sprite) : Texte affiché.
        """
        self.screen.blit(image, rect)
