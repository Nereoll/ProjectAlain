"""
main.py

Point d'entrée du jeu.
Gère la boucle principale entre le menu, les crédits et le lancement du jeu.
"""

import pygame
from game import Game
from menu import Menu
from credits import Credits
from lore import Lore
from settings import WIDTH, HEIGHT, TITLE
from utilitaire import chemin_relatif

def main():
    """
    Fonction principale du programme.

    - Initialise Pygame et la fenêtre.
    - Affiche le menu principal.
    - Permet d'accéder aux crédits.
    - Lance une partie si le joueur choisit de jouer.
    - Termine l'application si le joueur quitte depuis le menu ou les crédits.
    """
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    icon = pygame.image.load(chemin_relatif("assets/images/icon.ico"))
    pygame.display.set_icon(icon)

    fullscreen = False
    running = True

    while running:
        # Lancer le menu
        menu = Menu(screen, fullscreen)
        menu.run()
        fullscreen = menu.fullscreen


        if fullscreen:
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Lancer les crédits si nécessaire
        if menu.show_credits:
            credits = Credits(screen, fullscreen)
            credits.run()
            if credits.retour:  # Si on retourne au menu, continuer
                continue
            else:  # Si on ne retourne pas au menu, quitter le programme
                running = False
                break
        
        # Lancer le lore si nécessaire
        if menu.show_lore:
            lore = Lore(screen, fullscreen)
            lore.run()
            if lore.retour:  # Si on retourne au menu, continuer
                continue
            else:  # Si on ne retourne pas au menu, quitter le programme
                running = False
                break

        # Vérifier si le jeu doit démarrer
        if not menu.start_game:  # Si le menu est fermé sans lancer le jeu
            running = False
            break

        # Lancer le jeu en mode approprié
        game_mode = menu.start_game_infinite
        if not start_game(screen, fullscreen, game_mode):
            running = False

    pygame.quit()

def start_game(screen, fullscreen, is_dungeon=False):
    g = Game(screen, fullscreen, isDungeon=is_dungeon)
    g.new()
    return g.game_over  # Retourne True pour continuer (game over), False pour quitter

if __name__ == "__main__":
    main()
