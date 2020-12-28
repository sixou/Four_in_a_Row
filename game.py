import copy
import alphaBetaPruning


VICTORY=10**20 #The value of a winning board (for max) 
LOSS = -VICTORY #The value of a losing board (for max)
TIE=0 #The value of a tie
SIZE=4 #the length of winning seq.
COMPUTER=SIZE+1 #Marks the computer's cells on the board
HUMAN=1 #Marks the human's cells on the board

rows=6
columns=7


class game:
    board=[]
    size=rows*columns
    playTurn = HUMAN
    
     #Used by alpha-beta pruning to allow pruning

    '''
    The state of the game is represented by a list of 4 items:
        0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
        the comp's cells = COMPUTER and the human's = HUMAN
        1. The heuristic value of the state.
        2. Whose turn is it: HUMAN or COMPUTER
        3. Number of empty cells
    '''

def create(s):
        #Returns an empty board. The human plays first.
        #create the board
        s.board=[]
        for i in range(rows):
            s.board = s.board+[columns*[0]]
        
        s.playTurn = HUMAN
        s.size=rows*columns
        s.val=0.00001
    
        #return [board, 0.00001, playTurn, r*c]     # 0 is TIE

def cpy(s1):
        # construct a parent DataFrame instance
        s2=game()
        s2.playTurn = s1.playTurn
        s2.size=s1.size
        s2.board=copy.deepcopy(s1.board)
        print("board ", s2.board)
        return s2
    
    
    
#def value(s):
'''
The function returns 1 for victory, -1 for loss, 0 for draw
And when the game is not over yet, it returns a percentage estimate to the sequence, 
with the player's sequence being more estimated as a percentage, 
for a sequence to a computer it will return a negative estimate
'''    
def value(s):
    # Returns the heuristic value of s
    Horizontal=lengthOfHorizontal(s)
    Vertical=lengthOfVertical(s)
    posDiagonal=lengthOfposDiagonal(s)
    negDiagonal=lengthOfnegDiagonal(s)
    maxin=Horizontal
    if (Vertical> maxin):
        maxin=Vertical
    if(posDiagonal>maxin):
        maxin=posDiagonal
    if(negDiagonal>maxin):
        maxin=negDiagonal
        
    if s.playTurn==COMPUTER:
        if(maxin==4):
            return LOSS
        else:
            if s.size>0:
              return maxin*(-0.25)  
        
    else:
        if(maxin==4):
            return VICTORY
        else:
            if s.size>0:
              return (maxin*0.25+0.01) 
     
    if s.size == 0:
        return TIE
  
#
    # return random.choice([LOSS, VICTORY, TIE])

   

"""def findVertical(s: game):
    turn = {HUMAN: COMPUTER, COMPUTER: HUMAN}
    verticalFunc = lambda i: map(lambda x: x[i], s.board)
    return any(map(lambda i: longestSequenceOf(verticalFunc(i), turn[s.playTurn]) >= SIZE, range(columns)))"""

#Returns the longest vertical sequence
def lengthOfVertical(s: game):
    turn = {HUMAN: COMPUTER, COMPUTER: HUMAN}
    cond=0
    for j in range (columns):
        verticalFunc = lambda j: map(lambda x: x[j], s.board)
        maxi=longestSequenceOf( verticalFunc(j), turn[s.playTurn])
        if maxi>cond:
           cond=maxi
    return cond

#Returns the horizontal vertical sequence
def lengthOfHorizontal(s: game):
    turn = {HUMAN: COMPUTER, COMPUTER: HUMAN}
    cond=0
    for i in range (rows):
        maxi=longestSequenceOf(s.board[i], turn[s.playTurn])
        if maxi>cond:
           cond=maxi
    return cond

#define positive diagonal
def posDiagonal(board, start_index):
    current_column = start_index if start_index >= 0 else 0
    row = 0 if start_index >= 0 else -start_index
    while current_column < columns and row < rows:
        yield board[row][current_column]
        current_column += 1
        row += 1

