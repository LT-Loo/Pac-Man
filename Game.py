"""This module creates the Pac-Man game and runs the exact game."""

import pygame
import random
import math

from Character import *
from Environment import Map
from Layout import *

SCREEN_W = 800
SCREEN_H = 600
SIZE = 100


## Class to create new game - Control and run the game
class Game:
    ## Constructor
    def __init__(self, randomMap):
        self.lives = 3
        self.caught = False
        self.score = 0
        self.win = False
        self.pause = False
        self.gameOver = False
        self.gameOverBGM = 0
        self.map = Map(randomMap)
        self.powPal = False
        self.powPalTime = 0

        # Load sounds
        self.countdownBGM = pygame.mixer.Sound("./Sound/countdown.wav")
        self.gameBGM = pygame.mixer.Sound("./Sound/siren.mp3")
        self.deathBGM = pygame.mixer.Sound("./Sound/die.wav")
        self.eatDotBGM = pygame.mixer.Sound("./Sound/eating.mp3")
        self.eatEnemyBGM = pygame.mixer.Sound("./Sound/eatEnemy.wav")

        # Create buttons
        self.pauseB = Button("PAUSE", (SCREEN_W - SIZE * 1.35, SIZE * 0.04), "./Font/Arcade_Classic.TTF", SIZE * 0.3,
                             (250, 250, 0), (255, 255, 150), (180, 180, 0), "PAUSE", "RESUME")
        self.quitGameB = Button("QUIT", (SCREEN_W - SIZE * 0.4, SIZE * 0.04), "./Font/Arcade_Classic.TTF", SIZE * 0.3,
                                (250, 250, 0), (255, 255, 150), (180, 180, 0), "START")
        self.restartB = Button("PLAY  AGAIN", (SCREEN_W // 2, SCREEN_H // 2 + SIZE * 0.25), "./Font/Arcade_Classic.TTF", SIZE * 0.35,
                               (250, 250, 0), (255, 255, 150), (180, 180, 0), "RESTART")
        self.menuB = Button("BACK  TO  MENU", (SCREEN_W // 2, SCREEN_H // 2 + SIZE * 0.7), "./Font/Arcade_Classic.TTF", SIZE * 0.35,
                                (250, 250, 0), (255, 255, 150), (180, 180, 0), "START")
        
        # Create player with initial location randomly selected from intersect points
        coord = random.choice([path for path in self.map.getPathInfo() if "I" in path["restrict"]])
        self.player = Player(coord["pos"][0] + 16, coord["pos"][1] + 20)
        for dot in pygame.sprite.spritecollide(self.player, self.map.getDots(), True):
            while dot.powPal: 
                coord = random.choice([path for path in self.map.getPathInfo() if "I" in path["restrict"]])
                self.player = Player(coord["pos"][0] + 16, coord["pos"][1] + 20)

        # Create ghosts with initial location randomly selected from intersect points
        self.ghosts = pygame.sprite.Group()
        overlap = [coord]
        for i in range(4):
            path = random.choice([p for p in self.map.getPathInfo() if "B" in p["restrict"]])
            # Prevent ghost from being too close to each other before the game starts
            while path in overlap or "UD" in path["restrict"]: 
                path = random.choice([p for p in self.map.getPathInfo() if "B" in p["restrict"]])
            if i % 2 == 0: self.ghosts.add(Enemy(path, False, self.player.getRect().center, self.map.getIntersect(), (i + 1) * 150, self.map.getExit()))
            else: self.ghosts.add(Enemy(path, True, self.player.getRect().center, self.map.getIntersect(), (i + 1) * 150, self.map.getExit()))
            overlap.append(path)

    ## Displays game on screen
    def display(self, screen, buffer = False, timeLeft = None):
        screen = self.map.displayMap(screen)
        self.ghosts.draw(screen)
        if not self.gameOver or self.caught: screen.blit(self.player.getImage(), self.player.getRect())
        screen.blit(self.pauseB.getButton(), self.pauseB.getPos())
        screen.blit(self.quitGameB.getButton(), self.quitGameB.getPos())
        scoreTitle = Text("SCORE", "./Font/Arcade_Classic.TTF", SIZE * 0.3, (SIZE//2, SIZE * 0.2), (250, 250, 0))
        screen.blit(scoreTitle.getText(), scoreTitle.getPos())
        score = Text(str(self.score), "./Font/Arcade_Classic.TTF", SIZE * 0.3, (SIZE * 1.25, SIZE * 0.2), (250, 250, 0))
        screen.blit(score.getText(), score.getPos())
        lifeTitle = Text("LIFE", "./Font/Arcade_Classic.TTF", SIZE * 0.3, (SIZE * 2.2, SIZE * 0.2), (250, 250, 0))
        screen.blit(lifeTitle.getText(), lifeTitle.getPos())
        life = Text(str(self.lives), "./Font/Arcade_Classic.TTF", SIZE * 0.3, (SIZE * 2.85, SIZE * 0.2), (250, 250, 0))
        screen.blit(life.getText(), life.getPos())

        if buffer: # Countdown before game starts
            if self.countdownBGM.get_num_channels() == 0: self.countdownBGM.play()
            num = Text(str(timeLeft), "./Font/upheavtt.ttf", SIZE * 3.5, (SCREEN_W//2, SCREEN_H//2), (200, 200, 200))
            screen.blit(num.getText(), num.getPos())

        if self.gameOver or self.win: # If game over or player wins the game
            board = pygame.Surface((SCREEN_W // 2.5, SCREEN_H // 2)).convert()
            board.fill((1, 1, 30))
            board.set_alpha(230)
            rect = board.get_rect()
            rect.center = (SCREEN_W // 2, SCREEN_H // 2)
            screen.blit(board, rect)
            pygame.draw.rect(screen, (105, 105, 180), rect, 5, 2)
            if self.gameOver: # If game over
                message = Text("GAME OVER", "./Font/papercut.ttf", SIZE * 0.5, (rect.centerx, rect.centery - SIZE * 0.95), (250, 250, 250))
            else: # If player wins
                message = Text("CONGRATZZ", "./Font/papercut.ttf", SIZE * 0.5, (rect.centerx, rect.centery - SIZE * 0.95), (250, 250, 250))
            screen.blit(message.getText(), message.getPos())
            score = Text("Score  " + str(self.score), "./Font/Arcade_Classic.TTF", SIZE * 0.35, (rect.centerx, rect.centery - SIZE * 0.3), (250, 250, 250))
            screen.blit(score.getText(), score.getPos())
            screen.blit(self.restartB.getButton(), self.restartB.getPos())
            screen.blit(self.menuB.getButton(), self.menuB.getPos())
        
        pygame.display.flip() # Update screen displayed

    ## Pauses game
    def pauseGame(self, pause):
        if pause: self.gameBGM.stop()
        self.player.pausePlayer(pause)
        for ghost in self.ghosts: ghost.pauseEnemy(pause)

    ## Controls the player and buttons
    def eventControl(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

            if not self.pause: # If game not pause
                # If key is pressed
                if event.type == pygame.KEYDOWN: self.player.move(event.key)
                elif event.type == pygame.KEYUP: self.player.stopMove(event.key)

            if not (self.win or self.gameOver): # If game still running
                if self.pauseB.hover(event): # Pause or resume game 
                    if self.pause: self.pause = False
                    else: self.pause = True
                    self.pauseGame(self.pause)    
            else : # If win or lose game
                if self.restartB.hover(event): return self.restartB.getFunc() # Play again
                if self.menuB.hover(event): return self.menuB.getFunc() # Return to start up page
            if self.quitGameB.hover(event): # Quit game
                self.pause = True
                self.pauseGame(self.pause)
                return self.quitGameB.getFunc() 

    ## Run game
    def runGame(self):

        page = self.eventControl() # Control player and button

        if self.deathBGM.get_num_channels() == 0 and self.caught: # If player is caught
            self.gameOverBGM = 0
            self.caught = False
            self.lives -= 1
            self.player.caughtPlayer(self.caught)
            self.player.update(self.map, True)
            self.ghosts.update(self.map.getPathInfo(), self.player.getPosition(), self.map.getIntersect(), back = True)
            self.pause = False
            self.pauseGame(self.pause)

        else: # If player still alive
            if self.gameBGM.get_num_channels() == 0 and not self.pause and not self.gameOver and not self.win: # BGM
                self.gameBGM.set_volume(0.2)
                self.gameBGM.play()

            self.player.update(self.map) # Update player

            if self.powPal: # Power pallet effect
                self.powPalTime -= 1
                if self.powPalTime <= 0: 
                    self.powPal = False
                    for ghost in self.ghosts: ghost.powPalMode(self.powPal)

            # Increment score every time a dot is eaten
            for dot in pygame.sprite.spritecollide(self.player, self.map.getDots(), True):
                if dot.powPal: # Power pellet effect
                    self.score += 5
                    self.powPal = True
                    for ghost in self.ghosts: 
                        if not ghost.inBase: ghost.powPalMode(self.powPal)
                    self.powPalTime += 300
                else: self.score += 1 # Normal mode
                self.eatDotBGM.play()

            if not self.map.getDots(): # If all dots eaten, win game
                self.win = True
                self.pauseGame(self.win) 
            
            for ghost in self.ghosts: # Check if player collides with ghost
                pygame.sprite.collide_circle_ratio(0.5)
                if pygame.sprite.collide_mask(self.player, ghost):
                    if self.powPal and ghost.powPal: # Power paller effect
                        self.score += 15
                        ghost.update(self.map.getPathInfo(), self.player.getPosition(), self.map.getIntersect(), eaten = True)
                    else: # Normal mode
                        if self.gameOverBGM == 0: 
                            self.deathBGM.play()
                            self.gameOverBGM += 1
                        if self.lives > 1: # Life != 0
                            self.caught = True
                            self.player.caughtPlayer(self.caught)
                            self.pause = True
                            self.pauseGame(self.pause)
                        else: # Life == 0
                            if self.lives != 0: self.lives -= 1
                            self.player.caughtPlayer(True)
                            self.gameOver = True
                            self.pauseGame(self.gameOver)

            self.ghosts.update(self.map.getPathInfo(), self.player.getPosition(), self.map.getIntersect()) # Update movement of ghosts

        return page, self.lives # Return screen to display on screen
