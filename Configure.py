"""This module creates the Configure Page of the game program.
   It allows user to select desired type of map."""

import pygame
from Layout import *

SCREEN_W = 800
SCREEN_H = 600
SIZE = 100

## Class to create Configure/Map page
class Configure:
    background = pygame.Surface((SCREEN_W, SCREEN_H))
    random = False
    
    ## Constructor
    def __init__(self): 
        self.background = self.background.convert()    
        self.background.fill((1, 1, 30))

        # Create texts
        title = Text("SELECT MAP", "./Font/upheavtt.ttf", SIZE * 0.6, (SCREEN_W // 2 , SCREEN_H // 5), (250, 230, 0))
        self.defaultTxt = Text("Predefined Map", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.5, SCREEN_H * 0.45), (250, 250, 250))
        self.randomTxt = Text("Randomly Generated Map", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.5, SCREEN_H * 0.65), (250, 250, 250))

        self.background.blit(title.getText(), title.getPos())
        self.background.blit(self.defaultTxt.getText(), self.defaultTxt.getPos())
        self.background.blit(self.randomTxt.getText(), self.randomTxt.getPos())

        # Create buttons
        self.okB = Button("OK", (SCREEN_W//2, SCREEN_H-SCREEN_H//6), "./Font/dpcomic.ttf", SIZE * 0.4,
                       (250, 250, 250), (155, 155, 155), (75, 75, 75), "START")
        self.defaultB = Button("DEFAULT", (SCREEN_W // 2, SCREEN_H * 0.35), "./Font/upheavtt.ttf", SIZE * 0.45,
                       (250, 250, 250), (155, 155, 155), (75, 75, 75))
        self.randomB = Button("RANDOM", (SCREEN_W // 2, SCREEN_H * 0.55), "./Font/upheavtt.ttf", SIZE * 0.45,
                       (250, 250, 250), (155, 155, 155), (75, 75, 75))
        self.defaultClickedB = Button("DEFAULT", (SCREEN_W // 2, SCREEN_H * 0.35), "./Font/upheavtt.ttf", SIZE * 0.45,
                               (5, 255, 235), (0, 195, 210), (5, 50, 255))
        self.randomClickedB = Button("RANDOM", (SCREEN_W // 2, SCREEN_H * 0.55), "./Font/upheavtt.ttf", SIZE * 0.45,
                               (5, 255, 235), (0, 195, 210), (5, 50, 255))

    ## Displays map screen
    def display(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.okB.getButton(), self.okB.getPos())
        if self.random: 
            screen.blit(self.defaultB.getButton(), self.defaultB.getPos())
            screen.blit(self.randomClickedB.getButton(), self.randomClickedB.getPos())
        else:
            screen.blit(self.defaultClickedB.getButton(), self.defaultClickedB.getPos())
            screen.blit(self.randomB.getButton(), self.randomB.getPos())
        
        pygame.display.flip()
    
    ## Control buttons
    def eventControl(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            self.defaultClickedB.hover(event)
            self.randomClickedB.hover(event)
            if self.defaultB.hover(event): self.random = False # If default mode is chosen
            if self.randomB.hover(event): self.random = True # If random mode is chosen
            if self.okB.hover(event): return self.okB.getFunc(), self.random # Back to menu page 
        
        return "MAP", self.random
    
