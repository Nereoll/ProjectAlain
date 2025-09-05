import pygame
from settings import WIDTH, ATH_HEIGHT, BLACK, WHITE
from utilitaire import load_sprites, load_sprites_from_folder, animate

class Ath(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        
        # === Font ===
        self.font_title = pygame.font.Font("assets/fonts/GenAR102.TTF", 40)

        # === Player ===
        self.player = player
        
        # === Surface principale ===
        self.image = pygame.Surface((WIDTH, ATH_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))

        # === Sprites ===
        # Life
        self.fullLife = load_sprites_from_folder("assets/images/ath/fulllife")
        self.almostHalfLife = load_sprites_from_folder("assets/images/ath/almosthalflife")
        self.halflife = load_sprites_from_folder("assets/images/ath/halflife")
        self.onelife = load_sprites_from_folder("assets/images/ath/onelife")
        self.death = load_sprites_from_folder("assets/images/ath/death")

        # Mana
        self.noMana = load_sprites("assets/images/ath/noMana.png", 1)
        self.oneMana = load_sprites("assets/images/ath/oneMana.png", 1)
        self.halfMana = load_sprites("assets/images/ath/halfMana.png", 1)
        self.almostHalfMana = load_sprites("assets/images/ath/almostHalfMana.png", 1)
        self.fullMana = load_sprites("assets/images/ath/fullMana.png", 1)

        # Augmenter les tailles des sprites
        self.fullLife = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.fullLife]
        self.almostHalfLife = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.almostHalfLife]
        self.halflife = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.halflife]
        self.onelife = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.onelife]
        self.death = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.death]
        #/////
        self.noMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.noMana]
        self.oneMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.oneMana]
        self.halfMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.halfMana]
        self.almostHalfMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.almostHalfMana]
        self.fullMana = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in self.fullMana]

        # === Animation ===
        self.current_frame = 0
        self.animation_speed = 0.15
        self.frame_timer = 0
        self.current_sprite = None  # frame courante

    def update(self):
        # === Gestion des HP ===
        player_hp = self.player.hp
        if player_hp == 4:
            animate(self, self.fullLife, loop=True, assign_to_image=False)
        elif player_hp == 3:
            animate(self, self.almostHalfLife, loop=True, assign_to_image=False)
        elif player_hp == 2:
            animate(self, self.halflife, loop=True, assign_to_image=False)
        elif player_hp == 1:
            animate(self, self.onelife, loop=True, assign_to_image=False)
        elif player_hp <= 0:
            animate(self, self.death, loop=True, assign_to_image=False)

        # === Gestion du Mana ===
        player_mana = self.player.mana 
        if player_mana == 0:
            mana_sprite = self.noMana[0]
        elif player_mana == 1:
            mana_sprite = self.oneMana[0]
        elif player_mana == 2:
            mana_sprite = self.halfMana[0]
        elif player_mana == 3:
            mana_sprite = self.almostHalfMana[0]
        else:
            mana_sprite = self.fullMana[0]
        
        # === Redessiner l'ATH ===
        self.image.fill(BLACK)

        # HP - à gauche
        if self.current_sprite:
            rect_hp = self.current_sprite.get_rect(midleft=(40, self.rect.centery))
            self.image.blit(self.current_sprite, rect_hp)
            
        # Score - au milieu
        score_text = self.font_title.render(f"Score: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.rect.width // 2, 40))
        self.image.blit(score_text, score_rect)

        # Mana → à droite
        if mana_sprite:
            rect_mana = mana_sprite.get_rect(midright=(self.rect.width - 40, self.rect.centery))
            self.image.blit(mana_sprite, rect_mana)
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)