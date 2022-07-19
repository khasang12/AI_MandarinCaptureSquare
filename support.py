from copy import deepcopy

PLAYER1 = 'player1'
PLAYER2 = 'player2'
LEFT = 'Left'
RIGHT = 'Right'
#################### I/O HANDLER ######################
def getUser(user):
    if user is PLAYER1:
        return PLAYER2
    return PLAYER1

def getInput(player=None):
    direction = None
    while True:
        user = getUser(player)
        index = int(input('Index (0-4): ')) if user == PLAYER1 else int(input('Index (6-10): '))
        direction = input('Direction: ')
        direction = validDirection(direction)
        if validInput(user, index) and direction != False: break
    return user, index, direction
def validDirection(direction):
    char = direction.lower()
    if char != 'r' and char != 'l':
        print('Type R/r for Right and L/l for Left')
        return False
    elif char == 'r':
        return RIGHT
    else:
        return LEFT
def validInput(user, index):
    if user is PLAYER1:
        if 0 <= index < 5: 
            return True
        else: 
            print('You must input from 0 to 4')
            return False
    elif user is PLAYER2:
        if 6 <= index < 11: 
            return True
        else: 
            print('You must input from 6 to 10')
            return False
        
################## TABLE UTILITY ####################   
# F1: Calculate circular index
# Input: Index (maybe invalid)
# Output: Valid index in the board
def calculateIndex(index):
    if 0 <= index < 12:
        return index
    if index < 0:
        absIndex = abs(index)
        if absIndex < 12: return 12 - absIndex
        return 12 * (1 + int(absIndex/12)) % absIndex
    if index > 11:
        return index % 12

# F2: Handle Borrow Troops
# Input: State: [[Int, Int]], Player: [Str,Str], Score: [Int, Int], Agent: Bool
# Output: New State, New Score
def handleBorrow(state, player, score, agent=False):
    if agent:
        state, score = deepcopy(state), deepcopy(score)
    sum = 0
    if player is PLAYER1:
        for i in range(0, 5):
            sum += state[i][0]
    else:
        for i in range(6, 11):
            sum += state[i][0]
    # if needed
    if sum == 0:
        #print('Caution! Your cells are empty, so you must borrow troops.')
        if player is PLAYER1:
            score[0] -= 5
            for i in range(5):
                state[i][0] += 1
        elif player is PLAYER2:
            score[1] -= 5
            for i in range(6, 11):
                state[i][0] += 1
    return state, score
        #self.drawTable()
        
# F2.1: Sub-function of F2, handle one-time-picking troops
# Input: State: [[Int, Int]], Score: [Int, Int], Player: [Str,Str], Index: Int, Direction: Str, Agent: Bool
# Output: New State, New Score      
def handleMoving(state, score, player, index, direction):     
    # valid is change turn
    def isChangeTurns(cell1, cell2):
        if cell1.isQuanCell and cell1.score != 0:
            return True
        if cell1.score == 0 and cell2.score == 0:
            if cell2.isQuanCell is False:
                return True
            else:
                cell2.score += 5 if state[cell2.index][1] == 1 else 0
                return True if cell2.score == 0 else False
        return False
    
    # Moving function
    def move(player, index, direction,printed=True):
        tmp = state[index][0]
        if (direction == 'Right'):
            for i in range(tmp):
                state[calculateIndex(index + i + 1)][0] +=1
            nextIndex = calculateIndex(index + tmp +1) 
            nextnextIndex = calculateIndex(nextIndex + 1)
        else:
            for i in range(tmp):
                state[calculateIndex(index - i - 1)][0] +=1
            nextIndex = calculateIndex(index - tmp - 1) 
            nextnextIndex = calculateIndex(nextIndex - 1)
        state[index][0] = 0
        #if printed:
            #drawTable()
    
        cell1 = Cell(nextIndex, state[nextIndex][0])
        cell2 = Cell(nextnextIndex, state[nextnextIndex][0])
        return cell1, cell2
    
    # return None, None nếu dừng, return 2 cell tiếp theo nếu ăn tiếp
    def eatCells(player, cell1, cell2, direction):
        #print('Ăn điểm!')
        sc = state[cell2.index][0]
    
        # Nếu ô ăn được là ô quan thì cộng thêm điểm
        if cell2.isQuanCell:
            sc += state[cell2.index][1] * 5
            state[cell2.index][1] = 0
        # Gán điểm cho player
        if player is PLAYER1: 
            score[0] += sc
        elif player is PLAYER2:
            score[1] += sc
        
        state[cell2.index][0] = 0
        cell2.score = 0
        #drawTable()

        if direction == 'Right':
            nextIndex = calculateIndex(cell2.index + 1)
            nextnextIndex = calculateIndex(nextIndex + 1) 
        else:
            nextIndex = calculateIndex(cell2.index - 1)
            nextnextIndex = calculateIndex(nextIndex - 1)

        cell1Next = Cell(nextIndex, state[nextIndex][0])
        cell2Next = Cell(nextnextIndex, state[nextnextIndex][0])

        if isChangeTurns(cell1Next, cell2Next) is True:
            return None

        if cell1Next.score == 0:
            return cell1Next, cell2Next
    
    cell1, cell2 = move(player, index, direction)

    if isChangeTurns(cell1, cell2) is True:
        return state, score, None, True

    # ăn điểm
    if cell1.score == 0:
        keepEating = eatCells(player, cell1, cell2, direction)
        while keepEating is not None:
            keepEating = eatCells(player, keepEating[0], keepEating[1], direction)
        return state, score, None, True 
    
    # đi tiếp
    elif cell1.score != 0:
        return state, score, cell1, False
    
# F2: Handle Moving Troops over Squares
# Input: State: [[Int, Int]], Score: [Int, Int], Player: [Str,Str], Index: Int, Direction: Str, Agent: Bool
# Output: New State, New Score    
def movingTurn(state, score, player, index, direction,agent=False):
    if agent:
        state, score = deepcopy(state), deepcopy(score)
        
    state, score = handleBorrow(state, player, score)

    c1, swap = None, False

    while True:
        if swap is True:
            return state, score
        
        if c1 is None:
            state, score, c1, swap = handleMoving(state, score, player, index, direction)

        else:
            state, score, c1, swap = handleMoving(state, score, player, c1.index, direction) 
            
# F3: Check if Game Finished
# Input: State: [[Int, Int]]
# Output: Bool Flag
def finished(state):
    return state[5] == [0, 0] and state[11] == [0, 0]
    



    
#########################################################
# Class storing cell information
class Cell:
    def __init__(self, index, score):
        self.index = index
        self.isQuanCell = True if self.index == 5 or self.index == 11 else False
        self.score = score
        
# Normalize Map Number to [0,1]
def normalize(d,size):
    for item in d:
        d[item] /= size
    return d

if __name__ == "__main__":
    createRandomDataset(10)