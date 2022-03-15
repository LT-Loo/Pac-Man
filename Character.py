"""This module creates game characters of the pac-man game and
   also deals with the animation of the characters."""


import pygame
import random
import math
from Layout import *

SCREEN_W = 800
SCREEN_H = 600
SIZE = 100

## Class to create ghost/enemy
class Enemy(pygame.sprite.Sprite):
    ## Constructor
    def __init__(self, info, smart, pacmanPos, intersect, timeBase, baseExit):
        pygame.sprite.Sprite.__init__(self)
        self.smart = smart
        self.initial = info["pos"]
        if smart: self.ghostImg = Image("./Img/Smart.png", SIZE * 0.0007, info["pos"], 0, True)
        else: self.ghostImg = Image("./Img/Dummy.png", SIZE * 0.0007, info["pos"], 0, True)
        self.frightenedImg = Image("./Img/Frightened.png", SIZE * 0.0007, info["pos"], 0, True)
        self.image = self.ghostImg.getImg()
        self.rect = self.ghostImg.getRect()
        self.speed = random.randrange(1, 3) # Move in random speed
        self.pause = False # Whether the game is running or paused
        self.inBase = True
        self.timeBase = timeBase
        self.startTime = timeBase
        self.baseExit = baseExit
        self.powPal = False
        
    ## Updates movement of ghost
    def update(self, pathInfo, pacmanPos, intersect, eaten = False, back = False):

        # Image changed according to mode
        if self.powPal: self.image = self.frightenedImg.getImg()
        else: self.image = self.ghostImg.getImg()

        if back or eaten: # If caught by player / player is caught, return base
            self.inBase = True
            self.powPal = False
            self.rect.topleft = self.initial
            if back: self.timeBase = self.startTime
            elif eaten: self.timeBase = 150

        if self.inBase and not self.pause: # Move out from base
            if self.timeBase <= 50:
                if self.rect.x < self.baseExit["pos"][0]: self.rect.x += self.speed
                elif self.rect.x > self.baseExit["pos"][0]: self.rect.x -= self.speed
                elif self.rect.x == self.baseExit["pos"][0] and self.rect.y != self.baseExit["pos"][1]:
                    if self.rect.y < self.baseExit["pos"][1]: self.rect.y += self.speed
                    elif self.rect.y > self.baseExit["pos"][1]: self.rect.y -= self.speed
                elif self.rect.x == self.baseExit["pos"][0] and self.rect.y == self.baseExit["pos"][1]: 
                    self.inBase = False
                    self.chgDirection(pacmanPos, intersect, "UD", "D")
            self.timeBase -= 1

        if not self.pause and not self.inBase: # If not pause and not in base
            self.rect.x += self.moveX
            self.rect.y += self.moveY

        for path in pathInfo: # Change direction randomly when ghost in intersect path
            if self.rect.topleft == path["pos"] and "I" in path["restrict"]: 
                if self.moveX > 0: comeFrom = "L"
                elif self.moveX < 0: comeFrom = "R"
                if self.moveY > 0: comeFrom = "U"
                elif self.moveY < 0: comeFrom = "D"
                self.chgDirection(pacmanPos, intersect, path["restrict"], comeFrom)

        # When ghost is out of screen
        if self.rect.y == 0: self.rect.x += self.moveX
        elif self.rect.x == 0: self.rect.y += self.moveY
        if self.rect.right < 0: self.rect.left = SCREEN_W
        elif self.rect.left > SCREEN_W: self.rect.right = 0
        if self.rect.bottom < 0: self.rect.top= SCREEN_H
        elif self.rect.top > SCREEN_H: self.rect.bottom = 0
        
    ## Changes moving direction of ghost
    def chgDirection(self, pacmanPos, intersect, restrict, comeFrom):
        if self.smart: direction = self.pathSearch(pacmanPos, intersect, restrict, comeFrom)
        else: direction = self.randomSearch(restrict, comeFrom)

        if direction == "L": self.moveX = -self.speed; self.moveY = 0
        elif direction == "R": self.moveX = self.speed; self.moveY = 0
        elif direction == "U": self.moveY = -self.speed; self.moveX = 0
        elif direction == "D": self.moveY = self.speed; self.moveX = 0
    
    ## Random movement for normal ghosts
    def randomSearch(self, restrict, comeFrom):
        direction = random.choice(["L", "R", "U", "D"])
        # Restrict ghost movement due to blocking walls or prevent ghost reverse
        while direction in restrict or direction == comeFrom: 
            direction = random.choice(["L", "R", "U", "D"])

        return direction

    ## Search intersects that are nearest to player
    def searchIntersect(self, intersect, currentPos, direction, restrict):
        x, y = currentPos
        intersects = []
        for block in intersect: # Search for nearest intersects
            if direction == "U" and block.rect.top < y and block.rect.left == x: intersects.append((block, math.dist(block.rect.topleft, currentPos), "U"))
            elif direction == "D" and block.rect.top > y and block.rect.left == x: intersects.append((block, math.dist(block.rect.topleft, currentPos), "D"))
            elif direction == "L" and block.rect.left < x and block.rect.top == y: intersects.append((block, math.dist(block.rect.topleft, currentPos), "L"))
            elif direction == "R" and block.rect.left > x and block.rect.top == y: intersects.append((block, math.dist(block.rect.topleft, currentPos), "R"))

        if intersects: # If intersects found      
            if "C" in restrict: # If tunnel available (Eg. Move pass left border and appear at right border of window)
                opposite = max(intersects, key = lambda x:x[1])
                intersects.remove(opposite)
                opposite = list(opposite)
                # Change to shorter distance between ghost and intersect
                if (direction == "U" or direction == "D") and SCREEN_H - opposite[1] < opposite[1]:
                    opposite[1] = SCREEN_H - opposite[1]
                    if direction == "U": opposite[2] = "D"
                    else: opposite[2] = "U"
                elif (direction == "L" or direction == "R") and SCREEN_W - opposite[1] < opposite[1]: 
                    opposite[1] = SCREEN_W - opposite[1]
                    if direction == "L": opposite[2] = "R"
                    else: opposite[2] = "L"
                intersects.append(tuple(opposite))
            return intersects
        else: return [None]
  
    ## Movement for AI ghosts
    def pathSearch(self, pacmanPos, intersect, restrict, comeFrom):
        current = self.rect.topleft

        nearest = [] # Get intersects nearest to player
        if "U" not in restrict and comeFrom != "U": nearest += self.searchIntersect(intersect, current, "U", restrict)
        if "D" not in restrict and comeFrom != "D": nearest += self.searchIntersect(intersect, current, "D", restrict)
        if "L" not in restrict and comeFrom != "L": nearest += self.searchIntersect(intersect, current, "L", restrict)
        if "R" not in restrict and comeFrom != "R": nearest += self.searchIntersect(intersect, current, "R", restrict)

        intersectF = []
        for n in nearest: # Calculate f-values of each intersect found
            if n is None: continue
            dist = n[1] + math.dist(n[0].rect.center, pacmanPos) # Heuristic
            intersectF.append({"block": n[0], "dist": dist, "direction": n[2]})

        if intersectF: best = min(intersectF, key = lambda x:x["dist"]) # Find best option (min f-value)
        
        # Give priority if ghost and player in the same path instead of moving to intersect
        if pacmanPos[1] == current[1] + 20: 
            if best["dist"] > math.dist(pacmanPos, (current[0] + 16, current[1] + 20)):
                if pacmanPos[0] - current[0] < 0 and comeFrom != "L" and "L" not in restrict: return "L"
                elif pacmanPos[0] - current[0] > 0 and comeFrom != "R" and "R" not in restrict: return "R"
        elif pacmanPos[0] == current[0] + 16:
            if best["dist"] > math.dist(pacmanPos, (current[0] + 16, current[1] + 20)):
                if pacmanPos[1] - current[1] < 0 and comeFrom != "U" and "U" not in restrict: return "U"
                elif pacmanPos[1] - current[1] > 0 and comeFrom != "D" and "D" not in restrict: return "D" 

        return best["direction"]

                           
    ## Pauses movement of enemy when game is paused
    def pauseEnemy(self, pause): self.pause = pause

    ## Activate/deactivate power pallet effect
    def powPalMode(self, mode): self.powPal = mode 


