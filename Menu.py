import pygame
from Layout import *

SCREEN_W = 800
SCREEN_H = 600
SIZE = 100

### Class to create menu
class Menu:
    background = pygame.Surface((SCREEN_W, SCREEN_H))
    buttons = []

    def __init__(self):
        self.background = self.background.convert()    
        self.background.fill((1, 1, 30))

        # Create titles and logo
        title = Text("P A C M A N", "./Font/Arcade_Classic.TTF", SIZE, (SCREEN_W * 0.46, SCREEN_H / 3.5), (250, 230, 0))
        logo = Image("./Img/Logo.png", SIZE * 0.0003, (SCREEN_W * 0.76, SCREEN_H / 3.5), 0, True, True) 
        year = Text("Trimester 2, 2021", "./Font/dpcomic.ttf", int(SIZE * 0.3),
                     (SCREEN_W * 0.5, title.getPos()[1] - title.getHeight() * 0.4), (250, 250, 250))
        course = Text("2805ICT System and Software Design", "./Font/dpcomic.ttf", int(SIZE * 0.3),
                       (SCREEN_W * 0.5, year.getPos()[1] + year.getHeight()*1.5), (250, 250, 250))

        # Student list               
        stuText = ["Ler Theng Loo (s5212872)", "Luke Fisher (s5220734)", 
                   "Malachi Klar (s2937839)", "Richard Budden (s5097875)"]
        students = []
        for i in range(len(stuText)):
            y = title.getPos()[1] + year.getHeight() * (i + SIZE * 0.04)
            stu = Text(stuText[i], "./Font/dpcomic.ttf", int(SIZE * 0.3), (SCREEN_W * 0.5, y), (250, 250, 250))
            students.append((stu.getText(), stu.getPos()))

        # Add titles, logo and student details onto background
        self.background.blits([(title.getText(), title.getPos()), (logo.getImg(), logo.getRect()),
                               (year.getText(), year.getPos()), (course.getText(), course.getPos())])
        self.background.blits(students)

        # Create buttons
        self.buttons.append(Button("START", (SCREEN_W * 0.5, SCREEN_H * 0.6), "./Font/dpcomic.ttf", SIZE * 0.7,
                             (250, 250, 250), (155, 155, 155), (75, 75, 75), "GAME"))
        self.buttons.append(Button("MAP", (SCREEN_W * 0.5, self.buttons[-1].getPos()[1]+self.buttons[-1].getSize()[1]+2), "./Font/dpcomic.ttf", 
                               SIZE * 0.4, (250, 250, 250), (155, 155, 155), (75, 75, 75), "MAP"))
        self.buttons.append(Button("HELP", (SCREEN_W * 0.5, self.buttons[-1].getPos()[1]+self.buttons[-1].getSize()[1]+2), "./Font/dpcomic.ttf", 
                               SIZE * 0.4, (250, 250, 250), (155, 155, 155), (75, 75, 75), "HELP"))
        self.buttons.append(Button("QUIT", (SCREEN_W * 0.5, self.buttons[-1].getPos()[1]+self.buttons[-1].getSize()[1]+2), "./Font/dpcomic.ttf",
                            SIZE * 0.4, (250, 250, 250), (155, 155, 155), (75, 75, 75), "QUIT"))

    ## Returns data when button is clicked
    def eventControl(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            for button in self.buttons:
                if button.hover(event): 
                    if button.getFunc() == "SETTING": return "START" # SETTING button is not working for now
                    return button.getFunc() # Return screen to display

    ## Display menu screen
    def display(self, screen):
        screen.blit(self.background, (0, 0))
        for button in self.buttons: screen.blit(button.getButton(), button.getPos())
        pygame.display.flip()
