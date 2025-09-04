# main.py
import pygame
from game import Game
from menu import Menu  
from credits import Credits
from settings import WIDTH, HEIGHT

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        # Lancer le menu
        menu = Menu(screen)
        menu.run()

        # Lancer les crédits
        if menu.show_credits:
            c = Credits(screen)
            c.run()  # d'abord on exécute les crédits

            if c.retour:  
                # retour au menu sans quitter la boucle principale
                continue  
            else:
                # si on a quitté autrement -> fermer le programme
                running = False
                break

        if not menu.start_game:  # si le joueur a fermé la fenêtre
            running = False
            break

        # Lancer le jeu
        g = Game()
        g.new()

        # Si le joueur est mort -> retour menu
        if g.game_over:
            continue  # reboucle sur Menu
        else:
            running = False  # sinon on arrête tout

    pygame.quit()
