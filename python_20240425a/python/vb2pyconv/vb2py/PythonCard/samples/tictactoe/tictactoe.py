#!/usr/bin/python

"""
KEA notes to myself

Created: 2001-07-29
__version__ = "$Revision: 1.22 $"
__date__ = "$Date: 2004/08/12 19:19:04 $"
__author__ = "Kevin Altis <altis@semi-retired.com>"

It's a little too early to do a Tetris clone, so here's a Tic Tac Toe game
complete with a computer opponent that has no strategy (he's Mr. Gumby after
all). Not bad for an afternoon of work, including the image touchups.

There could very well be bugs in the "logic" since I could only play so many
games of Tic Tac Toe before going insane, so feel free to test away.

The main point of this exercise is to test the framework.

"""

import time
import random

from PythonCard import graphic, model

class Tic(model.Background) :

    def on_initialize(self, event):
        self.computerImage = 'lrggumby.gif'
        self.computer = -5
        self.human = 5
        self.draw = 0
        self.humanImage = 'sillywalk.gif'
        self.emptyImage = 'empty.gif'
        self.playfieldButtons = []
        for i in range(8):
            self.playfieldButtons.append(self.components['btn' + str(i + 1)])
        self.clearBoard()

    def setButtonImage(self, btnName, image):
        button = self.components[btnName]
        button.bitmap = graphic.Bitmap(image)
        #print 'setButtonImage', btnName, image
                       
    def clearBoard(self):
        self.board = [0,0,0,
                      0,0,0,
                      0,0,0]
        for i in range(9):
            name = 'btn' + str(i)
            self.setButtonImage(name, self.emptyImage)
        chk = self.components.chkComputerFirst
        if chk.checked:
            self.computerFirst = 1
        else:
            self.computerFirst= 0
        self.turn = 0
        self.gameOverFlag = 0
        wStaticTurn = self.components.staticTurn
        if self.computerFirst:
            self.doComputerMove()
        wStaticTurn.text = 'Your Turn'

    # the computer could be "smart" but that would be boring
    # since every game would be a draw or the human would
    # have to be really "slow"
    # games are more fun this way
    # also this way I'll get email from overly helpful computer science majors
    # telling me how to do the computer logic for tic-tac-toe ;-)
    def getRandomMove(self):
        legalMoves = []
        for i in range(9):
            if self.board[i] == 0:
                legalMoves.append(i)
        #print 'legal moves:', legalMoves
        return random.choice(legalMoves)

    def threeInARow(self):
        # the winning combos
        # yes, there is a clever way of calculating these
        # but it is left as an exercise for the reader
        combos =[
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8],[2,4,6]
            ]
        winner = 0
        for combo in combos:
            #print combo
            # I bet there is a clever map or lambda I could use here?!
            total = self.board[combo[0]] + self.board[combo[1]] + self.board[combo[2]]
            if total == self.computer * 3 or total == self.human * 3:
                winner = total
                break
        return winner

    def gameOver(self):
        """
        returns a tuple showing whether the game is over (0 or 1)
        and who won (computer, human, draw)
        if the game isn't over, then the 2nd item is None
        """

        # a game is is over when one player gets 3 in a row
        # or there are no empty squares left on the board
        # but you knew that...
        winner = self.threeInARow()
        #print "winner", winner
        if winner == 0:
            if 0 in self.board:
                return (0, None)
            else:
                # no winner and no board positions open, so must be a draw
                return (0, self.draw)
        else:
            # somebody won
            return (1, winner)

    def legalMove(self, btnName):
        if self.gameOverFlag:
            return 0
        pos = int(btnName[3])    # 0,1,2,3,4,5,6,7,8
        if self.board[pos] == 0:
            return 1

    def displayGameOverMessage(self, winner):
        # game is over
        self.gameOverFlag = 1
        #print "game over", gameOverMan
        wStaticTurn = self.components.staticTurn
        wStaticTurn.text = "Game Over"
        #print "displayGameOverMessage winner", winner
        if winner[1] == self.computer * 3:
            strWinner = "Mr. Gumby is the winner!"
        elif winner[1] == self.human * 3:
            strWinner = "You Won!"
        else:
            strWinner = "It's a draw."
        wStaticTurn.text = strWinner
        #dlg = dialog.messageDialog(self, strWinner, "Game Over", wx.ICON_EXCLAMATION | wx.OK)

    # this is automatically called at the end of a human move
    # or at the beginning of a new game if the computer goes first
    # so we can do most of the game logic here
    def doComputerMove(self):
        # first check to see if the human won on the last move or the game is a draw
        winner = self.gameOver()
        if winner[0] or winner[1] == self.draw:
            self.displayGameOverMessage(winner)
        else:
            # if not, then the computer does a move
            move = self.getRandomMove()
            # print move
            self.board[move] = self.computer
            self.setButtonImage('btn' + str(move), self.computerImage)
            # check to see if the computer just won or the game is a draw
            winner = self.gameOver()
            if winner[0] or winner[1] == self.draw:
                self.displayGameOverMessage(winner)



    # you'll notice all the button scripts are exactly the same
    # so now that messages are passed up the hierarchy, only a
    # single background mouseClick handler
    # is required. I left the on_btn0_mouseClick to show off
    # that we're binding correctly, that handler isn't actually
    # required

    def isPlayfieldButton(self, button):
        # only the playfield uses ImageButton, so this is safe
        #if isinstance(button, registry.Registry.getInstance().getComponentClass('ImageButton')):
        if button in self.playfieldButtons:
            return 1
        else:
            return 0

    def on_mouseUp(self, event):
        # make sure that we only handle a mouseClick for
        # the ImageButtons on the playfield
        if self.isPlayfieldButton(event.target):
            btnName = event.target.name
            print "bg1 mouseUp handler", btnName
            pos = int(btnName[3])
            #print event.target.getName(), 'clicked'
            if self.legalMove(btnName):
                self.board[pos] = self.human
                self.setButtonImage(btnName, self.humanImage)
                self.doComputerMove()
            else:
                print "illegal move"
                # play a beep or do some other warning, a dialog would be too much
        else:
            event.skip()

    def on_btn0_mouseUp(self, event):
        btnName = event.target.name
        print "btn0 mouseUp handler", btnName
        pos = int(btnName[3])
        #print event.target.getName(), 'clicked'
        if self.legalMove(btnName):
            self.board[pos] = self.human
            self.setButtonImage(btnName, self.humanImage)
            self.doComputerMove()
        else:
            print "illegal move"
            # play a beep or do some other warning, a dialog would be too much
    

    def on_btnNewGame_mouseClick(self, event):
        self.clearBoard()


if __name__ == '__main__':
    app = model.Application(Tic)
    app.MainLoop()
