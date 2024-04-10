
"""
__version__ = "$Revision: 1.135 $"
__date__ = "$Date: 2005/12/25 16:40:08 $"
"""

import wx
from wx import stc
import STCStyleEditor
import about
import event
import dialog
import font
import registry
import pprint
import configuration
import os, sys
import webbrowser

from wx import py as PyCrust
from wx.py.shell import Shell
from wx.py.shell import ShellFacade
from wx.py.filling import Filling
from wx.py import introspect

TOOL_WINDOW_STYLE = wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR
PYTHONCARD_DEBUG_MENU_RESOURCE_FILE = 'debugmenu.rsrc.py'
DEBUG_MENU_REDIRECT = 'Redirect stdout to Shell'
DEBUG_MENU_ONLINE_HOME = 'PythonCard Home Page'
DEBUG_MENU_ONLINE_HELP = 'Online Documentation'

class PythonCardShellFacade(ShellFacade):
    def _getAttributeNames(self):
        names = ShellFacade._getAttributeNames(self)
        names.append('autoCompleteWxMethods')
        names.sort()
        return names


class PythonCardShell(Shell):
    def setLocalShell(self):
        """Add 'shell' to locals as reference to ShellFacade instance."""
        self.interp.locals['shell'] = PythonCardShellFacade(other=self)
        self.autoCompleteWxMethods = True

    def autoCompleteShow(self, command):
        """Display auto-completion popup list."""
        names = self.interp.getAutoCompleteList(command,
                    includeMagic=self.autoCompleteIncludeMagic,
                    includeSingle=self.autoCompleteIncludeSingle,
                    includeDouble=self.autoCompleteIncludeDouble)
        if not self.autoCompleteWxMethods:
            root = introspect.getRoot(command, terminator='.')
            try:
                # we have to use locals, right?
                #print root
                object = eval(root, self.interp.locals)
                #print object
                # only filter attribute names of wxPython objects
                if isinstance(object, wx.Object):
                    names.remove('this')
                    names.remove('thisown')
                    names = [name for name in names if name[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
            except:
                # what is the proper thing to do here?
                pass
        if names:
            options = ' '.join(names)
            offset = 0
            self.AutoCompShow(offset, options)

 
class MessageWatcher(wx.Frame, event.EventListener):
    def __init__(self, parent, ID, title, pos, size, parentApp):
        wx.Frame.__init__(self, parent, ID, title, pos, size, TOOL_WINDOW_STYLE )        
        panel = wx.Panel(self, -1)
        self.parentApp = parentApp
        wx.EVT_CLOSE(self, self.onCloseMe)
        wx.EVT_WINDOW_DESTROY(self, self.onDestroyMe)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hideTimers = wx.CheckBox(panel, -1, 'Hide timers',
                                   wx.DefaultPosition, wx.DefaultSize,
                                   wx.NO_BORDER)
        #self.hideTimers.SetValue(1)

        sizer2.Add(self.hideTimers, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        sizer2.Add((5, 5), 1)  # spacer
        self.hideUnused = wx.CheckBox(panel, -1, 'Hide unused (#)',
                                     wx.DefaultPosition, wx.DefaultSize,
                                     wx.NO_BORDER)
        # KEA 2004-04-10
        # default to showing all events
        # otherwise unused events will be missed at startup
        # self.hideUnused.SetValue(1)

        sizer2.Add(self.hideUnused, 0, wx.LEFT | wx.BOTTOM, 5)
        sizer1.Add(sizer2, 0, wx.EXPAND)

        self.maxSizeMsgHistory = 29000
        #self.maxSizeMsgHistory = 0 # Turn off

        # eventually, the font size should be settable in the user config
        self.msgHistory = stc.StyledTextCtrl(panel, -1, size=(100, 60))
        self.msgHistory.SetReadOnly(True)
        if wx.Platform == '__WXMSW__':
            self.msgHistory.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:Arial,size:9")
        else:
            self.msgHistory.StyleSetSize(stc.STC_STYLE_DEFAULT, wx.NORMAL_FONT.GetPointSize())
        # KEA 2005-12-25
        # change the lexer to Python
        # and denote unused messages as comments (e.g. #mouseUp
        self.msgHistory.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#7F7F7F")
        self.msgHistory.SetLexer(stc.STC_LEX_PYTHON)
        self.msgHistory.SetUseHorizontalScrollBar(0)
        self.msgHistory.SetMarginWidth(1,0)
        self.msgHistory.SetUndoCollection(0)

        sizer1.Add(self.msgHistory, 1, wx.EXPAND)
        sizer1.Fit(panel)
        sizer1.SetSizeHints(self)
        panel.SetSizer(sizer1)
        panel.SetAutoLayout(1)
        panel.Layout()

        # and now for a hack-fest
        if wx.Platform == '__WXMSW__':
            self.SetSize(size)

        event.EventLog.getInstance().addEventListener( self )

    def eventOccurred(self, eventAdapter):
        # new way hack to stay compatible with one arg notifyEventListeners
        eventName, sourceName, used = eventAdapter
        if eventName == event.IdleEvent.name:
            return
        
        if used:
            eventText = eventName + ' : '  + sourceName
        else:
            eventText = '# ' + eventName + ' : '  + sourceName

        # show timer events?
        if (eventName == 'timer' and self.hideTimers.GetValue()):
            return

        if used or (not self.hideUnused.GetValue()):
            self.msgHistory.SetReadOnly(False)
            if self.maxSizeMsgHistory and self.msgHistory.GetLength() > self.maxSizeMsgHistory:
                # delete many lines at once to reduce overhead
                text = self.msgHistory.GetText()
                endDel = text.index('\n', self.maxSizeMsgHistory / 10) + 1
                self.msgHistory.SetTargetStart(0)
                self.msgHistory.SetTargetEnd(endDel)
                self.msgHistory.ReplaceTarget("")
            self.msgHistory.GotoPos(self.msgHistory.GetLength())
            self.msgHistory.AddText(eventText + '\n')
            self.msgHistory.GotoPos(self.msgHistory.GetLength())
            self.msgHistory.SetReadOnly(True)

    def onCloseMe(self, evt):
        # KEA fixed showMessageWatcher in model.py
        # however, the fix probably needs more work
        self.Hide()

    def onDestroyMe(self, evt):
        # KEA 2004-05-04
        # if we're in the midst of a shutdown
        # then the Message Watcher needs to be removed from the
        # event listeners so that we don't end up trying to access
        # a dead object
        event.EventLog.getInstance().removeEventListener( self )
        evt.Skip()

    position = property(wx.Frame.GetPositionTuple, wx.Frame.SetPosition)
    size = property(wx.Frame.GetSizeTuple, wx.Frame.SetSize)
    visible = property(wx.Frame.IsShown, wx.Frame.Show)


# KEA this is a load of dingos' kidneys and needs to be rewritten
class PropertyEditor(wx.Frame, event.ChangeListener):
    def __init__(self, parent, ID, title, pos, size, parentApp ):
        wx.Frame.__init__(self, parent, ID, title, pos, size, TOOL_WINDOW_STYLE)        
        panel = wx.Panel(self, -1)
        self.parentApp = parentApp
        bg = self.parentApp.getCurrentBackground()
        bg.components.addChangeEventListener(self)


        self.checkItems = ['enabled', 'visible', 'editable', 'checked', 'default', 'rules', 'labels', 'ticks', 'horizontalScrollbar']
        self.popItems = ['layout', 'border', 'style', 'alignment', 'stringSelection']
        self.cantModify = ['id', 'name', 'alignment', 'layout', 'style', 'border', 'horizontalScrollbar', \
            'min', 'max', 'columns', 'rules', 'labels', 'ticks']

        wx.EVT_CLOSE(self, self.onCloseMe)
        wx.StaticText(panel, -1, 'Name  :  Class', wx.Point(3, 3))
        wx.StaticText(panel, -1, 'Properties', wx.Point(228, 3))
        self.wComponentList = wx.ListBox(panel, -1, wx.Point(0, 20), wx.Size(200, 100))
        self.wPropertyList = wx.ListBox(panel, -1, wx.Point(225, 20), wx.Size(125, 100))
        self.wName = wx.StaticText(panel, -1, 'name:', wx.Point(3, 135), wx.Size(90, -1), style = wx.ALIGN_RIGHT | wx.ST_NO_AUTORESIZE)
        self.wField = wx.TextCtrl(panel, -1, '', wx.Point(100, 130), wx.Size(180, -1))
        self.wColor = wx.Button(panel, -1, 'Color...', wx.Point(290, 130), wx.Size(50, -1))
        self.wColor.Show(0)
        self.wFont = wx.Button(panel, -1, 'Font...', wx.Point(290, 130), wx.Size(50, -1))
        self.wFont.Show(0)
        self.wTextArea = wx.TextCtrl(panel, -1, '', wx.Point(100, 130), wx.Size(250, 50), style = wx.TE_MULTILINE)
        self.wTextArea.Show(0)
        self.wChecked = wx.CheckBox(panel, -1, '', wx.Point(100, 132), wx.DefaultSize, wx.NO_BORDER)
        self.wChecked.Show(0)
        self.wPop = wx.Choice(panel, -1, wx.Point(100, 130), wx.DefaultSize, [])
        self.wPop.Show(0)
        self.wCopy = wx.Button(panel, -1, 'Copy resource to clipboard', wx.Point(5, 185), wx.Size(150, -1))
        self.wCopy.Show(0)        
        self.wUpdate = wx.Button(panel, -1, 'Update', wx.Point(265, 185))
        self.wUpdate.Show(0)
        self.editItems = [self.wField, self.wColor, self.wFont, self.wTextArea, self.wChecked, self.wPop]
        # KEA 2001-08-14
        # this was causing an assertion error with the hybrid wxPython
        #self.wComponentList.SetSelection(0)
        if self.wComponentList.GetStringSelection() == "":
            wClass = ""
        else:
            wName, wClass = self.wComponentList.GetStringSelection().split("  :  ")
            
        self.setValidProps(wClass)
        wx.EVT_LISTBOX(self, self.wComponentList.GetId(), self.onSelectComponentListEvent)
        wx.EVT_LISTBOX(self, self.wPropertyList.GetId(), self.onSelectPropertyListEvent)
        wx.EVT_BUTTON(self, self.wColor.GetId(), self.onSelectColor)
        wx.EVT_BUTTON(self, self.wFont.GetId(), self.onSelectFont)
        wx.EVT_BUTTON(self, self.wCopy.GetId(), self.onSelectCopy)
        wx.EVT_BUTTON(self, self.wUpdate.GetId(), self.onSelectUpdate)

        # and now for a hack-fest
        if wx.Platform == '__WXMSW__':
            self.SetSize(size)

    def addWidgetToComponentsList(self, widget):
        wName = widget.name
        wClass = widget.__class__.__name__
        self.wComponentList.Append(wName + "  :  " + wClass)

    def deleteWidgetFromComponentsList(self, wName, wClass):
        i = self.wComponentList.GetSelection()
        j = self.wComponentList.FindString(wName + "  :  " + wClass)
        if i == -1 or i != j:
            if j != -1: 
                self.wComponentList.Delete(j)
        else:
            if j > 0:
                self.wComponentList.SetSelection(j - 1)
            if j != -1:
                self.wComponentList.Delete(j)
            if self.wComponentList.GetSelection() == -1:
                self.setValidProps("")
                self.hideAllBut(self.wField)
                self.wUpdate.Show(0)
                self.wCopy.Show(0)
            else:
                wName, wClass = self.wComponentList.GetStringSelection().split("  :  ")
                # deselect the name from properties list
                self.setValidProps(wClass)
                propName = self.wPropertyList.GetStringSelection()
                if propName == "":
                    propName = "name"
                    self.wPropertyList.SetStringSelection("name")
                self.displayProperty(wName, wClass, propName)

    def selectComponentsList(self, wName, wClass):
        self.wComponentList.SetStringSelection(wName + "  :  " + wClass)
        self.setValidProps(wClass)
        propName = self.wPropertyList.GetStringSelection()
        #print propName
        if propName == "":
            propName = "name"
            self.wPropertyList.SetStringSelection("name")
        self.displayProperty(wName, wClass, propName)

    def changed(self, evt):
        comp = self.parentApp.getCurrentBackground().components
        wName, wClass = evt.getOldValue().split(",")
        if wName in comp:
            # new item added
            self.addWidgetToComponentsList(comp[wName])
        else:
            # item deleted
            self.deleteWidgetFromComponentsList(wName, wClass)

    def onSelectCopy(self, evt):
        wName, wClass = self.wComponentList.GetStringSelection().split("  :  ")
        # what needs to happen here is to have a method for the Widget class that
        # will provide a valid resource description, each subclass of widget would
        # override the method to deal with their specific resource attributes
        # the Widget class should provide some ordering so that 'type',
        # 'position', 'size' comes before less commonly used items, the actual
        # ordering could just be defined in a list, so it is easy to change
        # also, if the current values match the defaults for a widget attribute
        # then that attribute should not be provided as part of the output
        print "this is just a placeholder method right now,"
        print "the resource is not actually copied to the clipboard yet"
        pprint.pprint(self.parentApp.getCurrentBackground().components[wName])

    # KEA 2002-08-22
    # this should be updated to match the resourceEditor Property Editor
    # or the Property Editor code should be changed so that the same module
    # could be used at runtime?
    def onSelectUpdate(self, evt):
        wName, wClass = self.wComponentList.GetStringSelection().split("  :  ")
        propName = self.wPropertyList.GetStringSelection()

        if propName not in self.cantModify:
            if propName in self.checkItems:
                value = self.wChecked.GetValue()
            elif propName in self.popItems:
                value = self.wPop.GetStringSelection()
            elif wClass == 'TextArea' and propName == 'text':
                value = self.wTextArea.GetValue()
            else:
                value = self.wField.GetValue()

        if propName not in ['label', 'text', 'toolTip']:
            try:
                value = eval(value)
            except:
                pass

        widget = self.parentApp.getCurrentBackground().components[wName]

        if propName == 'size':
            width, height = value
            if wClass not in ['BitmapCanvas', 'HtmlWindow']:
                bestWidth, bestHeight = widget.GetBestSize()
                if width == -1:
                    width = bestWidth
                if height == -1:
                    height = bestHeight
            widget.size = (width, height)
        else:
            setattr(widget, propName, value)

    def onSelectColor(self, evt):
        result = dialog.colorDialog(self)
        if result.accepted:
            self.wField.SetValue(str(result.color))

    def onSelectFont(self, evt):
        wName, wClass = self.wComponentList.GetStringSelection().split("  :  ")
        widget = self.parentApp.getCurrentBackground().components[wName]
        f = widget.font
        if f is None:
            desc = font.fontDescription(widget.GetFont())
            f = font.Font(desc)
        result = dialog.fontDialog(self, f)
        if result.accepted:
            #color = dlg.getColor()
            f = result.font
            self.wField.SetValue("%s" % f)

    def setValidProps(self, wClass):
        oldProp = self.wPropertyList.GetStringSelection()
        if wClass == "":
            self.wPropertyList.Clear()
        else:
            klass = registry.Registry.getInstance().getComponentClass(wClass)
            props = klass._spec.getAttributes().keys()
            props.sort()
            self.wPropertyList.Clear()
            self.wPropertyList.InsertItems(props, 0)
            if oldProp in props:
                self.wPropertyList.SetStringSelection(oldProp)

    def hideAllBut(self, widget):
        for w in self.editItems:
            if widget.GetId() != w.GetId():
                w.Show(0)

    def displayProperty(self, wName, wClass, propName):
        self.wName.SetLabel(propName + ":")
        widget = self.parentApp.getCurrentBackground().components[wName]
        if propName in ['label', 'text', 'toolTip'] or propName in self.checkItems:
            value = getattr(widget, propName)
        else:
            value = str(getattr(widget, propName))
        
        if propName in self.checkItems:
            self.hideAllBut(self.wChecked)
            self.wChecked.Show(1)
            self.wChecked.SetValue(int(value))
        elif propName in self.popItems:
            self.hideAllBut(self.wPop)
            self.wPop.Show(1)
            self.wPop.Clear()
            for v in widget._spec.getAttributes()[propName].values:
                self.wPop.Append(v)
            self.wPop.SetStringSelection(value)
        elif wClass == 'TextArea' and propName == 'text':
            self.hideAllBut(self.wTextArea)
            self.wTextArea.Show(1)
            self.wTextArea.SetValue(value)
        else:
            self.hideAllBut(self.wField)
            self.wField.Show(1)
            if propName == 'foregroundColor' or propName == 'backgroundColor':
                self.wColor.Show(1)
            elif propName == 'font':
                self.wFont.Show(1)
            self.wName.SetLabel(propName + ":")

            if propName == 'size':
                width, height = getattr(widget, propName)
                if wClass not in ['BitmapCanvas', 'HtmlWindow']:
                    bestWidth, bestHeight = widget.GetBestSize()
                    if width == bestWidth:
                        width = -1
                    if height == bestHeight:
                        height = -1
                size = (width, height)
                value = str(size)

            self.wField.SetValue(value)
        # this should only display if the attribute is settable
        # so name, alignment, and others are read-only
        self.wUpdate.Show((propName not in self.cantModify) and not (propName == 'items' and wClass == 'RadioGroup'))

    def onSelectComponentListEvent(self, evt):
        wName, wClass = evt.GetString().split("  :  ")
        # change the wPropertiesList to only show relevant properties
        # either display the name by default or try and preserve the
        # wPropertiesList selection and display that item, so for example
        # you could look at size for all widgets, simply by going up and down
        # the components list
        self.setValidProps(wClass)
        propName = self.wPropertyList.GetStringSelection()
        if propName == "":
            propName = "name"
            self.wPropertyList.SetStringSelection("name")
        self.displayProperty(wName, wClass, propName)

    def onSelectPropertyListEvent(self, evt):
        propName = evt.GetString()
        wName, wClass = self.wComponentList.GetStringSelection().split("  :  ")
        if wName != "":
            self.displayProperty(wName, wClass, propName)

    def clearComponentsList(self):
        self.wComponentList.Clear()

    def displayComponents(self, components):
        for c in components.order:
            self.addWidgetToComponentsList(components[c])

    def onCloseMe(self, evt):
        self.Show(0)

    position = property(wx.Frame.GetPositionTuple, wx.Frame.SetPosition)
    size = property(wx.Frame.GetSizeTuple, wx.Frame.SetSize)
    visible = property(wx.Frame.IsShown, wx.Frame.Show)


class PyCrustFrame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, parentApp):
        wx.Frame.__init__(self, parent, ID, title, pos, size, TOOL_WINDOW_STYLE )
        parentApp.shell = PythonCardShell(self, -1)

        configfile = configuration.getStyleConfigPath()
        if os.path.exists(configfile):
            STCStyleEditor.initSTC(parentApp.shell, configfile, 'python')

        # KEA this is temporary until we decide what reference
        # we want here
        parentApp.shell.interp.locals['pcapp'] = parentApp
        self.parentApp = parentApp

        wx.EVT_CLOSE(self, self.onCloseMe)

        # and now for a hack-fest
        if wx.Platform == '__WXMSW__':
            self.SetSize(size)

    def onCloseMe(self, evt):
        self.Show(0)

    position = property(wx.Frame.GetPositionTuple, wx.Frame.SetPosition)
    size = property(wx.Frame.GetSizeTuple, wx.Frame.SetSize)
    visible = property(wx.Frame.IsShown, wx.Frame.Show)


class PyCrustNamespaceFrame(wx.Frame):
    def __init__(self, parent, ID, title, pos, size, parentApp):
        wx.Frame.__init__(self, parent, ID, title, pos, size, TOOL_WINDOW_STYLE)

        parentApp.namespace = PyCrust.filling.Filling(parent = self, \
                                      rootObject = parentApp.shell.interp.locals, \
                                      rootLabel = 'Shell Namespace',
                                      rootIsNamespace = 1)
        self.parentApp = parentApp
        wx.EVT_CLOSE(self, self.onCloseMe)
        
        # and now for a hack-fest
        if wx.Platform == '__WXMSW__':
            self.SetSize(size)

    def onCloseMe(self, evt):
        self.Show(0)

    position = property(wx.Frame.GetPositionTuple, wx.Frame.SetPosition)
    size = property(wx.Frame.GetSizeTuple, wx.Frame.SetSize)
    visible = property(wx.Frame.IsShown, wx.Frame.Show)


def raiseAndShow(window):
    if window.IsIconized():
        window.Iconize(False)
    window.Show()
    window.Raise()

class DebugMenu:

    def __init__(self, parentApp):
        self.parentApp = parentApp
        self.menuIds = {DEBUG_MENU_REDIRECT:wx.NewId(),
                        DEBUG_MENU_ONLINE_HELP:wx.NewId(), 
                        DEBUG_MENU_ONLINE_HOME:wx.NewId()}
        # decided not to use a resource in order to avoid getting the Debug
        # menu caught up in the PythonCard event model
        #basePath = os.path.dirname(os.path.abspath( __file__))
        #path = os.path.join(basePath, PYTHONCARD_DEBUG_MENU_RESOURCE_FILE)
        #self._resource = ResourceFile(path).getResource()

    def createMenu(self, bg):
        menu = wx.Menu()
        menu.Append(wx.NewId(), '&Message Watcher')
        menu.Append(wx.NewId(), '&Namespace Viewer')
        menu.Append(wx.NewId(), '&Property Editor')
        menu.Append(wx.NewId(), '&Shell')
        menu.AppendSeparator()
        id = self.menuIds[DEBUG_MENU_REDIRECT]
        #menu.Append(id, "&" + DEBUG_MENU_REDIRECT, checkable = 1)
        menu.Append(id, "&" + DEBUG_MENU_REDIRECT, "", 1)
        # if we want to have a config option set redirect, this is the
        # place to do it
        menu.Append(wx.NewId(), 'Save &Configuration')
        menu.AppendSeparator()
        id = self.menuIds[DEBUG_MENU_ONLINE_HOME]
        menu.Append(wx.NewId(), DEBUG_MENU_ONLINE_HOME)
        id = self.menuIds[DEBUG_MENU_ONLINE_HELP]
        menu.Append(wx.NewId(), DEBUG_MENU_ONLINE_HELP)
        menu.AppendSeparator()
        menu.Append(wx.NewId(), '&About PythonCard...')
        
        menubar = bg.GetMenuBar()
        if menubar is None:
            menubar = wx.MenuBar()
            bg.SetMenuBar(menubar)
        menubar.Append(menu, 'Debug')

    def bindMenuEvents(self, bg):
        # it appears that at the time bindMenuEvent and createMenu are
        # called from Background, the _iterator doesn't exist yet?!
        # so I had to pass in the current background
        menubar = bg.GetMenuBar()
        id = menubar.FindMenuItem('Debug', 'About PythonCard...')
        wx.EVT_MENU(bg, id, self.doAboutPythonCard)
        id = menubar.FindMenuItem('Debug', 'Message Watcher')
        wx.EVT_MENU(bg, id, self.toggleMessageWatcher)
        id = menubar.FindMenuItem('Debug', 'Namespace Viewer')
        wx.EVT_MENU(bg, id, self.toggleNamespaceViewer)
        id = menubar.FindMenuItem('Debug', 'Property Editor')
        wx.EVT_MENU(bg, id, self.togglePropertyEditor)
        id = menubar.FindMenuItem('Debug', 'Shell')
        wx.EVT_MENU(bg, id, self.toggleShell)
        id = menubar.FindMenuItem('Debug', DEBUG_MENU_REDIRECT)
        wx.EVT_MENU(bg, id, self.toggleShellRedirect)
        id = menubar.FindMenuItem('Debug', 'Save Configuration')
        wx.EVT_MENU(bg, id, self.doSaveUserConfiguration)
        id = menubar.FindMenuItem('Debug', DEBUG_MENU_ONLINE_HOME)
        wx.EVT_MENU(bg, id, self.onlineHomePage)
        id = menubar.FindMenuItem('Debug', DEBUG_MENU_ONLINE_HELP)
        wx.EVT_MENU(bg, id, self.onlineDocumentation)

    def toggleMessageWatcher(self, evt):
        raiseAndShow(self.parentApp.mw)

    def toggleNamespaceViewer(self, evt):
        raiseAndShow(self.parentApp.namespaceFrame)

    def togglePropertyEditor(self, evt):
        raiseAndShow(self.parentApp.pw)

    def toggleShell(self, evt):
        raiseAndShow(self.parentApp.shellFrame)

    def toggleShellRedirect(self, evt):
        menubar = self.parentApp.getCurrentBackground().GetMenuBar()
        #id = menubar.FindMenuItem('Debug', 'Redirect stdout to Shell')
        id = self.menuIds[DEBUG_MENU_REDIRECT]
        # I don't know why, but this appears to be returning the opposite
        # of what it should return, so if IsChecked returns 1 (true) the
        # menu item isn't really checked
        checked = menubar.IsChecked(id)
        #print id, menubar.GetLabel(id), checked
        menubar.Check(id, checked)
        self.parentApp.shell.redirectStdout(checked)

    def doSaveUserConfiguration(self, evt):
        configuration.saveUserConfiguration(self.parentApp)

    def onlineHomePage(self, evt):
        url = 'http://pythoncard.sourceforge.net/'
        webbrowser.open(url, 1, 1) 

    def onlineDocumentation(self, evt):
        url = 'http://pythoncard.sourceforge.net/documentation.html'
        webbrowser.open(url, 1, 1) 

    # the references to self will have to be modified depending on where this
    # method ends up going. we do need a parent for the dialog
    def doAboutPythonCard(self, evt):
        about.aboutPythonCardDialog(self.parentApp.getCurrentBackground())
