#!/usr/bin/python

"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/09/14 23:41:14 $"
"""

"""
try:
    import Numeric
    import random
    import RandomArray
    haveNumeric = True
except ImportError:
    haveNumeric = False
"""

import os
import wx
from PythonCard import model

class Doodle(model.Background):

    def on_initialize(self, event):
        self.singleItemExpandingSizerLayout()
        
        ## getting all the colors and linestyles  for random objects
        # don't need this since PythonCard has already called it
        #wx.lib.colourdb.updateColourDB()
        self.colors = wx.lib.colourdb.getColourList()
        self.DrawTest()

    def DrawTest(self,event=None):
        wx.GetApp().Yield()
        import random
        import RandomArray
        Range = (-10,10)
        colors = self.colors

        #self.BindAllMouseEvents()
        Canvas = self.components.float

        Canvas.ClearAll()
        Canvas.SetProjectionFun(None)

        ## Random tests of everything:
        
        # Rectangles
        for i in range(3):
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            lw = random.randint(1,5)
            cf = random.randint(0,len(colors)-1)
            h = random.randint(1,5)
            w = random.randint(1,5)
            Canvas.AddRectangle(x,y,h,w,LineWidth = lw,FillColor = colors[cf])
          
        # Ellipses
        for i in range(3):
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            lw = random.randint(1,5)
            cf = random.randint(0,len(colors)-1)
            h = random.randint(1,5)
            w = random.randint(1,5)
            Canvas.AddEllipse(x,y,h,w,LineWidth = lw,FillColor = colors[cf])
          
##            # Dots -- Does anyone need this?
##            for i in range(5):
##                x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
##                D = random.randint(1,50)
##                lw = random.randint(1,5)
##                cf = random.randint(0,len(colors)-1)
##                cl = random.randint(0,len(colors)-1)
##                Canvas.AddDot(x,y,D,LineWidth = lw,LineColor = colors[cl],FillColor = colors[cf])
          
            # Circles
        for i in range(5):
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            D = random.randint(1,5)
            lw = random.randint(1,5)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            Canvas.AddCircle(x,y,D,LineWidth = lw,LineColor = colors[cl],FillColor = colors[cf])
            Canvas.AddText("Circle # %i"%(i),x,y,Size = 12,BackgroundColor = None,Position = "cc")
          
            # Lines
        for i in range(5):
            points = []
            for j in range(random.randint(2,10)):
                point = (random.randint(Range[0],Range[1]),random.randint(Range[0],Range[1]))
                points.append(point)
            lw = random.randint(1,10)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            Canvas.AddLine(points, LineWidth = lw, LineColor = colors[cl])
          
            # Polygons
        for i in range(3):
            points = []
            for j in range(random.randint(2,6)):
                point = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
                points.append(point)
            lw = random.randint(1,6)
            cf = random.randint(0,len(colors)-1)
            cl = random.randint(0,len(colors)-1)
            Canvas.AddPolygon(points,
                                   LineWidth = lw,
                                   LineColor = colors[cl],
                                   FillColor = colors[cf],
                                   FillStyle = 'Solid')
                            
        ## Pointset
        for i in range(4):
            points = []
            points = RandomArray.uniform(Range[0],Range[1],(100,2))
            cf = random.randint(0,len(colors)-1)
            D = random.randint(1,4)
            Canvas.AddPointSet(points, Color = colors[cf], Diameter = D)
        
        # Text
        String = "Unscaled text"
        for i in range(3):
            ts = random.randint(10,40)
            cf = random.randint(0,len(colors)-1)
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            Canvas.AddText(String, x, y, Size = ts, Color = colors[cf], Position = "cc")

        # Scaled Text
        String = "Scaled text"
        for i in range(3):
            ts = random.random()*3 + 0.2
            cf = random.randint(0,len(colors)-1)
            x,y = (random.uniform(Range[0],Range[1]),random.uniform(Range[0],Range[1]))
            Canvas.AddScaledText(String, x, y, Size = ts, Color = colors[cf], Position = "cc")

        Canvas.ZoomToBB()


if __name__ == '__main__':
    app = model.Application(Doodle)
    app.MainLoop()
