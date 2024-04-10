#!/usr/bin/python

"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2006/01/14 14:27:33 $"

"""

import os, sys
import wx
from wx.html import HtmlEasyPrinting
from PythonCard import configuration, dialog, model, helpful
import copy

COLOR = { 'a': (255,200,200), 'f': (255,255,255), 'p': (255,255,255), 'u': (255,255,255), 'z': (255,0,0), 
          'i': (200,255,200), 'o': (200,200,255), }

VERSION = "0.2"

def textToHtml(txt):
    # the wxHTML classes don't require valid HTML
    # so this is enough
    html = txt.replace('\n\n', '<P>')
    html = html.replace('\n', '<BR>')
    return html

class square:
    def __init__(self, x,y, comp):
        self.x = x
        self.y = y
        self.comp = comp
        self.state = None
        self.values = [1,2,3,4,5,6,7,8,9]
        self.color = (255,255,255)

class undosquare:
    def __init__(self, val, state):
        self.state = state
        self.values = val    
        
class MyBackground(model.Background):
    
    def on_initialize(self, event):
        # if you have any initialization
        # including sizer setup, do it here
        self.readme = None
        self.hideUndecided = False
        self.hideChoices = False
        self.squares = {}
        for i in range(9):
            for j in range(9):
                self.squares[i,j] = square(i,j, self.components["B%d%d" % (i,j)])
        self.peer = {}
        for i in range(3):
            for j in range(3):
                self.peer[3*i+j] = []
                for x in range(3):
                    for y in range(3):
                        self.peer[3*i+j].append( (3*i+x, 3*j+y) )
        
        self.sizerLayout()
        self.startTitle = self.title
        self.newFile()
        self.components.solveIt.SetFocus()

    def sizerLayout(self):
        # Need this nonsense because we are using list components in an unusual way
        # We want them to be entirely visible - and Mac OSX doesn't record an adequate
        #  minimum size (GetBestSize()) for list controls
        if wx.Platform == '__WXMSW__':
            minListSize = (45,44)
        elif wx.Platform <> '__WXMAC__':
            minListSize = (66,66)
        else:
            minListSize = (66,66)
            
        for i in range(9):
            for j in range(9):
                self.components["B%d%d" % (i,j)].SetMinSize( minListSize )
            
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
##        There is no sizer 3 !!
        sizer4 = wx.GridSizer(9, 9, 2, 2)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        
        stcSizerAttrs = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL         
        fldSizerAttrs = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL
        vertFlags = wx.LEFT | wx.TOP | wx.ALIGN_LEFT
        chkSizerAttrs = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        
        C = self.components

        sizer2.Add(C.solveIt, flag=fldSizerAttrs)
        sizer2.Add((5, 5), 0)
        sizer2.Add(C.Singles, flag=fldSizerAttrs)
        sizer2.Add((5, 5), 0)
        sizer2.Add(C.Soles, flag=fldSizerAttrs)
        sizer2.Add((45, 5), 0)

        sizer2.Add(C.Blank, flag=fldSizerAttrs)
        sizer2.Add((25, 5), 0)
        sizer2.Add(C.Undo, flag=fldSizerAttrs)
        sizer2.Add((5, 5), 0)
        sizer2.Add(C.Redo, flag=fldSizerAttrs)
        
        for i in range(9):
            for j in range(9):
                sizer4.Add(C["B"+str(i)+str(j)]) 
        
        sizer5.Add(C.hideUndecided, flag=fldSizerAttrs)
        sizer5.Add((5, 5), 0)
        sizer5.Add(C.hideChoices, flag=fldSizerAttrs)
        
        sizer1.Add(sizer2, 0, vertFlags)
        sizer1.Add((5, 15), 0)  # spacer
        sizer1.Add(sizer4, 0, vertFlags)
        sizer1.Add((5, 15), 0)  # spacer
        sizer1.Add(sizer5, 0, vertFlags)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()
        
        self.visible = True
        
        
        
    def reset(self):
        for i in range(9):
            for j in range(9):
                self.squares[i,j].values = [1,2,3,4,5,6,7,8,9]
                self.squares[i,j].color = (255,255,255)
                self.squares[i,j].state = 'u'
        self.undo = []
        self.redo = []
        
        
    def loadConfig(self):
        pass

    def saveConfig(self):
        pass

    def saveChanges(self):
        # save configuration info in the app directory
        #filename = os.path.basename(self.documentPath)
        if self.documentPath is None:
            filename = "Untitled"
        else:
            filename = self.documentPath
        msg = "The text in the %s file has changed.\n\nDo you want to save the changes?" % filename
        result = dialog.messageDialog(self, msg, 'textEditor', wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL)
        return result.returnedString

    def doExit(self):
        return 1
        
    def on_close(self, event):
        if self.doExit():
            # self.saveConfig()
            self.fileHistory = None
            self.printer = None
            event.skip()

    def on_menuFileSave_select(self, event):
        if self.documentPath is None:
            # this a "new" document and needs to go through Save As...
            self.on_menuFileSaveAs_select(None)
        else:
            self.saveFile(self.documentPath)

    def on_menuFileSaveAs_select(self, event):
        wildcard = "Text files (*.txt)|*.TXT;*.txt|All files (*.*)|*.*"
        if self.documentPath is None:
            dir = ''
            filename = '*.txt'
        else:
            dir = os.path.dirname(self.documentPath)
            filename = os.path.basename(self.documentPath)
        result = dialog.saveFileDialog(None, "Save As", dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.saveFile(path)
            return True
        else:
            return False

    def newFile(self):
        self.documentPath = None
        self.documentChanged = 0
        self.title = 'Untitled - ' + self.startTitle
        self.statusBar.text = 'Untitled'
        self.reset()
        for i in range(9):
            for j in range(9):
                self.updateList(self.squares[i,j])

    def setUpPuzzle(self, definition):
        self.reset()
        y = 0
        for line in definition:
            if line.strip() == "": continue
            if y == 9: 
                # must be the optional title
                self.title = line
                self.statusBar.text = line
                break
            x = 0
            for c in line.strip():
                sqr = self.squares[x,y]
                if c == " ": continue
                if c == "x":
                    sqr.state = 'u'
                else:
                    sqr.state = 'p'
                    sqr.values = [int(c),]
                self.updateList(sqr)
                x += 1
            y += 1
  
    def on_builtInPuzzle_command(self, event):
        self.documentPath = None
        self.documentChanged = 0
        self.title = 'Untitled - ' + self.startTitle
        self.statusBar.text = 'Untitled'
        tname = event.target.name.replace("menuFilePuzzle", "P")
        self.setUpPuzzle(self.components[tname].userdata.split("\n"))
        
        
    def openFile(self, path):
        # change the code below for
        # opening an existing document
        # the commented lines are from the textEditor tool
        
        # may be overridden if file includesthe optinoal title on last line
        self.title = os.path.split(path)[-1] + ' - ' + self.startTitle   
        f = open(path)
        self.setUpPuzzle(f)
        f.close()
        self.documentPath = path
        self.documentChanged = 0
        self.statusBar.text = path

    def saveFile(self, path):
        # change the code below for
        # saving an existing document
        f = open(path, 'w')
        for y in range(9):
            s = []
            for x in range(9):
                tList = self.squares[x,y].values
                if len(tList) == 1:
                    s.append(str(tList[0]))
                else:
                    s.append('x')
                if x == 2 or x == 5: s.append(' ')
            s.append("\n")
            f.write(''.join(s))
            if y == 2 or y == 5: f.write("\n")
        f.close()
        self.documentPath = path
        self.documentChanged = False
        self.title = os.path.split(path)[-1] + ' - ' + self.startTitle
        self.statusBar.text = path

    def on_menuFileNew_select(self, event):
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                pass
            elif save == "No":
                # any changes will be lost
                self.newFile()
            else:
                if self.documentPath is None:
                    if self.on_menuFileSaveAs_select(None):
                        self.newFile()
                else:
                    self.saveFile(self.documentPath)
                    self.newFile()
        else:
            # don't need to save
            self.newFile()

    def on_menuFileOpen_select(self, event):
        # split this method into several pieces to make it more flexible
        wildcard = "Text files (*.txt)|*.txt;*.TXT|All files (*.*)|*.*"
        result = dialog.openFileDialog(wildcard=wildcard)
        if result.accepted:
            path = result.paths[0]
            # an error will probably occur here if the text is too large
            # to fit in the wxTextCtrl (TextArea) or the file is actually
            # binary. Not sure what happens with CR/LF versus CR versus LF
            # line endings either
            self.openFile(path)

        
    def on_menuFilePrint_select(self, event):
        # put your code here for print
        # the commented code below is from the textEditor tool
        # and is simply an example
        
        #source = textToHtml(self.components.fldDocument.text)
        #self.printer.PrintText(source)
        pass

    def on_menuFilePrintPreview_select(self, event):
        # put your code here for print preview
        # the commented code below is from the textEditor tool
        # and is simply an example
        
        #source = textToHtml(self.components.fldDocument.text)
        #self.printer.PreviewText(source)
        pass

    def on_menuFilePageSetup_select(self, event):
        self.printer.PageSetup()

    def saveUndoPosition(self):
        st = {}
        for i in range(9):
            for j in range(9):
                sqr = self.squares[i,j]
                st[i,j] = undosquare(copy.copy(sqr.values), sqr.state)
        self.undo.append(st)
        self.redo = []
    
    def on_Blank_mouseClick(self, event):
        self.on_menuFileNew_select(event)
        
    def on_Undo_command(self, event):
        # if we are at the end - i.e. no redo info yet, then we should take a snapshot
        #  right now so that we can get back to this point
        if len(self.redo) == 0:
            self.saveUndoPosition()
            st = self.undo[-1]
            self.redo.append(st)
            del self.undo[-1]
            
##        print "undo", len(self.undo), len(self.redo)
        if len(self.undo) == 0:
            result = dialog.alertDialog(self, 'No more to Undo', 'Undo Alert')
            return
        st = self.undo[-1]
##        for k,v in self.undo[-1].iteritems():
##            print k, v.state, v.values
        for i in range(9):
            for j in range(9):
                sqr = self.squares[i,j]
                sqr.values = copy.copy(st[i,j].values)
                sqr.state = st[i,j].state
                self.updateList(sqr)
                
        self.redo.append(st)
        del self.undo[-1]
        t = self.count()
        self.statusBar.text = "Possible choices left %d" % t
##        print "undo", len(self.undo), len(self.redo)
        

    def on_Redo_command(self, event):
##        print "redo", len(self.undo), len(self.redo)
        if len(self.redo) == 0:
            result = dialog.alertDialog(self, 'No more to Redo', 'Redo Alert')
            return
        st = self.redo[-1]
        for i in range(9):
            for j in range(9):
                sqr = self.squares[i,j]
                sqr.values = copy.copy(st[i,j].values)
                sqr.state = st[i,j].state
                self.updateList(sqr)
                
        self.undo.append(st)
        del self.redo[-1]
        t = self.count()
        self.statusBar.text = "Possible choices left %d" % t
##        print "redo", len(self.undo), len(self.redo)
        

    def on_hideUndecided_mouseClick(self, event):
        self.hideUndecided = self.components.hideUndecided.checked
        for i in range(9):
            for j in range(9):
                self.updateList(self.squares[i,j])
        
    def on_hideChoices_mouseClick(self, event):
        self.hideChoices = self.components.hideChoices.checked
        
    def on_doHelpAbout_command(self, event):
        dialog.messageDialog(self,
                     "Sudoku Solver" + "\n\n" + \
                     "Version %s" % VERSION  + "\n\n" + \
                     "(c) 2005   Alex Tweedly",
                     "About Sudoku Solver",
                     wx.ICON_INFORMATION | wx.OK)
        pass

    def on_doHelpHelp_command(self, event):
        if not self.readme:
            self.readme = open('readme.txt').read()
        dialog.scrolledMessageDialog(self, self.readme, 'Help')
        pass

    def singles(self):
        self.saveUndoPosition()
        for i in range(9):
            for j in range(9):
                sqr = self.squares[i,j]
                if len(sqr.values) == 1 and (sqr.state == 'p' or sqr.state == 'a' or sqr.state == 'f'):
                    sqr.state = 'i'
                    self.fillin(sqr, i,j)

    def soles(self):
        self.saveUndoPosition()
        for i in range(9):
            # check the col
            used = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
            last = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
            for j in range(9):
                sqr = self.squares[i,j]
                for c in sqr.values:
                    used[c] += 1
                    last[c] = j
            for c,val in used.iteritems():
                if val == 1:
                    ss = self.squares[i, last[c]]
                    if len(ss.values) <> 1: 
                        ss.values = [c,]
                        ss.state = 'o'
                        #rint "col", i, last[c], c
                        self.fillin(ss,i,last[c])
            # check the row
            used = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
            last = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
            for j in range(9):
                sqr = self.squares[j,i]
                for c in sqr.values:
                    used[c] += 1
                    last[c] = j
            for c,val in used.iteritems():
                if val == 1:
                    ss = self.squares[last[c], i]
                    if len(ss.values) <> 1: 
                        ss.values = [c,]
                        ss.state = 'o'
                        #rint "row", last[c], i, c
                        self.fillin(ss,last[c],i)
            # check the square
            used = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
            last = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
            for j in range(9):
                sqr = self.squares[self.peer[i][j]]
                #rint i,j,self.peer[i][j]
                for c in sqr.values:
                    used[c] += 1
                    last[c] = self.peer[i][j]
            for c,val in used.iteritems():
                if val == 1:
                    x,y = last[c]
                    ss = self.squares[x,y]
                    #rint i,c,val,ss.values
                    if len(ss.values) <> 1: 
                        ss.values = [c,]
                        ss.state = 'o'
                        #rint "3x3", x, y, c
                        self.fillin(ss,x,y)

                    
    def fillin(self, sqr, i, j):
        if len(sqr.values) <> 1:
            print "help - bad values list", i,j, ss
            
        value = sqr.values[0]
        for d in range(9):
            if d == j: continue
            ss = self.squares[i,d]
            if value in ss.values:
                self.delValue(ss, value)
                ss.state = 'f'
                self.updateList(ss)
                #if len(ss.values) == 1:  self.fillin(ss,i,d)

        for d in range(9):
            if d == i: continue
            ss = self.squares[d,j]
            if value in ss.values:
                self.delValue(ss, value)
                #if len(ss.values) == 1:  self.fillin(ss,d,j)

        for d,e in self.peer[3*(i/3) + j/3]:
            if d == i and e == j: continue
            ss = self.squares[d,e]
            if value in ss.values:
                self.delValue(ss, value)
                ss.state = 'f'
                #if len(ss.values) == 1:  self.fillin(ss,d,e)
        self.updateList(sqr)
        t = self.count()
        self.statusBar.text = "Possible choices left %d" % t

    def count(self):
        t = 1
        for i in range(9):
            for j in range(9):
                t *= len(self.squares[i,j].values)
                if t == 0:
                    return 0
        return t

    def on_Singles_mouseClick(self, event):
        self.singles()
        
    def on_Soles_mouseClick(self, event):
        self.soles()
        
    def on_solveIt_mouseClick(self, event):
        last = -1
        t = self.count()            
        while last <> t and t > 1:
            last = t
            self.singles()
            t = self.count()
            if t == last: 
                self.soles()
                t = self.count()

                

    def updateList(self, sqr):
        if len(sqr.values) == 0:
            items = ["   ", "   ", "   "]
            sqr.state = 'z'
        elif len(sqr.values) == 1:
            items = ["   ", " "+str(sqr.values[0])+" ", "   "]
        else:
            s = []
            for c in xrange(1,10):
                if c in sqr.values:
                    s.append(str(c))
                else:
                    s.append(" ")
            all = " ".join(s)
            items = [all[:5], all[6:11], all[12:]]
        if self.hideUndecided and (sqr.state == 'u' or sqr.state == 'f'): items = ['   ', '   ', '   ']
        sqr.comp.items = items
        sqr.comp.backgroundColor = COLOR[sqr.state]
        
                    
        
    def delValue(self, sqr, value):
        if value in sqr.values:
            del sqr.values[sqr.values.index(value)]            
            self.updateList(sqr)
            
        
    def on_popup_command(self, event):
        comp = event.target

        selected = 0
        x = int(comp.name[1])
        y = int(comp.name[2])
        sqr = self.squares[x,y]
        
        if len(sqr.values) == 1:
            if self.hideChoices and (sqr.state == 'u' or sqr.state == 'f'):
                items = ['1','2','3','4','5','6','7','8','9']
            else:
                selected = sqr.values[0]
        else:
            # make a menu
            self.menu = wx.Menu()
            # add the items
            items = []
            if self.hideChoices:
                items = ['1','2','3','4','5','6','7','8','9']
            else:
                for c in sqr.values:
                    items.append(str(c))

        if selected == 0:
            # Popup the menu.
            selected = helpful.popUpMenu(self, items, comp.position)
            if selected: 
                selected = int(selected)
            else:
                selected = 0

        if selected > 0:
            self.saveUndoPosition()
            sqr.values = [selected,]
            sqr.state = 'a'
            self.updateList(sqr)
            comp.backgroundColor = (200,100,100)
            self.fillin(sqr, int(comp.name[1]), int(comp.name[2]))

                
if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
