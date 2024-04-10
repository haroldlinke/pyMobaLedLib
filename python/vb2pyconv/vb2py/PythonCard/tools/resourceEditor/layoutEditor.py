#!/usr/bin/python

"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2006/01/13 07:28:59 $"
"""

# TODO: Start using exceptions!

import os, sys, string, copy
import pprint
import webbrowser

import wx

import time

from PythonCard import about, clipboard, configuration, dialog, graphic, log
from PythonCard import menu, model, registry, resource, util
from PythonCard.templates.dialogs import runOptionsDialog

from modules import backgroundInfoDialog
from modules import stackInfoDialog
from modules import menuDialog
from modules import newComponentDialog
from modules import stringDialog
from modules import dialogInfoDialog
from modules.multipropertyEditor import PropertyEditor
from modules import multiresourceOutput

SIZING_HANDLE_SIZE = 7
NUM_SIZING_HANDLES = 8
RESOURCE_TEMPLATE = 'template.rsrc.py'
RESOURCE_DIALOG_TEMPLATE = 'dialogTemplate.rsrc.py'
USERCONFIG = 'user.config.txt'

# KEA doc handling adapted from python_docs 
# method in IDLE EditorWindow.py

pythoncard_url = util.documentationURL("documentation.html")
resourceeditor_url = util.documentationURL("resource_editor_overview.html")

def prefixSizingHandle(N):
    return ("_sh_%02d_" % N)
    
def cursor(name):
    return name[7:]

class DummyDialog(model.CustomDialog):
    def __init__(self, aBg, path):
        # load the resource
        aDialogRsrc = resource.ResourceFile(path).getResource()
        model.CustomDialog.__init__(self, aBg, aDialogRsrc)

    def on_mouseClick(self, event):
        event.skip()


class ResourceEditor(model.Background):
    
    def on_initialize(self, event):
        self.filename = None
        self.documentChanged = False
        self.cmdLineArgs = {'debugmenu':False, 'logging':False, 'messagewatcher':False,
                            'namespaceviewer':False, 'propertyeditor':False,
                            'shell':False, 'otherargs':''}

        self.lastCaptured = None
        self.startName = None
        self.lastSelection = None
        self.marquee = False
        self.startPosition = (0, 0)
        self.startSize = (0, 0)
        self.offset = (0, 0)
        self.offsets = None
        self.startToolTip = ''

        try:
            self.readme = open('multireadme.txt').read()
        except:
            self.readme = ''

        # KEA 2002-06-27
        # copied from codeEditor.py
        # wxFileHistory isn't wrapped, so use raw wxPython
        # also the file list gets appended to the File menu
        # rather than going in front of the Exit menu
        # I suspect I have to add the Exit menu after the file history
        # which means changing how the menus in resources are loaded
        # so I'll do that later
        self.fileHistory = wx.FileHistory()
        fileMenu = self.GetMenuBar().GetMenu(0)
        self.fileHistory.UseMenu(fileMenu)
        wx.EVT_MENU_RANGE(self, wx.ID_FILE1, wx.ID_FILE9, self.OnFileHistory)

        self.buildComponentsMenu()

        self.cursors = {}
        self.cursors['topRight'] = wx.StockCursor(wx.CURSOR_SIZENESW)
        self.cursors['bottomLeft'] = self.cursors['topRight']
        self.cursors['topMiddle'] = wx.StockCursor(wx.CURSOR_SIZENS)
        self.cursors['bottomMiddle'] = self.cursors['topMiddle']
        self.cursors['topLeft'] = wx.StockCursor(wx.CURSOR_SIZENWSE)
        self.cursors['bottomRight'] = self.cursors['topLeft']
        self.cursors['middleLeft'] = wx.StockCursor(wx.CURSOR_SIZEWE)
        self.cursors['middleRight'] = self.cursors['middleLeft']
        self.cursors['general'] = wx.StockCursor(wx.CURSOR_SIZING)
        self.cursors['null'] = wx.NullCursor
 
        self.sizingHandleNames = ['topLeft', 'topMiddle', 'topRight',
                         'middleLeft', 'middleRight',
                         'bottomLeft', 'bottomMiddle', 'bottomRight']

        if wx.Platform == '__WXMSW__':
            path = os.path.join(self.application.applicationDirectory, 'images', 'sizingHandle.bmp')
            self.sizingHandleTemplate = {'type':'ImageButton',
                                    'name':'topLeft',
                                    'position':(3, 3),
                                    'size':(SIZING_HANDLE_SIZE, SIZING_HANDLE_SIZE),
                                    'file':path,
                                    'border':'none',
                                    'visible':0}
        elif wx.Platform == '__WXMAC__':
            #self.resizingHandleColor = (0,0,128)
            path = os.path.join(self.application.applicationDirectory, 'images', 'sizingHandle.bmp')
            self.sizingHandleTemplate = {'type':'Image',
                                    'name':'topLeft',
                                    'position':(3, 3),
                                    'size':(SIZING_HANDLE_SIZE, SIZING_HANDLE_SIZE),
                                    'file':path,
                                    #'backgroundColor':self.resizingHandleColor,
                                    'border':'none',
                                    'visible':0}
        else:
            self.resizingHandleColor = (0,0,128)
            self.sizingHandleTemplate = {'type':'ImageButton',
                                    'name':'topLeft',
                                    'position':(3, 3),
                                    'size':(SIZING_HANDLE_SIZE, SIZING_HANDLE_SIZE),
                                    'file':'',
                                    'backgroundColor':self.resizingHandleColor,
                                    'visible':0}
            
        
        for sizingHandle in self.sizingHandleNames:
            self.sizingHandleTemplate['name'] = sizingHandle
            self.components[sizingHandle] = self.sizingHandleTemplate

        self.multipleSelected = False
        self.multipleComponents = []

        self.propertyEditorWindow = model.childWindow(self, PropertyEditor)

        self.xGridSize = 5
        self.yGridSize = 5
        self.alignToGrid = self.menuBar.getChecked('menuOptionsAlignToGrid')
        self.showGridLines = self.menuBar.getChecked('menuOptionsShowGridLines')

        path = os.path.join(self.application.applicationDirectory, 'templates', \
                            RESOURCE_TEMPLATE)
        self.rsrc = resource.ResourceFile(path).getResource()
        
        self.updatePanel(self.rsrc)
        # KEA 2004-05-14
        # this actually should only occur once for the panel
        # so I'm moving it into initialize which should work as long as
        # the panel isn't destroyed while editing, opening new files, etc.
        # KEA link up events for new dragging code
        wx.EVT_LEFT_DOWN(self.panel, self.on_mouseDown)
        wx.EVT_LEFT_UP(self.panel, self.on_mouseUp)
        wx.EVT_MOTION(self.panel, self.on_mouseDrag)
        wx.EVT_LEAVE_WINDOW(self.panel, self.on_mouseLeaveWindow)
        wx.EVT_ENTER_WINDOW(self.panel, self.on_mouseEnterWindow)
        wx.EVT_CHAR(self.panel, self.on_keyPress)
        
        self.configPath = os.path.join(configuration.homedir, 'resourceeditor')
        self.loadConfig()

        """
        # KEA 2002-03-03
        # this doesn't appear to work, some additional accelerator table modification
        # must be messing up the bindings
        # setup acceleratortable for background
        acctbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('C'), self.menuBar.getMenuId('menuEditCopy')),
            (wx.ACCEL_CTRL, ord('X'), self.menuBar.getMenuId('menuEditCut')),
            (wx.ACCEL_CTRL, ord('V'), self.menuBar.getMenuId('menuEditPaste'))
        ])
        self.SetAcceleratorTable(acctbl)
        """

        # KEA 2001-12-24
        # once we can do dynamic menus we should load the component list dynamically
        # to build the first part of the Component menu
        # Add BitmapCanvas
        # Add Button
        # ...
        # perhaps there should be a framework function to return the list of files in
        # the components directory or list of components and then a method in the
        # resourceEditor can load each component module as it builds the menu
        
        # MRV 2002-08-08
        # copied and changed from codeEditor to allow commandline argument for resource file
        # then can use from windows explorer rightclick...
        if len(sys.argv) > 1:
            # accept a file argument on the command-line
            filename = os.path.abspath(sys.argv[1])
            log.info('resourceEditor filename: ' + filename)
            if not os.path.exists(filename):
                filename = os.path.abspath(os.path.join(self.application.startingDirectory, sys.argv[1]))
            if os.path.isfile(filename):
                if filename.endswith('rsrc.py'):
                    self.filename = filename
                    self.openFile(filename)

        self.resizingHandler = {
            'topLeft':self.on_topLeft_mouseDrag,
            'topMiddle':self.on_topMiddle_mouseDrag,
            'topRight':self.on_topRight_mouseDrag,
            'middleLeft':self.on_middleLeft_mouseDrag,
            'middleRight':self.on_middleRight_mouseDrag,
            'bottomLeft':self.on_bottomLeft_mouseDrag,
            'bottomMiddle':self.on_bottomMiddle_mouseDrag,
            'bottomRight':self.on_bottomRight_mouseDrag
        }
        
        self.createDC()


    def isSizingHandle(self, name):
        return (name[:4] == "_sh_")
        
    def prefixIndexForComp(self, name):
        for i in range(len(self.multipleComponents)):
            if self.multipleComponents[i][0] == name:
                return i
        return -1

    def makeNewHandles(self, name):
        #print "make new", name
        for N in range(100):
            pre = prefixSizingHandle(N)
            #print name, N, pre
            if pre+"topLeft" in self.components:
                if self.components[pre+"topLeft"].visible:
                    continue
            else:
                for sizingHandle in self.sizingHandleNames:
                    fullname = pre + sizingHandle
                    #print fullname
                    if fullname in self.components.keys():
                        print "bad logic in makeNew", fullname
                        return
                    self.sizingHandleTemplate['name'] = fullname
                    self.components[fullname] = self.sizingHandleTemplate
            for sizingHandle in self.sizingHandleNames:
                fullname = pre + sizingHandle
                self.components[fullname].visible = True
            #print name, N
            self.positionSizingHandles(self.components[name].position, self.components[name].size, pre)
            return pre
        return None

    def OnFileHistory(self, event):
        fileNum = event.GetId() - wx.ID_FILE1
        path = self.fileHistory.GetHistoryFile(fileNum)
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                return
            elif save == "No":
                # any changes will be lost
                pass
            else:
                if self.filename is None:
                    # if the user cancels out of the Save As then go back to editing
                    if not self.on_menuFileSaveAs_select(None):
                        return
                else:
                    self.saveFile()
        self.openFile(path)

    # KEA 2004-05-12
    # transition to dynamic component menu
    # and component addition
    
    def buildComponentsMenu(self):
        """
        Dynamically build the menu for the components supported by the
        resourceEditor. Eventually this will be a list or some form of palette
        instead of a menu.
        """

        # only built-in components are handled currently, so an appcomponents
        # directory or fully-qualified component paths are handled
        # theoretically when the user loads a resource file the menu should
        # be updated, but this is all highly dependent on how imports are
        # handled, registry updated, etc.
        # One idea would be for the resourceEditor to register itself as
        # a change listener and have the registry subclass Changeable so it could
        # notify the resourceEditor. In that case, the algorithm below would
        # have to be modified since each menu item would be added as it receives
        # a change notice from the registry and would need to check the existing
        # menu to prevent duplicates as well as insert into the menu in the correct
        # order. Or perhaps, the menu items could be wiped out and recreated which 
        # is probably simpler.

        # get a list of all the modules in components
        moduleNames = registry.Registry.getInstance().findBuiltInComponents()
        # KEA 2004-05-12
        # I know that IEHtmlWindow is platform specific and has problems
        # in the resourceEditor and Grid doesn't work right either so I'm
        # conditionally preventing them from being loaded here until I figure
        # out how to deal with them
        # Container is another one that isn't applicable yet
        if True:
            try:
                moduleNames.remove('iehtmlwindow')
            except ValueError:
                pass
        if True:
            try:
                moduleNames.remove('grid')
            except ValueError:
                pass
        if True:
            try:
                moduleNames.remove('container')
            except ValueError:
                pass
                
        # need to force an import of all of the modules in components
        for name in moduleNames:
            resource.loadComponentModule(name)

        # should match based on name instead
        # name to object or id like menubar helpers?
        m = self.menuBar.menus[2]
        
        names = registry.Registry.getInstance().components.keys()
        names.sort()
        for key in names:
            rsrc = resource.Resource({'type':'MenuItem',
                'name': 'menuComponentAdd' + key, 
                'label': key,
                'command':'componentAdd'})
            mi = menu.MenuItem(self, m, rsrc)
            m.appendMenuItem(mi)

    def clearWidgets(self):
        for w in self.components.keys():
            if w not in self.sizingHandleNames:
                del self.components[w]

    def switchToMultipleMode(self, name = None):
        if self.propertyEditorWindow.components.wComponentList.stringSelection:
            self.lastSelection = self.propertyEditorWindow.components.wComponentList.stringSelection
        if self.startName:
            # 'second' component - exactly one currently selected
            #print 'second               ', self.startName
            self.multipleComponents.append( (self.startName, self.makeNewHandles(self.startName)))
            self.startName = None
        self.hideSizingHandles()
        if name:
            self.multipleComponents.append( (name, self.makeNewHandles(name)))
        self.propertyEditorWindow.statusBar.text = "Multiple Components"
        self.multipleSelected = True
            
        
        
    def positionSizingHandles(self, position, size, prefix = ""):
        x, y = position
        width, height = size
        halfHandleSize = SIZING_HANDLE_SIZE / 2
        log.debug('positionSizingHandles prefix:' + prefix + ', position:' + str(position) + ", size:" + str(size))
        
        self.components[prefix +'topLeft'].position = (x - SIZING_HANDLE_SIZE, y - SIZING_HANDLE_SIZE)
        self.components[prefix +'topMiddle'].position = (x + (width / 2) - halfHandleSize, y - SIZING_HANDLE_SIZE)
        self.components[prefix +'topRight'].position = (x + width, y - SIZING_HANDLE_SIZE)

        self.components[prefix +'middleLeft'].position = (x - SIZING_HANDLE_SIZE, y + (height / 2) - halfHandleSize)
        self.components[prefix +'middleRight'].position = (x + width, y + (height / 2) - halfHandleSize)

        self.components[prefix +'bottomLeft'].position = (x - SIZING_HANDLE_SIZE, y + height)
        self.components[prefix +'bottomMiddle'].position = (x + (width / 2) - halfHandleSize, y + height)
        self.components[prefix +'bottomRight'].position = (x + width, y + height)

    def showSizingHandles(self, name):
        self.startName = name
        self.positionSizingHandles(self.components[name].position, self.components[name].size)
        for sizingHandle in self.sizingHandleNames:
            self.components[sizingHandle].visible = True
            if wx.Platform == '__WXMAC__':
                pass
                #self.components[sizingHandle].backgroundColor = self.resizingHandleColor
            elif wx.Platform == '__WXGTK__':
                self.components[sizingHandle].backgroundColor = self.resizingHandleColor
        # overly conservative, but effective
        self.documentChanged = True

    def hideSizingHandles(self):
        if self.components.topLeft.visible:
            for sizingHandle in self.sizingHandleNames:
                self.components[sizingHandle].visible = False
            if wx.Platform == '__WXMAC__':
                self.panel.Refresh()

    def showMultiSizingHandles(self):
        if not self.multipleSelected:
            print "multi without multiple selected"
            return
        self.propertyEditorWindow.statusBar.text = "Multiple Components"
        for name, prefix in self.multipleComponents:
            self.positionSizingHandles(self.components[name].position, self.components[name].size, prefix)
            for sizingHandle in self.sizingHandleNames:
                self.components[prefix+sizingHandle].visible = True
                if wx.Platform == '__WXMAC__':
                    pass
                    #self.components[sizingHandle].backgroundColor = self.resizingHandleColor
                elif wx.Platform == '__WXGTK__':
                    self.components[prefix+sizingHandle].backgroundColor = self.resizingHandleColor
        # overly conservative, but effective
        self.documentChanged = True

    def hideMultiSizingHandles(self):
        if not self.multipleSelected:
            return
        changes = 0 
        for name, prefix in self.multipleComponents:
            if self.components[prefix+"topLeft"].visible:
                changes += 1
                for sizingHandle in self.sizingHandleNames:
                    self.components[prefix+sizingHandle].visible = False
        if wx.Platform == '__WXMAC__' and changes > 0:
            self.panel.Refresh()


## AGT 04-2005 This is no longer called !
##    def gtkHideSizingHandles(self, name):
##        for sizingHandle in self.sizingHandleNames:
##            if sizingHandle == name:
##                self.components[sizingHandle].backgroundColor = self.backgroundColor
##            else:
##                self.components[sizingHandle].visible = False
##                

    def setToolTip(self, target):
        if self.multipleComponents:
            self.propertyEditorWindow.statusBar.text = "Multiple Components"
        else:
            self.propertyEditorWindow.statusBar.text = "Component: %s  Pos: %s  Size: %s" % (str(target.name), 
                str(target.position),
                str(target.size))
        """
        x, y = target.position
        width, height = target.size
        tip = "name: " + target.name + "  \n" + \
              "position: " + str(x) + ", " + str(y) + "  \n" + \
              "size: " + str(width) + ", " + str(height)
        if tip != target.toolTip:
            target.toolTip = tip
        """

    def setToolTipDrag(self, name, position, size):
        if self.multipleComponents:
            self.propertyEditorWindow.statusBar.text = "Multiple Components"
        else:
            self.propertyEditorWindow.statusBar.text = "Component: %s  Pos: %s  Size: %s" % (name, 
                str(position),
                str(size))

    def on_mouseEnter(self, event):
        if self.marquee: return
        name = event.target.name
        if name in self.sizingHandleNames:
            try:
                self.SetCursor(self.cursors[name])
            except:
                # not all platforms have all cursors, but hopefully
                # the general sizing cursor is always available
                self.SetCursor(self.cursors['general'])
        else:
            # KEA 2003-05-05
            # get rid of cursor change on wxTextCtrl
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            self.setToolTip(event.target)

    def on_mouseLeave(self, event):
        if event.target.name in self.sizingHandleNames:
            self.SetCursor(self.cursors['null'])

    def pointInControl(self, position):
        #print 'pointInControl:'
        #position = self.panel.ClientToScreen( position )
        #print '    position=', position
        globalPosition = self.panel.ScreenToClient(wx.GetMousePosition())
        #print '    globalPosition=', globalPosition
        result = None
        for name in self.components.order:
            if name in self.sizingHandleNames:
                continue
            if self.isSizingHandle(name):
                continue
            control = self.components[name]
            r = control.GetRect()
            #print '    ', control, r
            if (r.Inside(globalPosition)):
                #print '    ', control
                result = control
                break
        #print "pointInControl", result
        return result

    def controlInRect(self, point, size):
        #print 'controlInRect:'
        
        #print '    p1, p2=', point, size
        result = []
        if size[0] < 0:
            bx = point[0]+size[0]
            tx = point[0]
        else:
            bx = point[0]
            tx = point[0]+size[0]
        if size[1] < 0:
            by = point[1]+size[1]
            ty = point[1]
        else:
            by = point[1]
            ty = point[1]+size[1]
            
        for name in self.components.order:
            if name in self.sizingHandleNames:
                continue
            if self.isSizingHandle(name):
                continue
            control = self.components[name]
            r = control.GetRect()
            #print bx, by, tx, ty, " :: ", control.name, r
            if bx <= r[0] and bx <= r[0]+r[2] and tx >= r[0] and tx >= r[0]+r[2]:
                if by <= r[1] and by <= r[1]+r[3] and ty >= r[1] and ty >= r[1]+r[3]:
                    #print '    ', control, r
                    result.append(control.name)
        return result


    # KEA 2004-03-27
    # the DC and lastPosition handling are basically a bunch
    # of hacks for event bugs in WXMAC and I'm sure I'm going to regret them
    def createDC(self):
        dc = wx.ClientDC(self.panel)
        dc.SetPen(wx.Pen('black', 1, wx.DOT))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetLogicalFunction(wx.INVERT)
        self.dc = dc

    def on_size(self, event):
        self.createDC()
        event.skip()

    def drawTheRect(self):
        position = [self.startGlobalPosition[0], self.startGlobalPosition[1]]
        position[0] = position[0] - self.startGlobalOffset[0]
        position[1] = position[1] - self.startGlobalOffset[1]

        self.dc.DrawRectanglePointSize((position[0], position[1]), (self.startSize[0], self.startSize[1]))
        self.lastPosition = position

    def on_mouseDoubleClick(self, event):
        # AGT 2005-05-12 Should be unnecessary - but seems to prevent the problem where a double-click
        #  was causing subsequent GetEventObjects to "stick" on the button
        ##print "dc",  event.GetEventObject().GetName()
        pass


    def on_mouseDown(self, event):
        # KEA 2003-03-23
        # protect against panel events
        #print "on_mouseDown"

        globalPosition = wx.GetMousePosition()
        cmdKey = event.CmdDown()

        control = event.GetEventObject()

        # mouseDown and already in marquee mode ?
        # can only be because of leaving the window issues !?
        if self.marquee:    
            # erase the last rect
            self.dc.DrawRectanglePointSize((self.marqueeBase[0], self.marqueeBase[1]), 
                (self.marqueeSize[0], self.marqueeSize[1]))
            self.marquee = False
            # overly conservative, but effective
            self.documentChanged = True

        
        # startGlobalPosition is the x,y where the initiating mouse event happened
        self.startGlobalPosition = self.panel.ScreenToClient(globalPosition)

        if control is self.panel:
            control = self.pointInControl(event.GetPosition())
            if control is None:
                self.resizingHandleTarget = None
                self.marquee = True
                self.marqueeBase = self.startGlobalPosition
                self.marqueeSize = (0,0)
                return
        else:
            #print control.name, cmdKey
            clientPosition = self.panel.ScreenToClient(wx.GetMousePosition())
            # AGT 04-2005
            # protect against bad events - claim to be from a button
            # even though not inside it  (after double-click button)
            #  Seems to be prevented by having an empty on_mouseDoubleClick()
            r = control.GetRect()
            if (not r.Inside(clientPosition)):
                self.panel.SetFocus()
                junk = dialog.alertDialog(self, "You double-clicked - please don't", 'a title')
                return

        target = control
        if self.isSizingHandle(target.name):
            # click on a multi-sizing handle
            self.resizingHandleTarget = None
            return

        if target.name in self.sizingHandleNames:
            if not self.startName:
                return
    
            #print "res4 sizing handles", self.startName
            self.resizingHandleTarget = target.name
            self.hideSizingHandles()

            self.startPosition = self.components[self.startName].position
            self.startSize = self.components[self.startName].size
            self.offset = target.ScreenToClient(globalPosition)
            return
            
        # so we must have selected one of the user's components
        if cmdKey:
            if self.startName == target.name: return
            #print "ctl-select", target.name, self.multipleComponents
            if self.multipleSelected:
                index = self.prefixIndexForComp(target.name)
                if index <> -1:
                    prefix = self.multipleComponents[index][1]
                    for sizingHandle in self.sizingHandleNames:
                        del self.components[prefix+sizingHandle]
                    del self.multipleComponents[index]
                    self.propertyEditorWindow.updateComponentList()
                    return
                # need to add it
                self.multipleComponents.append( (target.name, self.makeNewHandles(target.name) ) )
            else:
                self.switchToMultipleMode(target.name)
            self.propertyEditorWindow.updateComponentList()
        else:
            # plain mouse down
            if self.multipleSelected and self.prefixIndexForComp(target.name) <> -1:
                minx = None
                for c,pre in self.multipleComponents:
                    px,py = self.components[c].position
                    sx,sy = self.components[c].size
                    if not minx:
                        minx, miny = (px,py)
                        maxx, maxy = (px+sx, py+sy)
                    else:
                        minx = min(minx, px)
                        miny = min(miny, py)
                        maxx = max(maxx, px+sx)
                        maxy = max(maxy, py+sy)
                    
                self.startPosition = (minx, miny)
                self.startSize = (maxx-minx, maxy-miny)
                self.startGlobalPosition = self.panel.ScreenToClient(globalPosition)
                self.startGlobalOffset = (self.startGlobalPosition[0]-minx, self.startGlobalPosition[1]-miny)
                self.offset = self.panel.ScreenToClient(globalPosition)
            else:
                self.clearMultipleComponentSelection()
                self.multipleSelected = False
                self.propertyEditorWindow.clearComponentList()
                self.propertyEditorWindow.displayComponents(self.components)
                self.startName = target.name
                if self.application.pw is not None:
                    self.application.pw.selectComponentsList(target.name, target.__class__.__name__)
                # KEA 2002-02-23
                self.propertyEditorWindow.selectComponentList(target.name, target.__class__.__name__)
                
                # startGlobalOffset is the initiating mouse x,y wrt. the component
                self.startGlobalOffset = target.ScreenToClient(globalPosition)
                # KEA 2003-05-05
                # workaround for 3D border on Windows
                t = target.__class__.__name__
                if wx.Platform == "__WXMSW__":
                    if ['List', 'PasswordField', 'TextField', 'TextArea', 'Calendar'].count(t):
                        self.startGlobalOffset = [self.startGlobalOffset[0] + wx.SystemSettings.GetMetric(wx.SYS_EDGE_X), 
                            self.startGlobalOffset[1] + wx.SystemSettings.GetMetric(wx.SYS_EDGE_Y)]
                    elif ['Gauge', 'StaticLine'].count(t):
                        self.startGlobalOffset = [self.startGlobalOffset[0] + wx.SystemSettings.GetMetric(wx.SYS_BORDER_X), 
                            self.startGlobalOffset[1] + wx.SystemSettings.GetMetric(wx.SYS_BORDER_Y)]
                    elif t == 'Spinner':
                        # compensate for width of TextCtrl portion of 
                        # compound control - width of arrow buttons
                        self.startGlobalOffset[0] += target.size[0] - 16
                elif wx.Platform == "__WXMAC__":
                    # KEA 2004-07-27
                    # The SYS_EDGE and SYS_BORDER numbers don't seem to work on the Mac
                    # so I just experimented to find the values below to prevent the components
                    # from "hopping" when the user selects them
                    if ['List'].count(t):
                        self.startGlobalOffset = [self.startGlobalOffset[0] - 1, self.startGlobalOffset[1] - 1]
                    elif ['PasswordField', 'TextField', 'TextArea', 'Calendar'].count(t):
                        self.startGlobalOffset = [self.startGlobalOffset[0] + 3, self.startGlobalOffset[1] + 3]
                    elif ['StaticBox'].count(t):
                        # KEA 2004-08-16
                        # sigh, another complete behavior hack
                        if target.label:
                            self.startGlobalOffset = [self.startGlobalOffset[0] + 4, self.startGlobalOffset[1] + 18]
                        else:
                            self.startGlobalOffset = [self.startGlobalOffset[0] + 4, self.startGlobalOffset[1] + 3]
                self.hideSizingHandles()        
                self.startPosition = self.components[self.startName].position
                self.startSize = self.components[self.startName].size
                self.offset = target.ScreenToClient(globalPosition)
        
            self.drawTheRect()
            self.movingComponent = True
    
    def on_mouseLeaveWindow(self, event):
        #print "leave"
        pass
        
    def on_mouseEnterWindow(self, event):
        if not self.marquee: return
        #rint "enter window", event.LeftIsDown()
        if not event.LeftIsDown():
            # mouse has been released
            self.terminate_marquee(event.CmdDown(), event.m_shiftDown)
        
    def on_mouseDrag(self, event):
        # protect against double-clicks in the open file dialog
        # when switching rsrc.py files
        #if event.target.name not in self.sizingHandleNames and self.startName in self.components:
        if not event.Dragging():
            return

        #print "on_mouseDrag"
        if wx.Platform == '__WXMAC__' and not hasattr(self, 'lastPosition'):
            self.on_mouseDown(event)
        if self.marquee:
            # erase the last rect
            self.dc.DrawRectanglePointSize((self.marqueeBase[0], self.marqueeBase[1]), 
                (self.marqueeSize[0], self.marqueeSize[1]))
            # use the global mouse position and the initial offset and start
            # to figure out where to draw a rect in global coordinates
            x, y = self.panel.ScreenToClient(wx.GetMousePosition())
            self.marqueeSize = (x-self.startGlobalPosition[0], y-self.startGlobalPosition[1])
            self.dc.DrawRectanglePointSize((self.marqueeBase[0], self.marqueeBase[1]), 
                (self.marqueeSize[0], self.marqueeSize[1]))
            return

        if self.resizingHandleTarget:
            if self.startName in self.components:
                self.resizingHandler[self.resizingHandleTarget](event)
                return
            else:
                log.debug('resizingHandle set but no good startname' + self.resizingHandle.name)
                pass 

               
        if not self.movingComponent:
            return
                
        if self.multipleSelected:
            self.hideMultiSizingHandles()
        else:
            self.hideSizingHandles()
        
        # erase the last rect
        self.dc.DrawRectanglePointSize((self.lastPosition[0], self.lastPosition[1]), 
            (self.startSize[0], self.startSize[1]))
        # use the global mouse position and the initial offset and start
        # to figure out where to draw a rect in global coordinates
        x, y = self.panel.ScreenToClient(wx.GetMousePosition())
        xOffset = x - self.startGlobalOffset[0]
        yOffset = y - self.startGlobalOffset[1]
        if self.alignToGrid:
            xOffset = xOffset / self.xGridSize * self.xGridSize
            yOffset = yOffset / self.yGridSize * self.yGridSize
        self.lastPosition[0] = xOffset
        self.lastPosition[1] = yOffset           
        self.dc.DrawRectanglePointSize((self.lastPosition[0], self.lastPosition[1]), 
            (self.startSize[0], self.startSize[1]))

        if self.startName:
            # doesn't do anything if just drawing rects
            self.setToolTipDrag(self.startName, self.lastPosition, self.startSize)
            self.propertyEditorWindow.updateSingleProperty(self.startName, 'position', self.lastPosition)
        
    # KEA 2004-09-15
    # support cursor keys to move components one pixel at a time
    # the event is coming from the panel so we have to use the wx methods
    def nudge(self, delta, step, grid=False):
        s = self.propertyEditorWindow.components.wComponentList.stringSelection
        if s:
            name = s.split("  :  ")[0]
            if self.startName <> name:
                self.startName = name

        if self.startName:
            if not self.startName in self.components:
                return
            theList = [self.startName]
        elif self.multipleSelected:
            theList = [ x[0] for x in self.multipleComponents ]
        elif self.components.keys() == []:   # no components exist
            #print "no components"
            return
        else:
            #print "Bug ??"
            return
        
        dx,dy = delta
        while step > 1:  # one grid
            dx, dy = (dx * self.xGridSize, dy * self.yGridSize)
            step = step/2
        
        rx,ry = (1,1)
        if grid or self.alignToGrid:
            rx, ry = (self.xGridSize, self.yGridSize)
                
        for name in theList:
            x, y = self.components[name].position
            # for now I'm only going to align to grid
            # in the direction of the cursor movement 
            if dx:
                x = (x + dx) / rx * rx
            elif dy:
                y = (y + dy) / ry * ry
            else:
                print "no movement ??"
            self.components[name].position = (x, y)

        # make sure sizing handles follow component
        if self.multipleComponents:
            self.showMultiSizingHandles()
        else:
            ###self.startName = name
            self.showSizingHandles(name)
            # update the position on the propertyEditor status bar
            self.setToolTipDrag(name, (x, y), self.components[name].size)
            self.propertyEditorWindow.updateSingleProperty(self.startName, 'position', (x,y))

    def on_keyPress(self, event):
        keyCode = event.GetKeyCode()
        cmdKey = event.CmdDown()
        shiftKey = event.ShiftDown()
        keyDeltas = {wx.WXK_LEFT: (-1,0), wx.WXK_UP: (0,-1), 
                     wx.WXK_RIGHT: (1,0), wx.WXK_DOWN: (0,1)}
        if not keyCode in keyDeltas.keys():
            return
            
        dx,dy = keyDeltas[keyCode]
        grid = False
        step = 1
        if cmdKey or self.alignToGrid:
            step = 2
            grid = True
        if shiftKey:
            step = step*2
            
        self.nudge((dx,dy),step, grid)


    def terminate_marquee(self, cmdKey, shiftKey):
        # erase the last rect
##            print self.marqueeSize
        self.dc.DrawRectanglePointSize((self.marqueeBase[0], self.marqueeBase[1]), 
            (self.marqueeSize[0], self.marqueeSize[1]))
        if self.marqueeSize == (0,0) and not shiftKey and not cmdKey:
            # just a click - deselect anything
            if self.multipleSelected:
                self.clearMultipleComponentSelection()
                # but remain in multi mode
                # self.multipleSelected = False
                ## and switch back to single-mode, with the last select comp if known.
                self.multipleSelected = False
                self.propertyEditorWindow.clearComponentList()
                self.propertyEditorWindow.displayComponents(self.components)
                if self.startName:
                    name = self.startName
                else:
                    s = self.lastSelection
                    if s:
                        name, klass = s.split("  :  ")
                    else:
                        name = None
                        if self.startName <> name:
                            self.startName = name
                if self.application.pw is not None and name:
                    self.application.pw.selectComponentsList(name, klass)
                # KEA 2002-02-23
                if name: self.propertyEditorWindow.selectComponentList(name, klass)
                

            elif self.startName:
                self.hideSizingHandles()
                self.startName = None
            return
        #print "selct anything within", self.startGlobalPosition, self.marqueeSize
        res = self.controlInRect(self.startGlobalPosition, self.marqueeSize)
        self.marquee = False
        #print "we found", res
        if res == []: return

        self.switchToMultipleMode()

        # new selection - delete any existing selections
        if not shiftKey and not cmdKey: 
            self.clearMultipleComponentSelection()
            
        for name in res:
            index = self.prefixIndexForComp(name)
            if index == -1:  # not already there - add unless "remove only"
                if not (cmdKey and shiftKey): self.multipleComponents.append( (name, self.makeNewHandles(name)))
            else:   # already there - remove if toggle or remove
                if cmdKey:
                    prefix = self.multipleComponents[index][1]
                    for sizingHandle in self.sizingHandleNames:
                        del self.components[prefix+sizingHandle]
                    del self.multipleComponents[index]
                    
        self.propertyEditorWindow.updateComponentList()
        return



    def on_mouseUp(self, event):
        # protect against double-clicks in the open file dialog
        # when switching rsrc.py files
        ####print "on_mouseUp BEFORE", self.rect
        cmdKey = event.CmdDown()
        shiftKey = event.ShiftDown()
        if self.marquee:
            self.terminate_marquee(cmdKey, shiftKey)
            return

        # no marquee            
        if self.startName in self.components:
            if self.movingComponent:
                self.dc.DrawRectanglePointSize((self.lastPosition[0], self.lastPosition[1]), 
                    (self.startSize[0], self.startSize[1]))
                self.components[self.startName].position = (self.lastPosition[0], self.lastPosition[1])
                #print "on_mouseUp", self.lastPosition
                self.panel.Refresh()
                self.movingComponent = False

            if wx.Platform == '__WXMAC__':
                ##if self.lastCaptured is not None:
                ##    self.lastCaptured.ReleaseMouse()
                ##    self.lastCaptured = None
                #event.target.ReleaseMouse()
                # clear up drag artifacts
                self.Refresh()
            if wx.Platform == '__WXGTK__':
                ##if self.lastCaptured is not None:
                ##    self.lastCaptured.ReleaseMouse()
                ##    self.lastCaptured = None
                #event.target.ReleaseMouse()
                self.Refresh()
            self.showSizingHandles(self.startName)
            self.resizingHandleTarget = None
            #self.setToolTip(self.components[self.startName])
            #self.components[self.startName].toolTip = self.startToolTip
            return


        if self.multipleSelected:
            if self.movingComponent:
                self.dc.DrawRectanglePointSize((self.lastPosition[0], self.lastPosition[1]), 
                    (self.startSize[0], self.startSize[1]))
                for c,pre in self.multipleComponents:
                    x,y = self.components[c].position
                    nx = x + self.lastPosition[0] - self.startPosition[0]
                    ny = y + self.lastPosition[1] - self.startPosition[1]
                    #print c, x,y, nx,ny
                    self.components[c].position = nx,ny
                #print "on_mouseUp", self.lastPosition
                self.panel.Refresh()
                self.movingComponent = False

            if wx.Platform == '__WXMAC__':
                ##if self.lastCaptured is not None:
                ##    self.lastCaptured.ReleaseMouse()
                ##    self.lastCaptured = None
                #event.target.ReleaseMouse()
                # clear up drag artifacts
                self.Refresh()
            if wx.Platform == '__WXGTK__':
                ##if self.lastCaptured is not None:
                ##    self.lastCaptured.ReleaseMouse()
                ##    self.lastCaptured = None
                #event.target.ReleaseMouse()
                self.Refresh()
            self.showMultiSizingHandles()
            

    # KEA 2001-12-24
    # I need to refactor the common elements of the resizing handle code
    # I also want to add a Component info window to show the component
    # name, position, size as the component is moved and resized
    # THe 2002-08-29
    # Refactored the common elements of resizing handle code.
    
    def doResize(self, event, (n, w, s, e)):
        if not self.startName:
            return

        # AGT 2005-05-17 Removed obsolete Windows variant
        globalPosition = wx.GetMousePosition()
        x, y = self.components[self.resizingHandleTarget].ScreenToClient(globalPosition)
        xOffset = x - self.offset[0]
        yOffset = y - self.offset[1]
            
        xStartOffset = self.startPosition[0] + e * xOffset
        yStartOffset = self.startPosition[1] + n * yOffset
        if self.alignToGrid:
            xOffset = xOffset / self.xGridSize * self.xGridSize
            yOffset = yOffset / self.yGridSize * self.yGridSize
            xStartOffset = xStartOffset / self.xGridSize * self.xGridSize
            yStartOffset = yStartOffset / self.yGridSize * self.yGridSize

        width = self.startSize[0] + (w - e) * xOffset
        height = self.startSize[1] + (s - n) * yOffset
        self.components[self.startName].position = (xStartOffset, yStartOffset)
        self.components[self.startName].size = (width, height)
        self.setToolTip(self.components[self.startName])
        self.propertyEditorWindow.updateSingleProperty(self.startName, 'position', (xStartOffset, yStartOffset))
        self.propertyEditorWindow.updateSingleProperty(self.startName, 'size', (width, height))
        

    def on_topLeft_mouseDrag(self, event):
        if self.marquee: 
            self.on_mouseDrag(event)
            return
        self.doResize(event, (1, 0, 0, 1))
        
    def on_topMiddle_mouseDrag(self, event):
        if self.marquee: 
            self.on_mouseDrag(event)
            return
        self.doResize(event, (1, 0, 0, 0))

    def on_topRight_mouseDrag(self, event):
        if self.marquee: 
            self.on_mouseDrag(event)
            return
        self.doResize(event, (1, 1, 0, 0))

    def on_middleLeft_mouseDrag(self, event):
        if self.marquee: 
            self.on_mouseDrag(event)
            return
        self.doResize(event, (0, 0, 0, 1))

    def on_middleRight_mouseDrag(self, event):
        if self.marquee: 
            self.on_mouseDrag(event)
            return
        self.doResize(event, (0, 1, 0, 0))
        
    def on_bottomLeft_mouseDrag(self, event):
        if self.marquee: 
            self.on_mouseDrag(event)
            return
        self.doResize(event, (0, 0, 1, 1))
    
    def on_bottomMiddle_mouseDrag(self, event):
        if self.marquee: 
            self.on_mouseDrag(event)
            return
        self.doResize(event, (0, 0, 1, 0))
        
    def on_bottomRight_mouseDrag(self, event):
        if self.marquee: 
            self.on_mouseDrag(event)
            return
        self.doResize(event, (0, 1, 1, 0))

    def saveChanges(self):
        if self.filename is None:
            filename = "Untitled"
        else:
            filename = self.filename
        msg = "The data in the %s file has changed.\n\nDo you want to save the changes?" % filename
        result = dialog.messageDialog(self, msg, 'resourceEditor',
                                   wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL)
        return result.returnedString

    def newFile(self, fullTemplatePath):
        """
        KEA 2003-07-31
        the logic of where templates come from,
        the user selecting a template,
        prompting to save, etc. should be refactored
        especially if we are going to support a 
        pythoncard_config/resourceEditor/templates
        directory for user-specific resource/code templates
        for now we'll assume a single templates dir
        and put the save logic here
        
        also need to decide if resourceEditor should startup differently
        like not showing a new layout to begin with
        maybe have an option to start with a new project prompt,
        open resource dialog, or none so user can select from the
        history (always lots of UI decisions ;-)
        """
        # prompt to save
        # user will probably end up creating a new dir
        # and changing the filename
        templatePath, templateFilename = os.path.split(fullTemplatePath)
        #print path, filename
        # have the user save the source or resource?!
        wildcard = "Python files (*.py)|*.py"
        # don't set the starting dir, let user navigate
        result = dialog.saveFileDialog(None, "Save As", "", templateFilename[:-8] + ".py", wildcard)
        if result.accepted:
            path = result.paths[0]
            
            if path.endswith('.rsrc.py'):
                basepath = os.path.splitext(os.path.splitext(path)[0])[0]
            elif path.endswith('.py'):
                basepath = os.path.splitext(path)[0]
            else:
                # user didn't use a .py extension?
                # should this be an error?
                basepath = path

            #print basepath

            # now we need to copy and rename the
            # template files to the user chosen location
            import shutil

            destPath, destFilename = os.path.split(basepath)
            # copy the .py file
            fname = os.path.join(templatePath, templateFilename[:-8] + ".py")
            tname = os.path.join(destPath, destFilename + ".py")
            #print "copying", tname
            shutil.copy(fname, tname)
            # copy the .rsrc.py file
            fname = os.path.join(templatePath, templateFilename)
            tname = os.path.join(destPath, destFilename + ".rsrc.py")
            #print "copying", tname
            shutil.copy(fname, tname)
            
            self.filename = tname
            #print self.filename
        else:
            # present a dialog instead?!
            return
        
        self.resetAndClearWidgets()
        path = os.path.join(self.filename)
        self.rsrc = resource.ResourceFile(path).getResource()
        ##self.filename = None
        self.updatePanel(self.rsrc)
        if self.editingDialog: 
            comp = self.rsrc.components
        else:
            comp = self.rsrc.application.backgrounds[0].components
        for w in comp:
            self.components[w.name] = w
        self.rebindEventsForDragging()
        self.documentChanged = False
        # could change the resource and title bar
        # here to give the user more feedback

    def saveFile(self):
        if self.filename is None:
            return self.on_menuFileSaveAs_select(None)
        else:
            ##desc = self.resourceAttributes()
            desc = multiresourceOutput.resourceAttributes(self)
            try:
                f = open(self.filename, 'w')
                f.write(desc)
                f.close()
                self.documentChanged = False
                self.fileHistory.AddFileToHistory(self.filename)
                return True
            except Exception, e:
                message = 'The resource file could not be saved.\n' + str( e )
                dialog.messageDialog(self, message, 'ResourceEditor Error',
                                     wx.ICON_EXCLAMATION | wx.OK)
                return False

    def revertFile(self):
        self.resetAndClearWidgets()
        if self.filename is None:
            path = os.path.join(self.application.applicationDirectory, 'templates', \
                            RESOURCE_TEMPLATE)
            self.rsrc = resource.ResourceFile(path).getResource()
        else:
            self.rsrc = resource.ResourceFile(self.filename).getResource()
        self.updatePanel(self.rsrc)
        # KEA 2002-03-24
        # either we're editing a Background or a Dialog
        if self.editingDialog: 
            comp = self.rsrc.components
        else:
            comp = self.rsrc.application.backgrounds[0].components
        for w in comp:
            self.components[w.name] = w
        self.rebindEventsForDragging()
        self.documentChanged = False

    def getNewFileTemplates(self):
        templatesDir = os.path.join(self.application.applicationDirectory, 'templates')
        fileList = os.listdir(templatesDir)
        #fileList.sort()
        templates = []
        for filename in fileList:
            # get 'title'
            path = os.path.join(templatesDir, filename)
            if os.path.isfile(path):
                try:
                    rsrc = resource.ResourceFile(path).getResource()
                    try:
                        templates.append((rsrc.application.backgrounds[0].title, path, 'background'))
                    except:
                        templates.append((rsrc.title, path, 'dialog'))
                except:
                    # not a resource file
                    pass
        templates.sort()
        return templates

    def doNewFile(self):
        templates = self.getNewFileTemplates()
        listX = []
        for t in templates:
            #print t[0], t[2], t[1]
            listX.append(t[0])
        result = dialog.singleChoiceDialog(self, "Choose a resource template", "Templates", listX)
        if result.accepted:
            name = result.selection
            for t in templates:
                if t[0] == name:
                    filename = t[1]
            self.newFile(filename)

    def on_menuFileNew_select(self, event):
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                pass
            elif save == "No":
                # any changes will be lost
                #self.newFile(RESOURCE_TEMPLATE)
                self.doNewFile()
            else:
                if self.filename is None:
                    if self.on_menuFileSaveAs_select(None):
                        #self.newFile(RESOURCE_TEMPLATE)
                        self.doNewFile()
                else:
                    self.saveFile()
                    #self.newFile(RESOURCE_TEMPLATE)
                    self.doNewFile()
        else:
            #self.newFile(RESOURCE_TEMPLATE)
            self.doNewFile()

    def on_menuFileNewDialog_select(self, event):
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                pass
            elif save == "No":
                # any changes will be lost
                self.newFile(RESOURCE_DIALOG_TEMPLATE)
            else:
                if self.filename is None:
                    if self.on_menuFileSaveAs_select(None):
                        self.newFile(RESOURCE_DIALOG_TEMPLATE)
                else:
                    self.saveFile()
                    self.newFile(RESOURCE_DIALOG_TEMPLATE)
        else:
            self.newFile(RESOURCE_DIALOG_TEMPLATE)

    def on_menuFileSave_select(self, event):
        self.saveFile()

    def on_menuFileSaveAs_select(self, event):
        if self.filename is None:
            path = ''
            filename = ''
        else:
            path, filename = os.path.split(self.filename)
        wildcard = "resource files (*.rsrc.py)|*.rsrc.py"
        result = dialog.saveFileDialog(None, "Save As", path, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            # KEA 2002-06-01
            # force .rsrc.py extension
            # the one problem with this is that
            # the user won't be prompted for an overwrite
            # of a .rsrc.py file if they didn't enter that
            # in the save as dialog
            if not path.endswith('.rsrc.py'):
                path = os.path.splitext(path)[0] + '.rsrc.py'
            ##desc = self.resourceAttributes()
            desc = multiresourceOutput.resourceAttributes(self)
            try:
                f = open(path, 'w')
                f.write(desc)
                f.close()
                self.filename = path
                self.documentChanged = False
                return True
            except:
                return False
        else:
            return False

    def on_menuFileRevert_select(self, event):
        if self.documentChanged:
            if self.filename is None:
                filename = "Untitled"
            else:
                filename = self.filename
            msg = "You will lose any changes you've made to %s.\n\nAre you sure you want to revert to the last saved version?" % filename
            result = dialog.messageDialog(self, msg, 'resourceEditor',
                                       wx.ICON_EXCLAMATION | wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT)
            save = result.returnedString
            if save == "Cancel" or save == "No":
                # don't do anything, just go back to editing
                pass
            else:
                # any changes will be lost
                self.revertFile()
        else:
            self.revertFile()


    def resetAndClearWidgets(self):
        self.startName = None
        self.multipleSelected = False
        self.multipleComponents = []
        self.startPosition = (0, 0)
        self.startSize = (0, 0)
        self.offset = (0, 0)
        if self.application.pw is not None:
            if wx.Platform == '__WXMAC__':
                self.application.pw.selectComponentsList('topLeft', 'Image')
            else:
                self.application.pw.selectComponentsList('topLeft', 'ImageButton')
        # KEA 2002-02-23
        self.propertyEditorWindow.clearComponentList()
        self.propertyEditorWindow.clearPropertyList()
        self.hideSizingHandles()
        self.clearWidgets()

    def openFile(self, path):
        self.resetAndClearWidgets()

        os.chdir(os.path.dirname(path))
        self.filename = path
        rsrc = resource.ResourceFile(path).getResource()
        self.rsrc = rsrc
        
        self.updatePanel(self.rsrc)

        # KEA 2002-03-24
        # either we're editing a Background or a Dialog
        if self.editingDialog: 
            comp = self.rsrc.components
        else:
            comp = self.rsrc.application.backgrounds[0].components
        for w in comp:
            self.components[w.name] = w

        self.rebindEventsForDragging()

        self.documentChanged = False
        self.fileHistory.AddFileToHistory(self.filename)

    def doOpenFile(self):
        wildcard = "resource files (*.rsrc.py)|*.rsrc.py"
        result = dialog.openFileDialog(None, "Import which resource file?", '', '', wildcard)
        if result.accepted:
            self.openFile(result.paths[0])

    def on_menuFileOpen_select(self, event):
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                # don't do anything, just go back to editing
                pass
            elif save == "No":
                # any changes will be lost
                self.doOpenFile()
            else:
                if self.filename is None:
                    if self.on_menuFileSaveAs_select(None):
                        self.doOpenFile()
                else:
                    self.saveFile()
                    self.doOpenFile()
        else:
            self.doOpenFile()


    def on_menuHelpAbout_select(self, event):
        dialog.scrolledMessageDialog(self, self.readme, 'About resourceEditor...')

    def on_doHelpAboutPythonCard_command(self, event):
        about.aboutPythonCardDialog(self)

    def clearMultipleComponentSelection(self):
        changes = 0
        for c,prefix in self.multipleComponents:
            changes += 1
            for sizingHandle in self.sizingHandleNames:
                del self.components[prefix+sizingHandle]
        self.multipleComponents = []
        if wx.Platform == '__WXMAC__' and changes > 0:
            self.panel.Refresh()
        
    def fixComponentOrder(self, name):
        # KEA 2005-12-23
        # Lower() doesn't appear to always work correctly, 
        # so use Raise instead with a reversed list
        r = self.components.order[:]
        r.reverse()
        for c in r:
            self.components[c].Raise()
        
        if self.application.pw is not None:
            self.application.pw.clearComponentsList()
            self.application.pw.displayComponents(self.components)
            if name:
                self.application.pw.selectComponentsList(name, self.components[name].__class__.__name__)
        # KEA 2002-02-23
        ##self.propertyEditorWindow.Freeze()
        if not self.multipleSelected:
            self.propertyEditorWindow.clearComponentList()
            self.propertyEditorWindow.displayComponents(self.components)
            if name:
                self.propertyEditorWindow.selectComponentList(name, self.components[name].__class__.__name__)
        ##self.propertyEditorWindow.Thaw()

    def generateUniqueName(self, name):
        i = 1
        if name == "": name = "a"
        while True:
            if name + str(i) not in self.components:
                return name+str(i)
            i += 1

    def convertToValidName(self, v):
        # and make it into a valid name
        parts = v.split(' ')
        if len(parts) > 1:
            newparts = [p.lower().capitalize() for p in parts]
            newparts[0] = newparts[0].lower()
            v = ''.join(newparts)
        newv = ''
        if v == "": v = "a"
        for c in v:
            if newv == '':
                if c in string.ascii_letters: newv += c
            elif c in string.ascii_letters or c in string.digits or c in '_':
                newv += c
        return newv
        
    def deriveNameFromLabel(self, desc):
        if 'label' in desc.keys():
            v = desc['label']
        elif 'text' in desc.keys():
            v = desc['text']
        else: 
            v = ""
        newv = self.convertToValidName(v)
        desc['name'] = newv
        
    def deriveLabelFromName(self, desc):
        if 'label' in desc.keys():
            desc['label'] = desc['name']
        elif 'text' in desc.keys():
            desc['text'] = desc['name']

    def create_component(self, desc):
        optionalAttributes = registry.Registry.getInstance().components[desc['type']]._spec._optionalAttributes.keys()
        
        if 'label' in optionalAttributes:
            desc['label'] = desc['name']
        elif 'text' in optionalAttributes:
            desc['text'] = desc['name']

        self.deriveLabelFromName(desc)
        name = desc['name']
        self.components[name] = desc
        
        # offset the widget so that it isn't underneath the original
        x, y = self.components[name].position
        dx, dy = self.components[name].size
        #rint x, y, dx, dy
        if self.offsets == 'horizontal':
            x += dx+30
        elif self.offsets == 'vertical':
            y += dy+30
        elif self.offsets == 'both':
            x += dx+30
            y += dy+30
        else:
            x += 10
            y += 10
        self.components[name].position = (x, y)

        self.clearMultipleComponentSelection()
        # KEA 2001-12-20
        # hack to insert component so that it is the first one
        # in the list
        # a similar trick will be needed for re-ordering widgets
        self.components.order.remove(name)
        self.components.order.insert(NUM_SIZING_HANDLES, name)
        self.fixComponentOrder(name)

        self.startName = name
        self.startPosition = self.components[self.startName].position
        self.startSize = self.components[self.startName].size
        self.offset = (0, 0)
        self.showSizingHandles(name)
        self.documentChanged = True

        c = self.components[self.startName]
        wx.EVT_LEFT_DOWN(c, self.on_mouseDown)
        wx.EVT_LEFT_UP(c, self.on_mouseUp)
        wx.EVT_MOTION(c, self.on_mouseDrag)
##            name = result.name
##            if name in self.components:
##                dialog.alertDialog(self, name + " already exists", 'Error: Unable to '+errString+' widget')
##                return
##            if 'label' in optionalAttributes:
##                desc['label'] = result.labelortext
##            elif 'text' in optionalAttributes:
##                desc['text'] = result.labelortext
##
##            desc['name'] = name
##            self.components[name] = desc
##            if offsets:
##                # offset the widget so that it isn't underneath the original
##                x, y = self.components[name].position
##                dx, dy = self.components[name].size
##                #rint x, y, dx, dy
##                if result.horizontal:
##                    x += dx+30
##                    if result.vertical:
##                        y += dy+30
##                else:
##                    if result.vertical:
##                        y += dy+30
##                    else:
##                        x += 10
##                        y += 10
##                #rint "       => ", x, y
##                self.components[name].position = (x, y)
##    
##            self.clearMultipleComponentSelection()
##            # KEA 2001-12-20
##            # hack to insert component so that it is the first one
##            # in the list
##            # a similar trick will be needed for re-ordering widgets
##            self.components.order.remove(name)
##            self.components.order.insert(NUM_SIZING_HANDLES, name)
##            self.fixComponentOrder(name)
##    
##            self.startName = name
##            self.startPosition = self.components[self.startName].position
##            self.startSize = self.components[self.startName].size
##            self.offset = (0, 0)
##            self.showSizingHandles(name)
##            self.documentChanged = True
##    
##            c = self.components[self.startName]
##            wx.EVT_LEFT_DOWN(c, self.on_mouseDown)
##            wx.EVT_LEFT_UP(c, self.on_mouseUp)
##            wx.EVT_MOTION(c, self.on_mouseDrag)

    def on_componentDuplicate_command(self, event):
        if self.startName in self.components:
            aWidget = self.components[self.startName]

            # now loop through the original widget and build a dictionary suitable
            # for making a copy
            d = {}
            d['type'] = aWidget.__class__.__name__
            #for key in aWidget._getAttributeNames():
            attributes = aWidget._spec.getAttributes().keys()
            attributes.sort()
            for key in attributes:
                # I'm not exactly sure why I have to special-case these tuples
                if key == 'bitmap':
                    # this should get recreated from the file attribute
                    pass
                elif key == "id":
                    # must avoid duplicate IDs 
                    pass
                elif key in ['position', 'size']:
                    d[key] = getattr(aWidget, key)
                elif getattr(aWidget, key) is not None:
                    d[key] = getattr(aWidget, key)

            d['name'] = self.generateUniqueName(d['name'])
            #print d
            self.create_component(d)

    def on_componentDelete_command(self, event):
        if self.startName in self.components:
            aWidget = self.components[self.startName]
            msg = "Are you sure you want to delete %s %s?" % (aWidget.__class__.__name__, aWidget.name)
        elif self.multipleSelected:
            if len(self.multipleComponents) == 0: return
            nameList = [ x[0] for x in self.multipleComponents ]
            if len(self.multipleComponents) == 1:
                msg = "Are you sure you want to Delete this component ?"
            else:
                msg = "Are you sure you want to Delete %d components?" % (len(self.multipleComponents))
        result = dialog.messageDialog(self, msg, 'Delete Component',
            wx.ICON_INFORMATION | wx.YES_NO | wx.NO_DEFAULT)

        if result.accepted:
            if self.multipleSelected:
                self.hideMultiSizingHandles()
                for name in nameList:
                    del self.components[name]
            else:
                 self.hideSizingHandles()
                 del self.components[aWidget.name]
            self.documentChanged = True

    def on_componentAdd_command(self, event):
        # event.target.name will be something like
        # menuComponentAddButton, so the first 16 characters
        # can be thrown away to get the component name
        className = event.target.name[16:]

        # find a unique name
        # find a unique name
        name = self.generateUniqueName(className)
        desc = registry.Registry.getInstance().components[className]._spec.getMinimalResourceDict(name)
        desc['name'] = name
        desc['position'] = (10, 10)
        self.create_component(desc)
          
        
    def readingOrder(self, c1, c2):
        # compare two components to determine which is "earlier" in reading order
##        print c1, self.components[c1].position, self.components[c1].size
##        print c2, self.components[c2].position, self.components[c2].size
        if self.components[c1].position[1] + self.components[c1].size[1] < self.components[c2].position[1]:
            return -1
        if self.components[c2].position[1] + self.components[c2].size[1] < self.components[c1].position[1]:
            return 1
        if self.components[c1].position[0] < self.components[c2].position[0]:
            return -1
        return 1
    
    def moveList(self, tomove, dir, readingOrderFlag = False):
        list = copy.copy(self.components.order)
        # first remove all but the first (base) one of the tomove list from main list
        for x in tomove[1:]:
            if x in list:
                list.remove(x)
        # now we can get the proper relative index for the first one
        i = list.index(tomove[0])
        # and then remove it
        if tomove[0] in list:
            list.remove(tomove[0])
        j = i+dir
        if readingOrderFlag:
            sortlist = [ (x) for x in tomove ]
            #print sortlist
            sortlist.sort(self.readingOrder)
            #print sortlist
            newmove = [ name for name in sortlist ]
            tomove = newmove
            
        if j+len(tomove) > len(list):
            list = list + tomove
        elif j <= NUM_SIZING_HANDLES:
            j = NUM_SIZING_HANDLES
            list = list[:NUM_SIZING_HANDLES] + tomove + list[NUM_SIZING_HANDLES:]
        else:
            list = list[:j] + tomove + list[j:]
        if list <> self.components.order:
            while len(self.components.order):
                self.components.order.remove(self.components.order[0])
            for c in list:
                self.components.order.append(c)
            self.fixComponentOrder(self.startName)
                    
    def on_componentSendBack_command(self, event):
        self.on_componentMoveBack_command(event, len(self.components))

    def on_componentMoveBack_command(self, event, distance = 1):
        if self.startName in self.components:
            self.moveList([self.startName], distance)
        elif self.multipleSelected:
            self.moveList([ x[0] for x in self.multipleComponents ], distance)

    def on_componentMoveTogether_command(self, event):
        # useful to re-order multiple components without changing relative to non-selected ones
        if self.multipleSelected:
            self.moveList([ x[0] for x in self.multipleComponents ], 0)
        
    def on_componentRelayer_command(self, event):
        # useful to re-order multiple components without changing relative to non-selected ones
        if self.multipleSelected:
            self.moveList([ x[0] for x in self.multipleComponents ], 0, True)
        
    def on_componentMoveForward_command(self, event):
        self.on_componentMoveBack_command(event, -1)

    def on_componentBringFront_command(self, event):
        self.on_componentMoveBack_command(event, -len(self.components))


    def on_componentSelectAll_command(self, event):
        #Reset component list on the property editor
        self.clearMultipleComponentSelection()
        self.multipleSelected = False
        self.propertyEditorWindow.clearComponentList()
        self.propertyEditorWindow.displayComponents(self.components)

        res = self.propertyEditorWindow.components.wComponentList.items
        if res == []: return
         
        self.marquee = False
        self.switchToMultipleMode()
        self.clearMultipleComponentSelection()
                
        for ctrline in res:
            name = ctrline.split("  :  ")[0]
            self.multipleComponents.append( (name, self.makeNewHandles(name)))
             
        self.propertyEditorWindow.updateComponentList()
        return


    def on_displayAttributes_command(self, event):
        ##desc = self.resourceAttributes()
        desc = multiresourceOutput.resourceAttributes(self)
        dialog.scrolledMessageDialog(self, desc, 'Resource')

    def on_menuViewPropertyEditor_select(self, event):
        self.propertyEditorWindow.visible = not self.propertyEditorWindow.visible

    def updatePanel(self, rsrc):
        # KEA 2002-03-24
        # this will need to update different parameters
        # depending on whether we're editing a background or dialog
        self.editingDialog = False
        try: 
            background = rsrc.application.backgrounds[0]
        except:
            dlg = self.rsrc
            self.editingDialog = True

        # unhook the grid drawing and then rebind later if necessary
        if self.showGridLines:
            self.panel.Unbind(wx.EVT_ERASE_BACKGROUND)

        if self.editingDialog:
            self.menuBar.setEnabled('menuFileRun', False)
            self.menuBar.setEnabled('menuFileRunWithInterpreter', False)
            self.menuBar.setEnabled('menuFilePreviewDialog', True)
            self.menuBar.setEnabled('menuEditBackgroundInfo', False)
            self.menuBar.setEnabled('menuEditMenubar', False)
            self.menuBar.setEnabled('menuEditDialogInfo', True)
            
            self.title = dlg.title
            self._createStatusBar(dlg)
            self.position = dlg.position
            #self.setSize((dlg.size[0], dlg.size[1] + 20))
            self.size = dlg.size
            self.setImage('')
            self.setTiled(False)
            self.panel._imageFile = self.image
            self.panel._backgroundTiling = self.tiled

            defaultBgColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
            self.backgroundColor = defaultBgColor
            self.panel.Disconnect(-1, -1, wx.wxEVT_ERASE_BACKGROUND)
            self.panel._bitmap = None
        else:
            self.menuBar.setEnabled('menuFileRun', True)
            self.menuBar.setEnabled('menuFileRunWithInterpreter', True)
            self.menuBar.setEnabled('menuFilePreviewDialog', False)
            self.menuBar.setEnabled('menuEditBackgroundInfo', True)
            self.menuBar.setEnabled('menuEditMenubar', True)
            self.menuBar.setEnabled('menuEditDialogInfo', False)

            self.title = background.title
            self._createStatusBar(background)
            self.position = background.position
            if background.menubar is None:
                #self.setSize((background.size[0], background.size[1] + 20))
                self.size = background.size
            else:
                self.size = background.size
            self.setImage(background.image)
            self.setTiled(background.tiled)
            self.panel._imageFile = self.image
            self.panel._backgroundTiling = self.tiled

            defaultBgColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE)
            self.backgroundColor = defaultBgColor
            self.foregroundColor = background.foregroundColor
            self.backgroundColor = background.backgroundColor
            if self.image is not None :
                self.panel._bitmap = graphic.Bitmap(self.image)
                wx.EVT_ERASE_BACKGROUND( self.panel, self.panel.onEraseBackground )
            else:
                self.panel.Disconnect(-1, -1, wx.wxEVT_ERASE_BACKGROUND)
                self.panel._bitmap = None

        self.movingComponent = False
        self.resizingHandleTarget = None

        if self.showGridLines:
            self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.drawPanelGridLines)
        self.panel.Refresh()

    def drawPanelGridLines(self, event):
        dc = event.GetDC()
        if not dc :
            dc = wx.ClientDC(self.panel)
            r = self.panel.GetUpdateRegion().GetBox()
            dc.SetClippingRegion(r.x, r.y, r.width, r.height)
        # need to set the background color to the default panel color
        brush = dc.GetBackground()
        brush.SetColour(self.panel.GetBackgroundColour())
        dc.SetBackground(brush)
        dc.Clear()
        # should the color be settable by the user and then save
        # that in the prefs?
        dc.SetPen(wx.Pen('darkgray', 1, wx.SOLID))
        w, h = self.panel.size
        xgrid = self.xGridSize
        ygrid = self.yGridSize
        nx = w / xgrid
        ny = h / ygrid
        for x in range(1, nx + 1):
            dc.DrawLine(x * xgrid, 0, x * xgrid, h)
        for y in range(1, ny + 1):
            dc.DrawLine(0, y * ygrid, w, y * ygrid)
        
    def rebindEventsForDragging(self):
        for name in self.components.order:
            if name not in self.sizingHandleNames:
                #print name
                c = self.components[name]
                wx.EVT_LEFT_DOWN(c, self.on_mouseDown)
                wx.EVT_LEFT_UP(c, self.on_mouseUp)
                wx.EVT_MOTION(c, self.on_mouseDrag)

    # KEA 2004-08-12
    # for each of the dialogs below, the code should be refactored
    # so that the dialog modules have a function wrapper and the
    # result contains whatever attributes would be needed
    # the function should probably not have side-effects

    def on_fileRunOptions_command(self, event):
        result = runOptionsDialog.runOptionsDialog(self, self.cmdLineArgs)
        if result.accepted:
            self.cmdLineArgs['debugmenu'] = result.debugmenu
            self.cmdLineArgs['logging'] = result.logging
            self.cmdLineArgs['messagewatcher'] = result.messagewatcher
            self.cmdLineArgs['namespaceviewer'] = result.namespaceviewer
            self.cmdLineArgs['propertyeditor'] = result.propertyeditor
            self.cmdLineArgs['shell'] = result.shell
            self.cmdLineArgs['otherargs'] = result.otherargs

    def on_editStackInfo_command(self, event):
        result = stackInfoDialog.stackInfoDialog(self, self.rsrc)
        if result.accepted:
            self.rsrc.application.name = result.text
            self.documentChanged = True

    # need to change the logic so that self.rsrc
    # and the current window are updated
    def on_editBackgroundInfo_command(self, event):
        background = self.rsrc.application.backgrounds[0]
        background.position = self.GetPositionTuple()
        background.size = self.GetSizeTuple()
        result = backgroundInfoDialog.backgroundInfoDialog(self, background)
        if result.accepted:
            background.name = result.name
            background.title = result.title
            background.position = result.position
            background.size = result.size
            background.statusBar = result.statusBar
            background.foregroundColor = result.foregroundColor
            background.backgroundColor = result.backgroundColor
            background.image = result.image
            background.tiled = result.tiled
            background.visible = result.visible
            background.style = result.style
            background.icon = result.icon
            self.updatePanel(self.rsrc)
            self.documentChanged = True

    # need to change the logic so that self.rsrc
    # and the current window are updated
    def on_editDialogInfo_command(self, event):
        background = self.rsrc
        background.position = self.GetPositionTuple()
        background.size = self.GetSizeTuple()
        result = dialogInfoDialog.dialogInfoDialog(self, background)
        if result.accepted:
            background.name = result.name
            background.title = result.title
            background.position = result.position
            background.size = result.size
            self.updatePanel(self.rsrc)
            self.documentChanged = True
        

    def on_editMenubar_command(self, event):
        try:
            menubar = self.rsrc.application.backgrounds[0].menubar
        except:
            menubar = None
        result = menuDialog.menuDialog(self, menubar)
        if result.accepted:
            self.rsrc.application.backgrounds[0].menubar = result.menubar
            self.documentChanged = True

    def on_editStrings_command(self, event):
        stringList = {}
        try:
            if self.editingDialog: 
                strings = self.rsrc.strings
            else:
                strings = self.rsrc.application.backgrounds[0].strings
            for s in strings.__dict__:
                stringList[s] = strings.__dict__[s]
        except:
            stringList = {}
        result = stringDialog.stringDialog(self, stringList)
        if result.accepted:
            if self.editingDialog:
                self.rsrc.strings = result.stringList
            else:
                self.rsrc.application.backgrounds[0].strings = result.stringList
            self.documentChanged = True


    def on_optionGridSize_command(self, event):
        result = dialog.textEntryDialog(self, 
                                    'Enter the preferred grid size (e.g. 5):',
                                    'Grid Size', 
                                    str(self.xGridSize))
        if result.accepted:
            try:
                size = int(result.text)
                self.xGridSize = size
                self.yGridSize = size
                if self.showGridLines:
                    self.panel.Refresh()
            except:
                # should probably do an alert dialog here
                pass

    def on_menuOptionsAlignToGrid_select(self, event):
        self.alignToGrid = self.menuBar.getChecked('menuOptionsAlignToGrid')

    def on_menuOptionsShowGridLines_select(self, event):
        self.showGridLines = self.menuBar.getChecked('menuOptionsShowGridLines')
        if self.showGridLines:
            self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.drawPanelGridLines)
        else:
            self.panel.Unbind(wx.EVT_ERASE_BACKGROUND)
        self.panel.Refresh()

    def getCommandLineArgs(self):
        args = ' '
        if self.cmdLineArgs['debugmenu']:
            args += '-d '
        if self.cmdLineArgs['logging']:
            args += '-l '
        if self.cmdLineArgs['messagewatcher']:
            args += '-m '
        if self.cmdLineArgs['namespaceviewer']:
            args += '-n '
        if self.cmdLineArgs['propertyeditor']:
            args += '-p '
        if self.cmdLineArgs['shell']:
            args += '-s '
        """
        if self.menuBar.getChecked('menuOptionsLogging'):
            args += '-l '
        if self.menuBar.getChecked('menuOptionsMessageWatcher'):
            args += '-m '
        if self.menuBar.getChecked('menuOptionsNamespaceViewer'):
            args += '-n '
        if self.menuBar.getChecked('menuOptionsPropertyEditor'):
            args += '-p '
        if self.menuBar.getChecked('menuOptionsShell'):
            args += '-s '
        """
        return args

    def previewDialog(self):
        if self.filename is None:
            # KEA 2002-03-25
            # should probably present an error dialog here
            return

        dlg = DummyDialog(self, self.filename)
        dlg.showModal()
        dlg.destroy()

    def on_filePreviewDialog_command(self, event):
        # we should prompt to save the .rsrc.py file if needed
        # or in the case of a new file, do a save as before attempting
        # to do a preview
        self.previewDialog()

    def runScript(self, useInterpreter):
        # KEA 2004-05-08
        # auto-save code taken from codeEditor
        if self.filename is None:
            save = self.saveChanges()
            if save == "Cancel" or save == "No":
                # don't do anything, just go back to editing
                return
            else:
                if not self.on_menuFileSaveAs_select(None):
                    # they didn't actually save, just go back
                    # to editing
                    return
        elif self.documentChanged:
            # auto-save
            self.saveFile()

        if self.filename is None:
            # KEA 2002-03-25
            # should probably present an error dialog here
            return

        # this algorithm, taken from samples.py assumes the rsrc.py file and the main
        # program file have the same basename
        # if that isn't the case then this doesn't work and we need a different solution
        path, filename = os.path.split(self.filename)
        name = filename.split('.')[0]
        if os.path.exists(os.path.join(path, name + ".pyw")):
            filename = '"' + os.path.join(path, name + ".pyw") + '"'
        else:
            filename = '"' + os.path.join(path, name + ".py") + '"'
        # the args should come from a dialog or menu items that are checked/unchecked
        args = self.getCommandLineArgs()

        if useInterpreter:
            interp = ' -i '
        else:
            interp = ' '
            
        if sys.platform.startswith('win'):
            # KEA 2002-03-06
            # always launch with console in the resourceEditor for debugging purposes
            python = os.path.join(os.path.dirname(sys.executable), 'python.exe')
            if ' ' in python:
                pythonQuoted = '"' + python + '"'
            else:
                pythonQuoted = python
            if useInterpreter and os.name != 'nt':
                os.spawnv(os.P_NOWAIT, python, [pythonQuoted, interp, filename, args])
            else:
                os.spawnv(os.P_NOWAIT, python, [pythonQuoted, interp, filename, args])
        else:
            if ' ' in sys.executable:
                python = '"' + sys.executable + '"'
            else:
                python = sys.executable
            os.system(python + interp + filename + args + ' &')

    def on_fileRun_command(self, event):
        self.runScript(False)

    def on_fileRunWithInterpreter_command(self, event):
        self.runScript(True)

    def copyWidgetDescriptionsToClipboard(self, nameList):
        desc = ""
        for name in nameList:
            widget = self.components[name]
            desc += multiresourceOutput.widgetAttributes(self, widget)
        if desc.endswith(',\n'):
            desc = desc[:-2]
        clipboard.setClipboard(desc)

    def on_menuEditCut_select(self, event):
        if self.components.topLeft.visible and self.startName in self.components:
            aWidget = self.components[self.startName]
            nameList = [self.startName]
            msg = "Are you sure you want to Cut %s %s?" % (aWidget.__class__.__name__, aWidget.name)
            result = dialog.messageDialog(self, msg, 'Cut Component', 
                wx.ICON_INFORMATION | wx.YES_NO | wx.NO_DEFAULT)
        elif self.multipleSelected:
            nameList = [ x[0] for x in self.multipleComponents ]
            if len(self.multipleComponents) == 0: return
            if len(self.multipleComponents) == 1: 
                msg = "Are you sure you want to Cut this component ?"
            else:
                msg = "Are you sure you want to Cut %d components ?" % (len(self.multipleComponents))
            result = dialog.messageDialog(self, msg, 'Cut Component', 
                wx.ICON_INFORMATION | wx.YES_NO | wx.NO_DEFAULT)
        else:
            return
            
        if result.accepted:
            self.copyWidgetDescriptionsToClipboard(nameList)
            if self.multipleSelected:
                self.hideMultiSizingHandles()
            else:
                self.hideSizingHandles()
            for name in nameList:
                del self.components[name]
            self.documentChanged = True

    def on_menuEditCopy_select(self, event):
        if self.components.topLeft.visible and self.startName in self.components:
            nameList = [self.startName]
        elif self.multipleSelected:
            nameList = [ x[0] for x in self.multipleComponents ]
            if len(self.multipleComponents) == 0: return
        else:
            return
        self.copyWidgetDescriptionsToClipboard(nameList)

    def on_menuEditPaste_select(self, event):
        # need to figure out the logic of checking the contents
        # of the clipboard to see if it is something we can use
        # then checking whether the component already exists
        # if it exists, prompt for a new name
        # create the widget
        desc = clipboard.getClipboard()
        if not isinstance(desc, str):
            return
        # KEA 2004-09-10
        # the clipboard is converting newlines to returns
        # which causes eval to fail
        if wx.Platform == '__WXMAC__':
            desc = '\n'.join(desc.splitlines())
        # this is VERY dangerous so we need a better way of converting
        # the text in the clipboard to a dictionary safely
        start = 0
        while desc[start] == "{":
            end = desc[start:].find('},')
            if end < 0:
                if desc[-1] <> "}": break
                thisdesc = desc[start:]
            else:
                thisdesc = desc[start:start+end+1]

            thisdesc = eval(thisdesc)
            #print "pasting ", thisdesc['name']
            name = thisdesc['name']
            thisdesc['name'] = self.generateUniqueName(name)
            
            # AGT 2004-07-08
            # give dialog to set name
            self.create_component(thisdesc)

            if end < 0: break
            start = start+end+3
        

    def loadConfig(self):
        try:
            if not os.path.exists(self.configPath):
                os.mkdir(self.configPath)
            path = os.path.join(self.configPath, USERCONFIG)
            self.config = util.readAndEvalFile(path)
            if self.config != {}:
                if 'propertyEditorWindow.position' in self.config:
                    self.propertyEditorWindow.SetPosition(self.config['propertyEditorWindow.position'])
                if 'history' in self.config:
                    history = self.config['history']
                    history.reverse()
                    for h in history:
                        self.fileHistory.AddFileToHistory(h)
        except:
            self.config = {}

    def saveConfig(self):
        self.config['propertyEditorWindow.position'] = self.propertyEditorWindow.GetRestoredPosition()
        self.config['propertyEditorWindow.size'] = self.propertyEditorWindow.GetRestoredSize()
        history = []
        for i in range(self.fileHistory.GetCount()):
            history.append(self.fileHistory.GetHistoryFile(i))
        self.config['history'] = history
        try:
            path = os.path.join(self.configPath, USERCONFIG)
            f = open(path, "w")
            pprint.pprint(self.config, f)
            f.close()
        except:
            pass    # argh

    def doExit(self):
        if self.documentChanged:
            save = self.saveChanges()
            if save == "Cancel":
                return False
            elif save == "No":
                return True
            else:
                if self.filename is None:
                    return self.on_menuFileSaveAs_select(None)
                else:
                    return self.saveFile()
        else:
            return True

    def doCleanup(self):
        # memory leak cleanup
        for k in self.cursors:
            self.cursors[k] = None

    def on_close(self, event):
        try:
            # KEA 2004-04-08
            # if an exception occurs during on_initialize
            # then doCleanup and saveConfig could fail because some windows
            # might not exist, so in that situation just exit gracefully
            if self.doExit():
                self.saveConfig()
                self.doCleanup()
                event.skip()
        except:
            event.skip()

    def on_showPythonCardDocumentation_command(self, event):
        global pythoncard_url
        webbrowser.open(pythoncard_url)

    def on_showResourceEditorDocumentation_command(self, event):
        global resourceeditor_url
        webbrowser.open(resourceeditor_url)


if __name__ == '__main__':
    # now force the property editor to be enabled
    #configuration('showPropertyEditor', 1)
    #configuration('showShell', 1)

    app = model.Application(ResourceEditor)
    app.MainLoop()
