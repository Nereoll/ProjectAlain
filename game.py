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
from powerup import PowerUp
from utilitaire import SoundEffects


class Game:
    """
    Représente la boucle principale du jeu et gère l'ensemble de son état.

    Cette classe orchestre tous les éléments :
    - Initialisation de Pygame, de l'écran et des ressources.
    - Gestion des sprites (joueur, ennemis, bonus, interface…).
    - Boucle principale (événements, mise à jour, rendu).
    - Progression des stages et déclenchement des cutscenes.
    - Gestion de la mort du joueur et de l'écran de fin.

    Args:
        isDungeon (bool, optional): Active un mode donjon spécial.
            Par défaut False.

    Attributs principaux:
        screen (pygame.Surface): Surface d'affichage principale.
        clock (pygame.time.Clock): Gestion du temps et des FPS.
        running (bool): Indique si le jeu est en cours d'exécution.
        isDungeon (bool): Indique si le jeu est en mode donjon.
        all_sprites (pygame.sprite.LayeredUpdates): Tous les sprites du jeu.
        enemies (pygame.sprite.Group): Groupe des ennemis actifs.
        power_ups (pygame.sprite.Group): Groupe des bonus actifs.
        player (Player): Instance du joueur.
        ath (Ath): Interface de l'ATH (affichage de la vie, score, mana…).
        end_screen (End | None): Écran de fin affiché si le joueur meurt.
        stage (int): Numéro du stage actuel.
        stage_backgrounds (dict[int, pygame.Surface]): Fonds d'écran par stage.
        stage_thresholds (dict[int, int]): Score requis pour atteindre chaque stage.
        stage_spawns (dict[int, tuple[int, int]]): Positions de spawn du joueur par stage.
        boss (Enemy | None): Référence au boss si présent.
        dialogue_lines (list[str]): Répliques de dialogue en cours.
        dialogue_active (bool): True si un dialogue est en cours.
        in_cutscene (bool): True si une cinématique est en cours.
        door (bool): Indique si la porte du stage est ouverte.
        score (int): Score du joueur.
        spawn_delay (float): Temps entre chaque apparition d'ennemi.
        spawnable (bool): Indique si les ennemis peuvent apparaître.
        shadow_sprite (Shadow): Sprite représentant l'ombre du joueur selon ses HP.
        sound (SoundEffects): Gestionnaire des effets sonores.
    """
    def __init__(self, screen, fullscreen, isDungeon=False):
        self.screen = screen
        self.fullscreen = fullscreen
        self.isDungeon = isDungeon
        self.running = True

        self.clock = pygame.time.Clock()

        # Game Over
        self.end_screen = None

        # Groupes de sprites
        # Groupes de sprites avec gestion de layers
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        # Joueur
        self.player = Player(self)
        self.player.game = self
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

        #Cutscene
        self.in_cutscene = False
        self.boss = None
        self.dialogue_lines = []
        self.current_line = 0
        self.dialogue_active = False

        # Ressources à charger à l'initialisation
        self.font_title = pygame.font.Font("assets/fonts/Chomsky.otf", 64)
        self.shadow1 = pygame.image.load("assets/images/shadow/Shadow1.png").convert_alpha()
        self.shadow2 = pygame.image.load("assets/images/shadow/Shadow2.png").convert_alpha()
        self.shadow3 = pygame.image.load("assets/images/shadow/Shadow3.png").convert_alpha()

        # On garde un seul sprite shadow et on change son image selon le HP
        self.shadow_sprite = Shadow(self.shadow1, (0, 80))
        self.shadow_sprites = pygame.sprite.LayeredUpdates()
        self.shadow_sprites.add(self.shadow_sprite, layer=4)

        self.firstStage = pygame.image.load("assets/images/background/Base_Stage.png").convert()
        self.secondStage = pygame.image.load("assets/images/background/Second_Stage.png").convert()
        self.thirdStage = pygame.image.load("assets/images/background/Third_Stage.png").convert()
        self.fourthStage = pygame.image.load("assets/images/background/Fourth_Stage.png").convert()
        self.fifthStage = pygame.image.load("assets/images/background/Fifth_Stage.png").convert()

        # Gestion des stages
        self.stage = 1
        self.stage_backgrounds = {
            1: self.firstStage,
            2: self.secondStage,
            3: self.thirdStage,
            4: self.fourthStage,
            5: self.fifthStage,
            6: self.fifthStage
        }
        self.stage_thresholds = {
            2: 1000,   # score requis pour passer au stage 2
            3: 2000,   # score requis pour passer au stage 3
            4: 4000,   # score requis pour passer au stage 4
            5: 4000,   # score requis pour passer au stage 5
            6: 9000,   # score requis pour passer au stage 6, doit être différent des deux précédents
            7: 9000
        }

        self.stage_spawns = {
            1: (WIDTH // 2, HEIGHT // 2),
            2: (WIDTH // 2, HEIGHT // 2),
            3: (WIDTH // 2, HEIGHT // 2),
            4: (100, HEIGHT // 2),
            5: (100, HEIGHT // 2),
            6: (WIDTH // 2, HEIGHT // 2)
        }

        #door
        self.door_rect = pygame.Rect(WIDTH // 2 - 30, (HEIGHT - 650), 60, 15)
        self.door_image1 = pygame.image.load("assets/images/ressources/Door.png").convert_alpha()
        self.door_image2 = pygame.image.load("assets/images/ressources/Door2.png").convert_alpha()
        self.door_image3 = pygame.image.load("assets/images/ressources/Door3.png").convert_alpha()
        self.door_image4 = pygame.image.load("assets/images/Phara.png").convert_alpha()
        self.door=False


        self.font_text = pygame.font.Font("assets/fonts/Chomsky.otf", 32)

        self.sound = SoundEffects()

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
                if self.player.hp <= 0:
                    self.end_screen.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                if self.dialogue_active and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    self.current_line += 1
                    self.sound.play_one("assets/sounds/sound_effects/dialogue_box.ogg", 0.4)
                    if self.current_line >= len(self.dialogue_lines):
                        self.dialogue_active = False
                        self.in_cutscene = False
                        self.sound.stop_music()

                        # Si le boss est mort et encore présent, on le supprime
                        if self.boss and self.boss.is_dead:
                            self.stage = 6
                            self.boss.kill()
                            self.boss = None
                            self.spawnable = False
                            self.player.mana = 40000
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
            elif self.player.joystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.player.hp <= 0:
                        self.end_screen.handle_event(event)
                    if self.dialogue_active and event.button == 0:  # Bouton A
                        self.current_line += 1
                        self.sound.play_one("assets/sounds/sound_effects/dialogue_box.ogg", 0.4)
                        if self.current_line >= len(self.dialogue_lines):
                            self.dialogue_active = False
                            self.in_cutscene = False
                            self.sound.stop_music()
                            if self.boss and self.boss.is_dead:
                                self.stage = 6
                                self.boss.kill()
                                self.boss = None
                                self.spawnable = False
                                self.player.mana = 40000



    def update(self):
        """Mise à jour des objets"""
        current_time = time.time() - self.start_time
        # Spawner des ennemis au fil du temps
        if current_time - self.last_spawn >= self.spawn_delay and self.spawnable:
            self.spawn_enemy()
            self.last_spawn = current_time
            if self.spawn_delay > 0.8:
                self.spawn_delay -= 0.1


        self.all_sprites.update()

        if self.player.invisible and len(self.power_ups) == 0 and (time.time() - self.lastPowerUp >= 2) :
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
        if self.stage == 1 and not self.isDungeon:
            self.door_image = self.door_image1
        elif self.stage == 2 and not self.isDungeon:
            self.door_image = self.door_image2
        elif self.stage == 3 and not self.isDungeon:
            self.door_image = self.door_image3
            self.door_rect = pygame.Rect(WIDTH - 80, HEIGHT // 2 , 60, 100)
        elif self.stage == 4 and not self.isDungeon:
            self.door_rect = pygame.Rect(WIDTH - 80, HEIGHT // 2 - 20 , 60, 120)
        elif self.stage == 5:
            self.door=False
        elif self.stage == 6:
            self.door_image = self.door_image4
            self.door_rect = pygame.Rect(WIDTH -100, HEIGHT // 2 -50, 86, 121)
            if self.player.invisible:
                self.door=True
            else:
                self.door=False


        #Actions spécifiques à la fin du jeu
        if self.stage > 3:
            self.playerSpawn = (WIDTH // 2, 80) #deplaces le joueur au bon endroit
        if self.stage == 5 and not self.boss:
            self.start_boss_cutscene()


        # Changes de stage si on touches la porte
        for next_stage, threshold in self.stage_thresholds.items():
            if self.player.score >= threshold and self.stage < next_stage and not self.isDungeon:
                if not self.stage_cleared :
                    self.clear_stage()
                    self.stage_cleared = True
                if self.door and self.door_rect.colliderect(self.player.rect):
                    self.stage = next_stage
                    self.door = False
                    if not self.stage > 4:
                        self.spawnable = True
                    if self.stage >= 6:
                        self.running = False
                        self.game_over = True
                    self.stage_cleared = False
                    for enemy in self.enemies:
                        enemy.kill()
                    # Repositionner le joueur selon le stage
                    if self.stage in self.stage_spawns:
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



    def start_boss_cutscene(self):
        self.in_cutscene = True
        self.dialogue_active = True
        self.spawnable = False
        self.enemies.empty()
        for ennemies in self.enemies:
            ennemies.kill()

        # Spawn du boss mais sans qu'il attaque
        self.boss = Enemy("boss", self.player, self.screen, (WIDTH-350, HEIGHT//2))
        self.all_sprites.add(self.boss, layer=1)

        # Texte du dialogue
        self.dialogue_lines = [
            "Joris: Ah enfin tu arrives...",
            "Joris: Mehdi Sparu a tué mon père en faisant disparaitre son jeu",
            "Joris: Je dois te faire disparaitre pour me venger !",
            "Alain: ...",
            "Joris: Et oui j'ai rendu ta princesse invisible tu vas faire quoi !?",
            "Alain: Feur",
        ]
        self.current_line = 0

    def start_boss_death_cutscene(self):
        self.dialogue_active = True
        self.spawnable = False

        # Supprime tous les ennemis normaux
        for enemy in list(self.enemies):
            enemy.kill()

        # Dialogue de fin
        self.dialogue_lines = [
            "Joris (mort): Hahaha... je meurs mais ta princesse restera invisible...",
        ]
        self.current_line = 0


    def spawn_enemy(self):
        """Crée un ennemi aléatoire et l'ajoute au jeu"""
        if(self.stage == 1):
            if self.isDungeon :
                enemy_type = random.choice(["pawn", "goblin", "lancier", "scout", "archer", "tnt"])
            else :
                enemy_type = random.choice(["pawn", "lancier", "archer"])
        if(self.stage == 2):
            enemy_type = random.choice(["pawn", "lancier", "archer"])
        if(self.stage == 3):
            enemy_type = random.choice(["goblin", "scout", "tnt"])
        if(self.stage == 4):
            enemy_type = random.choice(["goblin", "scout", "tnt"])
        if(self.stage == 5):
            enemy_type = random.choice(["goblin", "scout", "tnt"])
        if(self.stage == 6):
            enemy_type = random.choice(["pawn", "goblin", "lancier", "scout", "archer", "tnt"])
        
        #enemy_type = random.choice(["archer"])

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
        self.spawn_delay = 2
        self.last_spawn = 0
        self.door=True
        if self.player.hp <4:
            self.player.hp+=2

    def draw(self):
        """Affichage"""
        # Fond du stage courant
        if self.stage in self.stage_backgrounds:
            self.screen.blit(self.stage_backgrounds[self.stage], (0, 0))


        # Sprites
        if self.player.invisible :
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

        if self.dialogue_active:
            box = pygame.Surface((WIDTH - 100, 150))
            box.fill((0, 0, 0))
            pygame.draw.rect(box, (255, 255, 255), box.get_rect(), 3)
            self.screen.blit(box, (50, HEIGHT - 200))

            text = self.font_text.render(self.dialogue_lines[self.current_line], True, WHITE)
            self.screen.blit(text, (70, HEIGHT - 180))



        pygame.display.flip()


