# 1-dimensional binary cellular automata example
# this is not done for maximum efficiency
# the line is a simple list with a simulated wrap-around if desired
# each bit and the bit to the left and right of it
# on the line is treated as a binary number
# 001 is 1 decimal and 111 is 7 decimal
# so a rule can be tested simply by seeing the sum
# of the bits
# and the rule itself is just a list of numbers to match
# [0, 7] for example means if the sum of the bits is 0 or 7
# then turn the bit on in the next iteration

# http://psoup.math.wisc.edu/mcell/rullex_1dbi.html
# http://psoup.math.wisc.edu/mcell/ca_rules.html
# http://psoup.math.wisc.edu/mcell/ca_gallery.html
# http://psoup.math.wisc.edu/mcell/rullex_1dto.html

from wrappers import Turtle
from random import randint

# wrapper for any additional drawing routines
# that need to know about each other
class WolframTurtle(Turtle):
    def wolframRule(self, str):
        """convert hex str to list of numbers"""
        hex = {'F':[1,1,1,1],'E':[1,1,1,0],'D':[1,1,0,1],'C':[1,1,0,0],
               'B':[1,0,1,1],'A':[1,0,1,0],'9':[1,0,0,1],'8':[1,0,0,0],
               '7':[0,1,1,1],'6':[0,1,1,0],'5':[0,1,0,1],'4':[0,1,0,0],
               '3':[0,0,1,1],'2':[0,0,1,0],'1':[0,0,0,1],'0':[0,0,0,0]}
        # first create a binary list
        str = str.upper()
        bList = []
        for c in str:
            bList += hex[c]
        # multiply each item in the list by its position
        # only return the non-zero items
        bList.reverse()
        nList = []
        for i in range(len(bList)):
            if bList[i]: nList.append(i)
        #print str, nList, bList
        return nList

    def drawLine(self, line, x, y):
        points = []
        for i in range(len(line)):
            if line[i]:
                # KEA 2004-05-10
                # it is faster to just draw on the BitmapCanvas directly
                # and even faster to use the drawPointList method
                # in fact this whole example doesn't have anything to
                # do with turtle graphics :)
                #self.plot(x + i, y)
                #self.canvas.drawPoint((x + i, y))
                points.append((x + i, y))
        self.canvas.drawPointList(points)
                

    def randomLine(self, n):
        r = []
        for i in range(n):
            r.append(randint(0, 1))
        return r

def draw(canvas):
    t = WolframTurtle(canvas)
    t.cls()

    # change wrap, ruleWidth, and r to get different patterns
    wrap = 1                # if 0, each side is padded with zeros
    ruleWidth = 2           # 1 or 2 - number of bits to check to the left or right
    
    r = t.randomLine(100)
    #r = [0] * 50 + [1] + [0] * 50    # a line with only one bit on in the center
    #r = [1] + [0] * 100
    #r = [1,0] * 9 + [1,1,1,1,0] + [1,1,0] * 20 + [0] * 20 + [1,0,0,1,0,1,1,1,1,0,0,0,1]
    
    print r

    pad = [0] * ruleWidth
    lpad = len(pad)
    
    if wrap:
        a = r[-lpad:] + r[:] + r[:lpad] # wrap line
    else:
        a = pad + r[:] + pad # wrap line

    """
    rule1 = [0, 7]
    rule2 = [1, 2, 3, 4, 5, 6]  # opposite of rule 1
    rule3 = [0, 5, 6, 7]
    rule4 = [0, 3, 5, 6, 7]
    rule5 = [1, 2, 4]           # opposite of rule 4
    rule6 = [1, 2, 4, 5, 6]
    #rule7 = [0, 3, 7]           # opposite of rule 6
    rule7 = [6,5,3,2,1] # R1,W6E
    rule8 = [5,4,2,1]   # R1,W36
    rule9 = [31,29,27,26,24,23,20,19,18,14,13,12,9,5,4,1]   # chaotic gliders
    rule10 = [29,27,26,25,24,23,19,17,12,11,6,4,3] # solitons D1
    """
    """
    rules.append(rule1)
    rules.append(rule2)
    rules.append(rule3)
    rules.append(rule4)
    rules.append(rule5)
    rules.append(rule6)
    rules.append(rule7)
    rules.append(rule8)
    """

    # create a method to turn rule notation like R1,W6E into
    # the search width (R1 is 1 cell to the left and 1 cell to
    # the right) and a list of numbers (W36 is [5,4,2,1]
    # create another method to handle this syntax
    # R2,C10,M1,S0,S1,B0,B3
    # from http://psoup.math.wisc.edu/mcell/rullex_1dto.html
    # 1D CA at http://psoup.math.wisc.edu/mcell/rullex_1dbi.html

    rules = []          # now create a list of rules
    if ruleWidth == 1:
        rules.append(t.wolframRule("36"))       # brownian motion
        rules.append(t.wolframRule("6E"))       # fishing-net
        rules.append(t.wolframRule("16"))       # heavy triangles
        rules.append(t.wolframRule("5A"))       # linear a
        rules.append(t.wolframRule("96"))       # linear b
        rules.append(t.wolframRule("12"))       # pascal's triangle (use just a single bit in the center)
    else:
        rules.append(t.wolframRule("BC82271C")) # bermuda triangle
        rules.append(t.wolframRule("AD9C7232")) # chaotic gliders
        rules.append(t.wolframRule("89ED7106")) # compound gliders
        rules.append(t.wolframRule("1C2A4798")) # fliform gliders 1
        rules.append(t.wolframRule("5C6A4D98")) # fliform gliders 2
        rules.append(t.wolframRule("5F0C9AD8")) # fish bones
        rules.append(t.wolframRule("B51E9CE8")) # glider p106 W4668ED14
        rules.append(t.wolframRule("4668ED14")) # raindrops

    x = 10
    original = a[:]
    lena = len(a) - (2 * lpad)
    for rule in rules:
        # R2 rules are too long to write on the screen
        # but this works fine for R1 rules
        if ruleWidth == 1:
            t.moveTo(x, 0)
            t.write(str(rule))

        #print a[lpad:-lpad]
        #print a
        t.drawLine(a[lpad:-lpad], x, 19)
        for i in range(500):
            b = [0] * lena # a[lpad:-lpad]
            for j in range(lena):
                # generalize this to check an arbitrary number of
                # cells to the left and right
                if ruleWidth == 1:
                    sum = a[j + lpad - 1] * 4 + a[j + lpad] * 2 + a[j + lpad + 1]
                else:
                    sum = a[j + lpad - 2] * 16 + a[j + lpad - 1] * 8 + a[j + lpad] * 4 + a[j + lpad + 1] * 2 + a[j + lpad + 2]
                if sum in rule:
                    b[j] = 1
                else:
                    b[j] = 0
            t.drawLine(b, x, 20 + i)
            if wrap:
                a = b[-lpad:] + b[:] + b[:lpad]
            else:
                a = pad + b[:] + pad
        x += lena + 10
        a = original[:]


