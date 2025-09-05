import pygame
from settings import TITLE, BLACK, HEIGHT
from utilitaire import pixelate

class Credits:
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption(TITLE)
        
        # Fonts
        self.font_title = pygame.font.Font("assets/fonts/Chomsky.otf", 52)
        self.font_subtitle = pygame.font.Font("assets/fonts/Chomsky.otf", 34)
        self.font_text = pygame.font.Font("assets/fonts/GenAR102.TTF", 18)
        
        # Back to menu
        self.back = pygame.image.load("assets/images/ressources/Pressed_01.png")
        
        # Actions
        self.running = True
        self.retour = False

        self.pixel_ratio = 0.8

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.retour = True
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    back_rect = self.back.get_rect(topleft=(10, 10))
                    if back_rect.collidepoint(mouse_pos):
                        self.retour = True
                        self.running = False
                        
            # --- Dessin ---
            gameCredits = pygame.image.load("assets/images/background/Credit_Page.png").convert_alpha()
            self.screen.blit(gameCredits, (0, 0))
            
            # Back
            self.screen.blit(self.back, (10, 10))

            # Titre
            title_text = self.font_title.render("Crédits", True, BLACK)
            title_rect = title_text.get_rect(midtop=(self.screen.get_width() // 2, 50))
            self.screen.blit(pixelate(title_text, self.pixel_ratio), title_rect)

            # Assets
            assets_subtitle = self.font_subtitle.render("Assets", True, BLACK)
            assets_rect = assets_subtitle.get_rect(topleft=(240, 180))
            self.screen.blit(pixelate(assets_subtitle, self.pixel_ratio), assets_rect)
            #####
            assets_content = [
                "Tiny Sword Pack by Pixel Frog on itch.io",
            ]
            for i, line in enumerate(assets_content):
                line_text = self.font_text.render(line, True, BLACK)
                self.screen.blit(line_text, (220, 220 + i * 30))
            
            # Sounds
            sounds_subtitle = self.font_subtitle.render("Sounds", True, BLACK)
            sounds_rect = sounds_subtitle.get_rect(topright=(self.screen.get_width() - 300, 280))
            self.screen.blit(pixelate(sounds_subtitle, self.pixel_ratio), sounds_rect)
            #####
            sounds_content = [
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
            ]
            for i, line in enumerate(sounds_content):
                line_text = self.font_text.render(line, True, BLACK)
                self.screen.blit(line_text, (self.screen.get_width() - 500, 320 + i * 30))
            
            # Developers
            dev_subtitle = self.font_subtitle.render("Développeurs", True, BLACK)
            dev_rect = dev_subtitle.get_rect(topleft=(220, HEIGHT - 420))
            self.screen.blit(pixelate(dev_subtitle, self.pixel_ratio), dev_rect)
            #####
            dev_content = [
                "Bastien ALLEGRE / Hugo BARBIERI",
                "Emeric DIEUDONNE / Vianney MIQUEL",
                "Cyrian TORREJON"
            ]
            for i, line in enumerate(dev_content):
                line_text = self.font_text.render(line, True, BLACK)
                self.screen.blit(line_text, (220, (HEIGHT - 380) + i * 30))
            
            pygame.display.flip()