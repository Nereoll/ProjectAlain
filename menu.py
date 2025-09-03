# menu.py
import pygame
from settings import WIDTH, HEIGHT, TITLE, WHITE, BLACK

class Menu:



    def __init__(self, screen):
        self.screen = screen

        self.font_title = pygame.font.Font("assets/fonts/Chomsky.otf", 64)
        self.font_text = pygame.font.Font("assets/fonts/Chomsky.otf", 32)
        self.font_button = pygame.font.SysFont("gentiumalt", 40)

        # Bouton start
        self.start_button = pygame.Rect(WIDTH // 2 - 310, HEIGHT // 4, 300, 200)

        self.running = True
        self.start_game = False

        # Animation
        self.animation_speed = 0.15   # vitesse de défilement des frames de mouvement
        self.frame_timer = 0
        self.current_frame = 0 #Index de la frame actuelle dans la liste de sprites.


    def load_sprites(self, path, num_frames):
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

    def animate(self, sprites, loop=True):
            """Anime un spritesheet"""
            self.frame_timer += self.animation_speed
            if self.frame_timer >= 1:
                self.frame_timer = 0
                self.current_frame += 1
                if self.current_frame >= len(sprites):
                    if loop:
                        self.current_frame = 0
                    else:
                        self.current_frame = len(sprites) - 1  # rester sur la dernière frame
                self.image = sprites[self.current_frame]


    def run(self):
        """Boucle du menu"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        self.start_game = True
                        self.running = False

            # --- Dessin ---
            gameMenu = pygame.image.load("assets/images/bg_menu.png").convert_alpha()
            self.screen.blit(gameMenu, (0, 0))

            # Titre
            title_text = self.font_title.render(TITLE, True, WHITE)
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

            # Bouton Start
            start_text = self.font_button.render("START", True, WHITE)
            self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width() // 2,
                                          self.start_button.centery - start_text.get_height() -0.5 // 2))

            # Chevalier animé
            knight_sprites = self.load_sprites("assets/images/Warrior_Idle.png", 8)
            self.animate(knight_sprites)

            # Instructions
            pygame.display.flip()
