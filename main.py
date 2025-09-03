# main.py
import pygame
from game import Game
from menu import Menu  
from settings import WIDTH, HEIGHT

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


    # Lancer le menu  
    menu = Menu(screen)
    menu.run()

    # Si le joueur clique sur Start -> lancer le jeu
    if menu.start_game:
        g = Game()
        g.new()

    pygame.quit()
