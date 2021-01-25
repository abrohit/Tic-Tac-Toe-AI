import pygame
from pygame.locals import *

import os, sys, random, copy

pygame.init()

sw = 600
sl = 600

WHITE = (255, 255, 255)

win = pygame.display.set_mode((sw,sl))
pygame.display.set_caption("Tic Tac Toe")

clock = pygame.time.Clock()

blockSize = sw / 3#Gets the width or height of one block.
mid = blockSize / 2#Gets the mid value of the width or height of one block.

xPic = pygame.image.load('X.png')
xPic = pygame.transform.scale(xPic, (150, 150))
xRect = xPic.get_rect()

oPic = pygame.image.load('O.png')
oPic = pygame.transform.scale(oPic, (150, 150))
oRect = oPic.get_rect()

hPic = pygame.image.load('hLine.png')
hPic = pygame.transform.scale(hPic, (550, 70))

vPic = pygame.image.load('vLine.png')
vPic = pygame.transform.scale(vPic, (70, 550))

d1Pic = pygame.image.load('d1Line.png')
d1Pic = pygame.transform.scale(d1Pic, (350, 500))

d0Pic = pygame.image.load('d0Line.png')
d0Pic = pygame.transform.scale(d0Pic, (350, 500))

gameList = [['','',''],#The 2d array of the tiles value
            ['','',''],
            ['','','']]

def selectRandom(li):#Given a list it randomly selects an item in the list.
    ln = len(li)
    r = random.randrange(0, ln)
    print(r)
    return li[r]

def IsWinner(bo, le):
    return ((bo[0][0] == le and bo[0][1] == le and bo[0][2] == le) or # across the top
    (bo[1][0] == le and bo[1][1] == le and bo[1][2] == le) or # across the middle
    (bo[2][0] == le and bo[2][1] == le and bo[2][2] == le) or # across the bottom
    (bo[0][0] == le and bo[1][0] == le and bo[2][0] == le) or # down the left side
    (bo[0][1] == le and bo[1][1] == le and bo[2][1] == le) or # down the middle
    (bo[0][2] == le and bo[1][2] == le and bo[2][2] == le) or # down the right side
    (bo[0][2] == le and bo[1][1] == le and bo[2][0] == le) or # diagonal
    (bo[0][0] == le and bo[1][1] == le and bo[2][2] == le)) # diagonal

def CompMove():#Returns the comp move as a tuple.

    possibleMoves = []

    for row in range(3):
        for column in range(3):
            if gameList[row][column] == '':
                possibleMoves.append((row, column))#Gets all the possible moves as a tuple by checking if the tile is empty.

    move = 0
    
    for let in ['O', 'X']:
        for item in possibleMoves:
            boardCopy = copy.deepcopy(gameList)#Makes a Copy of the 2d array(gameList).
            boardCopy[item[0]][item[1]] = let
            if IsWinner(boardCopy, let):#Checks if the user is about to win or if the comp is about to win.
                move = item
                return move

    if (1,1) in possibleMoves:#Checks if the middle tile is empty.
        move = (1,1)
        return move



    edgesOpen = []
    for item in possibleMoves:#Checks if the edges are open.
        if item in [(0,1), (1,0), (1,2), (2,1)]:
            edgesOpen.append(item)

    if len(edgesOpen) > 0:#If the edges are open it randomly selects one.
        move = selectRandom(edgesOpen)
        print('edge')
        return move

    cornersOpen = []
    for item in possibleMoves:#Checks if the corners are open.
        if item in [(0,0), (0,2), (2,0), (2,2)]:
            cornersOpen.append(item)
    
    if len(cornersOpen) > 0:#If the corners are open it randomly selects one.
        move = selectRandom(cornersOpen)
        print('corners')
        return move

    return move#Returns 0 if no move is possible.
            
