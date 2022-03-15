"""This module sets up the environment of the game with white dots on
   the pre-defined or randomly generated map."""

import pygame
import random

SCREEN_W = 800
SCREEN_H = 600
SIZE = 100
ROWS = 15
COLS = 25

## Class to create block of path in game map
class Path(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, restrict = None): ## Constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.restrict = restrict # Show which direction is blocked

## Class to create white dots
class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y, r, powPal = False): ## Constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((r, r), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.ellipse(self.image, (250, 250, 250), (0, 0, r, r))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.powPal = powPal

    def getPowPal(self): return self.powPal

## Class to create cells/grid (for random man generation)
class Cell:
    def __init__(self, row, col): ## Constructor
        self.row = row
        self.col = col
        self.top = True
        self.btm = True
        self.left = True
        self.right = True
        self.visited = False

## Class to create and draw map of game
class Map:
    pathInfo = []

    def __init__(self, random): ## Constructor
        if random: self.map = self.generateRandomMap() 
        else: self.map = open("./Map/1.txt", "r").readlines() 
        self.random = random
        self.horizPath = pygame.sprite.Group()
        self.vertPath = pygame.sprite.Group()
        self.intersect = pygame.sprite.Group()
        self.base = pygame.sprite.Group()
        self.dots = pygame.sprite.Group()
        self.background = self.getPath_DrawMap()

    ## Generate random map
    def generateRandomMap(self):
        rowN = 7
        colN = 12
        mazeMap = [[Cell(r, c) for c in range(colN)] for r in range(rowN)]

        base = []
        for r in range(3, 6):
            for c in range(6, 10):
                base.append((r, c))
        
        # Generate map with DFS in 7 x 12 grids
        mazeMap[0][0].visited = True # Choose initial cell and marked visited
        stack= [mazeMap[0][0]] # Push initial cell to stack
        while stack:
            current = stack.pop() # Pop cell from stack as current cell
            currR = current.row
            currC = current.col

            neighbours = [] # Search for unvisited neighbours
            if currC - 1 >= 0 and (currR, currC - 1) not in base and not mazeMap[currR][currC - 1].visited: neighbours.append(mazeMap[currR][currC - 1])
            if currC + 1 < colN and (currR, currC + 1) not in base and not mazeMap[currR][currC + 1].visited: neighbours.append(mazeMap[currR][currC + 1])
            if currR - 1 >= 0 and (currR - 1, currC) not in base and not mazeMap[currR - 1][currC].visited: neighbours.append(mazeMap[currR - 1][currC])
            if currR + 1 < rowN and (currR + 1, currC) not in base and not mazeMap[currR + 1][currC].visited: neighbours.append(mazeMap[currR + 1][currC])

            if neighbours: # While stack not empty
                stack.append(current) # Push current cell into stack

                nextCell = random.choice(neighbours) # Select one unvisited neighbour
                # Remove wall between current cell and selected neighbour cell
                if currR + 1 == nextCell.row:
                    mazeMap[currR][currC].btm = False
                    mazeMap[nextCell.row][nextCell.col].top = False
                elif currR - 1 == nextCell.row:
                    mazeMap[currR][currC].top = False
                    mazeMap[nextCell.row][nextCell.col].btm = False
                elif currC + 1 == nextCell.col:
                    mazeMap[currR][currC].right = False
                    mazeMap[nextCell.row][nextCell.col].left = False
                elif currC - 1 == nextCell.col:
                    mazeMap[currR][currC].left = False
                    mazeMap[nextCell.row][nextCell.col].right = False

                mazeMap[nextCell.row][nextCell.col].visited = True # Mark chosen cell as visited
                stack.append(mazeMap[nextCell.row][nextCell.col]) # Push chosen cell into stack

        # Convert map into 15 x 25 grids
        mapTxt = []
        for i in range(rowN): 
            if i == 0: rng = 3 # If first row
            else: rng = 2 # If not first row
            for k in range(rng): 
                r = []
                for j in range(colN):  
                    if i == 0 and k == 0: # Cell in first row first col (Convert top)
                        if mazeMap[i][j].top: sym = ["0", "0", "0"]
                        elif (mazeMap[i][j].left or mazeMap[i][j].right) and not mazeMap[i][j].top: sym = ["0", "2", "0"]
                        elif not (mazeMap[i][j].top or mazeMap[i][j].left or mazeMap[i][j].right): sym = ["0", "0", "0"]
                    elif (i == 0 and k == 1) or (i != 0 and k == 0): # All row and col (Convert center)
                        if mazeMap[i][j].top or mazeMap[i][j].btm: 
                            if not (mazeMap[i][j].left or mazeMap[i][j].right): sym = ["1", "1", "1"]
                            elif mazeMap[i][j].left and not mazeMap[i][j].right: sym = ["0", "3", "1"]
                            elif mazeMap[i][j].right and not mazeMap[i][j].left: sym = ["1", "3", "0"]
                            elif mazeMap[i][j].right and mazeMap[i][j].left: sym = ["0", "3", "0"]
                        elif (mazeMap[i][j].left or mazeMap[i][j].right) and not (mazeMap[i][j].top or mazeMap[i][j].btm): sym = ["0", "2", "0"]                       
                    elif (i == 0 and k == 2) or (i != 0 and k == 1): # All row and col (Convert middle)
                        if mazeMap[i][j].btm: sym = ["0", "0", "0"]
                        elif (mazeMap[i][j].left or mazeMap[i][j].right) and not mazeMap[i][j].btm: sym = ["0", "2", "0"]
                        elif not (mazeMap[i][j].btm or mazeMap[i][j].left or mazeMap[i][j].right): sym = ["0", "0", "0"]
                    if j != 0: sym.pop(0) # If cell not in first col
                    r += sym
                mapTxt.append(r)

        base = [["0", "0", "0", "0", "0", "0", "0", "0"],
                ["0", "3", "1", ".", "1", "3", "1", "1"],
                ["0", "2", ".", ".", ".", "2", "0", "0"],
                ["0", "2", ".", ".", ".", "2", "0", "0"],
                ["1", "3", "1", "1", "1", "3", "1", "1"],
                ["0", "0", "0", "0", "0", "0", "0", "0"]]

        for i, r in enumerate(range(3, 9)): # Insert base into map
            for j, c in enumerate(range(10, 17)):
                mapTxt[r][c] = base[i][j]

        # Modify and improvise map
        for i in range(ROWS): # Checking in rows
            for j in range(COLS):
                if mapTxt[i][j] == "3":
                    if j + 2 < COLS:
                        if mapTxt[i][j + 1] == "0" and (mapTxt[i][j + 2] == "3" or mapTxt[i][j + 2] == "2"):
                            mapTxt[i][j + 1] = "1"
                            mapTxt[i][j + 2] = "3"
                        elif mapTxt[i][j + 1] == "0" and mapTxt[i][j + 2] == "1": mapTxt[i][j + 2] = "1"
                    if j - 2 > 0:
                        if mapTxt[i][j - 1] == "0" and mapTxt[i][j - 2] == "2":
                            mapTxt[i][j - 1] = "1"
                            mapTxt[i][j - 2] = "3"
                    if j + 1 < COLS and j - 1 > 0:
                        if mapTxt[i][j + 1] == "1" and mapTxt[i][j - 1] == "1" and mapTxt[i - 1][j] == "0" and mapTxt[i + 1][j] == "0":
                            mapTxt[i][j] = "1" 
                if mapTxt[i][j] == "2":
                    if j + 1 < COLS: 
                        if mapTxt[i][j + 1] == "1": mapTxt[i][j] = "3"
                if mapTxt[i][j] == "1": 
                    if j + 1 < COLS:
                        if mapTxt[i][j + 1] == "2": mapTxt[i][j + 1] = "3"
                        if mapTxt[i][j + 1] == "0": 
                            if j + 2 < COLS and mapTxt[i][j + 2] == "2":
                                mapTxt[i + 1] = "1"
                                mapTxt[i + 2] = "3"
                            else: mapTxt[i][j + 1] = "3"
                    if j - 1 > 0:
                        if mapTxt[i][j - 1] == "0": mapTxt[i][j] = "3"
 
        for j in range(COLS): # Checking in columns
            for i in range(ROWS):
                if mapTxt[i][j] == "3":
                    if i + 2 > ROWS:
                        if mapTxt[i + 1][j] == "0" and (mapTxt[i + 2][j] == "3" or mapTxt[i + 2][j] == "2"): mapTxt[i + 1][j] = "2" 
                        if mapTxt[i + 1][j] == "2" and mapTxt[i + 2][j] == "1": mapTxt[i + 2][j] = "3" 
                if mapTxt[i][j] == "2":
                    if i + 1 < ROWS:
                        if mapTxt[i + 1][j] == "1": mapTxt[i + 1][j] = "3"
                        if mapTxt[i + 1][j] == "0":
                            if i + 2 < ROWS and mapTxt[i + 2][j] == ".": mapTxt[i][j] = "0"
                            else: mapTxt[i + 1][j] = "2"
                if mapTxt[i][j] == "1": 
                    if i + 1 < ROWS:
                        if mapTxt[i + 1][j] == "2": mapTxt[i][j] = "3"
                        if mapTxt[i + 1][j] == "1": mapTxt[i + 1][j] = "0"
                    if i + 2 < ROWS:
                        if mapTxt[i + 1][j] == "0" and mapTxt[i + 2][j] == "2":
                            mapTxt[i][j] = "3"
                            mapTxt[i + 1][j] = "2"

        return mapTxt

    ## Collects path info and create path and dots for the game
    def getPath_DrawMap(self):
        bg = pygame.Surface((SCREEN_W, SCREEN_H)).convert()
        bg.fill((1, 1, 30))
        t = int(SIZE * 0.03) # Thickness of line

        # Draw lines according to numbers and record details of every block of path
        y = SCREEN_H // len(self.map)
        powerRow = []
        powerCol = []
        for r, row in enumerate(self.map):
            if not self.random: row = row.strip()
            x = SCREEN_W // len(row)
            for c, col in enumerate(row): # Add white dots in every block of path
                if col != "0" and col != ".":
                    if col == "3" or col == "4":
                        pwr = random.choice([True, False, False, False, True, False, True])
                        if len(powerRow) == 10 or c in powerCol or r in powerRow: pwr = False
                        if pwr: 
                            powerRow.append(r)
                            powerCol.append(c)
                            dotSize = SIZE * 0.15
                        else: dotSize = SIZE * 0.05
                        self.dots.add(Dot(c * x + x / 2, r * y + y / 2, dotSize, pwr))
                    else: self.dots.add(Dot(c * x + x / 2, r * y + y / 2, SIZE * 0.05))

                if col == "1": # Horizontal path
                    self.pathInfo.append({"pos": (c * x, r * y), "restrict" : "UD"})
                    self.horizPath.add(Path(c * x, r * y, x, y, "UD"))
                    pygame.draw.line(bg, (0, 210, 255), (c * x, r * y), (c * x + x, r * y), t)
                    pygame.draw.line(bg, (0, 210, 255), (c * x, r * y + y), (c * x + x, r * y + y), t)

                elif col == "2": # Vertical path
                    self.pathInfo.append({"pos": (c * x, r * y), "restrict": "LR"})
                    self.vertPath.add(Path(c * x, r * y, x, y, "LR"))
                    pygame.draw.line(bg, (0, 210, 255), (c * x, r * y), (c * x, r * y + y), t)
                    pygame.draw.line(bg, (0, 210, 255), (c * x + x, r * y), (c * x + x, r * y + y), t)

                elif col == "3" or col == "4": # Intersect
                    self.pathInfo.append({"pos": (c * x, r * y), "restrict": "I"})
                    if c == 0 or row[c - 1] == "0" or row[c - 1] == ".": 
                        self.pathInfo[-1]["restrict"] += "L"
                        pygame.draw.line(bg, (0, 210, 255), (c * x, r * y), (c * x, r * y + y), t)
                    if c == len(row) or row[c + 1] == "0" or row[c + 1] == ".": 
                        self.pathInfo[-1]["restrict"] += "R"
                        pygame.draw.line(bg, (0, 210, 255), (c * x + x, r * y), (c * x + x, r * y + y), t)
                    if r == 0 or self.map[r - 1][c] == "0" or self.map[r - 1][c] == ".": 
                        self.pathInfo[-1]["restrict"] += "U"
                        pygame.draw.line(bg, (0, 210, 255), (c * x, r * y), (c * x + x, r * y), t)
                    if r == len(self.map) or self.map[r + 1][c] == "0" or self.map[r + 1][c] == ".": 
                        self.pathInfo[-1]["restrict"] += "D"
                        pygame.draw.line(bg, (0, 210, 255), (c * x, r * y + y), (c * x + x, r * y + y), t)
                    if col == "4": self.pathInfo[-1]["restrict"] += "C"
                    self.intersect.add(Path(c * x, r * y, x, y, self.pathInfo[-1]["restrict"]))
                
                elif col == ".": # Base
                    self.pathInfo.append({"pos": (c * x, r * y), "restrict": "B"})
                    self.base.add(Path(c * x, r * y, x, y, "B"))
                    if row[c - 1] == "1" and row[c + 1] == "1":
                        self.pathInfo[-1]["restrict"] += "UD"
                        self.exit = {"pos": (c * x, r * y), "restrict": "E"}
                        self.horizPath.add(Path(c * x, r * y, x, y, "BUD"))
                        self.dots.add(Dot(c * x + x / 2, r * y + y / 2, SIZE * 0.05))
                        pygame.draw.line(bg, (0, 210, 255), (c * x, r * y), (c * x + x, r * y), t)
                    elif row[c - 1] != ".":
                        self.base.add(Path(c * x, r * y, x, y, "B"))
                        pygame.draw.line(bg, (0, 210, 255), (c * x, r * y), (c * x, r * y + y), t)
                    elif row[c + 1] != ".":
                        self.base.add(Path(c * x, r * y, x, y, "B"))
                        pygame.draw.line(bg, (0, 210, 255), (c * x + x, r * y), (c * x + x, r * y + y), t)
                    elif self.map[r + 1][c] != ".":
                        self.base.add(Path(c * x, r * y, x, y, "B"))
                        pygame.draw.line(bg, (0, 210, 255), (c * x, r * y + y), (c * x + x, r * y + y), t)

        return bg
    
    ## Draws and returns map
    def displayMap(self, screen): 
        self.horizPath.draw(screen)
        self.vertPath.draw(screen)
        self.intersect.draw(screen)
        screen.blit(self.background, (0, 0))
        self.dots.draw(screen)
        return screen

    def getPathInfo(self): return self.pathInfo
    def getDots(self): return self.dots
    def getHorizPath(self): return self.horizPath
    def getVertPath(self): return self.vertPath
    def getIntersect(self): return self.intersect
    def getBase(self): return self.base
    def getExit(self): return self.exit