#!/usr/bin/python

"""
Simplistic implementation of the board game reversi, better known as Othello.

The algorithm for determining legal moves is not particularly efficient since
no attempt is made to cache legal moves.
"""

"""
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2004/10/10 01:20:20 $"
"""

from PythonCard import model
from random import randint
import time

EMPTY = 0
BLOCK = 1
HUMAN = RED = 2
COMPUTER = PLAYER2 = BLUE = 3
BOARDWIDTH = BOARDHEIGHT = 7

DIRECTIONS = ((-1, -1), (0, -1), (1, -1),
              (-1, 0),           (1, 0),
              (-1, 1),  (0, 1),  (1, 1))

SPLIT = DIRECTIONS
JUMP = ((-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
        (-2, -1),                             (2, -1),
        (-2, 0),                              (2, 0),
        (-2, 1),                              (2, 1),
        (-2, 2),  (-1, 2),  (0, 2),  (1, 2),  (2, 2))

BOARDCOLOR = 'black'
GRIDCOLOR = 'cyan'
BLOCKCOLOR = 'light gray'
CELLWIDTH = CELLHEIGHT = 37

class GameBoard:
    def __init__(self):
        self.initializeBoard()

    def initializeBoard(self):
        self.board = {}
        # the board references are column, row
        # to simplify x, y translation
        for column in range(BOARDWIDTH):
            for row in range(BOARDHEIGHT):
                self.board[(column, row)] = EMPTY
        # different board arrangements could be used
        # to vary the gameplay
        self.board[(3, 0)] = BLOCK
        self.board[(0, 3)] = BLOCK
        self.board[(6, 3)] = BLOCK
        self.board[(3, 6)] = BLOCK

        self.board[(0, 0)] = HUMAN
        self.board[(6, 6)] = HUMAN
        self.board[(6, 0)] = COMPUTER
        self.board[(0, 6)] = COMPUTER
        
        # black always goes first
        self.nextMove = HUMAN
        #self.buildLegalMoves(self.nextMove)
        self.gameOver = False

    def opponentColor(self, color):
        if color == HUMAN:
            return COMPUTER
        else:
            return HUMAN

    def buildLegalMoves(self, column, row):
        """build a dictionary of legal moves with the (column, row) as the key
        and the number of pieces flipped as the value"""

        board = self.board
        legalMoves = {}
        for dx, dy in SPLIT:
            x = column + dx
            y = row + dy
            if board.get((x, y), None) == EMPTY:
                legalMoves[(x, y)] = 1
        for dx, dy in JUMP:
            x = column + dx
            y = row + dy
            if board.get((x, y), None) == EMPTY:
                legalMoves[(x, y)] = 1
        return legalMoves

    def makeMove(self, fromX, fromY, toX, toY):
        board = self.board
        color = board[(fromX, fromY)]
        opponent = self.opponentColor(color)
        
        dx = toX - fromX
        dy = toY - fromY

        if abs(dx) == 2 or abs(dy) == 2:
            # jump, so move the piece
            board[(fromX, fromY)] = EMPTY
        board[(toX, toY)] = color

        # now flip all the opponent pieces touching the new position
        for dx, dy in DIRECTIONS:
            x = toX + dx
            y = toY + dy
            if board.get((x, y), None) == opponent:
                board[(x, y)] = color
        
        self.nextMove = opponent

    def getScore(self):
        """return a tuple containing the number of 
        empty, black, and white squares"""
        score = {HUMAN:0, COMPUTER:0, EMPTY:0, BLOCK:0}
        for value in self.board.values():
            score[value] += 1
        return score


class Ataxx(model.Background):

    def on_initialize(self, event):        
        self.boardModel = GameBoard()
        self.components.bufOff.size = (BOARDWIDTH * CELLWIDTH + 1, BOARDHEIGHT * CELLHEIGHT + 1)
        self.singleItemExpandingSizerLayout()
        
        self.drawBoard()
        self.updateStatus()
        
        self.player = HUMAN
        self.computer = COMPUTER
        self.lastHover = None
        self.startLocation = None

##        # this is leftover from the reversi sample
##        # and has to be updated once there is an ataxx computer strategy
##        # rather than just human vs. human
##        if self.computer == HUMAN:
##            self.boardModel.doComputerMove(HUMAN)
##
##
##    def computerMove(self):
##        if self.menuBar.getChecked('menuStrategyFlipMostPieces'):
##            self.boardModel.doFlipMostPiecesComputerMove(self.computer)
##        else:
##            self.boardModel.doRandomComputerMove(self.computer)
##        # sleep for a second to make it appear
##        # the computer thought long and hard on her choice :)
##        time.sleep(1)
##        self.drawBoard()
##        self.updateStatus()

    def newGame(self):
        self.boardModel.initializeBoard()
        self.drawBoard()
        self.updateStatus()
##        if self.computer == COMPUTER:
##            self.computerMove()

    def drawCell(self, x, y, state):
        view = self.components.bufOff
        if state in [HUMAN, COMPUTER]:
            if state == HUMAN:
                color = 'red'
            else:
                color = 'blue'
            view.fillColor = color
            view.foregroundColor = 'black'
            center = (x * CELLWIDTH + CELLWIDTH / 2 + 1, y * CELLHEIGHT + CELLHEIGHT / 2 + 1)
            view.drawCircle(center, round((CELLWIDTH / 2.0) - 3))
        elif state == BLOCK:
            view.fillColor = BLOCKCOLOR
            view.foregroundColor = BLOCKCOLOR
            view.drawRectangle((x * CELLWIDTH + 3, y * CELLHEIGHT + 3), (CELLWIDTH - 5, CELLHEIGHT - 5))
        else:
            view.fillColor = BOARDCOLOR
            view.foregroundColor = BOARDCOLOR
            view.drawRectangle((x * CELLWIDTH + 1, y * CELLHEIGHT + 1), (CELLWIDTH - 2, CELLHEIGHT - 2))
        
    def drawBoard(self):
        view = self.components.bufOff
        view.autoRefresh = False
        view.backgroundColor = BOARDCOLOR
        view.clear()
        # draw the right and bottom edge borders
        view.foregroundColor = GRIDCOLOR
        view.drawLine((0, BOARDHEIGHT * CELLHEIGHT), (BOARDWIDTH * CELLWIDTH, BOARDHEIGHT * CELLHEIGHT))
        view.drawLine((BOARDWIDTH * CELLWIDTH, 0), (BOARDWIDTH * CELLWIDTH, BOARDHEIGHT * CELLHEIGHT))
        for x in range(BOARDWIDTH):
            view.foregroundColor = GRIDCOLOR
            view.drawLine((x * CELLWIDTH, 0), (x * CELLWIDTH, BOARDHEIGHT * CELLHEIGHT))
            for y in range(BOARDHEIGHT):
                view.foregroundColor = GRIDCOLOR
                view.drawLine((0, y * CELLHEIGHT), (BOARDWIDTH * CELLWIDTH, y * CELLHEIGHT))
                state = self.boardModel.board[(x, y)]
                self.drawCell(x, y, state)
        view.autoRefresh = True
        view.refresh()

    def updateStatus(self):
        if self.boardModel.gameOver:
            score = self.boardModel.getScore()
            playerScore = score[self.player]
            computerScore = score[self.computer]
            scoreString = "Red: %d  Blue: %d" % (score[HUMAN], score[COMPUTER])
            if playerScore > computerScore:
                message = "Player won!"
            elif playerScore < computerScore:
                message = "Computer won!"
            else:
                message = "Tie Game"
            status = message + "  -  " + scoreString
        else:
            if self.boardModel.nextMove == HUMAN:
                status = "Red's move"
            else:
                status = "Blue's move"
        self.statusBar.text = status

    def on_bufOff_mouseDown(self, event):
        self.startLocation = None
        x, y = event.position
        x = x / CELLWIDTH
        y = y / CELLHEIGHT
        if (x >= 0 and x < BOARDWIDTH) and (y >= 0 and y < BOARDHEIGHT):
            if self.boardModel.board[(x, y)] == self.boardModel.nextMove:
                self.startLocation = (x, y)
                self.legalMoves = self.boardModel.buildLegalMoves(x, y)
        
    def on_bufOff_mouseDrag(self, event):
        if self.startLocation:
            x, y = event.position
            x = x / CELLWIDTH
            y = y / CELLHEIGHT
            #if self.boardModel.legalMove(x, y, self.boardModel.nextMove):
            if (x, y) != self.lastHover:
                # erase lastHover if needed
                if self.lastHover and self.boardModel.board[self.lastHover] is EMPTY:
                    self.drawCell(self.lastHover[0], self.lastHover[1], EMPTY)
                # if the move is legal, show it
                if self.legalMoves.get((x, y), None):
                    self.drawCell(x, y, self.boardModel.nextMove)
                # don't track positions outside the valid range
                if (x >= 0 and x < BOARDWIDTH) and (y >= 0 and y < BOARDHEIGHT):
                    self.lastHover = (x, y)

    def on_bufOff_mouseUp(self, event):
        if self.startLocation:
            x, y = event.position
            # this is a simplistic translation
            # when users click on the lines
            # separating cells they may get a cell
            # they didn't expect
            x = x / CELLWIDTH
            y = y / CELLHEIGHT
            if self.legalMoves.get((x, y), None):
                self.boardModel.makeMove(self.startLocation[0], self.startLocation[1], x, y)
                self.drawBoard()
                self.updateStatus()

    def on_menuFileNewGame_select(self, event):
        self.newGame()


if __name__ == '__main__':
    app = model.Application(Ataxx)
    app.MainLoop()
