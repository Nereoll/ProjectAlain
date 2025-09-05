"""
player.py

Définit la classe Player, représentant le personnage jouable.

Le joueur peut se déplacer, attaquer, devenir invisible, prendre des dégâts,
et interagir avec son environnement. La classe gère :
- les sprites et animations (idle, marche, attaque, invisible, mort),
- les contrôles clavier et manette,
- les points de vie, mana et score,
- les sons associés (attaques, pas, dégâts, mort).
"""
import pygame
import time
from settings import WIDTH, HEIGHT, GAME_ZONE_BOTTOM, GAME_ZONE_LEFT, GAME_ZONE_RIGHT, GAME_ZONE_TOP
from PIL import Image , ImageOps
from utilitaire import load_sprites, animate, SoundEffects

class Player(pygame.sprite.Sprite):
    """
    Classe représentant le joueur.

    Attributes:
        game (Game | None): Référence optionnelle au jeu en cours.
        image (pygame.Surface): Sprite actuel affiché.
        rect (pygame.Rect): Zone de collision du joueur.
        mask (pygame.Mask): Masque pour collisions pixel-perfect.
        hp (int): Points de vie du joueur.
        mana (int): Ressource consommée pour l’invisibilité.
        score (int): Score du joueur.
        state (str): État actuel ("idleR", "walkL", "attackR", "invisible", "dead", ...).
        attacking (bool): Indique si le joueur est en train d’attaquer.
        invisible (bool): Indique si le joueur est invisible.
        is_invulnerable (bool): Indique si le joueur est temporairement invulnérable.
        joystick (pygame.joystick.Joystick | None): Manette détectée (si disponible).
    """
    def __init__(self, game=None):
        super().__init__()
        self.game = game

        # Miror srite
        imageLwalk = ImageOps.mirror(Image.open("assets/images/player/Warrior_Run.png"))
        imageLattack = ImageOps.mirror(Image.open("assets/images/player/Warrior_Attack2.png"))
        imageLidle = ImageOps.mirror(Image.open("assets/images/player/Warrior_Idle.png"))


        # === Sprites ===
        self.walkRSprites = load_sprites("assets/images/player/Warrior_Run.png", 6) # 6 frames d'animation
        self.idleRSprites = load_sprites("assets/images/player/Warrior_Idle.png",8)
        self.walkLSprites = load_sprites(imagestring= imageLwalk,num_frames=6, nopath =True)
        self.attackRSprites = load_sprites("assets/images/player/Warrior_Attack2.png", 4)
        self.attackLSprites = load_sprites(imagestring= imageLattack, num_frames= 4, nopath =True)
        self.idleLSprites = load_sprites(imagestring= imageLidle, num_frames= 8, nopath =True)
        self.invisibleSprite = load_sprites("assets/images/items/Foam.png", 8)

        # Animation courante
        self.current_frame = 0 #Index de la frame actuelle dans la liste de sprites.
        self.image = self.walkLSprites[self.current_frame] #Image actuelle du sprite affichée à l’écran.
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2)) #Rectangle qui définit la position et la taille du sprite.
        self.original_rect = self.rect.copy()

        # Pixel perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        # Cooldown d'attaque
        self.last_attack_time = 0  # Temps de la dernière attaque
        self.attack_cooldown = 0.65 # Cooldown en secondes

        # Frame d'invulnérabilité
        self.iframe_duration = 1 # temps en secondes
        self.iframe_start_time = 0
        self.is_invulnerable = False  # Indique si le joueur est invulnérable
        self.blink_timer = 0

        # Variables de déplacement
        self.speed = 5

        # Animation
        self.animation_speed = 0.15   # vitesse de défilement des frames de mouvement
        self.frame_timer = 0 #Compte le temps pour passer à la frame suivante.

        # États possibles : "idleR", "idleL", "walkR", "walkL", "attackR", "attackL", "invisible", "dead"
        self.state = "idleR" #État actuel du joueur (idle, walk, attack, invisible).
        self.attacking = False
        self.invisible = False
        self.invisible_start_time = 0
        self.invisible_duration = 2  # secondes
        # Ne pas équilibrer les power ups ici
        self.damageAmpStart = 0
        self.damageAmpValue = 0
        self.damageAmpDuration = 0

        self.invisibilityDurationLeft = 0

        # Stats
        self.hp = 4
        self.mana = 40000
        self.score = 0

        #initialisation sons
        self.sound = SoundEffects()

        self.sound.load_sound_group("sword_swings", [ 
            "assets/sounds/sound_effects/sword_swing_1.ogg",
            "assets/sounds/sound_effects/sword_swing_2.ogg",
            "assets/sounds/sound_effects/sword_swing_3.ogg",
            "assets/sounds/sound_effects/sword_swoosh_1.ogg"
        ]) # sons attaque du joueur

        self.sound.load_sound_group("player_hurts", [
            "assets/sounds/sound_effects/hit_1.ogg",
            "assets/sounds/sound_effects/hit_2.ogg",
            "assets/sounds/sound_effects/hit_3.ogg"
        ]) #sons dégat joueur

        self.sound.load_sound_group("footstep_stone", [
            "assets/sounds/sound_effects/footstep_stone_1.ogg",
            "assets/sounds/sound_effects/footstep_stone_2.ogg",
            "assets/sounds/sound_effects/footstep_stone_3.ogg"
        ]) #sons pas lvl 1

        # Initialisation manette si dispo
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print("Manette détectée :", self.joystick.get_name())

        # Direction face
        self.faceRorL = "R"

    def handle_keys(self):
            keys = pygame.key.get_pressed()
            moving = False

            # ============================================
            # Controle Clavier
            # ============================================
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.rect.x -= self.speed
                moving = True
                self.faceRorL = "L"
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += self.speed
                moving = True
                self.faceRorL = "R"
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.rect.y -= self.speed
                moving = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += self.speed
                moving = True

            # Empêche le joueur de sortir de la fenêtre
            if self.rect.left < GAME_ZONE_LEFT:
                self.rect.left = GAME_ZONE_LEFT
            if self.rect.right > GAME_ZONE_RIGHT:
                self.rect.right = GAME_ZONE_RIGHT
            if self.rect.top < GAME_ZONE_TOP:
                self.rect.top = GAME_ZONE_TOP
            if self.rect.bottom > GAME_ZONE_BOTTOM:
                self.rect.bottom = GAME_ZONE_BOTTOM

            # === Déclenchement invisibilité ===
            if keys[pygame.K_LSHIFT] and not self.invisible and self.mana >= 4:
                self.invisible = True
                self.invisible_start_time = time.time()
                self.mana -=4

            # === Déclenchement attaque ===
            if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and not self.attacking and not self.invisible and self.faceRorL == "L":
                current_time = time.time()
                if current_time - self.last_attack_time >= self.attack_cooldown:  # Vérifie le cooldown
                    self.state = "attackL"
                    self.attacking = True
                    self.current_frame = 0
                    self.frame_timer = 0
                    self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque
            elif (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and not self.attacking and not self.invisible and self.faceRorL == "R":
                current_time = time.time()
                if current_time - self.last_attack_time >= self.attack_cooldown:  # Vérifie le cooldown
                    self.state = "attackR"
                    self.attacking = True
                    self.current_frame = 0
                    self.frame_timer = 0
                    self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque

            # ============================================
            # Controle Manette
            # ============================================

            if self.joystick :
                # Stick gauche
                axis_x = self.joystick.get_axis(0)  # -1 = gauche, +1 = droite
                axis_y = self.joystick.get_axis(1)  # -1 = haut,   +1 = bas
                axis_rt= self.joystick.get_axis(5)  # gachette gauche

                if (self.joystick.get_button(0) or axis_rt > 0.5 ) and not self.attacking and not self.invisible and self.faceRorL == "L":
                    current_time = time.time()
                    if current_time - self.last_attack_time >= self.attack_cooldown:  # Vérifie le cooldown
                        self.state = "attackL"
                        self.attacking = True
                        self.current_frame = 0
                        self.frame_timer = 0
                        self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque
                
                if (self.joystick.get_button(0) or axis_rt > 0.5) and not self.attacking and not self.invisible and self.faceRorL == "R":
                    current_time = time.time()
                    if current_time - self.last_attack_time >= self.attack_cooldown:  # Vérifie le cooldown
                        self.state = "attackR"
                        self.attacking = True
                        self.current_frame = 0
                        self.frame_timer = 0
                        self.last_attack_time = current_time  # Met à jour le temps de la dernière attaque

                if ( self.joystick.get_button(4) or self.joystick.get_button(2) )  and not self.invisible and self.mana >= 4:
                    self.invisible = True 
                    self.invisible_start_time = time.time()
                    self.mana -=4

                # Deadzone (évite les petits tremblements du stick)
                # Droite
                if axis_x > 0.5 :
                    self.rect.x += self.speed
                    moving = True
                    self.faceRorL = "R"
                # Gauche
                if axis_x < -0.5 :
                    self.rect.x -= self.speed
                    moving = True
                    self.faceRorL = "L" 
                # Haut / Bas
                if abs(axis_y) > 0.2:
                    self.rect.y += int(axis_y * self.speed)
                    moving = True


            
            if not moving and not self.attacking and not self.invisible and self.faceRorL == "L":
                self.state = "idleL"
            elif not moving and not self.attacking and not self.invisible and self.faceRorL == "R":
                self.state = "idleR"
            elif moving and not self.attacking and not self.invisible and self.faceRorL == "L":
                self.state = "walkL"
            elif moving and not self.attacking and not self.invisible and self.faceRorL == "R":
                self.state = "walkR"


    def update(self):
        """Mets à jour le joueur

        - update est appelée à chaque frame du jeu.
        - Elle traite l'input, met à jour l'état et l'animation.

        - Walk : animation en boucle.
        - Attack : animation non bouclée. Quand l'attaque finit, on revient à idle.
        - Idle : on prend juste la première frame de marche.
        - Invisible : on prend la frame d'invisibilité.
        """

        # print((str)(self.invisibilityDurationLeft) + " | " + (str)(self.state))
        
        # Vérifie si l’invisibilité est terminée
        self.invisibilityDurationLeft = 2 - (time.time() - self.invisible_start_time)
        if self.invisibilityDurationLeft < 0 :
            self.invisible = False

        # Vérifie si le joueur est dans une cutscene (si game est défini)
        # Vérifie si le joueur est dans une cutscene et ce n'est pas la mort du boss
        if self.game and getattr(self.game, "in_cutscene", False):
            if not (self.game.boss and getattr(self.game.boss, "is_dead", False)):
                self.state = "idleR"
                return


        if self.state == "dead" :
            if self.faceRorL == "R" :
                animate(self, self.idleRSprites, loop=True)
            elif self.faceRorL == "L" :
                animate(self, self.idleLSprites, loop=True)
        else:
            self.handle_keys()

        if time.time() - self.damageAmpStart >= 2 :
            self.str = 1

        # Gérer les iframes
        if self.is_invulnerable:

            current_time = time.time()
            # Clignotement visuel
            self.blink_timer += self.animation_speed
            if self.blink_timer >= 0.25:  # Change de visibilité toutes les 0.1 secondes
                self.blink_timer = 0
                if self.image.get_alpha() == 255:
                    self.image.set_alpha(100)  # Rend le joueur semi-transparent
                else:
                    self.image.set_alpha(255)  # Rétablit l'opacité normale

            # Vérifie si les iframes sont terminées
            if current_time - self.iframe_start_time >= self.iframe_duration:
                self.is_invulnerable = False
                self.iframe_duration = 1
                self.image.set_alpha(255)  # Rétablit l'opacité normale
        else :
            self.image.set_alpha(255)

        # Animation selon l’état
        if self.invisible :
            animate(self, self.invisibleSprite, loop=True)
            # Rendre translucide
            self.image.set_alpha(10)
        elif self.state == "walkR":
            animate(self, self.walkRSprites, loop=True)
            self.sound.play_group("footstep_stone", 0.2, 0.4)
            self.image.set_alpha(255)  # normal
        elif self.state == "walkL" :
            animate(self, self.walkLSprites, loop=True)
            self.sound.play_group("footstep_stone", 0.2, 0.4)
            self.image.set_alpha(255)  # normal
        elif self.state == "attackR":
            animate(self, self.attackRSprites, loop=False)
            self.sound.play_group("sword_swings", 0.2)
            self.image.set_alpha(255)  # normal
            # Quand l'animation d'attaque est terminée
            if self.current_frame == len(self.attackRSprites) - 1 and self.frame_timer == 0:
                self.state = "idleR"
                self.attacking = False
                self.current_frame = 0
        elif self.state == "attackL":
            animate(self, self.attackLSprites, loop=False)
            self.sound.play_group("sword_swings", 0.2)
            self.image.set_alpha(255)  # normal
            # Quand l'animation d'attaque est terminée
            if self.current_frame == len(self.attackLSprites) - 1 and self.frame_timer == 0:
                self.state = "idleL"
                self.attacking = False
                self.current_frame = 0
        elif self.state == "idleR" :
            animate(self, self.idleRSprites, loop=True)
        elif self.state == "idleL" :
            animate(self, self.idleLSprites, loop=True)

    def take_damage(self, amount):
        if not self.is_invulnerable and self.state != "dead":  # Vérifie si le joueur est invulnérable ou mort
            self.hp -= amount
            self.sound.play_group("player_hurts", 0.2)
            if self.hp <= 0:
                self.state = "dead"
                self.sound.play_one("assets/sounds/sound_effects/player_death.ogg", volume=0.4)
            else:
                # Active les iframes
                self.is_invulnerable = True
                self.iframe_start_time = time.time()  # Enregistre le début des iframes

        def died(self):
            if self.hp <=0:
                print("Game Over")
                return True
            return False

    def enemy_killed(self, points):
        #self.sound.play_one("assets/sounds/sound_effects/mob_death.ogg", volume=1)
        self.score += points
        if self.mana < 4:
            self.mana += 1
