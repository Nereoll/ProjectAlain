# enemie.py
import pygame
import math
import time
from PIL import Image , ImageOps
from utilitaire import load_sprites, animate, scale_sprites


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, player, screen, pos=(0, 0)):
        super().__init__()
        self.enemy_type = enemy_type
        self.player = player
        self.screen = screen
        self.last_attack_time = 0


        # Stats selon le type
        if enemy_type == "pawn":
            self.hp = 1
            self.speed = 2
            self.attack_points = 1
            self.stagger_timer = 0.3
            self.knockback_distance = 50
            self.knockback_speed = 5
            color = (200, 200, 200)
        elif enemy_type == "goblin":
            self.hp = 2
            self.speed = 4
            self.attack_points = 1
            self.stagger_timer = 0.5
            self.knockback_distance = 100
            self.knockback_speed = 5
            color = (0, 200, 0)
        elif enemy_type == "scout" :
            self.hp = 1
            self.speed = 7
            self.attack_points = 1
            self.stagger_timer = 0.5
            self.knockback_distance = 250
            self.knockback_speed = 100
        elif enemy_type == "tnt" :
            self.hp = 3
            self.speed = 2.5
            self.attack_points = 2
            self.stagger_timer = 0.4
            self.knockback_distance = 60
            self.knockback_speed = 10
        elif enemy_type == "archer" :
            self.hp = 2
            self.speed = 2
            self.attack_points = 2
            self.stagger_timer = 0.5
            self.knockback_distance = 50
            self.knockback_speed = 10
        elif enemy_type == "lancier":
            self.hp = 3
            self.speed = 1.5
            self.attack_points = 1
            self.stagger_timer = 0.2
            self.knockback_distance = 40
            self.knockback_speed = 5
            color = (150, 150, 255)
        elif enemy_type=="boss":
            self.hp = 50
            self.speed = 4
            self.attack_points = 2
            self.stagger_timer = 0.5
            self.knockback_distance = 10
            self.knockback_speed = 3
        else:
            raise ValueError("Type d'ennemi inconnu")

        self.currentKB = self.knockback_distance
        self.default_speed = self.speed  # Sauvegarde de la vitesse initiale

        self.question_mark = pygame.image.load("assets/images/ressources/question_mark.png").convert_alpha()
        self.question_mark = pygame.transform.scale(self.question_mark, (30, 30))  # Redimensionne à 20x20 pixels
        self.question_mark_rect = self.question_mark.get_rect()

        # === Sprites ===
        # Miror srite pawn
        imageLwalkpawn = ImageOps.mirror(Image.open("assets/images/enemy/pawn/Pawn_Run.png"))
        # Miror srite goblin
        imageLwalkgoblin = ImageOps.mirror(Image.open("assets/images/enemy/goblin/Goblin_Run.png"))
        # Miror srite lancier
        imageLwalklancier = ImageOps.mirror(Image.open("assets/images/enemy/lancier/Lancier_Run.png"))
        # Miror sprite scout
        imageLwalkscout = ImageOps.mirror(Image.open("assets/images/enemy/scout/scoutRun.png"))
        # Miror sprite tnt
        imageLwalktnt = ImageOps.mirror(Image.open("assets/images/enemy/tnt/tntRun.png"))
        # Miror sprite tnt
        imageLwalkarcher = ImageOps.mirror(Image.open("assets/images/enemy/archer/archerWalkR.png"))

        if self.enemy_type == "pawn":
            self.walkRSprites = load_sprites("assets/images/enemy/pawn/Pawn_Run.png", 6)
            self.attackRSprites = load_sprites("assets/images/enemy/pawn/Pawn_Attack.png", 6)
            self.walkLSprites = load_sprites(imagestring= imageLwalkpawn, num_frames=6, nopath =True)
            self.attackLSprites = load_sprites("assets/images/enemy/pawn/Pawn_Attack_reversed.png", 6)
            self.idleRSprites = load_sprites("assets/images/enemy/pawn/Pawn_IdleR.png", 6)
            self.idleLSprites = load_sprites("assets/images/enemy/pawn/Pawn_IdleL.png", 6)
            self.animation_speed = 0.15 
        elif self.enemy_type == "goblin":
            self.walkRSprites = load_sprites("assets/images/enemy/goblin/Goblin_Run.png", 6)
            self.attackRSprites = load_sprites("assets/images/enemy/goblin/Goblin_Attack.png", 6)
            self.walkLSprites = load_sprites(imagestring= imageLwalkgoblin, num_frames=6, nopath =True)
            self.attackLSprites = load_sprites("assets/images/enemy/goblin/Goblin_Attack_reversed.png", 6)
            self.idleRSprites = load_sprites("assets/images/enemy/goblin/Goblin_IdleR.png", 7)
            self.idleLSprites = load_sprites("assets/images/enemy/goblin/Goblin_IdleL.png", 7)
            self.animation_speed = 0.15 
        elif self.enemy_type == "scout":
            scale_factor = 3
            self.walkRSprites = scale_sprites(load_sprites("assets/images/enemy/scout/scoutRun.png", 8), scale_factor)
            self.attackRSprites = scale_sprites(load_sprites("assets/images/enemy/scout/scoutAttack.png", 3), scale_factor)
            self.walkLSprites = scale_sprites(load_sprites(imagestring=imageLwalkscout, num_frames=8, nopath=True), scale_factor)
            self.attackLSprites = scale_sprites(load_sprites("assets/images/enemy/scout/scoutAttack.png", 3), scale_factor)
            self.idleRSprites = scale_sprites(load_sprites("assets/images/enemy/scout/scoutIdle.png", 8), scale_factor)
            self.idleLSprites = scale_sprites(load_sprites("assets/images/enemy/scout/scoutIdle.png", 8), scale_factor)
            self.animation_speed = 0.15 
        elif self.enemy_type == "tnt":
            self.walkRSprites = load_sprites("assets/images/enemy/tnt/tntRun.png", 6)
            self.attackRSprites = load_sprites("assets/images/enemy/tnt/tntAttack.png", 7)
            self.walkLSprites = load_sprites(imagestring= imageLwalktnt, num_frames=6, nopath =True)
            self.attackLSprites = load_sprites("assets/images/enemy/tnt/tntAttack.png", 7)
            self.idleRSprites = load_sprites("assets/images/enemy/tnt/tntIdle.png", 6)
            self.idleLSprites = load_sprites("assets/images/enemy/tnt/tntIdle.png", 6)
            self.animation_speed = 0.15 
        elif self.enemy_type == "lancier":
            self.walkRSprites = load_sprites("assets/images/enemy/lancier/Lancier_Run.png", 6)
            self.attackRSprites = load_sprites("assets/images/enemy/lancier/Lancier_Attack.png", 3)
            self.walkLSprites = load_sprites(imagestring= imageLwalklancier, num_frames=6, nopath =True)
            self.attackLSprites = load_sprites("assets/images/enemy/lancier/Lancier_Attack_reversed.png", 3)
            self.idleRSprites = load_sprites("assets/images/enemy/lancier/Lancier_IdleR.png", 12)
            self.idleLSprites = load_sprites("assets/images/enemy/lancier/Lancier_IdleL.png", 12)
            self.animation_speed = 0.15
        elif self.enemy_type == "archer":
            self.walkRSprites = load_sprites("assets/images/enemy/archer/archerWalkR.png", 6)
            self.attackRSprites = load_sprites("assets/images/enemy/archer/archerAttackR.png", 8)
            self.walkLSprites = load_sprites(imagestring=imageLwalkarcher, num_frames=6, nopath=True)
            self.attackLSprites = load_sprites("assets/images/enemy/archer/archerAttackR.png", 8)
            self.idleRSprites = load_sprites("assets/images/enemy/archer/archerIdleR.png", 6)
            self.idleLSprites = load_sprites("assets/images/enemy/archer/archerIdleR.png", 6)
            self.animation_speed = 0.15
        elif self.enemy_type=="boss":
            self.walkRSprites = scale_sprites(load_sprites("assets/images/Boss_Run.png", 8), 5)
            self.attackRSprites = scale_sprites(load_sprites("assets/images/Boss_Attack.png", 6), 5)
            self.walkLSprites = scale_sprites(load_sprites("assets/images/Boss_Run_reversed.png", 8), 5)
            self.attackLSprites = scale_sprites(load_sprites("assets/images/Boss_Attack_reversed.png", 6), 5)
            self.idleRSprites = scale_sprites(load_sprites("assets/images/Boss_IdleR.png", 12), 5)
            self.idleLSprites = scale_sprites(load_sprites("assets/images/Boss_IdleL.png", 12), 5)
            self.deathSprites = scale_sprites(load_sprites("assets/images/Boss_Death.png", 10), 5)
            self.animation_speed = 0.05
        else:
            # fallback : un carré rouge
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))

        self.explosionFrames = load_sprites("assets/images/items/explosion.png", 11)
        self.explosion_frame_index = 0  # Index de la frame actuelle
        self.is_dead = False
        self.explosionFrames = [
            pygame.transform.scale(frame, (100, 100))  # Redimensionne chaque frame à 128x128
            for frame in load_sprites("assets/images/items/explosion.png", 11)
        ]

        # Animation courante
        self.current_frame = 0 #Index de la frame actuelle dans la liste de sprites.
        self.image = self.walkRSprites[self.current_frame] #Image actuelle du sprite affichée à l’écran.
        self.rect = self.image.get_rect(center=pos)

        # Animation
          # vitesse de défilement des frames de mouvement
        self.default_animation_speed = self.animation_speed  # Sauvegarde de la vitesse d'animation initiale (pour le stagger)
        self.frame_timer = 0 #Compte le temps pour passer à la frame suivante.

        # États possibles : "idleR", "idleL", "walkR", "walkL", "attackR", "attackL"
        self.state = "idleR" #État actuel de l'ennemi (idleR, walk, attack).
        self.attacking = False

        self.last_damage_time = 0

        self.faceRorL= "R"

        # Distance minimale entre joueur et ennemi
        self.stop_distance = 35

    def handle_state(self):
        """Gère l'état actuel de l'ennemi"""
        if self.state == "walkR":
            animate(self, self.walkRSprites, loop=True, animation_speed=self.animation_speed)
        elif self.state == "walkL":
            animate(self, self.walkLSprites, loop=True, animation_speed=self.animation_speed)
        elif self.state == "attackR":
            animate(self, self.attackRSprites, loop=False, animation_speed=self.animation_speed)
            if self.current_frame == len(self.attackRSprites) - 1 and self.frame_timer == 0:
                self.state = "idleR"
                self.attacking = False
                self.current_frame = 0
        elif self.state == "attackL":
            animate(self, self.attackLSprites, loop=False, animation_speed=self.animation_speed)
            if self.current_frame == len(self.attackLSprites) - 1 and self.frame_timer == 0:
                self.state = "idleL"
                self.attacking = False
                self.current_frame = 0
        elif self.state == "idleR":
            animate(self, self.idleRSprites, loop=True, animation_speed=self.animation_speed)
        elif self.state == "idleL":
            animate(self, self.idleLSprites, loop=True, animation_speed=self.animation_speed)


    def update(self):
        """Déplacement vers le joueur + attaque si proche"""
        # Si le boss est mort et doit jouer son animation
        if self.enemy_type == "boss" and self.is_dead:
            if self.current_frame < len(self.deathSprites):
                self.image = self.deathSprites[self.current_frame]
                self.rect = self.image.get_rect(center=self.rect.center)
                self.current_frame += 1
            else:
                self.kill()  # Supprime définitivement le boss après animation
            return

        # Animation normale
        self.handle_state()

        if self.enemy_type == "boss" and self.player.game.in_cutscene:
            # Le boss reste idle pendant les dialogues
            self.state = "idleL"
            self.handle_state()
            return
        
        if self.enemy_type == "boss" and not self.player.game.in_cutscene:
            self.player.game.spawnable = True
            self.player.game.spawn_delay = 3

        # Ennemis normaux : explosion ou destruction
        if self.is_dead:
            if self.explosion_frame_index < len(self.explosionFrames):
                self.image = self.explosionFrames[self.explosion_frame_index]
                self.rect = self.image.get_rect(center=self.rect.center)
                self.explosion_frame_index += 1
            else:
                self.kill()

        if self.is_dead:
            # Affiche l'animation d'explosion
            if self.explosion_frame_index < len(self.explosionFrames):
                self.image = self.explosionFrames[self.explosion_frame_index]
                self.explosion_frame_index += 1
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()

        if self.state == "staggered":
            if self.is_knockback:
                dx, dy = self.knockback_direction
                self.rect.x += dx * self.knockback_speed
                self.rect.y += dy * self.knockback_speed
                self.currentKB -= self.knockback_speed
                if self.currentKB <= 0:  # Fin du knockback
                    self.is_knockback = False
                    self.currentKB = self.knockback_distance
            current_time = time.time()  # Obtenir le temps actuel
            # Vérifie si le temps de stagger est écoulé
            if current_time - self.stagger_start_time >= self.stagger_timer:
                # Fin du stagger, réinitialise les vitesses
                if self.faceRorL == "L":
                    self.state = "idleL"
                else:
                    self.state = "idleR"
                self.speed = self.default_speed
                self.animation_speed = self.default_animation_speed

                # Vérifie si l'ennemi doit marcher ou rester idle
                player_x, player_y = self.player.rect.center
                enemy_x, enemy_y = self.rect.center
                distance = math.hypot(player_x - enemy_x, player_y - enemy_y)

                if distance > self.stop_distance and self.faceRorL =="L":
                    self.state = "walkL"  # Passe à l'état "walk" si trop loin
                if distance > self.stop_distance and self.faceRorL =="R":
                    self.state = "walkR"  # Passe à l'état "walk" si trop loin

        elif (self.player.state == "attackR" or self.player.state == "attackL") and self.player.rect.colliderect(self.rect):
            current_time = time.time()
            # Vérifie si l'ennemi peut prendre des dégâts (délai entre deux dégâts)
            if current_time - self.last_damage_time >= 0.5:  # Délai de 0.5 seconde
                if self.state != "staggered":
                    self.take_damage(self.player.str)
                    self.last_damage_time = current_time  # Met à jour le temps du dernier dégât
        else :
            if self.player.state == "invisible":
                if self.faceRorL == "L":
                    self.state = "idleL"
                else:
                    self.state = "idleR"
                self.question_mark_rect.center = (self.rect.centerx, self.rect.top -20)  # Position au-dessus de l'ennemi
                self.screen.blit(self.question_mark, self.question_mark_rect)
            else :
                # Position du joueur
                player_x, player_y = self.player.rect.center
                enemy_x, enemy_y = self.rect.center
                moving = False
                # Calcul du vecteur direction
                dx, dy = player_x - enemy_x, player_y - enemy_y
                distance = math.hypot(dx, dy)
                # Face direction
                if player_x < enemy_x :
                    self.faceRorL = "L"
                else :
                    self.faceRorL = "R"

                # Déplacement seulement si trop loin
                if distance > self.stop_distance:
                    dx, dy = dx / distance, dy / distance  # normalisation
                    moving=True
                    self.rect.x += dx * self.speed
                    self.rect.y += dy * self.speed

                # Vérifie si assez proche pour attaquer
                if distance <= 50 and not self.attacking:  # rayon d'attaque
                    current_time = time.time()
                    if current_time - self.last_attack_time >= 1:  # attaque toutes les secondes
                        self.attacking = True
                        if self.faceRorL == "R":
                            self.state = "attackR"
                        else :
                            self.state = "attackL"
                        self.current_frame = 0
                        self.frame_timer = 0
                        self.attack()
                        self.last_attack_time = current_time

                # Si pas en attaque, choisir l'état
                if not self.attacking:
                    if moving and self.faceRorL == "R":
                        self.state = "walkR"
                    elif moving and self.faceRorL == "L":
                        self.state = "walkL"
                    elif self.faceRorL == "R":
                        self.state = "idleR"
                    elif self.faceRorL == "L":
                        self.state = "idleL"

        # Toujours gérer l'animation selon l'état
        self.handle_state()

    def attack(self):
        """Inflige des dégâts au joueur"""
        self.player.take_damage(self.attack_points)

    def take_damage(self, amount):
        """Le joueur ou d'autres entités peuvent attaquer l'ennemi"""
        if self.enemy_type != "boss":
            self.state = "staggered"
            self.speed = 0
            self.animation_speed = 0
            self.stagger_start_time = time.time()

            player_x, player_y = self.player.rect.center
            enemy_x, enemy_y = self.rect.center
            dx, dy = enemy_x - player_x, enemy_y - player_y
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx, dy = dx / distance, dy / distance
            self.knockback_direction = (dx, dy)
            self.is_knockback = True

        self.hp -= amount
        if self.hp <= 0:
            if self.enemy_type == "boss":
                self.player.enemy_killed(5000)
                self.is_dead = True
                self.current_frame = 0  # Pour commencer l'animation Boss_Death
                self.player.game.start_boss_death_cutscene()
            else:
                self.is_dead = True
                self.explosion_frame_index = 0
                # Score
                if self.enemy_type == "pawn":
                    self.player.enemy_killed(100)
                elif self.enemy_type == "goblin":
                    self.player.enemy_killed(150)
                elif self.enemy_type == "scout":
                    self.player.enemy_killed(100)
                elif self.enemy_type == "tnt" :
                    self.player.enemy_killed(150)
                elif self.enemy_type == "archer":
                    self.player.enemy_killed(150)
                elif self.enemy_type == "lancier":
                    self.player.enemy_killed(200)

