#!/usr/bin/python

# Monty Hall game

from random import randint

class MontyHall:
    
    prizedoor = 0
    guessdoor = 0
    bogusdoor = 0

    def __init__(self):
        
        pick = randint(1,3)
        self.prizedoor = pick

    def guessDoor(self, door):
        
        self.guessdoor = door

        # Show Bogus Door
        
        pick = randint(1,3)
        while pick == self.prizedoor or pick == self.guessdoor:
            pick = randint(1,3)
        self.bogusdoor = pick

    def changeDoor(self):
        
        doors = [1, 2, 3]
        doors.remove(self.bogusdoor)
        doors.remove(self.guessdoor)
        self.guessdoor = doors[0]

    def win(self):
        
        if self.guessdoor == self.prizedoor:
            return True
        else:
            return False
