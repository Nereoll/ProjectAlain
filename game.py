# game.py
import pygame
import random
import time
from settings import WIDTH, HEIGHT, ATH_HEIGHT, FPS, TITLE, WHITE
from player import Player
from enemy import Enemy
from ath import Ath
from end import End
from shadow import Shadow
from menu import Menu 
from audio import get_max_db 
from powerup import PowerUp


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Game Over
        self.end_screen = None

        # Buttons Game over
        self.retrie_button = pygame.Rect(WIDTH // 2 - 310, HEIGHT // 4, 300, 200)
        self.menu_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 4, 300, 200)

        # Groupes de sprites
        # Groupes de sprites avec gestion de layers
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        # Joueur
        self.player = Player()
        self.player.mana=0
        self.playerSpawn = (WIDTH // 2, HEIGHT // 2)
        self.all_sprites.add(self.player, layer=2)

        # Ath
        self.ath = Ath(self.player)

        self.stage_cleared = False

        # Timer de spawn
        self.start_time = time.time()
        self.last_spawn = 0
        self.spawn_delay = 3  # premier ennemi toutes les 3 sec
        self.spawnable = True
        # Score
        self.score = 0

        self.lastPowerUp = 0


        # Ressources à charger à l'initialisation
        self.font_title = pygame.font.Font("assets/fonts/Chomsky.otf", 64)
        self.shadow1 = pygame.image.load("assets/images/Shadow1.png").convert_alpha()
        self.shadow2 = pygame.image.load("assets/images/Shadow2.png").convert_alpha()
        self.shadow3 = pygame.image.load("assets/images/Shadow3.png").convert_alpha()

        # On garde un seul sprite shadow et on change son image selon le HP
        self.shadow_sprite = Shadow(self.shadow1, (0, 80))
        self.shadow_sprites = pygame.sprite.LayeredUpdates()
        self.shadow_sprites.add(self.shadow_sprite, layer=4)

        self.firstStage = pygame.image.load("assets/images/Base_Stage.png").convert()
        self.secondStage = pygame.image.load("assets/images/Second_Stage.png").convert()
        self.thirdStage = pygame.image.load("assets/images/Third_Stage.png").convert()
        self.fourthStage = pygame.image.load("assets/images/Fourth_Stage.png").convert()
        self.fifthStage = pygame.image.load("assets/images/Fifth_Stage.png").convert()

        # Gestion des stages
        self.stage = 1
        self.stage_backgrounds = {
            1: self.firstStage,
            2: self.secondStage,
            3: self.thirdStage,
            4: self.fourthStage,
            5: self.fifthStage
        }
        self.stage_thresholds = {
            2: 100,   # score requis pour passer au stage 2
            3: 400,   # score requis pour passer au stage 3
            4: 800,   # score requis pour passer au stage 4
            5: 800,   # score requis pour passer au stage 5
        }

        self.stage_spawns = {
            1: (WIDTH // 2, HEIGHT // 2),
            2: (WIDTH // 2, HEIGHT // 2),
            3: (WIDTH // 2, HEIGHT // 2),
            4: (100, HEIGHT // 2),
            5: (100, HEIGHT // 2)
        }


        self.stage_changed = False  # évite de répéter clear_stage

        #door
        self.door_rect = pygame.Rect(WIDTH // 2 - 30, (HEIGHT - 650), 60, 60)
        self.door_image1 = pygame.image.load("assets/images/Door.png").convert_alpha()
        self.door_image2 = pygame.image.load("assets/images/Door2.png").convert_alpha()
        self.door_image3 = pygame.image.load("assets/images/Door3.png").convert_alpha()
        self.door=False


        self.font_text = pygame.font.Font("assets/fonts/Chomsky.otf", 32)


    def new(self):
        """Nouvelle partie"""
        self.run()

    def run(self):
        """Boucle principale"""
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Gestion des événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.retrie_button.collidepoint(event.pos) and self.player.hp < 0:
                    max_value = get_max_db(5)
                    print(max_value)
                    if max_value >= 130 :
                        self.spawnable = True
                        self.spawn_delay = 3
                        self.last_spawn = 0
                        self.player.hp = 4
                        self.player.state = "idleR"
                elif self.menu_button.collidepoint(event.pos) and self.player.hp < 0:
                    self.running = False
                    self.game_over = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.player.hp <= 0 and self.end_screen:
                self.end_screen.handle_event(event)


    def update(self):
        """Mise à jour des objets"""
        current_time = time.time() - self.start_time
        # Spawner des ennemis au fil du temps
        if current_time - self.last_spawn >= self.spawn_delay and self.spawnable:
            self.spawn_enemy()
            self.last_spawn = current_time
            if self.spawn_delay > 0.8:
                self.spawn_delay -= 0.1
        oldLength = self.enemies.__len__()
        self.all_sprites.update()

        if self.player.state == "invisible" and len(self.power_ups) == 0 and (time.time() - self.lastPowerUp >= 2) :
            self.lastPowerUp = time.time()
            # Génère une position aléatoire dans la zone de jeu
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            if self.player.hp < 4 : # Le joueur ne peut pas avoir plus de 4 coeurs
                bonus_type = random.choice(["damageAmp", "invulnerability", "heart"])  # Type de bonus aléatoire
            else :
                bonus_type = random.choice(["damageAmp", "invulnerability"])
            power_up = PowerUp((x, y), bonus_type, self.player)
            self.power_ups.add(power_up)
            self.all_sprites.add(power_up, layer=3)

        #change la porte en fonction du stage
        if self.stage == 1:
            self.door_image = self.door_image1
        elif self.stage == 2:
            self.door_image = self.door_image2
        elif self.stage == 3:
            self.door_image = self.door_image3
            self.door_rect = pygame.Rect(WIDTH - 80, HEIGHT // 2 , 60, 60)
        elif self.stage == 4:
            self.door_rect = pygame.Rect(WIDTH - 80, HEIGHT // 2 , 60, 60)


        #Actions spécifiques à la fin du jeu
        if self.stage > 3:
            self.spawnable = False #empeche le spawn de nouceaux ennemis
            self.enemies.empty()
            self.playerSpawn = (WIDTH // 2, 80) #deplaces le joueur au bon endroit

        # Changes de stage si on touches la porte
        for next_stage, threshold in self.stage_thresholds.items():
            if self.player.score >= threshold and self.stage < next_stage:
                if not self.stage_cleared :
                    self.clear_stage()
                    self.stage_cleared = True
                if self.door_rect.colliderect(self.player.rect):
                    self.stage = next_stage
                    self.door = False
                    self.spawnable = True
                    self.stage_cleared = False
                    for enemy in self.enemies:
                        enemy.kill()
                    # Repositionner le joueur selon le stage
                    self.player.rect.center = self.stage_spawns[self.stage]
                    self.player.mask = pygame.mask.from_surface(self.player.image)  # recalcule la mask collision
                break


        # Mise à jour explicite de l'ATH
        self.ath.update()
        
        if self.player.hp <= 0:
            if not self.end_screen:
                self.end_screen = End(self.screen, self.player, self)
            self.end_screen.update()
            return 

    def spawn_enemy(self):
        """Crée un ennemi aléatoire et l'ajoute au jeu"""
        enemy_type = random.choice(["pawn", "goblin", "lancier"])

        # Spawn autour de la zone de jeu (hors écran)
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            pos = (random.randint(0, WIDTH), ATH_HEIGHT)
        elif side == "bottom":
            pos = (random.randint(0, WIDTH), HEIGHT + 20)
        elif side == "left":
            pos = (-20, random.randint(ATH_HEIGHT, HEIGHT))
        else:  # right
            pos = (WIDTH + 20, random.randint(ATH_HEIGHT, HEIGHT))

        enemy = Enemy(enemy_type, self.player, self.screen, pos)
        self.all_sprites.add(enemy, layer=1)
        self.enemies.add(enemy)

    def clear_stage(self):
        self.spawnable = False
        self.spawn_delay = 3
        self.last_spawn = 0
        self.door=True
        if self.player.hp <4:
            self.player.hp=4

    def draw(self):
        """Affichage"""
        # Fond du stage courant
        self.screen.blit(self.stage_backgrounds[self.stage], (0, 0))


        # Sprites
        if self.player.state == "invisible":
            for enemy in self.enemies:
                self.screen.blit(enemy.question_mark, enemy.question_mark_rect)
                enemy.update()

        self.all_sprites.draw(self.screen)

        if self.door:
            self.screen.blit(self.door_image, self.door_rect)

        # Ombres selon HP
        if self.player.hp == 3:
            self.shadow_sprite.image = self.shadow1
        elif self.player.hp == 2:
            self.shadow_sprite.image = self.shadow2
        elif self.player.hp == 1:
            self.shadow_sprite.image = self.shadow3
        elif self.player.hp <= 0 and self.end_screen:
            for enemy in self.enemies:
                enemy.kill()
            self.player.image.set_alpha(0)
            self.shadow_sprites.draw(self.screen)
            self.end_screen.draw()
        else:
            self.shadow_sprite.image = pygame.Surface(self.shadow1.get_size(), pygame.SRCALPHA)
                    

        # Dessiner le sprite shadow
        if self.player.hp > 0:
            self.shadow_sprites.draw(self.screen)
            self.ath.draw(self.screen)


        pygame.display.flip()


