"""This module creates basic components and layouts such as 
   texts, images and buttons for the entire program"""

import pygame

## Class to create text
class Text:
    ## Constructor
    def __init__(self, text, font, fontSize, pos, color): 
        self.font = pygame.font.Font(font, int(fontSize))
        self.text = self.font.render(text, 1, color)
        self.pos = self.text.get_rect()
        self.pos.center = pos

    def getText(self): return self.text
    def getPos(self): return self.pos
    def getHeight(self): return self.font.get_height()

## Class to create image
class Image:
    ## Constructor
    def __init__(self, path, size, pos, rotate, alpha = False, center = False):
        self.img = pygame.image.load(path)
        if alpha: self.img = self.img.convert_alpha()
        else: self.img = self.img.convert()
        self.img = pygame.transform.rotozoom(self.img, rotate, size)
        self.rect = self.img.get_rect()
        if center: self.rect.center = pos
        else: self.rect.topleft = pos
    
    def getImg(self): return self.img
    def getRect(self): return self.rect

## Class to create button
class Button:
    ## Constructor
    def __init__(self, text, pos, font, fontSize, color, hoverCol, clickedCol, clickedFunc = None, change = None):
        self.x, self.y = pos
        self.font = pygame.font.Font(font, int(fontSize))
        self.current = text # Current label to be displayed on button
        self.initial = text
        self.change = change # Label to change when button is clicked (Optional)
        self.color = color
        self.hoverCol = hoverCol
        self.clickedCol = clickedCol
        self.clickedFunc = clickedFunc
        self.changeText(color)
    
    ## Changes label or colour of button
    def changeText(self, color, clicked = False):
        if clicked and self.change: # Change label of button
            if self.current == self.initial: self.current = self.change
            else: self.current = self.initial
        self.button = self.font.render(self.current, 1, color)
        self.size = self.button.get_size()
        self.rect = pygame.Rect(int(self.x-self.size[0]/2), self.y, self.size[0], self.size[1])

    ## Checks if button is pointed or clicked and makes changes when necessary
    def hover(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()): # If cursor hovers to button
            self.changeText(self.hoverCol) 
            if event.type == pygame.MOUSEBUTTONDOWN: # If button is clicked
                if pygame.mouse.get_pressed()[0] == 1: 
                    self.changeText(self.clickedCol, True)
                    return True
            if event.type == pygame.MOUSEBUTTONUP: self.changeText(self.hoverCol) # If button is released
        else: self.changeText(self.color) # If cursor is not placed on button
        return False

    def getButton(self): return self.button
    def getPos(self): return int(self.x-self.size[0]/2), self.y
    def getSize(self): return self.size
    def getFunc(self): return self.clickedFunc
        