import pygame
import math
import time
from PIL import Image, ImageOps
from utilitaire import load_sprites, animate, scale_sprites

# Dictionnaire contenant les statistiques des différents types d'ennemis
ENEMY_STATS = {
    "pawn": {
        "hp": 1,
        "speed": 2,
        "attack_points": 1,
        "stagger_timer": 0.3,
        "knockback_distance": 50,
        "knockback_speed": 5,
    },
    "goblin": {
        "hp": 2,
        "speed": 4,
        "attack_points": 1,
        "stagger_timer": 0.5,
        "knockback_distance": 100,
        "knockback_speed": 5,
    },
    "scout": {
        "hp": 1,
        "speed": 7,
        "attack_points": 1,
        "stagger_timer": 0.5,
        "knockback_distance": 250,
        "knockback_speed": 100,
    },
    "tnt": {
        "hp": 3,
        "speed": 2.5,
        "attack_points": 2,
        "stagger_timer": 0.4,
        "knockback_distance": 60,
        "knockback_speed": 10,
    },
    "archer": {
        "hp": 2,
        "speed": 2,
        "attack_points": 2,
        "stagger_timer": 0.5,
        "knockback_distance": 50,
        "knockback_speed": 10,
    },
    "lancier": {
        "hp": 3,
        "speed": 1.5,
        "attack_points": 1,
        "stagger_timer": 0.2,
        "knockback_distance": 40,
        "knockback_speed": 5,
    },
    "boss": {
        "hp": 50,
        "speed": 4,
        "attack_points": 2,
        "stagger_timer": 0.5,
        "knockback_distance": 10,
        "knockback_speed": 3,
    }
}

ENEMY_SPRITES = {
    "pawn": {
        "walkR": ("assets/images/enemy/pawn/Pawn_Run.png", 6, False, 1),
        "attackR": ("assets/images/enemy/pawn/Pawn_Attack.png", 6, False, 1),
        "walkL": ("assets/images/enemy/pawn/Pawn_Run.png", 6, True, 1),
        "attackL": ("assets/images/enemy/pawn/Pawn_Attack_reversed.png", 6, False, 1),
        "idleR": ("assets/images/enemy/pawn/Pawn_IdleR.png", 6, False, 1),
        "idleL": ("assets/images/enemy/pawn/Pawn_IdleL.png", 6, False, 1),
        "animation_speed": 0.15
    },
    "goblin": {
        "walkR": ("assets/images/enemy/goblin/Goblin_Run.png", 6, False, 1),
        "attackR": ("assets/images/enemy/goblin/Goblin_Attack.png", 6, False, 1),
        "walkL": ("assets/images/enemy/goblin/Goblin_Run.png", 6, True, 1),
        "attackL": ("assets/images/enemy/goblin/Goblin_Attack_reversed.png", 6, False, 1),
        "idleR": ("assets/images/enemy/goblin/Goblin_IdleR.png", 7, False, 1),
        "idleL": ("assets/images/enemy/goblin/Goblin_IdleL.png", 7, False, 1),
        "animation_speed": 0.15
    },
    "scout": {
        "walkR": ("assets/images/enemy/scout/scoutRun.png", 8, False, 3),
        "attackR": ("assets/images/enemy/scout/scoutAttack.png", 3, False, 3),
        "walkL": ("assets/images/enemy/scout/scoutRun.png", 8, True, 3),
        "attackL": ("assets/images/enemy/scout/scoutAttack.png", 3, False, 3),
        "idleR": ("assets/images/enemy/scout/scoutIdle.png", 8, False, 3),
        "idleL": ("assets/images/enemy/scout/scoutIdle.png", 8, False, 3),
        "animation_speed": 0.15
    },
    "tnt": {
        "walkR": ("assets/images/enemy/tnt/tntRun.png", 6, False, 1),
        "attackR": ("assets/images/enemy/tnt/tntAttack.png", 7, False, 1),
        "walkL": ("assets/images/enemy/tnt/tntRun.png", 6, True, 1),
        "attackL": ("assets/images/enemy/tnt/tntAttack.png", 7, False, 1),
        "idleR": ("assets/images/enemy/tnt/tntIdle.png", 6, False, 1),
        "idleL": ("assets/images/enemy/tnt/tntIdle.png", 6, False, 1),
        "animation_speed": 0.15
    },
    "lancier": {
        "walkR": ("assets/images/enemy/lancier/Lancier_Run.png", 6, False, 1),
        "attackR": ("assets/images/enemy/lancier/Lancier_Attack.png", 3, False, 1),
        "walkL": ("assets/images/enemy/lancier/Lancier_Run.png", 6, True, 1),
        "attackL": ("assets/images/enemy/lancier/Lancier_Attack_reversed.png", 3, False, 1),
        "idleR": ("assets/images/enemy/lancier/Lancier_IdleR.png", 12, False, 1),
        "idleL": ("assets/images/enemy/lancier/Lancier_IdleL.png", 12, False, 1),
        "animation_speed": 0.15
    },
    "archer": {
        "walkR": ("assets/images/enemy/archer/archerWalkR.png", 6, False, 1),
        "attackR": ("assets/images/enemy/archer/archerAttackR.png", 8, False, 1),
        "walkL": ("assets/images/enemy/archer/archerWalkR.png", 6, True, 1),
        "attackL": ("assets/images/enemy/archer/archerAttackR.png", 8, False, 1),
        "idleR": ("assets/images/enemy/archer/archerIdleR.png", 6, False, 1),
        "idleL": ("assets/images/enemy/archer/archerIdleR.png", 6, False, 1),
        "animation_speed": 0.15
    },
    "boss": {
        "walkR": ("assets/images/enemy/boss/Boss_Run.png", 8, False, 5),
        "attackR": ("assets/images/enemy/boss/Boss_Attack.png", 6, False, 5),
        "walkL": ("assets/images/enemy/boss/Boss_Run_reversed.png", 8, False, 5),
        "attackL": ("assets/images/enemy/boss/Boss_Attack_reversed.png", 6, False, 5),
        "idleR": ("assets/images/enemy/boss/Boss_IdleR.png", 12, False, 5),
        "idleL": ("assets/images/enemy/boss/Boss_IdleL.png", 12, False, 5),
        "death": ("assets/images/enemy/boss/Boss_Death.png", 10, False, 5),
        "animation_speed": 0.05
    }
}

