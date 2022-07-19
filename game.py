import time
from time import sleep, time_ns
import pygame,sys
import os
from agent import Agent, Human, Minimax, NaiveBayes, RandomAgent
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from GUI import TableGUI,SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_CAPTION,USER_GO_FIRST,RES
PLAYER1 = 'player1'
PLAYER2 = 'player2'



def text_to_screen(screen, text, x, y, fontsize, color):
    try:
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', fontsize)
        textsurface = myfont.render(text, True, color)
        screen.blit(textsurface, (x, y))

    except Exception as e:
        print('Font Error')
        raise e
def getMenu(screen,font,fontbig):
    background = pygame.image.load(os.path.join(RES, 'background.png')) 
    screen.blit(background, (0, 0))
    pygame.display.set_caption("Mandarin Capture Square")
    color=(255,102,0)
    label = fontbig.render(' MANDARIN CAPTURE SQUARE ', True, (255,0,0))
    noti = font.render(' Press To Play: ', True, color)
    text1 = font.render(' A - Easy', True, color)
    text2 = font.render(' B - Medium', True, color)
    text3 = font.render(' C - Hard', True, color)
    text4 = font.render(' N - Naive Bayes', True, color)

    screen.blit(label, (100,100))
    screen.blit(noti, (200,40+150))
    screen.blit(text1, (220,80+150))
    screen.blit(text2, (220,110+150))
    screen.blit(text3, (220,140+150))
    screen.blit(text4, (220,170+150))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()		
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: # dfs
                    return "easy"
                if event.key == pygame.K_b:
                    return "medium"
                if event.key == pygame.K_c:
                    return "hard"
                if event.key == pygame.K_n:
                    return "naiveBayes"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()	
            pygame.display.flip()

def goFirst(screen,font,fontbig):
    background = pygame.image.load(os.path.join(RES, 'background.png')) 
    screen.blit(background, (0, 0))
    pygame.display.set_caption("Mandarin Capture Square")
    color=(255,102,0)
    label = fontbig.render(' Who go First ', True, (255,0,0))
    noti = font.render(' Press To Play: ', True, color)
    text1 = font.render(' A - Player1', True, color)
    text2 = font.render(' B - Player2', True, color)

    screen.blit(label, (275,100))
    screen.blit(noti, (200,50+150))
    screen.blit(text1, (215,100+150))
    screen.blit(text2, (215,130+150))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()		
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: # dfs
                    return 0
                if event.key == pygame.K_b:
                    return 1
            pygame.display.flip()
class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.fontbig = pygame.font.Font('freesansbold.ttf', 40)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_CAPTION)
        
        self.table = TableGUI(self.screen)

        self.players = []

    def redraw(self, turn):
        self.table.redraw(turn)
    
    def finished(self):
        return self.table.finished()

    def update(self,turn, move):
        # Chỉnh lại khúc này
        self.table.movingTurnTable(turn, move[0], move[1])

    def run(self):
        # User go first or agent go first
        turn = 0 if USER_GO_FIRST else 1

        # Display Menu
        level = getMenu(self.screen,self.font,self.fontbig).lower()

        # Change PLAYER1 or PLAYER2 to go first or seccond 
        self.players.append(self.AgentFactory("human",PLAYER1))
        self.players.append(self.AgentFactory(level,PLAYER2))

        turn = goFirst(self.screen,self.font,self.fontbig)

        print("*** Level : {} ***".format(level))
        # Game loop
        self.redraw(turn)
        while not self.finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()		

                        
            move = self.players[turn].execute(self.table.state)
            self.update(self.players[turn].player_id,move)

            print(f"USER_{turn}'s move: {move[0]} {move[1]}")
            turn ^= 1
            self.redraw(turn)

        self.redraw(turn)
        ######## Inform the winner
        # You won
        if self.table.player1Score > self.table.player2Score:
            result = 'player1 won!'
        # Computer won
        elif self.table.player1Score < self.table.player2Score:
            result = 'player2 won!'
        # Or draw
        else: result = 'Draw'

        # Show the message box to inform the result
        print(result)
        while True:
            # tk.Tk().wm_withdraw()  # to hide the main window
            messagebox.showinfo('End Game !', 'Result: ' + result)
            sleep(1)
            break  

    def reset(self): 
        self.table = TableGUI(self.screen)
        self.players.clear()
        self.move = None
        level = getMenu(self.screen,self.font,self.fontbig)
        self.players.append(self.AgentFactory('human',PLAYER1))
        self.players.append(self.AgentFactory(level,PLAYER2))


    def AgentFactory(self,str,playerID):
        if str == "easy":
            return NaiveBayes(playerID,self.screen,self.table)
        elif str == 'medium':
            return Minimax(playerID,self.screen,self.table,depth=3)
        elif str == 'hard':
            return Minimax(playerID,self.screen,self.table,depth=4)
        elif str == 'human':
            return Human(playerID,self.screen,self.table)
        elif str == "naiveBayes":
            return NaiveBayes(playerID,self.screen,self.table)
        else :
            return RandomAgent(playerID,self.screen,self.table)

    def statistic(self, goFirst, level):
        # User go first or agent go first
        turn = 0 if goFirst else 1
        moves = []
        # Change PLAYER1 or PLAYER2 to go first or seccond 
        self.players.append(self.AgentFactory("naiveBayes",PLAYER1))
        self.players.append(self.AgentFactory(level,PLAYER2))

        # Game loop
        thinking = []
        self.redraw(turn)
        while not self.finished():
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()		
            start = end = 0
            if(turn == 1):
                start = time.time()            
            move = self.players[turn].execute(self.table.state)
            moveStr = str(move[0])+move[1][0]
            moves.append(moveStr)
            if(turn == 1):
                end = time.time()    
                thinking.append(end-start)
            self.update(self.players[turn].player_id,move)

            turn ^= 1
            self.redraw(turn)

        self.redraw(turn)
     

        ######## Inform the winner
        # You won
        if self.table.player1Score > self.table.player2Score:
            result = -1
        # Computer won
        elif self.table.player1Score < self.table.player2Score:
            result = 1
        # Or draw
        else: result = 0

        # Show the message box to inform the result
        return moves,thinking,result
       
