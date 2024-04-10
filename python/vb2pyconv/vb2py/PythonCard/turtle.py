
"""
Created: 2001/10/12

__version__ = "$Revision: 1.21 $"
__date__ = "$Date: 2005/03/28 05:46:59 $"

"""

import math
import wx
import time

class AbstractTurtle:
    def __init__(self, size):
        """ this should be called after a subclass has done its init """
        self._size = size
        self._tracing = False
        self._degrees()

        # KEA 2002-03-01
        # define abbreviated versions of commands
        # these should still work even if the AbstractTurtle or BitmapTurtle
        # classes are subclasses

        # Get the class for an instance.
        selfClass = self.__class__
        # Assign several synonyms as Class attributes.
        if not hasattr(selfClass, 'fd'): selfClass.fd = selfClass.forward
        if not hasattr(selfClass, 'bk'): selfClass.bk = selfClass.backward
        if not hasattr(selfClass, 'back'): selfClass.back = selfClass.backward
        if not hasattr(selfClass, 'rt'): selfClass.rt = selfClass.right
        if not hasattr(selfClass, 'lt'): selfClass.lt = selfClass.left
        if not hasattr(selfClass, 'st'): selfClass.st = selfClass.showTurtle
        if not hasattr(selfClass, 'ht'): selfClass.ht = selfClass.hideTurtle
        if not hasattr(selfClass, 'pu'): selfClass.pu = selfClass.penUp
        if not hasattr(selfClass, 'pd'): selfClass.pd = selfClass.penDown
        if not hasattr(selfClass, 'clearScreen'): selfClass.clearScreen = selfClass._clear
        if not hasattr(selfClass, 'cg'): selfClass.cg = selfClass._clear
        if not hasattr(selfClass, 'cs'): selfClass.cs = selfClass._clear
        if not hasattr(selfClass, 'cls'): selfClass.cls = selfClass._clear
        if not hasattr(selfClass, 'pc'): selfClass.pc = selfClass.color
        if not hasattr(selfClass, 'setPenColor'): selfClass.setPenColor = selfClass.color
        if not hasattr(selfClass, 'bc'): selfClass.bc = selfClass.setBackColor
        if not hasattr(selfClass, 'draw'): selfClass.draw = selfClass.lineTo
        
        # this caused some problems when reset() in the subclass tried
        # to call its superclass AbstractTurtle.reset() so I probably wasn't doing
        # the method calls correctly
        # until I figure it out, I put all the needed code of reset() into
        # the subclass
        self.reset()
       
    def distance(self, t2):
        """returns the distance between two turtles"""
        return math.sqrt(math.pow(self._position[0] - t2._position[0], 2) + 
            math.pow(self._position[1] - t2._position[1], 2))

    def distanceXY(self, x, y):
        """returns the distance between turtle (self) and a point (x, y)"""
        return math.sqrt(math.pow(self._position[0] - x, 2) + math.pow(self._position[1] - y, 2))

    def _degrees(self, fullcircle=360.0):
        self._fullcircle = fullcircle
        self._invradian = math.pi / (fullcircle * 0.5)

    # illegal syntax, so I used None and the if tests instead
    #def plot(self, x=self._position[0], y=self._position[1]):
    def plot(self, x=None, y=None):
        """ override """
        pass

    # may have to do multiple versions of methods if case-sensitivity
    # is an issue
    def dot(self, x, y):
        """Logo plot, should only be 1 pixel wide though"""
        self.plot(x, y)
    # there are also setX and setY, but I don't remember if they do a plot or a moveTo...

    def getXY(self):
        """returns the turtle position"""
        return self._position

    # this may actually be the Logo plot command rather than
    # the equivelant of a moveTo
    # need to change these methods so they can handle
    # x, y or a tuple (x, y)
    def setXY(self, pos):
        """another name for moveTo
        this may actually be the Logo plot command rather than the
        equivelant of a moveTo"""
        self.moveTo(pos[0], pos[1])

    def line(self, x1, y1, x2, y2):
        """ override """
        pass

    def getHeading(self):
        """returns the turtle heading in degrees"""
        return self._angle

    def setHeading(self, angle):
        """set the turtle heading in degrees"""
        if self._dirty:
            self._drawTurtle()
        self._angle = angle % self._fullcircle
        if self._visible:
            self._drawTurtle()

    # my math is shaky, there has to be a shorter
    # way to return an angle between 0 - 360
    # remember however that 0,0 is the top-left corner
    # and positive x, positive y is the bottom-right
    # not positive x, negative y as in normal cartesian coordinates
    # THIS WAS HACKED TOGETHER SO IT COULD VERY WELL BE BUGGY
    def towardsXY(self, x, y):
        """returns the angle the turle would need to heading towards
        to face the position x, y"""
        xDir = x - self._position[0]
        yDir = y - self._position[1]
        try:
            angle = math.atan(yDir / xDir) * 180 / math.pi
        except:
            # should occur when xDir == 0.0 (divide by zero)
            if yDir == 0.0:
                return 0.0
            elif yDir < 0:
                return 90.0
            else:
                return 270.0
        if xDir < 0:
            angle = 180 - angle
        elif yDir < 0:
            angle = -1.0 * angle
        elif yDir > 0:
            angle = 360.0 - angle
        return angle

    def towards(self, t):
        """equivelant to towardsXY
        returns the angle the turle would need to heading towards
        to face the position x, y"""
        return self.towardsXY(t._position[0], t._position[1])

    def _radians(self):
        self._degrees(2.0 * math.pi)

    def forward(self, distance):
        """moves the turtle forward distance"""
        angle = self._angle * self._invradian
        self._goto(self._position[0] + distance * math.cos(angle),
                   self._position[1] - distance * math.sin(angle))
        
    def backward(self, distance):
        """moves the turtle backward distance"""
        self.forward(-distance)

    def left(self, angle):
        """turns the turtle left angle degrees"""
        if not self._drawingTurtle and self._dirty:
            self._drawTurtle()
        self._angle = (self._angle + angle) % self._fullcircle
        #print self._angle
        if not self._drawingTurtle and self._visible:
            self._drawTurtle()

    def right(self, angle):
        """turns the turtle right angle degrees"""
        self.left(-angle)
    
    def polygon(self, sides, distance):
        """draws a polygon with sides of length distance
        (e.g. polygon(4, 100) draws a square)
        polygon uses the forward and right methods to move the turtle"""
        angle = 360.0 / sides
        for i in range(sides):
            self.forward(distance)
            self.right(angle)

    def cPolygon(self, sides, radius):
        """draws a polygon centered on the current turtle position
        (e.g. cPolygon(4, 100) draws a square)
        the radius determines the size of the polygon, so that
        a circle with the same radius would intersect the vertices
        cPolygon uses the forward and right methods to move the turtle"""
        self.penUp()
        self.forward(radius)
        angle = 180.0 - (90.0 * (sides - 2) / sides)
        self.right(angle)   # must be the same as polygon turn above
        self.penDown()
        edge = 2 * radius * math.sin(math.pi / sides) # logo uses sin(180 / sides); Python uses radians
        self.polygon(sides, edge)
        self.left(angle)    # turn back to where we started
        self.penUp()
        self.backward(radius)
        self.penDown()

    def showTurtle(self):
        """makes the turtle visible
        the visibility of the turtle is independent of the turtle pen,
        use penUp() and penDown() to control the pen state"""
        if not self._visible:
            self._drawTurtle()
        self._visible = True

    def hideTurtle(self):
        """hides the turtle
        the visibility of the turtle is independent of the turtle pen,
        use penUp() and penDown() to control the pen state"""
        if self._dirty:
            self._drawTurtle()
        self._visible = False

    def _drawTurtle(self):
        """ override """
        pass

    def suspendOdometer(self):
        """suspends the turtle odometer"""
        self._odometerOn = False

    def resumeOdometer(self):
        """resumes the turtle odometer"""
        self._odometerOn = True

    def getOdometer(self):
        """returns the turtle odometer"""
        return self._odometer

    def resetOdometer(self):
        """resets the turtle odometer to 0.0"""
        self._odometer = 0.0

    def penUp(self):
        """raises the turtle pen, so no drawing will occur on subsequent
        commands until the pen is lowered with penDown"""
        self._drawing = False

    def penDown(self):
        """lowers the turtle pen"""
        self._drawing = True

    """
    # Logo functions to implement
    # see http://www.embry.com/rLogo/rLogoReference.html
    # and http://www.embry.com/rLogo/Index.html for a working logo applet
    
    # setpencolor will be handled by color()
    setpencolor and setpc (red) (green) (blue)
    - changes the pen color to the specified color.
    (red), (green), and (blue) must range from 0 to 255.
    
    setbackcolor and setbc (red) (green) (blue)
    - changes the background color to the specified color.
    (red), (green), and (blue) must range from 0 to 255

    write
    """
    def write(self, txt):
        """ override """
        pass
    
    def width(self, width):
        """set the pen width"""
        self._width = float(width)

    def home(self):
        """resets the turtle back to its starting location"""
        x0, y0 = self._origin
        self._goto(x0, y0)
        #self._goto(self._origin)
        self._angle = 0.0

    def _clear(self):
        """ override """
        pass

    # need to enhance this to support the various
    # color settings: colourName, rgb
    """ valid named colors from wxWindows http://www.lpthe.jussieu.fr/~zeitlin/wxWindows/docs/wxwin64.htm#wxcolourdatabase

aquamarine, black, blue, blue violet, brown, cadet blue, coral, cornflower blue, cyan, dark grey, 
dark green, dark olive green, dark orchid, dark slate blue, dark slate grey dark turquoise, dim 
grey, firebrick, forest green, gold, goldenrod, grey, green, green yellow, indian red, khaki, 
light blue, light grey, light steel blue, lime green, magenta, maroon, medium aquamarine, medium 
blue, medium forest green, medium goldenrod, medium orchid, medium sea green, medium slate blue, 
medium spring green, medium turquoise, medium violet red, midnight blue, navy, orange, orange 
red, orchid, pale green, pink, plum, purple, red, salmon, sea green, sienna, sky blue, slate 
blue, spring green, steel blue, tan, thistle, turquoise, violet, violet red, wheat, white, 
yellow, yellow green
    """

    def color(self, *args):
        """ override """
        pass

    def setBackColor(self, *args):
        """ override """
        pass

    def turtleDelay(self, s):
        """set the delay the turtle waits between drawing commands"""
        self._turtleDelay = s

    def reset(self):
        """ this should be called after a subclass has done its reset """

        width, height = self._size
        self._origin = width/2.0, height/2.0
        #print "width: %d, height: %d" % (width, height)
        #print "_origin.x: %f, _origin.y: %f" % (self._origin[0], self._origin[1])
        self._position = self._origin
        self._angle = 0.0
        # used for save and restore methods
        self._savePosition = self._position
        self._saveAngle = self._angle
        # used for LIFO stack of turtle state
        self._turtleStack = []
        self._odometer = 0.0
        # don't waste time tracking unless requested
        self._odometerOn = False
        # whether the pen is down
        self._drawing = True
        # the pen width
        self._width = 1
        # whether the turtle is visible, independent of the pen state
        self._visible = False
        # if _dirty then erase old turtle before drawing
        self._dirty = False
        # only true while drawing the turtle
        self._drawingTurtle = False
        # number of seconds to pause after drawing the turtle
        self._turtleDelay = 0

    # implicit save of pen state, penUp, pen state restore
    # KEA 2004-05-09
    # why the heck did I not require both x and y to be specified?
    # is that the way Logo works?
    def moveTo(self, x=None, y=None):
        """move the turtle to position x, y"""
        if x is None:
            x = self._position[0]
        if y is None:
            y = self._position[1]
        drawingState = self._drawing
        self._drawing = False
        self._goto(x, y)
        self._drawing = drawingState

    # this might get an implicit save of pen state, penDown, pen state restore
    def lineTo(self, x=None, y=None):
        """draw a line between the current turtle position and x, y
        the turtle is moved to the new x, y position"""
        if x is None:
            x = self._position[0]
        if y is None:
            y = self._position[1]
        self._goto(x, y)

    def _goto(self, x1, y1):
        """ override """
        self._position = (float(x1), float(y1))

    # could save more than position and heading below
    # perhaps the turtle color, whether it is shown or not?
    
    def save(self):
        """save the current turtle position and heading"""
        self._savePosition = self._position
        self._saveAngle = self._angle

    def restore(self):
        """restore the turtle position and heading to the last saved state"""
        self.moveTo(self._savePosition[0], self._savePosition[1])
        self.setHeading(self._saveAngle)

    def push(self):
        """push the current turtle position and heading onto a LIFO stack"""
        self._turtleStack.append((self._position, self._angle))

    def pop(self):
        """set the turtle position and heading to the state popped from a LIFO stack"""
        try:
            position, angle = self._turtleStack.pop()
            self.moveTo(position[0], position[1])
            self.setHeading(angle)
        except IndexError:
            pass


