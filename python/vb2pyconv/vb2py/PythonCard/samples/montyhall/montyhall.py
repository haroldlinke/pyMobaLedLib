#!/usr/bin/python

# Monty Hall GUI

from PythonCard import model

import mh

class MontyHallApp(model.Background):
    
    imgdoor1 = 'closed1.jpg'
    imgdoor2 = 'closed2.jpg'
    imgdoor3 = 'closed3.jpg'
    imgbooby = 'open-cents.jpg'
    imgprize = 'open-dollars.jpg'
    games = 0
    wins = 0
    changes = 0
    wins_change = 0
    
    def on_initialize(self, event):
        self.game = mh.MontyHall()

    def on_bOne_mouseClick(self, event):
        self.guessDoor(1)
        
    def on_bTwo_mouseClick(self, event):
        self.guessDoor(2)
        
    def on_bThree_mouseClick(self, event):
        self.guessDoor(3)
        
    def on_bYes_mouseClick(self, event):
        self.changeDoor(True)
        
    def on_bNo_mouseClick(self, event):
        self.changeDoor(False)
        
    def on_bAgain_mouseClick(self, event):
        self.playAgain()
        
    def on_bResults_mouseClick(self, event):
        self.showResults()
        
    def guessDoor(self, door):

        self.game.guessDoor(door)
        
        if self.game.bogusdoor == 1:
            self.components.image1.file = self.imgbooby
        elif self.game.bogusdoor == 2:
            self.components.image2.file = self.imgbooby
        else:
            self.components.image3.file = self.imgbooby
        
        self.components.bOne.enabled = False
        self.components.bTwo.enabled = False
        self.components.bThree.enabled = False
        self.components.bResults.enabled = False
        self.components.bAgain.enabled = False
        self.components.bYes.enabled = True
        self.components.bNo.enabled = True
        self.components.txtBox.text = self.guessMsg()
        
    def changeDoor(self, change):
        
        if change:
            self.game.changeDoor()
            self.changes += 1
            if self.game.win():
                self.wins_change += 1
            
        self.games += 1
        
        if self.game.win():
            self.wins += 1
            img = self.imgprize
        else:
            img = self.imgbooby
            
        if self.game.guessdoor == 1:
            self.components.image1.file = img
        elif self.game.guessdoor == 2:
            self.components.image2.file = img
        else:
            self.components.image3.file = img

        self.components.bYes.enabled = False
        self.components.bNo.enabled = False
        self.components.bResults.enabled = True
        self.components.bAgain.enabled = True
        self.components.txtBox.text = self.components.txtBox.text + self.prizeMsg()

    def playAgain(self):
        
        self.game = mh.MontyHall()
        self.components.image1.file = self.imgdoor1
        self.components.image2.file = self.imgdoor2
        self.components.image3.file = self.imgdoor3
        self.components.bOne.enabled = True
        self.components.bTwo.enabled = True
        self.components.bThree.enabled = True
        self.components.bYes.enabled = False
        self.components.bNo.enabled = False
        self.components.bResults.enabled = False
        self.components.bAgain.enabled = False
        self.components.txtBox.text = ''
                
    def showResults(self):
        
        self.components.txtBox.text = self.resultsMsg()
        self.components.bResults.enabled = False
        self.resetResults()

    def resetResults(self):
        
        self.games = 0
        self.changes = 0
        self.wins = 0
        self.wins_change = 0

    def guessMsg(self):
        
        msg = """
            You guessed Door %d

            Monty opens Door %d
            to reveal a worthless object.
            """
        return msg % (self.game.guessdoor, self.game.bogusdoor)

    def prizeMsg(self):
        
        msg = """
            Monty opens Door %d
            to reveal %s
             """
        if self.game.win():
            prize = "A GREAT PRIZE."
        else:
            prize = "a booby prize."
            
        return msg % (self.game.guessdoor, prize)

    def resultsMsg(self):
        
        games = self.games
        changes = self.changes
        wins = self.wins
        wins_change = self.wins_change
        
        no_changes = games - changes
        wins_no_change = wins - wins_change
        lost_change = changes - wins_change
        lost_no_change = no_changes - wins_no_change
        
        msg = """
            Games Played: %d

            Changed Guess: %d
            Won: %d Lost: %d

            No Change: %d
            Won: %d Lost: %d
            """
        return msg % (games, changes, wins_change, lost_change, no_changes, wins_no_change, lost_no_change)

if __name__ == '__main__':
    app = model.Application(MontyHallApp)
    app.MainLoop()
