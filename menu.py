# menu.py
import pygame
from player import Player
from settings import WIDTH, HEIGHT, TITLE, WHITE, BLACK
from utilitaire import load_sprites, AnimatedEntity

class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.font_title = pygame.font.Font("assets/fonts/Chomsky.otf", 64)
        self.font_text = pygame.font.Font("assets/fonts/Chomsky.otf", 32)
        self.font_button = pygame.font.Font("assets/fonts/GenAR102.TTF", 40)

        self.playerSprites = pygame.sprite.LayeredUpdates()
        self.player = Player()
        self.playerSpawn = (WIDTH // 2 -145, HEIGHT // 2 + 120)
        self.playerSprites.add(self.player, layer=2)

        # Bouton start
        self.start_button = pygame.Rect(WIDTH // 2 + 120, HEIGHT // 3, 200, 130)

        self.running = True
        self.start_game = False

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
            # --- Dessin ---
            gameMenu = pygame.image.load("assets/images/bg_menu.png").convert_alpha()
            self.screen.blit(gameMenu, (0, 0))

            # Titre
            title_text = self.font_title.render(TITLE, True, WHITE)
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))


            # Bouton Start
            start_text = self.font_button.render("", True, WHITE)
            self.screen.blit(start_text, (self.start_button.centerx - start_text.get_width() // 2,
                                          self.start_button.centery - start_text.get_height() // 2))

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



            pygame.display.flip()
