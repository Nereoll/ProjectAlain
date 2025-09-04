# end.py
import pygame
from settings import TITLE, WHITE, WIDTH, HEIGHT
from utilitaire import load_sprites, animate
from audio import get_max_db

class End:
    def __init__(self, screen, player, game):
        self.screen = screen
        self.player = player
        self.game = game
        pygame.display.set_caption(TITLE)
        
        # Text
        self.font_title = pygame.font.Font("assets/fonts/Chomsky.otf", 64)
        self.font_button = pygame.font.Font("assets/fonts/GenAR102.TTF", 32)

        # Sprite
        self.death_sprite = load_sprites("assets/images/player/Dead.png", 14)
        
        # Animation
        self.current_frame = 0
        self.animation_speed = 0.2
        self.frame_timer = 0 
        
        # Boutons
        self.retry_button = pygame.Rect(WIDTH // 2 - 310, HEIGHT // 4, 300, 200)
        self.menu_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 4, 300, 200)
        
        
    def handle_event(self, event):
        """Gestion des clics souris"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.retry_button.collidepoint(event.pos):
                # Vérifie le cri pour ressusciter
                max_value = get_max_db(5)
                print("Max DB:", max_value)
                if max_value >= 130:
                    self.respawn_player()
            elif self.menu_button.collidepoint(event.pos):
                # Retour menu = arrêter la game loop
                self.game.running = False
                self.game.game_over = True

    def respawn_player(self):
        """Ramène le joueur à la vie"""
        self.game.spawnable = True
        self.game.spawn_delay = 3
        self.game.last_spawn = 0
        self.player.hp = 4
        self.player.state = "idleR"
        
    def update(self):
        """Met à jour l’animation"""
        animate(self, self.death_sprite, loop=True)
        
    def draw(self):
        """Affiche l’écran de fin"""
        # Titre
        end_title = self.font_title.render("Game Over", True, WHITE)
        end_title_rect = end_title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(end_title, end_title_rect)
        
        # Affiche l'animation de mort
        if self.current_frame < len(self.death_sprite):
            death_image = self.death_sprite[self.current_frame]
            death_rect = death_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(death_image, death_rect)

        # Bouton retry
        retry_text = self.font_button.render("Scream to continue", True, WHITE)
        retry_rect = retry_text.get_rect(center=self.retry_button.center)
        self.screen.blit(retry_text, retry_rect)

        # Bouton menu
        menu_text = self.font_button.render("Main Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        self.screen.blit(menu_text, menu_rect)