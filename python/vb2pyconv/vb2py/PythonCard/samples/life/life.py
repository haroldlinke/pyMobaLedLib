#!/usr/bin/python

"""
__version__ = "$Revision: 1.49 $"
__date__ = "$Date: 2006/01/24 20:49:27 $"
"""

try:
    import psyco
    psyco.full()
except ImportError:
    pass

import os, sys
import shutil
import wx
import util as lifeutil
from PythonCard import clipboard, configuration, dialog, graphic, model, util

from patterns import Patterns
from lexicon import Lexicon


class Life(model.Background):

    def on_initialize(self, event):
        self.createConfigDir()
        self.filename = None

        self.grid = None
        self.toggleToLife = 1
        self.resizing = False
        # used to protect against
        # mouseClick after file dialog
        self.openingFileDialog = False
        scale = self.getScaleFromMenu()
        if scale:
            self.setCanvasAttributes(self.getScaleFromMenu())
        else:
            self.menuBar.setChecked('menuScale5')
            self.setCanvasAttributes(5)

        self.initSizers()

        self.lexiconWindow = model.childWindow(self, Lexicon)
        self.lexiconWindow.position = (650, 25)
        self.patternsWindow = model.childWindow(self, Patterns)
        self.patternsWindow.position = (650, 300)

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        comp = self.components
        flags = wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_BOTTOM
        sizer2.Add(comp.btnStart, 0, flags, 5)
        sizer2.Add(comp.btnStop, 0, flags, 5)
        sizer2.Add(comp.btnStep, 0, flags, 5)
        sizer1.Add(sizer2, 0, flags, 5)
        sizer1.Add(comp.bufOff, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.sizer = sizer1
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def createConfigDir(self):
        self.configPath = os.path.join(configuration.homedir, 'life')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        basePath = self.application.applicationDirectory
        self.lexiconPath = os.path.join(self.configPath, 'lexicon.txt')
        if not os.path.exists(self.lexiconPath) and os.path.exists(os.path.join(basePath, 'lexicon.txt')):
            shutil.copy2(os.path.join(basePath, 'lexicon.txt'), self.lexiconPath)
        else:
            # currently lexicon.txt is not part of the distribution
            # but it might be in the future
            pass
        self.patternsPath = os.path.join(self.configPath, 'patterns')
        if not os.path.exists(self.patternsPath):
            os.mkdir(self.patternsPath)
        basePath = os.path.join(basePath, 'patterns')
        for name in os.listdir(basePath):
            if name.lower().endswith('.lif') and not os.path.exists(os.path.join(self.patternsPath, name)):
                shutil.copy2(os.path.join(basePath, name), os.path.join(self.patternsPath, name))

    def initGrid(self):
        # a populated grid has (x, y) tuples for keys
        # with 1 (alive) or 0 (dead) for the value of each key
        self.grid = {}
        self.generation = 0

    def recenterCells(self, oldCenter):
        diffX = self.center[0] - oldCenter[0]
        diffY = self.center[1] - oldCenter[1]
        grid = {}
        #print "self.center", self.center, "oldCenter", oldCenter
        for cell in self.grid:
            grid[(cell[0] + diffX, cell[1] + diffY)] = self.grid[cell]
        self.grid = grid

    def setCanvasAttributes(self, scale):
        # whenever the window size or scale changes
        # this needs to be called
        canvas = self.components.bufOff

        color = 'blue'
        canvas.fillColor = color
        canvas.foregroundColor = color

        if self.grid is None or scale != self.scale or canvas.size != (self.width, self.height):
            self.scale = scale
            # have to resize the grid
            
            # setting self.spacing to 0 will mean
            # that the blocks have no space between them
            if self.scale < 3:
                self.spacing = 0
            else:
                self.spacing = 1

            if self.grid is not None:
                oldCenter = self.center
                oldSize = self.size

            self.width, self.height = canvas.size
            self.width = self.width / self.scale
            self.height = self.height / self.scale
            self.universeSize = (self.width, self.height)
            self.center = (self.width / 2, self.height / 2)

            if self.grid is None:
                self.initGrid()
            else:
                #self.initGrid()
                # attempt to preserve the existing pattern
                self.recenterCells(oldCenter)

        #print "self.universeSize:", self.universeSize, "self.center:", self.center, "self.scale:", self.scale
        #print "Universe Size: (%d, %d)  Scale: %d" % (self.universeSize[0], self.universeSize[1], self.scale)

    def doRunLife(self, steps=-1):
        while self.keepDrawing and steps != 0:
            grid = self.grid
            newgrid = {}
            for cell in grid:
                sum = 0
                #neighbors = lifeutil.neighborsTuple(cell[0], cell[1])
                # it is a bit faster to inline this rather than
                # calling a function
                col, row = cell
                prevRow = row - 1
                nextRow = row + 1
                prevCol = col - 1
                nextCol = col + 1
                neighbors = ((prevCol, prevRow), (col, prevRow), (nextCol, prevRow),
                            (prevCol, row), (nextCol, row),
                            (prevCol, nextRow), (col, nextRow), (nextCol, nextRow))

                # I tried a version where the dictionary kept a copy of the neighbors tuple
                # but the overhead in storing the data seemed to outweigh the cost
                # of calculating the neighbors and made this about 50% slower
                # also using get() with a default appears to be about 20-25% faster
                # than using a try/except block style access of sum += grid[neighbor]
                for neighbor in neighbors:
                    sum += grid.get(neighbor, 0)
                #print "cell", cell, grid[cell]
                #print neighbors
                #print sum
                if sum == 3 or (grid[cell] and sum == 2):
                    # cell will be alive next generation
                    newgrid[cell] = 1
                    for neighbor in neighbors:
                        newgrid.setdefault(neighbor, 0)

            self.generation += 1
            steps -= 1
            self.grid = newgrid
            self.displayGeneration()
            wx.SafeYield(self)

    def displayGeneration(self):
        canvas = self.components.bufOff
        width = self.scale - self.spacing
        canvas.autoRefresh = False
        canvas.clear()
        grid = self.grid

        # uncomment to see the size of the dictionary (hash)
        # a blinker (3 live cells in a row) will have a 15 total cells
        # in the dictionary for the 3 cells and the 12 surrounding neighbors
        #print "len(grid)", len(grid)

        population = 0
        # very small optimization
        # but it avoids an if statement for every iteration
        if width == 1:
            points = []
            for cell in grid:
                if grid[cell]:
                    population += 1
                    points.append(cell)
            canvas.drawPointList(points)
        else:
            rects = []
            scale = self.scale
            for cell in grid:
                if grid[cell]:
                    population += 1
                    rects.append((cell[0] * scale, cell[1] * scale, width, width))
                    #canvas.drawRectangle(cell[0] * scale, cell[1] * scale, width, width)
            canvas.drawRectangleList(rects)

        canvas.refresh(True)
        self.statusBar.text = "Generation: %d    Population: %d" % (self.generation, population)

    def cellAlive(self, position):
        col = position[0] / self.scale
        row = position[1] / self.scale
        return self.grid.get((col, row), 0)

    def setCell(self, col, row, alive):
        self.grid[(col, row)] = alive
        if alive:
            # make sure neighbors are in grid
            for neighbor in lifeutil.neighborsTuple(col, row):
                self.grid.setdefault(neighbor, 0)
        
    def toggleCell(self, position):
        x, y = position
        scale = self.scale
        cellWidth = scale - self.spacing
        row = y / scale
        col = x / scale
        
        alive = self.grid.get((col, row), 0)
        #print x, y, col, row, scale, alive

        if alive == self.toggleToLife:
            # no need to toggle
            return

        self.setCell(col, row, self.toggleToLife)

        y1 = row * scale
        x1 = col * scale
        canvas = self.components.bufOff
        
        if not self.toggleToLife:
            # need to erase a cell
            oldColor = canvas.foregroundColor
            canvas.foregroundColor = canvas.backgroundColor
            canvas.fillColor = canvas.backgroundColor
        
        if cellWidth == 1:
            canvas.drawPoint((x1, y1))
        else:
            canvas.drawRectangle((x1, y1), (cellWidth, cellWidth))

        if not self.toggleToLife:
            # need to restore the colors
            canvas.foregroundColor = oldColor
            canvas.fillColor = oldColor
    
    def on_bufOff_mouseDown(self, event):
        if self.openingFileDialog:
            return

        self.toggleToLife = not self.cellAlive(event.position)
        self.toggleCell(event.position)

    def on_bufOff_mouseDrag(self, event):
        if self.openingFileDialog:
            return

        self.toggleCell(event.position)
        
    def on_btnStart_mouseClick(self, event):
        self.components.btnStart.enabled = False
        self.components.btnStep.enabled = False
        self.keepDrawing = True
        startTime = util.time()

        self.doRunLife()
        
        print "Draw time: %f" % (util.time() - startTime)

    def on_btnStop_mouseClick(self, event):
        self.keepDrawing = False
        self.components.btnStart.enabled = True
        self.components.btnStep.enabled = True

    def on_btnStep_mouseClick(self, event):
        self.keepDrawing = True
        self.doRunLife(1)

    def initAndPlacePatterns(self, patterns, topLeft, size):
        width, height = size
        # at some point there might be an option to
        # not clear the current grid/universe
        # so that patterns can be placed, moved, and rotated
        # without disturbing existing patterns
        self.initGrid()
        centerX, centerY = self.center
        # if the pattern will fit within the current grid
        # it may still need to be shifted in order to be
        # centered correctly
        # this is my first attempt to shift the patterns
        # it isn't quite right so it is best to have at least a few
        # blank rows and columns of padding on each side if possible
        # until this algorithm is corrected
        left, top = topLeft
        if (left + width) > (width / 2):
            # need to shift the pattern left
            xDiff = (width / 2) + left
        elif (left + (width / 2)) < 0:
            xDiff = ((width / 2) + left)
        else:
            xDiff = 0
        if (top + height) > (height / 2):
            yDiff = (height / 2) + top
        elif (top + (height / 2)) < 0:
            yDiff = ((height / 2) + top)
        else:
            yDiff = 0
        #print "topLeft", topLeft, "xDiff, yDiff", xDiff, yDiff
        
        for pattern in patterns:
            x, y = pattern['position']
            column = centerX + x - xDiff
            row = centerY + y - yDiff
            self.grid = lifeutil.placePattern(self.grid, column, row, pattern['rows'])
        self.displayGeneration()

    def openFile(self):
        self.openingFileDialog = 1
        wildcard = "Life files (*.lif)|*.lif;*.LIF"
        directory = os.path.join(self.application.applicationDirectory, 'patterns')
        result = dialog.openFileDialog(None, "Import which file?", directory, '', wildcard)
        if result.accepted:
            path = result.paths[0]
            os.chdir(os.path.dirname(path))
            self.filename = path
            
            description, patterns, topLeft, size = lifeutil.readLifeFile(path)
            print description
            print "topLeft:", topLeft, "size", size
            self.initAndPlacePatterns(patterns, topLeft, size)

    def on_menuFileOpen_select(self, event):
        self.openFile()

    def on_menuFileSaveAs_select(self, event):
        if self.filename is None:
            path = ''
            filename = ''
        else:
            path, filename = os.path.split(self.filename)
        wildcard = "All files (*.*)|*.*"
        result = dialog.saveFileDialog(None, "Save As", path, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            fileType = graphic.bitmapType(path)
            print fileType, path
            try:
                bmp = self.components.bufOff.getBitmap()
                bmp.SaveFile(path, fileType)
                return True
            except IOError:
                return False
        else:
            return False

    def on_menuEditCopy_select(self, event):
        clipboard.setClipboard(self.components.bufOff.getBitmap())

    # assumes the clipboard contains a valid
    # text pattern like you would find in the lifep glossary.doc
    #
    # acorn
    # .*.....
    # ...*...
    # **..***
    def on_menuEditPaste_select(self, event):
        data = clipboard.getClipboard()
        if isinstance(data, str):
            description, patterns, topLeft, size = lifeutil.translateClipboardPattern(data)
            print description
            print "topLeft:", topLeft, "size", size
            self.initAndPlacePatterns(patterns, topLeft, size)

    def on_editClear_command(self, event):
        #self.components.bufOff.clear()
        self.initGrid()
        self.displayGeneration()

    def on_close(self, event):
        self.keepDrawing = False
        event.skip()

    # it would be nice to get the scales from the resource file
    # rather than hard coding them here
    # that should be possible by walking the resource or the Scale menu
    # looking for a prefix menu item name of 'menuScale'
    def getScaleFromMenu(self):
        for i in [1, 2, 3, 4, 5, 10]:
            if self.menuBar.getChecked('menuScale' + str(i)):
                return i

    def uncheckScaleMenuItems(self, scale):
        for i in [1, 2, 3, 4, 5, 10]:
            if i != scale:
                self.menuBar.setChecked('menuScale' + str(i), False)
        
    def on_setScale_command(self, event):
        scale = int(event.target.name[9:])
        self.uncheckScaleMenuItems(scale)
        self.setCanvasAttributes(scale)
        self.displayGeneration()

    def on_doAutomata_command(self, event):
        automata = event.target.name

        if automata == 'menuAutomataLife':
            result = dialog.textEntryDialog(self, 'Steps (-1 means continuous):', 'Number of steps', '-1')
            if result.accepted:
                steps = int(result.text)
                self.keepDrawing = True
                startTime = util.time()
                self.doRunLife(steps)
                print "Draw time: %f" % (util.time() - startTime)

    def on_idle(self, event):
        # have to handle resizing during idle
        # because the sizer hasn't done the work yet
        # of resizing self.components.bufOff
        #print "idle", self.resizing, self.GetSize(), self.components.bufOff.size
        if self.resizing:
            self.setCanvasAttributes(self.scale)
            self.displayGeneration()
            self.resizing = False
        self.openingFileDialog = False
            
    def on_size(self, event):
        # user resized the window
        self.resizing = True
        #print "on_size"
        #self.setCanvasAttributes(self.scale)
        event.skip()

    def on_menuAutomataLexicon_select(self, event):
        self.lexiconWindow.visible = True

    def on_menuAutomataPatternsList_select(self, event):
        self.patternsWindow.visible = True
        
    def on_menuAutomataDownloadLexiconAndPatterns_select(self, event):
        cwd = os.getcwd()
        os.chdir(self.application.applicationDirectory)
        self.statusBar.text = 'Downloading Lexicon...'
        lifeutil.getLexicon(self.configPath)
        self.lexiconWindow.populatePatternsList()
        self.statusBar.text = 'Downloading Patterns...'
        lifeutil.getPatterns(self.configPath)
        self.patternsWindow.populatePatternsList()
        os.chdir(cwd)
        self.statusBar.text = 'Done'
        
if __name__ == '__main__':
    app = model.Application(Life)
    app.MainLoop()