#define negetive diagonal
def negDiagonal(board, start_index):
    current_column = start_index if start_index >= 0 else 0
    current_row = rows-1 if start_index >= 0 else rows + start_index - 1
    while current_column < columns and current_row >= 0:
        yield board[current_row][current_column]
        current_column += 1
        current_row -= 1

#returns the positive diagonal  sequence 
def lengthOfposDiagonal(s):
    turn = {HUMAN: COMPUTER, COMPUTER: HUMAN}
    cond=0
    for i in range (-rows+1,columns):
        temp=posDiagonal(s.board, i)
        maxi=longestSequenceOf(temp, turn[s.playTurn])
        if maxi>cond:
           cond=maxi
    return cond


#returns the positive diagonal  sequence 
def lengthOfnegDiagonal(s):
    turn = {HUMAN: COMPUTER, COMPUTER: HUMAN}
    cond=0
    for i in range (-rows+1,columns):
        temp=negDiagonal(s.board, i)
        maxi=longestSequenceOf(temp, turn[s.playTurn])
        if maxi>cond:
           cond=maxi
    return cond


def longestSequenceOf(mylist, num):
    max_counter = 0
    counter = 0
    for item in mylist:
        if item != num:
            counter = 0
            continue
        counter += 1
        max_counter = max(counter, max_counter)
        if max_counter >= SIZE:
            break
    return max_counter     

def printState(s):
#Prints the board. The empty cells are printed as numbers = the cells name(for input)
#If the game ended prints who won.
        for r in range(rows):
            print("\n|",end="")
        #print("\n",len(s[0][0])*" --","\n|",sep="", end="")
            for c in range(columns):
                if s.board[r][c]==COMPUTER:
                    print("X|", end="")
                elif s.board[r][c]==HUMAN:
                    print("O|", end="")
                else:
                    print(" |", end="")

        print()

        for i in range(columns):
            print(" ",i,sep="",end="")

        print()
        
        val=value(s)

        if val==VICTORY:
            print("I won!")
        elif val==LOSS:
            print("You beat me!")
        elif val==TIE:
            print("It's a TIE")



def isFinished(s):
#Seturns True iff the game ended
        return value(s) in [LOSS, VICTORY, TIE] or s.size==0


def isHumTurn(s):
#Returns True iff it is the human's turn to play
        return s.playTurn==HUMAN
    


def decideWhoIsFirst(s):
#The user decides who plays first
        if int(input("Who plays first? 1-me / anything else-you : "))==1:
            s.playTurn=COMPUTER
        else:
            s.playTurn=HUMAN
            
        return s.playTurn
        

def makeMove(s, c):
#Puts mark (for huma. or comp.) in col. c
#and switches turns.
#Assumes the move is legal.

        r=0
        while r<rows and s.board[r][c]==0:
            r+=1

        s.board[r-1][c]=s.playTurn # marks the board
        s.size -= 1 #one less empty cell
        if (s.playTurn == COMPUTER ):
            s.playTurn = HUMAN
        else:
            s.playTurn = COMPUTER

   
def inputMove(s):
#Reads, enforces legality and executes the user's move.

        #self.printState()
        flag=True
        while flag:
            c=int(input("Enter your next move: "))
            if c<0 or c>=columns or s.board[0][c]!=0:
                print("Illegal move.")

            else:
                flag=False
                makeMove(s,c)

        
def getNext(s):
#returns a list of the next states of s
        ns=[]
        for c in list(range(columns)):
            print("c=",c)
            if s.board[0][c]==0:
                print("possible move ", c)
                tmp=cpy(s)
                makeMove(tmp, c)
                print("tmp board=",tmp.board)
                ns+=[tmp]
                print("ns=",ns)
        print("returns ns ", ns)
        return ns

def inputComputer(s):    
        return alphaBetaPruning.go(s)