class Enemy(pygame.sprite.Sprite):
    """
    Représente un ennemi dans le jeu.

    Chaque ennemi hérite de pygame.sprite.Sprite et possède :
    - Des stats propres (HP, vitesse, dégâts…)
    - Des animations (idle, walk, attack, death)
    - Une IA simple (suivi du joueur, attaque à distance rapprochée)
    - Un comportement spécifique en cas de mort (explosion ou cutscene pour le boss)

    Args:
        enemy_type (str): Type d'ennemi (clé dans ENEMY_STATS et ENEMY_SPRITES).
        player (Player): Référence au joueur.
        screen (pygame.Surface): Surface d’affichage.
        pos (tuple[int, int], optional): Position initiale. Par défaut (0, 0).

    Attributs principaux :
        hp (int): Points de vie.
        speed (float): Vitesse de déplacement.
        attack_points (int): Dégâts infligés au joueur.
        state (str): État actuel de l’ennemi (idleR, walkL, attackR, etc.).
        is_dead (bool): True si l’ennemi est mort.
        attacking (bool): True si l’ennemi est en train d’attaquer.
        faceRorL (str): Direction ("R" ou "L").
        explosionFrames (list[Surface]): Frames d’explosion (non-boss).
        deathSprites (list[Surface]): Animation de mort (boss).
    """
    def __init__(self, enemy_type, player, screen, pos=(0, 0)):
        super().__init__()
        self.enemy_type = enemy_type
        self.player = player
        self.screen = screen
        self.last_attack_time = 0

        # Charger les stats de l'ennemi à partir du dictionnaire
        self.load_stats()
        self.load_common_assets()
        self.load_sprites()

        self.is_dead = False
        self.explosion_frame_index = 0
        self.explosionFrames = [
            pygame.transform.scale(frame, (100, 100))
            for frame in load_sprites("assets/images/items/explosion.png", 11)
        ]

        self.current_frame = 0
        self.image = self.walkRSprites[self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        self.default_animation_speed = self.animation_speed
        self.frame_timer = 0
        self.state = "idleR"
        self.attacking = False
        self.last_damage_time = 0
        self.faceRorL = "R"
        self.stop_distance = 35

    def load_stats(self):
        stats = ENEMY_STATS.get(self.enemy_type)
        if stats:
            self.hp = stats["hp"]
            self.speed = stats["speed"]
            self.attack_points = stats["attack_points"]
            self.stagger_timer = stats["stagger_timer"]
            self.knockback_distance = stats["knockback_distance"]
            self.knockback_speed = stats["knockback_speed"]
        else:
            raise ValueError("Type d'ennemi inconnu")

        self.currentKB = self.knockback_distance
        self.default_speed = self.speed

    def load_common_assets(self):
        self.question_mark = pygame.image.load("assets/images/ressources/question_mark.png").convert_alpha()
        self.question_mark = pygame.transform.scale(self.question_mark, (30, 30))
        self.question_mark_rect = self.question_mark.get_rect()

    def load_sprites(self):
        sprite_data = ENEMY_SPRITES.get(self.enemy_type, {})

        # Charger les sprites selon le type
        for state, sprite_info in sprite_data.items():
            if state == "animation_speed":  # Gérer la vitesse d'animation séparément
                self.animation_speed = sprite_info
                continue

            path, frames, mirror, scale_factor = sprite_info
            if mirror:
                image = Image.open(path)
                mirrored_image = ImageOps.mirror(image)
                sprites = load_sprites(imagestring=mirrored_image, num_frames=frames, nopath=True)
            else:
                sprites = load_sprites(path, frames)

            if scale_factor is not None and scale_factor != 1:
                sprites = scale_sprites(sprites, scale_factor)

            # Assigner les sprites à l'instance
            if state == "walkR":
                self.walkRSprites = sprites
            elif state == "walkL":
                self.walkLSprites = sprites
            elif state == "attackR":
                self.attackRSprites = sprites
            elif state == "attackL":
                self.attackLSprites = sprites
            elif state == "idleR":
                self.idleRSprites = sprites
            elif state == "idleL":
                self.idleLSprites = sprites
            elif state == "death":
                self.deathSprites = sprites

    def handle_state(self):
        sprite_map = {
            "walkR": (self.walkRSprites, True),
            "walkL": (self.walkLSprites, True),
            "attackR": (self.attackRSprites, False),
            "attackL": (self.attackLSprites, False),
            "idleR": (self.idleRSprites, True),
            "idleL": (self.idleLSprites, True),
        }

        sprite_info = sprite_map.get(self.state)
        if sprite_info:
            sprites, loop = sprite_info
            animate(self, sprites, loop=loop, animation_speed=self.animation_speed)

            if not loop and self.current_frame == len(sprites) - 1 and self.frame_timer == 0:
                idle_state = "idleR" if self.state.endswith("R") else "idleL"
                self.state = idle_state
                self.attacking = False
                self.current_frame = 0

    def update(self):
        if self.enemy_type == "boss" and self.is_dead:
            self.handle_boss_death()
            return

        self.handle_state()

        if self.enemy_type == "boss" and self.player.game.in_cutscene:
            self.state = "idleL"
            self.handle_state()
            return

        if self.is_dead:
            self.handle_death()

        if self.state == "staggered":
            self.handle_stagger()
        elif (self.player.state == "attackR" or self.player.state == "attackL") and self.player.rect.colliderect(self.rect):
            self.handle_player_attack()
        else:
            self.handle_movement_and_attack()

    def handle_boss_death(self):
        if self.current_frame < len(self.deathSprites):
            self.image = self.deathSprites[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.current_frame += 1
        else:
            self.kill()

    def handle_death(self):
        if self.explosion_frame_index < len(self.explosionFrames):
            self.image = self.explosionFrames[self.explosion_frame_index]
            self.rect = self.image.get_rect(center=self.rect.center)
            self.explosion_frame_index += 1
        else:
            self.kill()

    def handle_stagger(self):
        if getattr(self, 'is_knockback', False):
            dx, dy = getattr(self, 'knockback_direction', (0, 0))
            self.rect.x += dx * self.knockback_speed
            self.rect.y += dy * self.knockback_speed
            self.currentKB -= self.knockback_speed
            if self.currentKB <= 0:
                self.is_knockback = False
                self.currentKB = self.knockback_distance

        current_time = time.time()
        if current_time - getattr(self, 'stagger_start_time', 0) >= self.stagger_timer:
            self.reset_from_stagger()

    def reset_from_stagger(self):
        if self.faceRorL == "L":
            self.state = "idleL"
        else:
            self.state = "idleR"
        self.speed = self.default_speed
        self.animation_speed = self.default_animation_speed
        self.check_distance_and_move()

    def handle_player_attack(self):
        current_time = time.time()
        if current_time - self.last_damage_time >= 0.5:
            if self.state != "staggered":
                self.take_damage(self.player.str)
                self.last_damage_time = current_time

    def handle_movement_and_attack(self):
        if self.player.invisible :
            self.handle_invisible_player()
        else:
            self.handle_visible_player()

    def handle_invisible_player(self):
        if self.faceRorL == "L":
            self.state = "idleL"
        else:
            self.state = "idleR"
        self.question_mark_rect.center = (self.rect.centerx, self.rect.top - 20)
        self.screen.blit(self.question_mark, self.question_mark_rect)

    def handle_visible_player(self):
        player_x, player_y = self.player.rect.center
        enemy_x, enemy_y = self.rect.center
        moving = False

        dx, dy = player_x - enemy_x, player_y - enemy_y
        distance = math.hypot(dx, dy)

        if player_x < enemy_x:
            self.faceRorL = "L"
        else:
            self.faceRorL = "R"

        if distance > self.stop_distance:
            dx, dy = dx / distance, dy / distance
            moving = True
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        if distance <= 50 and not self.attacking:
            current_time = time.time()
            if current_time - self.last_attack_time >= 1:
                self.start_attack()

        if not self.attacking:
            self.set_state_based_on_movement(moving)

    def set_state_based_on_movement(self, moving):
        if moving and self.faceRorL == "R":
            self.state = "walkR"
        elif moving and self.faceRorL == "L":
            self.state = "walkL"
        elif self.faceRorL == "R":
            self.state = "idleR"
        elif self.faceRorL == "L":
            self.state = "idleL"

    def start_attack(self):
        self.attacking = True
        if self.faceRorL == "R":
            self.state = "attackR"
        else:
            self.state = "attackL"
        self.current_frame = 0
        self.frame_timer = 0
        self.attack()
        self.last_attack_time = time.time()

    def check_distance_and_move(self):
        player_x, player_y = self.player.rect.center
        enemy_x, enemy_y = self.rect.center
        distance = math.hypot(player_x - enemy_x, player_y - enemy_y)
        if distance > self.stop_distance and self.faceRorL == "L":
            self.state = "walkL"
        elif distance > self.stop_distance and self.faceRorL == "R":
            self.state = "walkR"

    def attack(self):
        """Inflige des dégâts au joueur"""
        self.player.take_damage(self.attack_points)

    def take_damage(self, amount):
        """Le joueur peut attaquer l'ennemi"""
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
            self.handle_death_by_type()

    def handle_death_by_type(self):
        if self.enemy_type == "boss":
            self.player.enemy_killed(5000)
            self.is_dead = True
            self.current_frame = 0
            self.player.game.start_boss_death_cutscene()
        else:
            self.is_dead = True
            self.explosion_frame_index = 0
            score_map = {
                "pawn": 100,
                "goblin": 150,
                "scout": 100,
                "tnt": 150,
                "archer": 150,
                "lancier": 200,
            }
            self.player.enemy_killed(score_map.get(self.enemy_type, 0))