## Class to create player
class Player(pygame.sprite.Sprite):
    moveX = moveY = 0
    gameOver = False
    pause = False
    caught = False

    def __init__(self, x, y): ## Constructor
        pygame.sprite.Sprite.__init__(self)
        img = Image("./Img/Player/1.png", SIZE * 0.005, (x, y), 0, True, True)
        self.playerImg = img.getImg()
        self.image = img.getImg()
        self.rect = img.getRect()
        self.initial = (x, y)
        self.direction = 'R'

        # To make animation of moving player
        movingImg = "./Img/Player/" 
        self.rightAni = Animation(movingImg)
        self.leftAni = Animation(movingImg, flip = True)
        self.upAni = Animation(movingImg, 90)
        self.downAni = Animation(movingImg, 270)

        explosionImg = "./Img/Explosion/"
        self.rightExp = Animation(explosionImg)
        self.leftExp = Animation(explosionImg, flip = True)   
        self.upExp = Animation(explosionImg, 90)   
        self.downExp = Animation(explosionImg, 270)   

    def getImage(self): return self.image
    def getRect(self): return self.rect
    def getPosition(self): return self.rect.center

    ## Updates the movement of player
    def update(self, path, relocate = False):
        if self.caught: # Animation if player is caught
            if self.direction == 'R': 
                self.rightExp.update(2)
                self.image = self.rightExp.getCurrent()
            elif self.direction == 'L':
                self.leftExp.update(2)
                self.image = self.leftExp.getCurrent()
            if self.direction == 'D':
                self.downExp.update(2)
                self.image = self.downExp.getCurrent()
            elif self.direction == 'U':
                self.upExp.update(2)
                self.image = self.upExp.getCurrent()

        if relocate: # Relocate player after player is caught (life != 0)
            self.moveX = self.moveY = 0
            self.image = self.playerImg
            self.rect.center = self.initial

        if not self.pause: # If game running
            self.rect.x += self.moveX
            self.rect.y += self.moveY

        # When player is out of screen
        if self.rect.right < 0: self.rect.left = SCREEN_W
        elif self.rect.left > SCREEN_W: self.rect.right = 0
        if self.rect.bottom < 0: self.rect.top = SCREEN_H
        elif self.rect.top > SCREEN_H: self.rect.bottom = 0

        # Allows player to move in certain directions according to the path it is moving on
        for wall in pygame.sprite.spritecollide(self, path.getHorizPath(), False): # In horizontal path
            self.rect.centery = wall.rect.centery
            self.moveY = 0
        for wall in pygame.sprite.spritecollide(self, path.getVertPath(), False): # In vertical path
            self.rect.centerx = wall.rect.centerx
            self.moveX = 0
        pygame.sprite.collide_circle_ratio(0.38)
        for wall in pygame.sprite.spritecollide(self, path.getIntersect(), False): # In intersection point
            if "U" in wall.restrict and self.moveY < 0 and self.rect.centery <= wall.rect.centery:
                 self.rect.centery = wall.rect.centery
            if "D" in wall.restrict and self.moveY > 0 and self.rect.centery >= wall.rect.centery:
                 self.rect.centery = wall.rect.centery
            if "L" in wall.restrict and self.moveX < 0 and self.rect.centerx <= wall.rect.centerx:
                 self.rect.centerx = wall.rect.centerx
            if "R" in wall.restrict and self.moveX > 0 and self.rect.centerx >= wall.rect.centerx:
                 self.rect.centerx = wall.rect.centerx

        # Run animation of moving player
        if not self.caught:
            if self.moveX > 0: 
                self.rightAni.update(10)
                self.image = self.rightAni.getCurrent()
            elif self.moveX < 0:
                self.leftAni.update(10)
                self.image = self.leftAni.getCurrent()
            if self.moveY > 0:
                self.downAni.update(10)
                self.image = self.downAni.getCurrent()
            elif self.moveY < 0:
                self.upAni.update(10)
                self.image = self.upAni.getCurrent()

    ## Controls moving direction of player
    def move(self, key):
        if self.pause: self.moveX = self.moveY = 0
        else:
            if key == pygame.K_RIGHT: self.moveX = 3; self.direction = 'R'
            elif key == pygame.K_LEFT: self.moveX = -3; self.direction = 'L'
            if key == pygame.K_UP: self.moveY = -3; self.direction = 'U'
            elif key == pygame.K_DOWN: self.moveY = 3; self.direction = 'D'

    ## Player stops moving when arrow key is released
    def stopMove(self, key): 
        if key == pygame.K_RIGHT:
            if self.moveX != 0: self.image = self.playerImg
            if self.moveX > 0: self.moveX = 0
        elif key == pygame.K_LEFT:            
            if self.moveX != 0: self.image = pygame.transform.flip(self.playerImg, True, False)
            if self.moveX < 0: self.moveX = 0
        if key == pygame.K_UP:
            if self.moveY != 0: self.image = pygame.transform.rotate(self.playerImg, 90)
            if self.moveY < 0: self.moveY = 0
        elif key == pygame.K_DOWN: 
            if self.moveY != 0: self.image = pygame.transform.rotate(self.playerImg, -90)
            if self.moveY > 0: self.moveY = 0

    ## Restricts player from moving when game is paused
    def pausePlayer(self, pause): self.pause = pause

    ## Determine if player is caught by ghost
    def caughtPlayer(self, caught): self.caught = caught


## Class to create animation of moving player
class Animation:
    index = 0
    clock = 1

    def __init__(self, filename, rotate = 0, flip = False): ## Constructor
        self.imgList = []
        self.loadImg(rotate, flip, filename)
    
    ## Loads images of animation and changes facing direction accordingly
    def loadImg(self, rotate, flip, filename):
        for i in range(1, 7):
            img = Image(filename + str(i) + ".png", SIZE * 0.005, (0, 0), rotate, True).getImg()
            if flip: img = pygame.transform.flip(img, True, False)
            self.imgList.append(img)

    ## Updates animation
    def update(self, fps = 30):
        step = 30 // fps
        if self.clock == 30: self.clock = 1
        else: self.clock += 1
        if self.clock in range(1, 30, step):
            self.index += 1
            if self.index == len(self.imgList): self.index = 0

    def getCurrent(self): return self.imgList[self.index]
