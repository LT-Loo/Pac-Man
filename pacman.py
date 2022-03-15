"""This module determines which page to switch upon
   user's request."""

import pygame

from Menu import *
from Help import *
from Game import *
from Configure import *

## Main program - Run screens
def main():
    pygame.init() # Initialize pygame modules
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("PAC-MAN")
    
    # Create pages
    startUpPage = Menu()
    helpPage = Help()
    mapPage = Configure()

    clock = pygame.time.Clock()
    running = True
    buffer = True
    random = False
    nav = "START" # Start up page as initial screen

    while running:
        temp = nav
        if "START" in nav: # Start up page
            if nav == "START": # Show start up page
                startUpPage.display(screen)
                nav = startUpPage.eventControl()  
            elif nav == "RESTART": nav = "GAME" # Restart game

            if nav == "GAME":
                buffer = True
                game = Game(random) # Create game
                currLife = lifeLeft = 3

        elif nav == "GAME": # Show game page and run game
            if buffer: # Countdown before game starts
                for i in range(3, -1, -1):
                    game.display(screen, True, i)
                    pygame.time.delay(1000)    
                buffer = False
            else: # Game runs after countdown
                game.display(screen)
                if lifeLeft < currLife:
                    currLife = lifeLeft
                    pygame.time.delay(3000)
                nav, lifeLeft = game.runGame()

            clock.tick(50)
        
        elif nav == "HELP": # Help page
            helpPage.display(screen)
            nav = helpPage.eventControl()

        elif nav == "MAP": # Configure / Map selection page
            mapPage.display(screen)
            nav, random = mapPage.eventControl()

        elif nav == "QUIT": break # Quit game and terminate program

        if not nav: nav = temp # If NoneType is returned
        
    pygame.quit()


if __name__ == '__main__': main()