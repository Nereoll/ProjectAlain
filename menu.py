# menu.py
import pygame
from player import Player
from settings import WIDTH, HEIGHT, TITLE, WHITE, SUBTITLE, BLUE
from utilitaire import load_sprites, AnimatedEntity, pixelate, SoundEffects

class Menu:
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption(TITLE)

        self.font_title = pygame.font.Font("assets/fonts/Chomsky.otf", 52)
        self.font_subtitle = pygame.font.Font("assets/fonts/GenAR102.TTF", 24)
        self.font_text = pygame.font.Font("assets/fonts/Chomsky.otf", 32)
        self.font_button = pygame.font.Font("assets/fonts/GenAR102.TTF", 40)
        self.font_credits = pygame.font.Font("assets/fonts/Chomsky.otf", 28)

        self.playerSprites = pygame.sprite.LayeredUpdates()
        self.player = Player()
        self.playerSpawn = (WIDTH // 2 -145, HEIGHT // 2 + 120)
        self.playerSprites.add(self.player, layer=2)

        # Bouton start
        self.start_button = pygame.Rect(WIDTH // 2 + 120, HEIGHT // 3, 200, 130)

        # Bouton crédit
        self.credit_text = self.font_credits.render("Crédits", True, WHITE)
        self.credit_x = WIDTH - 415
        self.credit_y = HEIGHT - 297
        self.credit_rect = self.credit_text.get_rect(topleft=(self.credit_x, self.credit_y))
        self.padding = 10
        self.box_rect = pygame.Rect(
            self.credit_rect.left - self.padding,
            self.credit_rect.top - self.padding,
            self.credit_rect.width + 5 * self.padding,
            self.credit_rect.height + 7 * self.padding
        )

        self.running = True
        self.start_game = False
        self.show_credits = False

        # === Ribbon ===
        self.ribbon = pygame.image.load("assets/images/Ribbon_Blue_3Slides.png").convert_alpha()
        
        # === Banner ===
        self.banner_rotation_angle = -25
        self.banner = pygame.image.load("assets/images/Carved_3Slides.png").convert_alpha()
        self.banner = pygame.transform.rotate(self.banner, self.banner_rotation_angle  - 30)

        # === Chevalier ===
        knight_sprites = load_sprites("assets/images/Warrior_Idle.png", 8)
        self.knight = AnimatedEntity(knight_sprites, (WIDTH // 2 - 100, HEIGHT // 2))

        # === Mouton ===
        sheep_sprites = load_sprites("assets/images/Sheep_Idle.png", 12)
        self.sheep = AnimatedEntity(sheep_sprites, (WIDTH // 4 - 80, HEIGHT // 2 + 100))

        # === Arbre ===
        tree_sprites = load_sprites("assets/images/Tree3.png", 8)
        self.tree = AnimatedEntity(tree_sprites, (WIDTH - 140, HEIGHT // 2))

        # === Bush ===
        bush_sprites = load_sprites("assets/images/Bushe3.png", 8)
        self.bush = AnimatedEntity(bush_sprites, (WIDTH // 2 - 80, 80))


        # Paramètres communs d’animation
        self.animation_speed = 0.15

        # Repositionner le joueur sur le spawn défini
        self.player.rect.center = self.playerSpawn
        self.player.mask = pygame.mask.from_surface(self.player.image)  # recalcule la mask collision

        self.music = SoundEffects()
        if not self.music.is_playing():
            self.music.play_music("assets/sounds/music/menu_music.ogg", volume=0.2)


    def run(self):
        """Boucle du menu"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # Vérifie si le joueur collide avec le bouton Start avec son sprite
            if self.start_button.collidepoint(self.playerSprites.sprites()[0].rect.center):
                self.start_game = True
                self.running = False
                self.music.stop_music()
                
            # Vérifie si le joueur collide sur le bouton Crédit
            if self.box_rect.collidepoint(self.playerSprites.sprites()[0].rect.center):
                self.show_credits = True
                self.running = False
            
            # --- Dessin ---
            gameMenu = pygame.image.load("assets/images/bg_menu.png").convert_alpha()
            self.screen.blit(gameMenu, (0, 0))

            # Titre
            title_text = self.font_title.render(TITLE, True, WHITE)
            title_x = WIDTH // 2 - title_text.get_width() // 2
            title_y = 15

            # Ribbon
            ribbon_height = self.ribbon.get_height()
            scaled_ribbon = pygame.transform.scale(self.ribbon, (title_text.get_width() * 1.7, ribbon_height + 40))
            ribbon_rect = scaled_ribbon.get_rect(midtop=(WIDTH // 2, title_y - 10))
            self.screen.blit(scaled_ribbon, ribbon_rect)
            self.screen.blit(pixelate(title_text, 0.7), (title_x, title_y))


            # Bouton Start
            start_text = self.font_button.render("", True, WHITE)
            self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width() // 2,
                                          self.start_button.centery - start_text.get_height() - 0.5 // 2))
            
            # Bouton Crédit
            self.screen.blit(self.credit_text, (self.credit_x + 20, self.credit_y + 80))
            # pygame.draw.rect(self.screen, BLUE, self.box_rect, 4)

            
            
            # === Chevalier animé ===
            #self.knight.update()
            #self.knight.draw(self.screen)

            # === Mouton animé ===
            self.sheep.update()
            self.sheep.draw(self.screen)

            # === Arbre animé ===
            self.tree.update()
            self.tree.draw(self.screen)

            # === Bush animé ===
            self.bush.update()
            self.bush.draw(self.screen)

            # === Joueur ===
            self.playerSprites.update()
            self.playerSprites.draw(self.screen)


            # === Subtitle ===
            subtitle_text = self.font_subtitle.render(SUBTITLE, True, WHITE)
            lines = SUBTITLE.split('\n')
            subtitle_x = 20
            subtitle_y = HEIGHT - 200
            

            # === Banner ===
            banner_height = self.banner.get_height()
            scaled_banner = pygame.transform.scale(self.banner, (subtitle_text.get_width() + 400, banner_height + 100))
            banner_rect = scaled_banner.get_rect(midtop=(subtitle_x + 120, subtitle_y - 30))

            self.screen.blit(scaled_banner, banner_rect)
            for i, line in enumerate(lines):
                subtitle_text = self.font_subtitle.render(line, True, (0, 0, 0))
                subtitle_text = pygame.transform.rotate(subtitle_text, self.banner_rotation_angle+3)
                self.screen.blit(subtitle_text, (subtitle_x, (subtitle_y + 35) + i * (subtitle_text.get_height() - 90)))

            pygame.display.flip()