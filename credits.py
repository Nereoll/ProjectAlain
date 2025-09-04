import pygame
from settings import TITLE, BLACK, HEIGHT

class Credits:
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption(TITLE)
        
        # Fonts
        self.font_title = pygame.font.Font("assets/fonts/Chomsky.otf", 52)
        self.font_subtitle = pygame.font.Font("assets/fonts/Chomsky.otf", 34)
        self.font_text = pygame.font.Font("assets/fonts/GenAR102.TTF", 18)
        
        # Actions
        self.running = True
        self.retour = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        
            # --- Dessin ---
            gameCredits = pygame.image.load("assets/images/Credit_Page.png").convert_alpha()
            self.screen.blit(gameCredits, (0, 0))
            
            # Titre
            title_text = self.font_title.render("Crédits", True, BLACK)
            title_rect = title_text.get_rect(midtop=(self.screen.get_width() // 2, 50))
            self.screen.blit(title_text, title_rect)

            # Assets
            assets_subtitle = self.font_subtitle.render("Assets", True, BLACK)
            assets_rect = assets_subtitle.get_rect(topleft=(240, 180))
            self.screen.blit(assets_subtitle, assets_rect)
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
            self.screen.blit(sounds_subtitle, sounds_rect)
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
            self.screen.blit(dev_subtitle, dev_rect)
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