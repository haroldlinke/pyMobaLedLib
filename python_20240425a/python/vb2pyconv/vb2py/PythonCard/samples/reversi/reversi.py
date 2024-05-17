#!/usr/bin/python

"""
Simplistic implementation of the board game reversi, better known as Othello.

The algorithm for determining legal moves is not particularly efficient since
no attempt is made to cache legal moves.
"""

"""
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2004/10/10 01:20:21 $"
"""

from PythonCard import dialog, model
from random import randint
import time
import wx

EMPTY = None
BLACK = True
WHITE = False
BOARDWIDTH = BOARDHEIGHT = 8

DIRECTIONS = ((-1, -1), (0, -1), (1, -1),
              (-1, 0),           (1, 0),
              (-1, 1),  (0, 1),  (1, 1))

BOARDCOLOR = 'dark green'
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
        self.board[(3, 3)] = WHITE
        self.board[(4, 4)] = WHITE
        self.board[(3, 4)] = BLACK
        self.board[(4, 3)] = BLACK
        
        # black always goes first
        self.nextMove = BLACK
        self.buildLegalMoves(self.nextMove)
        self.gameOver = False

    def opponentColor(self, color):
        if color == BLACK:
            return WHITE
        else:
            return BLACK

    def legalMove(self, column, row, color):
        """returns the number of pieces flipped if the move is legal
        otherwise it returns 0"""
        totalFlipped = 0
        if self.board[(column, row)] == EMPTY:
            opponent = self.opponentColor(color)
            # to be a legal move 
            #   the position must be empty
            #   the position must be adjacent to an opponent
            #     color piece
            #   searching in the direction of the opposing
            #     color piece there must be a position matching
            #     the starting position color
            #   the edges of the board don't count
            board = self.board
            for dx, dy in DIRECTIONS:
                flipped = 0
                x = column + dx
                y = row + dy
                if board.get((x, y), EMPTY) == opponent:
                    # now check to see if we run into our
                    # own color so we have something to flip
                    # if we run into an empty space or off the board
                    # then it isn't a legal move
                    while board.get((x, y), EMPTY) == opponent:
                        x += dx
                        y += dy
                        flipped += 1
                        if board.get((x, y), EMPTY) == color:
                            totalFlipped += flipped
        return totalFlipped

    def buildLegalMoves(self, color):
        """build a dictionary of legal moves with the (column, row) as the key
        and the number of pieces flipped as the value"""

        self.legalMoves = {}
        for column, row in self.board.keys():
            flipped = self.legalMove(column, row, color)
            if flipped:
                self.legalMoves[(column, row)] = flipped
        
    def legalMovesAvailable(self, color):
        self.buildLegalMoves(color)
        # look at all empty positions on the board to determine
        # whether any legal moves exist
        if self.legalMoves == {}:
            return False
        else:
            return True

    def makeMove(self, column, row, color):
        self.board[(column, row)] = color
        # now flip all the pieces        
        
        opponent = self.opponentColor(color)
        # to be a legal move 
        #   the position must be empty
        #   the position must be adjacent to an opponent
        #     color piece
        #   searching in the direction of the opposing
        #     color piece there must be a position matching
        #     the starting position color
        #   the edges of the board don't count
        board = self.board
        for dx, dy in DIRECTIONS:
            x = column + dx
            y = row + dy
            if board.get((x, y), EMPTY) == opponent:
                flip = []
                # now check to see if we run into our
                # own color so we have something to flip
                # if we run into an empty space or off the board
                # then it isn't a legal move
                while board.get((x, y), EMPTY) == opponent:
                    # add pieces to flip
                    flip.append((x, y))
                    x += dx
                    y += dy
                    if board.get((x, y), EMPTY) == color:
                        for position in flip:
                            board[position] = color
                        break
                    

        # change who has the next move
        # if there are no legal moves left for the opponent
        # then we check whether there are any legal moves
        # left for the current player
        # if neither has a legal move then the game is over
        if self.legalMovesAvailable(opponent):
            self.nextMove = opponent
        elif self.legalMovesAvailable(color):
            self.nextMove = color
        else:
            self.gameOver = True

    # computer is currently stupid and just
    # randomly picks from the available legal moves
    # if you lose then you're Mr. Gumby <wink>
    # what it should do instead is be able to use
    # various strategies such as flip the most pieces
    # favor certain positions like the edges but avoid the
    # the spots next to the corners (weighted positions)
    # okay, I added the flip the most pieces strategy
    # but it is still pretty dumb
    
    def doRandomComputerMove(self, color):
        legalMoves = self.legalMoves.keys()
        column, row = legalMoves[randint(0, len(legalMoves) - 1)]
        self.makeMove(column, row, color)

    def doFlipMostPiecesComputerMove(self, color):
        flipped = 0
        for position in self.legalMoves.keys():
            #print "  ", position, self.legalMoves[position]
            if self.legalMoves[position] > flipped:
                best = position
                flipped = self.legalMoves[best]
        #print "picked:", best, self.legalMoves[best], "\n"
        self.makeMove(best[0], best[1], color)

    def getScore(self):
        """return a tuple containing the number of 
        empty, black, and white squares"""
        score = {BLACK:0, WHITE:0, EMPTY:0}
        for value in self.board.values():
            score[value] += 1
        return score


