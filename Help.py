"""This module creates the Help Page of the game program."""

import pygame
from Layout import *

SCREEN_W = 800
SCREEN_H = 600
SIZE = 100

## Class to create Help page
class Help:
    background = pygame.Surface((SCREEN_W, SCREEN_H))

    ## Constructor
    def __init__(self): 
        self.background = self.background.convert()    
        self.background.fill((1, 1, 30))

        # Create texts
        txtList = []
        imgList = []
        txtList.append(Text("HOW TO PLAY", "./Font/upheavtt.ttf", SIZE * 0.6, (SCREEN_W //2 , SCREEN_H * 0.1), (250, 230, 0)))
        txtList.append(Text("PAC-MAN", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.24, SCREEN_H * 0.25), (250, 250, 250)))
        txtList.append(Text("GHOSTS", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.56, SCREEN_H * 0.25), (250, 250, 250)))
        txtList.append(Text("DOTS", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.81, SCREEN_H * 0.25), (250, 250, 250)))
        txtList.append(Text("Pac-man eats dots to gain points.", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.5, SCREEN_H * 0.36), (250, 250, 250)))
        txtList.append(Text("Pac-man avoids ghosts to survive.", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.5, SCREEN_H * 0.41), (250, 250, 250)))
        txtList.append(Text("MOVE DOWN", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.69, SCREEN_H * 0.55), (250, 250, 250)))
        txtList.append(Text("MOVE UP", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.37, SCREEN_H * 0.55), (250, 250, 250)))
        txtList.append(Text("MOVE RIGHT", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.69, SCREEN_H * 0.70), (250, 250, 250)))
        txtList.append(Text("MOVE LEFT", "./Font/VPPixel-Simplified.otf", SIZE * 0.25, (SCREEN_W * 0.38, SCREEN_H * 0.70), (250, 250, 250)))

        # Create images
        imgList.append(Image("./Img/Player/1.png", SIZE * 0.008, (SCREEN_W * 0.12, SCREEN_H * 0.25), 0, True, True))
        imgList.append(Image("./Img/Dummy.png", SIZE * 0.001, (SCREEN_W * 0.40, SCREEN_H * 0.25), 0, True, True))
        imgList.append(Image("./Img/Smart.png", SIZE * 0.001, (SCREEN_W * 0.46, SCREEN_H * 0.25), 0, True, True))
        imgList.append(Image("./Img/Arrow.png", SIZE * 0.02, (SCREEN_W * 0.25, SCREEN_H * 0.55), 0, True, True))
        imgList.append(Image("./Img/Arrow.png", SIZE * 0.02, (SCREEN_W * 0.25, SCREEN_H * 0.70), 90, True, True))
        imgList.append(Image("./Img/Arrow.png", SIZE * 0.02, (SCREEN_W * 0.55, SCREEN_H * 0.55), 180, True, True))
        imgList.append(Image("./Img/Arrow.png", SIZE * 0.02, (SCREEN_W * 0.55, SCREEN_H * 0.70), 270, True, True))
        pygame.draw.circle(self.background, (250, 250, 250), (SCREEN_W * 0.73, SCREEN_H * 0.25), 8)
        self.background.blits([(txt.getText(), txt.getPos()) for txt in txtList])
        self.background.blits([(img.getImg(), img.getRect()) for img in imgList])

        # Create BACK button
        self.backB = Button("BACK", (SCREEN_W//2, SCREEN_H-SCREEN_H//6), "./Font/dpcomic.ttf", SIZE * 0.4,
                       (250, 250, 250), (155, 155, 155), (75, 75, 75), "START")

    ## Displays help screen
    def display(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.backB.getButton(), self.backB.getPos())
        pygame.display.flip()
    
    ## Returns data when button is clicked
    def eventControl(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            if self.backB.hover(event): return self.backB.getFunc()

        
