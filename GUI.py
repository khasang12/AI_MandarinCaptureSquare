'''

Author:
'''

import os
import pygame
from math import pi as PI

from table import Table

from table import*

################# Configuration ###################
RES = 'res/'
QUANVALUE = 5
USER_GO_FIRST = True # Player will go first

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
SCREEN_CAPTION = 'O An Quan'


class Color():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (70, 0, 0)
    GREY = (128, 128, 128)
    YELLOW = (255, 255, 0)
    GREEN = (126, 202, 24)
    BLUE = (0, 0, 255)
    PALEGREEN = (130, 224, 170)
    ORANGE = (211, 84, 0)
    PURPLE = (73,0,131)
    DARKRED = (137,14,14)

##################################################
background = pygame.image.load(os.path.join(RES, 'background.png'))   

################# Properties ###################
O_DAN = (50, 50)
O_QUAN = (100, 100)  # Draw Eclipse
DAN = pygame.image.load(os.path.join(RES, 'dan.png'))
QUAN = pygame.image.load(os.path.join(RES, 'quan.png'))
QUANVALUE = 5
STATISTIC = [0, 0, 0]
TOTAL_SCORE_ = [0, 0]
HIGHEST_ = [0,0]


COLOR = Color()
##################################################


def to_screen(screen, text, x, y, fontsize, color):
    try:
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        textsurface = myfont.render(text, True, color)
        screen.blit(textsurface, (x, y))

    except Exception as e:
        print('Font Error')
        raise e



class TableGUI(Table):
    '''
    O an quan table with GUI feature
    '''
    def __init__(self, screen=None):
        super().__init__()
        self.screen = screen
        if screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(SCREEN_CAPTION)


    def draw_table(self, turn):
        self.screen.fill((255, 255, 255))
        self.screen.blit(background, (0, 0))
        to_screen(self.screen, "Player 2", 200, 60, 25, COLOR.DARKRED)
        to_screen(self.screen, str(self.player2Score), 370, 40, 50, COLOR.DARKRED)
        to_screen(self.screen, "Player 1", 470, 380, 25, COLOR.PURPLE)
        to_screen(self.screen, str(self.player1Score), 370, 365, 50, COLOR.PURPLE)
        if turn == 0:
            to_screen(self.screen, "Player " + str(turn + 1) + " is thinking...", 300, 450, 20 , COLOR.PURPLE)
        else:
            to_screen(self.screen, "Player " + str(turn + 1) + " is thinking...", 300, 10, 20, COLOR.RED)



        # So quan trong cac o
        for i in range (0,5):
            to_screen(self.screen, str(self.state[i][0]), 170+i*100, 250, 20, COLOR.ORANGE)
        for i in range (10,5):
            to_screen(self.screen, str(self.state[10][0]), 170+(10-i)*100, 150, 20, COLOR.ORANGE) 
        
        # So dan trong o ben trai 
        to_screen(self.screen, str(self.state[11][1]), 120, 170, 30, COLOR.ORANGE)
        to_screen(self.screen, str(self.state[11][0]), 120, 230, 20, COLOR.ORANGE) 
        # So dan trong o ben phai
        to_screen(self.screen, str(self.state[5][1]), 670, 170, 30, COLOR.ORANGE)
        to_screen(self.screen, str(self.state[5][0]), 670, 230, 20, COLOR.ORANGE) 

        # Quan ben trai
        if (self.state[11][1] == 1):
            self.screen.blit(QUAN, (80, 200))
        # Quan ben phai
        if (self.state[5][1] == 1):
            self.screen.blit(QUAN, (685, 200))

        # Dat soi quan tren o ben trai
        if (self.state[11][0] >= 1): self.screen.blit(DAN, (130, 260))
        if (self.state[11][0] >= 2): self.screen.blit(DAN, (130, 275))
        if (self.state[11][0] >= 3): self.screen.blit(DAN, (115, 260))
        if (self.state[11][0] >= 4): self.screen.blit(DAN, (115, 275))
        if (self.state[11][0] >= 5): self.screen.blit(DAN, (100, 260))
        if (self.state[11][0] >= 6): self.screen.blit(DAN, (100, 275))
        if (self.state[11][0] >= 7): self.screen.blit(DAN, (85, 260))
        if (self.state[11][0] >= 8): self.screen.blit(DAN, (85, 275))

        # Dat soi quan tren o ben trai
        if (self.state[5][0] >= 1): self.screen.blit(DAN, (660, 260))
        if (self.state[5][0] >= 2): self.screen.blit(DAN, (660, 275))
        if (self.state[5][0] >= 3): self.screen.blit(DAN, (675, 260))
        if (self.state[5][0] >= 4): self.screen.blit(DAN, (675, 275))
        if (self.state[5][0] >= 5): self.screen.blit(DAN, (690, 260))
        if (self.state[5][0] >= 6): self.screen.blit(DAN, (690, 275))
        if (self.state[5][0] >= 7): self.screen.blit(DAN, (705, 260))
        if (self.state[5][0] >= 8): self.screen.blit(DAN, (705, 275))

        # Dat soi cho USER_0
        for i in range(0,5):
            j = i+1
            if (self.state[i][0] >= 1): self.screen.blit(DAN, (75 + 100*j, 285))
            if (self.state[i][0] >= 2): self.screen.blit(DAN, (75 + 100*j, 300))
            if (self.state[i][0] >= 3): self.screen.blit(DAN, (90 + 100*j, 285))
            if (self.state[i][0] >= 4): self.screen.blit(DAN, (90 + 100*j, 300))
            if (self.state[i][0] >= 5): self.screen.blit(DAN, (105 + 100*j, 285))
            if (self.state[i][0] >= 6): self.screen.blit(DAN, (105 + 100*j, 300))
            if (self.state[i][0] >= 7): self.screen.blit(DAN, (120 + 100*j, 285))
            if (self.state[i][0] >= 8): self.screen.blit(DAN, (120 + 100*j, 300))

        # Dat soi cho USER_1
        for i in range(6,11):
            j = i+1
            if (self.state[i][0] >= 1): self.screen.blit(DAN, (75 + 100*(12-j), 185))
            if (self.state[i][0] >= 2): self.screen.blit(DAN, (75 + 100*(12-j), 200))
            if (self.state[i][0] >= 3): self.screen.blit(DAN, (90 + 100*(12-j), 185))
            if (self.state[i][0] >= 4): self.screen.blit(DAN, (90 + 100*(12-j), 200))
            if (self.state[i][0] >= 5): self.screen.blit(DAN, (105 + 100*(12-j), 185))
            if (self.state[i][0] >= 6): self.screen.blit(DAN, (105 + 100*(12-j), 200))
            if (self.state[i][0] >= 7): self.screen.blit(DAN, (120 + 100*(12-j), 185))
            if (self.state[i][0] >= 8): self.screen.blit(DAN, (120 + 100*(12-j), 200))

        pygame.display.flip()
    
    def redraw(self, turn):
        self.draw_table(turn)