class Reversi(model.Background):

    def on_initialize(self, event):        
        self.boardModel = GameBoard()
        self.components.bufOff.size = (BOARDWIDTH * CELLWIDTH + 1, BOARDHEIGHT * CELLHEIGHT + 1)
        self.singleItemExpandingSizerLayout()
        
        self.drawBoard()
        self.updateStatus()
        
        self.player = BLACK
        self.computer = WHITE
        self.lastHover = None
        if self.computer == BLACK:
            self.boardModel.doComputerMove(BLACK)


    def computerMove(self):
        if self.menuBar.getChecked('menuStrategyFlipMostPieces'):
            self.boardModel.doFlipMostPiecesComputerMove(self.computer)
        else:
            self.boardModel.doRandomComputerMove(self.computer)
        # sleep for a second to make it appear
        # the computer thought long and hard on her choice :)
        time.sleep(1)
        self.drawBoard()
        self.updateStatus()

    def newGame(self):
        self.boardModel.initializeBoard()
        self.drawBoard()
        self.updateStatus()
        if self.computer == BLACK:
            self.computerMove()

    def drawCell(self, x, y, state):
        view = self.components.bufOff
        if state in [BLACK, WHITE]:
            if state == BLACK:
                color = 'black'
            else:
                color = 'white'
            view.fillColor = color
            center = (x * CELLWIDTH + CELLWIDTH / 2 + 1, y * CELLHEIGHT + CELLHEIGHT / 2 + 1)
            view.drawCircle(center, round((CELLWIDTH / 2.0) - 3))
        else:
            view.fillColor = BOARDCOLOR
            view.foregroundColor = BOARDCOLOR
            view.drawRectangle((x * CELLWIDTH + 1, y * CELLHEIGHT + 1), (CELLWIDTH - 2, CELLHEIGHT - 2))
            view.foregroundColor = 'black'
        
    def drawBoard(self):
        view = self.components.bufOff
        view.autoRefresh = False
        view.backgroundColor = BOARDCOLOR
        view.clear()
        # draw the right and bottom edge borders
        view.drawLine((0, BOARDHEIGHT * CELLHEIGHT), (BOARDWIDTH * CELLWIDTH, BOARDHEIGHT * CELLHEIGHT))
        view.drawLine((BOARDWIDTH * CELLWIDTH, 0), (BOARDWIDTH * CELLWIDTH, BOARDHEIGHT * CELLHEIGHT))
        for x in range(BOARDWIDTH):
            view.drawLine((x * CELLWIDTH, 0), (x * CELLWIDTH, BOARDHEIGHT * CELLHEIGHT))
            for y in range(BOARDHEIGHT):
                view.drawLine((0, y * CELLHEIGHT), (BOARDWIDTH * CELLWIDTH, y * CELLHEIGHT))
                state = self.boardModel.board[(x, y)]
                self.drawCell(x, y, state)
        view.autoRefresh = True
        view.refresh()
        if wx.Platform == '__WXMAC__':
            # Mac won't update screen even after a Blit 
            # until the event handler ends, so we have to force an update
            view.redraw()

    def updateStatus(self):
        if self.boardModel.gameOver:
            score = self.boardModel.getScore()
            playerScore = score[self.player]
            computerScore = score[self.computer]
            scoreString = "Black: %d  White: %d" % (score[BLACK], score[WHITE])
            if playerScore > computerScore:
                message = "Player won!"
            elif playerScore < computerScore:
                message = "Computer won!"
            else:
                message = "Tie Game"
            status = message + "  -  " + scoreString
        else:
            if self.boardModel.nextMove == BLACK:
                status = "Black's move"
            else:
                status = "White's move"
        self.statusBar.text = status

    def on_bufOff_mouseMove(self, event):
        x, y = event.position
        x = x / CELLWIDTH
        y = y / CELLHEIGHT
        #if self.boardModel.legalMove(x, y, self.boardModel.nextMove):
        if (x, y) != self.lastHover:
            # erase lastHover if needed
            if self.lastHover and self.boardModel.board[self.lastHover] is None:
                self.drawCell(self.lastHover[0], self.lastHover[1], EMPTY)
            # if the move is legal, show it
            if self.boardModel.legalMoves.get((x, y), None):
                self.drawCell(x, y, self.player)
            # don't track positions outside the valid range
            if (x >= 0 and x < BOARDWIDTH) and (y >= 0 and y < BOARDHEIGHT):
                self.lastHover = (x, y)

    def on_bufOff_mouseUp(self, event):
        x, y = event.position
        # this is a simplistic translation
        # when users click on the lines
        # separating cells they may get a cell
        # they didn't expect
        x = x / CELLWIDTH
        y = y / CELLHEIGHT
        if self.boardModel.legalMove(x, y, self.boardModel.nextMove):
            self.boardModel.makeMove(x, y, self.boardModel.nextMove)
            self.drawBoard()
            self.updateStatus()
            if not self.boardModel.gameOver:
                if self.boardModel.nextMove == self.computer:
                    self.computerMove()
        event.skip()

    def on_menuFileNewGame_select(self, event):
        self.newGame()


if __name__ == '__main__':
    app = model.Application(Reversi)
    app.MainLoop()