class Frame(object):

    def __init__(self):
        
        self.clickCounter = 0
        self.vClick = False
        self.winC = False
        self.boardFull = False
        self.winner = ''
        self.winRow = -1
        self.winColumn = -1
        self.winDiag = -1

    def UserUpdate(self, mouseP):#Upadates the 2d array(gameList) of the move made by the user.

        self.vClick = False

        if mouseP[0] < blockSize:
            column = 0
        elif mouseP[0] > blockSize and mouseP[0] < (blockSize * 2):
            column = 1
        elif mouseP[0] > (blockSize * 2) and mouseP[0] < sw:
            column = 2

        if mouseP[1] < blockSize:
            row = 0
        elif mouseP[1] > blockSize and mouseP[1] < (blockSize * 2):
            row = 1
        elif mouseP[1] > (blockSize * 2) and mouseP[1] < sw:
            row = 2

        if gameList[row][column] == '':
            self.vClick = True
            gameList[row][column] = 'X'

    def CompUpdate(self, point):#Upadates the 2d array(gameList) of the move made by the computer.

        self.clickCounter += 1
        
        if gameList[point[0]][point[1]] == '':
            gameList[point[0]][point[1]] = 'O'
        

    def draw(self, win):#Draws the 2d array(gameList) onto the pygame window.
        
        yPixel = blockSize / 2
        for row in range(3):
            
            xPixel = blockSize / 2
            for column in range(3):
                
                if gameList[row][column] == 'X':
                    xRect.center = ((xPixel, yPixel))
                    win.blit(xPic, xRect)
                    
                if gameList[row][column] == 'O':
                    oRect.center = ((xPixel, yPixel))
                    win.blit(oPic, oRect)
                    
                xPixel += blockSize
                
            yPixel += blockSize

    def Check(self):#Checks if user won or drew.

        count = 0
        for item in gameList:
            count += item.count('')#Checks how many are empty tiles
        
        if count == 0:
            self.boardFull = True
            
        for row in range(3):#Checks if user won horizontally.
            if gameList[row][0] == gameList[row][1] == gameList[row][2]and gameList[row][0] != '':
                self.winRow = row
                
                if gameList[row][0] == 'X':
                    self.winner = 'X'
                else:
                    self.winner = 'O'
                self.winC = True

        for column in range(3):#Checks if user won vertically.
            if gameList[0][column] == gameList[1][column] == gameList[2][column] and gameList[0][column] != '':
                self.winColumn = column
                if gameList[row][0] == 'X':
                    self.winner = 'X'
                else:
                    self.winner = 'O'
                self.winC = True

        if gameList[0][0] == gameList[1][1] == gameList[2][2]and gameList[0][0] != '':#Checks if user won diagonally.

            self.winDiag = 0
            if gameList[row][0] == 'X':
                self.winner = 'X'
            else:
                self.winner = 'O'

            self.winC = True

        if gameList[0][2] == gameList[1][1] == gameList[2][0]and gameList[0][2] != '':#Checks if user won diagonally.

            self.winDiag = 1
            if gameList[row][0] == 'X':
                self.winner = 'X'
            else:
                self.winner = 'O'

            self.winC = True    

    def Vict(self, win):#Checks if someone won and retrieves the winner information such as user and row or column.
        
        if self.winRow != -1:
            yPoint = int(mid + (self.winRow * blockSize))
            win.blit(hPic, ((sw / 24), yPoint - (sw / 15)))
            
        if self.winColumn != -1:
            xPoint = int(mid + (self.winColumn * blockSize))
            win.blit(vPic, (xPoint - (sl / 20), (sl / 24)))

        if self.winDiag == 0:
            win.blit(d0Pic, (100,65))

        if self.winDiag == 1:
            win.blit(d1Pic, (100,65))
            

            
def RedrawGameWindow():#Redraw function. Manages all the redraw for pygame.
    win.fill(WHITE)

    pygame.draw.line(win, (0, 0, 0), (blockSize,0), (blockSize, sl))#Horizontal line.
    pygame.draw.line(win, (0, 0, 0), (2 * blockSize,0), ((2 * blockSize), sl))#Horizontal line.

    pygame.draw.line(win, (0, 0, 0), (0,blockSize), (sw, blockSize))#Vertical line.
    pygame.draw.line(win, (0, 0, 0), (0,2 * blockSize), (sw, 2 * blockSize))#Vertical line.

    T.draw(win)
    T.Check()
    T.Vict(win)
    
    pygame.display.update()

T = Frame()#Calls the frame object.

run = True
while run:#Main Game Loop.

    clock.tick(20)
    
    for event in pygame.event.get():#Gets events. For example when the left mouse if clicked.

        if event.type == pygame.QUIT:#If the user closes the application.
            run = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not(T.winC) and not(T.boardFull):#Makes sure the game isn't over and checks if the user clicked.
            if event.button == 1:#Checks if the event was a left click.
                
                mouseP = pygame.mouse.get_pos()#Gets the x and y co-ordinates of the click.

                T.UserUpdate(mouseP)#Updates the row and column of the click.
                
                if T.vClick:#Checks if the click was on a proper tile.
                    T.clickCounter += 1#Adds one when the click has been validated.
                    if T.clickCounter < 9 and not(T.winC):#Checks if the counter in less than 9 and no one has won yet.
                        T.CompUpdate(CompMove())#Once users move is completely validated computer will play.

    if T.winC or T.boardFull:#If someone has won or it's a draw the game will end.
        run = False
        #pygame.quit()
        sys.exit()

    RedrawGameWindow()

    
