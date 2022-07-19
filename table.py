from copy import deepcopy
import tkinter as tk
from tkinter import messagebox
from time import sleep
from support import *

myState = [
    [1, 0], [7, 0], [0, 0], [7, 0], [7, 0], [2, 1],
    [1, 0], [1, 0], [8, 0], [7, 0], [7, 0], [1, 0]
]
    
class Table:  
    def __init__(self):
        self.draw = '''
	    10  9  8  7	 6
        +--------------------+
    11  |{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|{:2}| 5
        |{:2}|--------------|{:2}|
        |  |{:2}|{:2}|{:2}|{:2}|{:2}|  |
        +--------------------+
            0  1  2  3  4
        '''

        '''
		        10	9  8  7	 6
            +--------------------+
        11	| x| x| x| x| x| x| x| 5
            | Q|--------------| Q|
            |  | x| x| x| x| x|  |
            +--------------------+
                0  1  2  3  4
        '''
        self.turn = 0
        self.player1Score = 0
        self.player2Score = 0
        self.playerScore = [0, 0]
        # self.state = myState
        self.state = [
            [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1],
            [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1]
        ]
    
    # draw table as in initial state
    def initDrawTable(self):
        arr = []
        for i in range(11,5,-1):
            arr.append(self.state[i][0])
        arr.append(self.state[5][0])
        arr.append(self.state[11][1])
        arr.append(self.state[5][1])
        for i in range(0,5):
            arr.append(self.state[i][0])    
        return arr

    def validIndex(self, index):
        while True:
            if self.state[index][0] != 0:
                return index
            print('You can not choose this cell!')
            index = int(input('Index: ')) 

    # Start the game and Finish
    def start(self):
        self.drawTable()
        user = None
        while True:
            user, index, direction = getInput(user)
            index = self.validIndex(index)
            result = self.movingTurnTable(user, index, direction)
            if result is True:
                break
    
    # movingTurn with I/O 
    def movingTurnTable(self, player, index, direction):
        self.drawTable()
        # self.handleBorrow(player)
        score = [self.player1Score, self.player2Score]
        self.state, [self.player1Score, self.player2Score] = handleBorrow(self.state, player, score)

        text = 'Turn {}: {} chọn ô {}, hướng {}'
        print(text.format(self.turn + 1, player, index, direction))
        c1, swap = None, False

        while True:
            if swap is True:
                print('Change Turn!')
                self.turn += 1
                return self.validFinish()
            
            score = [self.player1Score, self.player2Score]
            if c1 is None:
                self.state, [self.player1Score, self.player2Score], c1, swap = handleMoving(self.state, score, player, index, direction)

            else:
                self.state, [self.player1Score, self.player2Score], c1, swap = handleMoving(self.state, score, player, c1.index, direction) 
            self.drawTable()
 
           
    def validFinish(self):
        quanPhai = self.state[5][0] + self.state[5][1]
        quanTrai = self.state[11][0] + self.state[11][1]
        if (quanPhai == 0 and quanTrai == 0):
            self.playerScore = [self.player1Score, self.player2Score]
        return self.finished()

    # draw table to console
    def drawTable(self, arr = None):
        if arr is None:
            arr = self.initDrawTable()
        print(self.draw.format(*arr))
        text = """        Player1's score: {}   Player2's score: {}\n"""
        print(text.format(self.player1Score, self.player2Score))
        # self.validFinish() 

    '''Checking whether if Game is finished'''
    def finished(self):
        return self.state[5] == [0, 0] and self.state[11] == [0, 0]
