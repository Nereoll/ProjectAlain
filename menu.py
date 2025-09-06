"""
menu.py

Définit l'écran de menu principal du jeu.

Le joueur peut déplacer son personnage (sprite) et interagir avec les boutons
du menu en les "touchant" avec son sprite (Start, Crédits, Dungeon).
Le menu contient aussi des animations, une musique de fond et un rendu graphique
(personnage, mouton, arbres, buissons, ruban, bannière, etc.).
"""
import pygame
from player import Player
from settings import WIDTH, HEIGHT, TITLE, WHITE, SUBTITLE
from utilitaire import load_sprites, pixelate, SoundEffects, chemin_relatif
from components.button import Button
from components.animatedElement import AnimatedElement

class Menu:
    """
    Classe représentant le menu principal du jeu.

    Attributes:
        screen (pygame.Surface): Surface d'affichage Pygame.
        player (Player): Sprite du joueur permettant d'interagir avec le menu.
        start_game (bool): Indique si une partie doit être lancée.
        start_game_infinite (bool): Indique si la partie doit démarrer en mode infini/donjon.
        show_credits (bool): Indique si les crédits doivent être affichés.
        running (bool): Boucle de contrôle du menu.
    """
    def __init__(self, screen, fullscreen):
        self.screen = screen
        self.fullscreen = fullscreen

        # pygame.display.set_caption(TITLE)

        # Charger les polices
        self.font_title = pygame.font.Font(chemin_relatif("assets/fonts/Chomsky.otf"), 52)
        self.font_subtitle = pygame.font.Font(chemin_relatif("assets/fonts/GenAR102.TTF"), 24)
        self.font_text = pygame.font.Font(chemin_relatif("assets/fonts/Chomsky.otf"), 32)
        self.font_button = pygame.font.Font(chemin_relatif("assets/fonts/GenAR102.TTF"), 40)
        self.font_credits = pygame.font.Font(chemin_relatif("assets/fonts/Chomsky.otf"), 28)

        # Initialiser le joueur
        self.playerSprites = pygame.sprite.LayeredUpdates()
        self.player = Player()
        self.playerSpawn = (WIDTH // 2 - 145, HEIGHT // 2 + 120)
        self.playerSprites.add(self.player, layer=2)

        # Boutons
        self.start_button = pygame.Rect(WIDTH // 2 + 120, HEIGHT // 3, 200, 130)
        self.credit_button = Button("Crédits", self.font_credits, WIDTH - 255, HEIGHT - 215)
        self.credit_button.box_rect = pygame.Rect(WIDTH - 280, HEIGHT - 306, 120, 100)
        self.infinite_button = Button("Dungeon", self.font_credits, 55, 115, 10, WHITE)
        self.infinite_button.box_rect = pygame.Rect(40, 40, 120, 180)
        self.lore_button = Button("Histoire", self.font_credits, WIDTH - 330, HEIGHT - 590)
        self.lore_button.box_rect = pygame.Rect(WIDTH - 455, HEIGHT - 740, 350, 120)

        # Charger les sprites animées
        knight_sprites = load_sprites(chemin_relatif("assets/images/player/Warrior_Idle.png"), 8)
        self.knight = AnimatedElement(knight_sprites, (WIDTH // 2 - 100, HEIGHT // 2))

        sheep_sprites = load_sprites(chemin_relatif("assets/images/ressources/Sheep_Idle.png"), 12)
        self.sheep = AnimatedElement(sheep_sprites, (WIDTH // 4 - 80, HEIGHT // 2 + 100))

        tree_sprites = load_sprites(chemin_relatif("assets/images/ressources/Tree3.png"), 8)
        self.tree = AnimatedElement(tree_sprites, (WIDTH - 140, HEIGHT // 2))

        bush_sprites = load_sprites(chemin_relatif("assets/images/ressources/Bushe3.png"), 8)
        self.bush = AnimatedElement(bush_sprites, (WIDTH // 2 - 80, 80))

        # Charger les images statiques
        self.ribbon = pygame.image.load(chemin_relatif("assets/images/ressources/Ribbon_Blue_3Slides.png")).convert_alpha()
        self.banner = pygame.image.load(chemin_relatif("assets/images/ressources/Carved_3Slides.png")).convert_alpha()
        self.banner_rotation_angle = -25
        self.banner = pygame.transform.rotate(self.banner, self.banner_rotation_angle - 30)

        # États du menu
        self.running = True
        self.start_game = False
        self.start_game_infinite = False
        self.show_credits = False   
        self.show_lore = False

        # Repositionner le joueur sur le spawn défini
        self.player.rect.center = self.playerSpawn
        self.player.mask = pygame.mask.from_surface(self.player.image)  # recalcule la mask collision

        # Charger les effets sonores
        self.sound = SoundEffects()
        if not self.sound.is_playing():
            self.sound.play_music(chemin_relatif("assets/sounds/music/menu_music.ogg"), volume=0.2)

    def run(self):
        """Boucle du menu"""
        while self.running:
            self.handle_events()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                    self.fullscreen = not self.fullscreen

        # Vérifie si le joueur collide avec le bouton Start avec son sprite
        player_rect_center = self.playerSprites.sprites()[0].rect.center

        if self.start_button.collidepoint(player_rect_center):
            self.start_game = True
            self.running = False
            self.sound.stop_music()
            self.sound.play_music(chemin_relatif("assets/sounds/music/lvl_1_bridge.ogg"), volume=0.2)

        # Vérifie si le joueur collide sur le bouton Crédit
        if self.credit_button.collidepoint(player_rect_center):
            self.show_credits = True
            self.running = False

        # Vérifie si le joueur collide sur le bouton Lore
        if self.lore_button.collidepoint(player_rect_center):
            self.show_lore = True
            self.running = False

        # Vérifie si le joueur collide sur le bouton Dungeon
        if self.infinite_button.collidepoint(player_rect_center):
            self.start_game = True
            self.start_game_infinite = True
            self.running = False
            self.sound.play_music(chemin_relatif("assets/sounds/music/lvl_dungeon_bridge.ogg"), volume=0.2)

        #verifie si la musique du menu est e, cours
        if not self.sound.is_playing():
            self.sound.play_music(chemin_relatif("assets/sounds/music/menu_music.ogg"), volume=0.2)

    def draw(self):
        # Fond du menu
        gameMenu = pygame.image.load(chemin_relatif("assets/images/background/bg_menu.png")).convert_alpha()
        self.screen.blit(gameMenu, (0, 0))

        # Titre
        title_text = self.font_title.render(TITLE, True, WHITE)
        title_x = WIDTH // 2 - title_text.get_width() // 2
        title_y = 15

        # Ruban
        ribbon_height = self.ribbon.get_height()
        scaled_ribbon = pygame.transform.scale(self.ribbon, (title_text.get_width() * 1.7, ribbon_height + 40))
        ribbon_rect = scaled_ribbon.get_rect(midtop=(WIDTH // 2, title_y - 10))
        self.screen.blit(scaled_ribbon, ribbon_rect)
        self.screen.blit(pixelate(title_text, 0.7), (title_x, title_y))

        # Dessiner les boutons
        self.credit_button.draw(self.screen)
        # pygame.draw.rect(self.screen, BLUE, self.credit_button.box_rect, 4) # Debug box
        self.infinite_button.draw(self.screen)
        # pygame.draw.rect(self.screen, BLUE, self.infinite_button.box_rect, 4) # Debug box
        self.lore_button.draw(self.screen)
        #pygame.draw.rect(self.screen, BLUE, self.lore_button.box_rect, 4) # Debug box

        # Mise à jour et rendu des éléments animés
        self.sheep.update()
        self.sheep.draw(self.screen)
        self.tree.update()
        self.tree.draw(self.screen)
        self.bush.update()
        self.bush.draw(self.screen)

        # Mise à jour et rendu du joueur
        self.playerSprites.update()
        self.playerSprites.draw(self.screen)

        # Sous-titre
        lines = SUBTITLE.split('\n')
        subtitle_x = 70
        subtitle_y = HEIGHT - 200

        # Bannière
        subtitle_text_temp = self.font_subtitle.render(lines[0], True, (0, 0, 0))
        banner_height = self.banner.get_height()
        scaled_banner = pygame.transform.scale(self.banner, (subtitle_text_temp.get_width() + 400, banner_height + 100))
        banner_rect = scaled_banner.get_rect(midtop=(subtitle_x + 70, subtitle_y - 30))
        self.screen.blit(scaled_banner, banner_rect)

        for i, line in enumerate(lines):
            subtitle_text = self.font_subtitle.render(line, True, (0, 0, 0))
            subtitle_text = pygame.transform.rotate(subtitle_text, self.banner_rotation_angle - 5)
            self.screen.blit(subtitle_text, (subtitle_x - 20, (subtitle_y + 35) + i * 30))

        pygame.display.flip()