class BitmapTurtle(AbstractTurtle):
    def __init__(self, canvas):
        self.canvas = canvas
        #self.dc.SetOptimization(1)

        AbstractTurtle.__init__(self, canvas.size)

    # illegal syntax, so I used None and the if tests instead
    #def plot(self, x=self._position[0], y=self._position[1]):
    def plot(self, x=None, y=None):
        """draws a point at x, y using the current pen color and width
        note that the the turtle position is not changed by plot"""
        #self.dc.SetPen(self._color, self._width)
        ###self.dc.SetPen(self._pen)
        self.canvas._bufImage.SetPen(self._pen)
        if x is None:
            x = self._position[0]
        if y is None:
            y = self._position[1]
        # setting the color makes chaos1 over 3 times slower
        # so we probably need to do a simpler if/then check
        # prior to setting the color
        # that means keeping the variable in a form that is
        # simple to compare to the underlying dc canvas
        self.canvas.drawPoint((round(x), round(y)))
        # other variations
        #self.dc.DrawLine(x, y, x+1, y+1)
        #self._goto(x, y)   # actually this isn't equivelant

        # KEA 2005-03-26
        # this is necessary to force a screen update on the Mac
        if wx.Platform == '__WXMAC__' and self.canvas.autoRefresh:
            #self.canvas.Refresh()
            self.canvas.Update()

    def line(self, x1, y1, x2, y2):
        """draws a line from x1, y1 to x2, y2 using the current
        pen color and width
        note that the the turtle position is not changed by line"""
        ###self.dc.SetPen(self._pen)
        self.canvas._bufImage.SetPen(self._pen)
        ###self.dc.DrawLine(x1, y1, x2, y2)
        self.canvas.drawLine((round(x1), round(y1)), (round(x2), round(y2)))

        # KEA 2005-03-26
        # this is necessary to force a screen update on the Mac
        if wx.Platform == '__WXMAC__' and self.canvas.autoRefresh:
            #self.canvas.Refresh()
            self.canvas.Update()

    # probably replace this with a wxPython primitive for polygons
    # so we can support filled polys...
    # def polygon(self, sides, distance):


    """
    # Logo functions to implement
    # see http://www.embry.com/rLogo/rLogoReference.html
    # and http://www.embry.com/rLogo/ for a working logo applet
    
    # setpencolor will be handled by color()
    setpencolor and setpc (red) (green) (blue)
    - changes the pen color to the specified color.
    (red), (green), and (blue) must range from 0 to 255.
    
    setbackcolor and setbc (red) (green) (blue)
    - changes the background color to the specified color.
    (red), (green), and (blue) must range from 0 to 255
    """

    def write(self, txt):
        """prints txt at the current turtle position"""
        ###self.dc.DrawText(txt, self._position[0], self._position[1])
        self.canvas.drawText(txt, self._position)
    
    def _clear(self):
        ###self.dc.Clear()
        self.canvas.clear()
        self._dirty = False

        # KEA 2005-03-26
        # this is necessary to force a screen update on the Mac
        if wx.Platform == '__WXMAC__' and self.canvas.autoRefresh:
            #self.canvas.Refresh()
            self.canvas.Update()

    # need to enhance this to support the various
    # color settings: colourName, rgb
    """ valid named colors from wxWindows http://www.lpthe.jussieu.fr/~zeitlin/wxWindows/docs/wxwin64.htm#wxcolourdatabase

aquamarine, black, blue, blue violet, brown, cadet blue, coral, cornflower blue, cyan, dark grey, 
dark green, dark olive green, dark orchid, dark slate blue, dark slate grey dark turquoise, dim 
grey, firebrick, forest green, gold, goldenrod, grey, green, green yellow, indian red, khaki, 
light blue, light grey, light steel blue, lime green, magenta, maroon, medium aquamarine, medium 
blue, medium forest green, medium goldenrod, medium orchid, medium sea green, medium slate blue, 
medium spring green, medium turquoise, medium violet red, midnight blue, navy, orange, orange 
red, orchid, pale green, pink, plum, purple, red, salmon, sea green, sienna, sky blue, slate 
blue, spring green, steel blue, tan, thistle, turquoise, violet, violet red, wheat, white, 
yellow, yellow green
    """

    def width(self, w):
        """set the pen width"""
        if self._dirty:
            self._drawTurtle()
        #self._width = float(width)
        #self._width = w
        self._pen.SetWidth(w)
        if self._visible:
            self._drawTurtle()

    def color(self, *args):
        """set the foreground pen color
        both (r, g, b) values and named colors are valid"""
        
        if self._dirty:
            self._drawTurtle()
        # _color is actually the pen here
        # I need to just keep a pen and change the elements
        # of it
        if len(args) == 1:
            #self._color = wx.Pen(wx.NamedColour(args[0]))
            #self._color = wx.NamedColour(args[0])
            self._pen.SetColour(wx.NamedColour(args[0]))
        else:
            # self._color = wx.Pen(wx.Colour(args[0], args[1], args[2]))
            #self._color = wx.Colour(args[0], args[1], args[2])
            self._pen.SetColour(wx.Colour(args[0], args[1], args[2]))

        if self._visible:
            self._drawTurtle()
        # http://www.lpthe.jussieu.fr/~zeitlin/wxWindows/docs/wxwin265.htm
        # wxPen reference for pen width and style
        # colourdb.py for actual rgb color values of named colors in wxPython
        
        """
        print self._color.GetCap()
        print self._color.GetColour()
        #print self._color.GetDashes()
        print self._color.GetJoin()
        print self._color.GetStipple()
        print self._color.GetStyle()
        print self._color.GetWidth()
        """
        """ example output
        130
        (0, 0, 255)
        122
        <C wxBitmap instance at _3331988_wxBitmap_p>
        100
        1
        """
        
        #print self._color
        # self.dc.SetPen(wx.Pen(wx.NamedColour(args[0])))

    # the background is shared, not specific to each turtle
    def setBackColor(self, *args):
        """set the background pen color
        both (r, g, b) values and named colors are valid"""
        if len(args) == 1:
            self.canvas.backgroundColor = args[0]
        else:
            self.canvas.backgroundColor = (args[0], args[1], args[2])

    # non-optimized turtle
    # the turtle rotates from its base rather than a pivot point
    # in the "center" of the turtle shape
    #
    # as currently implemented drawTurtle is designed to erase
    # itself on a subsequent call to drawTurtle
    # in addition, this version does not use offscreen bitmaps
    # so an inversion is done on the pixels underneath the turtle
    # rather than showing the actual color of the current turtle
    def _drawTurtle(self):
        """private method for drawing the turtle when showTurtle()
        has been called to make the turtle visible"""
        #if not self._drawingTurtle:
        self._dirty = not self._dirty
        self._drawingTurtle = True
        drawingState = self._drawing
        currentPos = self._position
        currentAngle = self._angle
        #self._pen.SetCap(wx.CAP_PROJECTING)
        #self._pen.SetJoin(wx.JOIN_BEVEL)
        ###self.dc.SetPen(self._pen)
        self.canvas._bufImage.SetPen(self._pen)
        ###self.dc.SetLogicalFunction(wx.INVERT)
        self.canvas._bufImage.SetLogicalFunction(wx.INVERT)

        a = 30  # make a larger to get a bigger turtle
        b = 2 * a * math.tan(15 * self._invradian)
        c = a / math.cos(15 * self._invradian)
        self.pu(); self.forward(a); self.pd()
        self.left(165)
        self.forward(c)
        self.left(105)
        self.forward(b)
        self.left(105)
        self.forward(c)
        
        #self._pen.SetJoin(wx.JOIN_ROUND)
        #self._pen.SetCap(wx.CAP_ROUND)
        ###self.dc.SetLogicalFunction(wx.COPY)
        self.canvas._bufImage.SetLogicalFunction(wx.COPY)
        
        self._angle = currentAngle
        self._drawing = drawingState
        self._position = currentPos
        self._drawingTurtle = False
        if self._dirty and self._turtleDelay > 0:
            time.sleep(self._turtleDelay)

    def reset(self):
        """reset the turtle to its initial state"""
        self._size = self.canvas.size
        self._color = wx.Pen(wx.NamedColour("black"))
        self._pen = wx.Pen('black', 1, wx.SOLID)
        self.setBackColor('white')
        AbstractTurtle.reset(self)        

    def _goto(self, x1, y1):
        if not self._drawingTurtle:
            if self._odometerOn:
                self._odometer += self.distanceXY(x1, y1)
            if self._dirty:
                # this is necessary to avoid an endless loop as drawTurtle uses _goto
                #self._dirty = 0
                #visible = self._visible
                #self._visible = 0
                self._drawTurtle()
                #self._visible = visible

        x0, y0 = start = self._position
        self._position = (float(x1), float(y1))
        if self._drawing:
            """
            if self._tracing:
                dx = float(x1 - x0)
                dy = float(y1 - y0)
                distance = hypot(dx, dy)
                nhops = int(distance)
                #print "tracing %d %d %d %d" % (x0, y0, x0, y0)
                #self.dc.SetPen(self._color, self._width)
                self.dc.SetPen(self._pen)
                self.dc.DrawLine(x0, y0, x1, y1)
            else:
            """
            #print "%d %d %d %d" % (x0, y0, x0, y0)
            #self.dc.SetPen(self._color, self._width)
            if not self._drawingTurtle:
                ###self.dc.SetPen(self._pen)
                self.canvas._bufImage.SetPen(self._pen)
            ###self.dc.DrawLine(x0, y0, x1, y1)
            self.canvas.drawLine((round(x0), round(y0)), (round(x1), round(y1)))
                
        if not self._drawingTurtle:
            # KEA 2005-03-26
            # this is necessary to force a screen update on the Mac
            if wx.Platform == '__WXMAC__' and self.canvas.autoRefresh:
                self.canvas.Update()
            if self._visible:
                # this is necessary to avoid an endless loop as drawTurtle uses _goto
                #self._visible = 0
                #self._dirty = 1
                self._drawTurtle()
                #self._visible = 1
