
"""
__version__ = "$Revision: 1.197 $"
__date__ = "$Date: 2006/01/13 23:33:37 $"
"""

import os, sys

# KEA 2004-08-09
# assert some minimum requirements and attempt to exit cleanly
# if they aren't met

try:
    # some things might work with lesser
    # versions, but this is a reasonable base
    assert sys.version_info >= (2, 3)
    # sys.modules relative path fix
    sys.path[0] = os.path.abspath(sys.path[0])
    #sys.path = [os.path.abspath(p) for p in sys.path]
    
    import wx
    assert wx.VERSION >= (2, 5, 2, 8)
except AssertionError:
    from wxPython.wx import wxPySimpleApp, wxFrame, wxMessageDialog, wxICON_EXCLAMATION, wxOK, wxVERSION_STRING
    app = wxPySimpleApp()
    frame = wxFrame(None, -1, "Minimum Requirements Not Met")
    #frame.Show(1)
    message = "PythonCard minimum requirements:\nPython 2.3 and wxPython 2.5.2.8\n\n" + \
        "You are using Python %s\nand wxPython %s.\n\nClick OK to exit." % (sys.version, wxVERSION_STRING)
    dialog = wxMessageDialog(frame, message,
                            "Minimum Requirements Not Met", 
                            wxICON_EXCLAMATION | wxOK)
    dialog.ShowModal()
    dialog.Destroy()
    #app.MainLoop()
    sys.exit(0)



import configuration
import log
import event
import resource
import widget
import menu
import statusbar
import debug
import component
import util
import dialog

import types
import UserDict
import new
import locale
import inspect

# KEA 2001-07-27
from wx.lib import colourdb

class WidgetDict(UserDict.UserDict, event.Changeable):
    def __init__(self, parent, d=None):
        self.__dict__['parent'] = parent
        self.__dict__['data'] = {}
        self.__dict__['order'] = []
        if d is not None: self.update(d)
        event.Changeable.__init__(self)

    # __getattr__ and __setattr__ need to be cleaned up
    # to support more attributes
    def __getattr__(self, key):
        if key == '_listeners':
            return self.__dict__[key]
        elif key == 'order':
            pass
        else:
            return self.data[key]

    def __setattr__(self, key, item):
        if key == '_listeners':
            self.__dict__[key] = item
        elif key == 'order':
            pass
        else:
            self.__setitem__(key, item)

    """
    def __delattr__(self, key):
        if key == '_listeners':
            pass
        else:
            self.__delitem__(key)
    """

    def __setitem__(self, key, item):
        if isinstance(item, dict):
            item = resource.Resource(item)
        control = component.ComponentFactory().createComponent(self.parent, self.parent.panel, item)
        if key in self.data:
            self.order.remove(key)
        self.order.append(key)
        self.data[key] = control
        # notify listeners
        self.fireChanged(key + "," + control.__class__.__name__)

    def __delitem__(self, key):
        control = self.data[key]
        # KEA 2002-05-20
        # hack for 2.3.3 focus problem?
        visible = control.visible
        control.Show(0)
        wClass = control.__class__.__name__
        focusWin = wx.Window_FindFocus()
        if focusWin is not None and focusWin == control:
            #print "disconnecting wx.wxEVT_KILL_FOCUS", control.name
            focusWin.Disconnect(-1, -1, wx.wxEVT_KILL_FOCUS) 
        if self.data[key].Destroy():
            self.order.remove(key)
            del self.data[key]
            self.fireChanged(key + "," + wClass)
        else:
            # why would Destroy fail?
            # if it does fail we have
            # a problem since we disconnected wx.wxEVT_KILL_FOCUS
            print "destroy failed", control
            control.Show(visible)

    def clear(self):
        for key in self.data.keys():
            self.__delitem__(key)

    def _getAttributeNames(self):
        return self.data.keys()


# KEA 2005-03-30
# revised to support platform-specific resource files
def internationalResourceName(base):
    postfix = ".rsrc.py"
    # build up a list of possible filenames
    # in order of preference and use the first one that exists
    filenames = [base + postfix]
    
    if wx.Platform == '__WXMSW__':
        platform = 'win'
    elif wx.Platform == '__WXGTK__':
        platform = 'gtk'
    elif wx.Platform == '__WXMAC__':
        platform = 'mac'
    else:
        platform = None
    if platform:
        filenames.insert(0, base + '.' + platform + postfix)
        
    try:
        default = locale.getdefaultlocale()
    except:
        default = None
    log.debug('default: ' + str(default))
    
    if default and default[0] is not None:
        language, country = default[0].split('_')
        log.debug(language + ' ' + country)
        # languageOnlyName
        filenames.insert(0, base + '.' + language + postfix)
        # languageCountryName
        filenames.insert(0, base + '.' + language + '_' + country + postfix)
        # now with platform specified as well
        if platform:
            filenames.insert(0, base + '.' + platform + '.' + language + postfix)
            filenames.insert(0, base + '.' + platform + '.' + language + '_' + country + postfix)
        
    log.debug(filenames)
    # AGT 2005-05-17 Detect missing resource file, give some warning; no clean recovery possible.
    filename = None
    for f in filenames:
        if os.path.exists(f):
            filename = f
            break
    if not filename:
        print "no resource file for", base
    return filename


# KEA 2002-09-09
# this is derived from the frame loading in
# Application below
def childWindow(parent, frameClass, filename=None, rsrc=None):
    if filename is None:
        if rsrc is None:
            if util.main_is_frozen():
                # KEA 2004-05-20
                # running standalone
                # need to support py2exe differently than bundlebuilder and mcmillan probably
                # but this is the py2exe 0.5 way
                # figure out the .rsrc.py filename based on the module name stored in library.zip
                filename = os.path.split(sys.modules[frameClass.__module__].__file__)[1]
                # KEA 2004-09-14
                # it seems sort of dumb to duplicate this function
                # just to handle the parent differently
                # so I'm adding this check
                if isinstance(parent, wx.Notebook):
                    parentFrame = parent.GetParent().GetParent()
                    filename = os.path.join(parentFrame.application.applicationDirectory, filename)
                else:
                    filename = os.path.join(parent.application.applicationDirectory, filename)
            else:
                # figure out the .rsrc.py filename based on the module name
                filename = sys.modules[frameClass.__module__].__file__
            # chop the .pyc or .pyo from the end
            base, ext = os.path.splitext(filename)
            filename = internationalResourceName(base)
            rsrc = resource.ResourceFile(filename).getResource()
        elif isinstance(rsrc, dict):
            rsrc = resource.Resource(rsrc)
    else:
        rsrc = resource.ResourceFile(filename).getResource()
    return frameClass(parent, rsrc.application.backgrounds[0])


# KEA 2002-02-25
# custom event for running a pycrustrc.py file
# after openBackground event
wxEVT_RUN_PYCRUSTRC = wx.NewEventType()

def EVT_RUN_PYCRUSTRC(win, func):
    win.Connect(-1, -1, wxEVT_RUN_PYCRUSTRC, func)

class wxRunPycrustrcEvent(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(wxEVT_RUN_PYCRUSTRC)

# KEA 2004-04-08
# custom event for hooking up the background events
# after openBackground event
# this means the initial idle, move, size, and activate events
# will not be available to PythonCard user code
wxEVT_LATENT_BACKGROUNDBIND = wx.NewEventType()

def EVT_LATENT_BACKGROUNDBIND(win, func):
    win.Connect(-1, -1, wxEVT_LATENT_BACKGROUNDBIND, func)

class wxLatentBackgroundBindEvent(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(wxEVT_LATENT_BACKGROUNDBIND)

# background events

class ActivateEvent(event.Event, event.InsteadOfTypeEvent):
    name = 'activate'
    binding = wx.EVT_ACTIVATE
    id = wx.wxEVT_ACTIVATE

    def translateEventType(self, aWxEvent):
        if aWxEvent.GetActive():
            return self.id
        else:
            return DeactivateEvent.id

class DeactivateEvent(ActivateEvent):
    name = 'deactivate'
    id = wx.NewEventType()

class CloseEvent(event.Event):
    name = 'close'
    binding = wx.EVT_CLOSE
    id = wx.wxEVT_CLOSE_WINDOW

class MaximizeEvent(event.Event):
    name = 'maximize'
    binding = wx.EVT_MAXIMIZE
    id = wx.wxEVT_MAXIMIZE

    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        aWxEvent.maximized = aWxEvent.target.IsMaximized()
        return aWxEvent

class MinimizeEvent(event.Event, event.InsteadOfTypeEvent):
    name = 'minimize'
    binding = wx.EVT_ICONIZE
    id = wx.wxEVT_ICONIZE

    def translateEventType(self, aWxEvent):
        if aWxEvent.Iconized():
            return self.id
        else:
            return RestoreEvent.id

class RestoreEvent(MinimizeEvent):
    name = 'restore'
    id = wx.NewEventType()

class MoveEvent(event.Event):
    name = 'move'
    binding = wx.EVT_MOVE
    id = wx.wxEVT_MOVE

    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        aWxEvent.position = tuple(aWxEvent.GetPosition())
        return aWxEvent

class SizeEvent(event.Event):
    name = 'size'
    binding = wx.EVT_SIZE
    id = wx.wxEVT_SIZE

    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        aWxEvent.size = tuple(aWxEvent.GetSize())
        return aWxEvent

BackgroundEvents = (
    ActivateEvent,
    CloseEvent,
    DeactivateEvent,
    event.IdleEvent,
    MaximizeEvent,
    MinimizeEvent,
    MoveEvent,
    RestoreEvent,
    SizeEvent,
)


class Application(wx.App):
    """
    The runtime environment for PythonCard Stacks.
    """

    def __init__(self, frameClass, aFileName=None, rsrc=None):
        configuration.configOptions()
        showProperties = configuration.getOption('showPropertyEditor')
        showMessages = configuration.getOption('showMessageWatcher')
        enableLogging = configuration.getOption('enableLogging')
        showShell = configuration.getOption('showShell')
        showNamespace = configuration.getOption('showNamespace')
        showDebugMenu = configuration.getOption('showDebugMenu')

        if enableLogging:
            log.enable()

        # KEA save the current directory just in case
        self.startingDirectory = os.getcwd()
        # KEA 2004-04-13
        # was this just for debugging?
        # print os.getcwd()
        # RDS - Need to get the absolute pathname of aFileName before
        # getting the directory name .
        # keep track of the path to prefix with
        self.applicationDirectory = util.dirname(os.path.abspath(sys.argv[0]))
        # always run in the app's directory
        os.chdir(self.applicationDirectory)

        if aFileName is None:
            if rsrc is None:
                filename = os.path.split(sys.argv[0])[-1]
                base, ext = os.path.splitext(filename)
                aFileName = internationalResourceName(base)

                # Load the user-defined resource file, 
                # validating it against spec.py
                self.resource = resource.ResourceFile(aFileName).getResource()
            else:
                if isinstance(rsrc, dict):
                    rsrc = resource.Resource(rsrc)
                self.resource = rsrc
        else:
            # Load the user-defined resource file, 
            # validating it against spec.py
            self.resource = resource.ResourceFile(aFileName).getResource()

        self.frameClass = frameClass
        self.pw = None
        self.mw = None
        self.shellFrame = None
        self.shell = None
        self.namespaceFrame = None
        self.namespace = None
        # KEA 2001-08-11
        # if any of the debug windows are going to be used then
        # we will have a debug menu and all the windows will be available
        # but only the ones requested at startup will be visible initially
        # this seems like a nice compromise, but we can change the behavior
        # if it seems strange
        self._showDebugMenu = showProperties or showMessages or showShell or showNamespace or showDebugMenu
        # KEA 2004-01-02
        # moved colourdb initialization to work with wxPython 2.5
        # which requires a wxApp instance to exist before using colourdb
        wx.InitAllImageHandlers()
        wx.App.__init__(self, 0)
        colourdb.updateColourDB()

    def showPropertyEditor(self):
        bg = self.getCurrentBackground()
        position = configuration.getOption('propertyEditorPosition')
        size = configuration.getOption('propertyEditorSize')
        self.pw = debug.PropertyEditor(bg, -1, "Property Editor",
                          position, size,
                          parentApp=self)
        self.pw.displayComponents(bg.components)
        self.pw.Show(configuration.getOption('showPropertyEditor'))

    def showMessageWatcher(self):
        bg = self.getCurrentBackground()
        position = configuration.getOption('messageWatcherPosition')
        size = configuration.getOption('messageWatcherSize')
        self.mw = debug.MessageWatcher(bg, -1, "Message Watcher",
                          position, size,
                          parentApp=self)
        self.mw.Show(configuration.getOption('showMessageWatcher'))

    def showShell(self):
        bg = self.getCurrentBackground()
        position = configuration.getOption('shellPosition')
        size = configuration.getOption('shellSize')
        self.shellFrame = debug.PyCrustFrame(bg, -1, 'Shell',
                                             position, size,
                                             parentApp=self)
        self.shellFrame.Show(configuration.getOption('showShell'))
        EVT_RUN_PYCRUSTRC(self, self.OnRunPycrustrc)
        wx.PostEvent(self, wxRunPycrustrcEvent())


    def showNamespace(self):
        bg = self.getCurrentBackground()
        position = configuration.getOption('namespacePosition')
        size = configuration.getOption('namespaceSize')
        self.namespaceFrame = debug.PyCrustNamespaceFrame(bg, -1, 'Namespace Viewer',
                                             position, size,
                                             parentApp=self)
        self.namespaceFrame.Show(configuration.getOption('showNamespace'))

    def _initBackgrounds(self, aResource):
        for bgRsrc in aResource.application.backgrounds:            
            bg = self.frameClass(None, bgRsrc)
            self.backgrounds.append(bg)

    # wxWindows calls this method to initialize the application
    def OnInit(self):
        log.debug('Initializing Background...')
        self.backgrounds = []
        self._initBackgrounds(self.resource)

        if self._showDebugMenu:
            self.showPropertyEditor()
            self.showMessageWatcher()
            self.showShell()        # KEA pyCrust support
            self.showNamespace()    # KEA pyCrust support
        return True

    def getCurrentBackground(self):
        return self.backgrounds[0]

    # RDS - new API
    def getWindows( self ) :
        return [ self.getCurrentBackground() ]

    def OnRunPycrustrc(self, evt):
        #print "OnRunPycrustrc", self.shell
        if self.shell is not None:
            path = os.path.dirname(__file__)
            filename = os.path.join(path, 'pycrustrc.py')
            if os.path.exists(filename):
                try:
                    self.shell.runfile(filename)
                except:
                    pass

            # we will have already changed into the running module
            # directory, so this should be okay
            filename = os.path.join(self.applicationDirectory, 'pycrustrc.py')
            if os.path.exists(filename):
                try:
                    self.shell.runfile(filename)
                except:
                    pass

class Scriptable:
    """
    All classes that may contain PythonCard Handler definitions
    must implement Scriptable.

    A Scriptable object may be specified as the parent of
    this object.  The parent will be searched for Handlers
    if a Handler can't be found in this object.
    """

    def __init__(self, aScriptableParent):
        self._parentScript = aScriptableParent
        self._handlers = {}
        self._parseHandlers()
        if False:
            print "Scriptable init", self._handlers.keys()

    def _parseHandlers(self):
        """
        Find all of the methods in this object that are
        PythonCard handlers, and register them.
        """

        # KEA 2004-03-05
        # an even slicker way of finding event handlers
        # using the inspect module
        pythoncardMethods = []
        # KEA 2004-05-09
        # if we use bound methods then we'll have to change the
        # initialization order so that Scriptable.__init__
        # is done after the object is actually created
        # all _dispatch methods have to be updated to use bound
        # methods if this is changed
        methods = inspect.getmembers(self.__class__, inspect.ismethod)
##        # use bound methods instead of the class unbound methods
##        methods = inspect.getmembers(self, inspect.ismethod)
        for m in methods:
            if m[0].split('_')[0] == 'on':
                pythoncardMethods.append(m[1])

        map(self._addHandler, pythoncardMethods)

    def isPythonCardHandler(self, aObject):
        """
        Return true if the object is a PythonCard handler.
        """
        return isinstance(aObject, types.FunctionType) and aObject.__name__.split('_')[0] == 'on'
    
    def _addHandler(self, aMethod):
        # Add the Handler to our Handler list.
        if aMethod.__name__ not in self._handlers:
            log.debug("_addHandler: " + aMethod.__name__)
            #self._handlers[aMethod.__name__] = event.Handler(aMethod)
            self._handlers[aMethod.__name__] = aMethod

    def addMethod(self, aFunction):
        if isinstance(aFunction, types.FunctionType):
            if self.isPythonCardHandler(aFunction) :
                #aMethod = new.instancemethod(aFunction, self, self.__class__)
                aMethod = new.instancemethod(aFunction, None, self.__class__)
                #print aFunction
                #print self.__class__
                #print aMethod.__name__
                #print aMethod
                setattr(self.__class__, aMethod.__name__, aMethod)
                # now add the method info to our handler lookup dictionary
                # KEA 2001-11-29 simplified _addHandler
                #handler = event.Handler(aMethod.__name__, aMethod)
                #self._addHandler(aMethod.__name__, handler)
                self._addHandler(aMethod)
                
                # KEA 2004-05-13
                # will need to call _bindEvents here to make sure the event handler
                # is bound to the right component instances
                # trying to figure out all the components as well as the reverse mapping
                # from an event name like mouseDown to event.MouseDownEvent is tricky
                # at best so we'll probably need to have user-code make explicit calls
                # to _bindEvents for each component they want to bind
                # the name to event class mapping can be found by iterativing over the
                # events defined in the spec for a given component to find a name match
                # maybe just calling _bindEvents with a full list of relevant events
                # would work, since the boundEvents list will prevent double-binding 
        
    def findHandler(self, aString):
        """
        Look for a Handler that matches aString in our 
        list of Handlers.  If a Handler is not found,
        ask our parent script to look for the Handler, 
        continuing up the Scriptable hierarchy until
        either a Handler is found, or None is returned.
        """
        # KEA 2004-04-26
        # findHandler is actually called for each event dispatch
        # depending on the level of dynamic code we think we're going
        # to have it might be simpler to just statically bind when
        # the component is created
        if False:
            print "findHandler", aString, self
        handler = self._handlers.get(aString, None)

        if handler:
            return handler

        # We couldn't find a handler, so look in our parent.

        if self._parentScript:
            handler = self._parentScript.findHandler( aString )
        
        # have we found a Handler yet?

        if handler:
            return handler
        

        # Change the handler name to target this Scriptable object
        # and look in our list of Handlers.

        words = aString.split('_')
        #print words, self._getName()
        #if len(words) == 2:
        #    print words
        #    aString = words[ 0 ] + '_' + words[ 1 ]
        #else:
        aString = words[0] + '_' + self.getName() + '_' + words[len(words) - 1]
        temp = self._handlers.get(aString, None)
        if temp:
            return temp
        else:
            # search for Background and Stack handlers like
            # on_mouseClick, on_initialize
            aString = words[0] + '_' + words[len(words) - 1]
            return self._handlers.get(aString, None)


class Background(Scriptable, wx.Frame, event.EventSource):
    """
    A window that contains Widgets.
    """

    def __init__(self, aParent, aBgRsrc):
        """
        Initialize this instance.
        """
        Scriptable.__init__(self, None)
        event.EventSource.__init__(self)
        self.id = wx.NewId()
        self.resource = aBgRsrc
        # KEA 2005-12-29
        # this is a hack to make sure the background has a defined spec
        # attribute for documentation purposes, but the spec should be defined
        # just like we do for components
        # Also need to verify that the currently defined component specs are 
        # being used to enforce the attributes when loading a resource and not
        # just using the default defined in spec.py
        self._spec = aBgRsrc._spec.getEntry('Background')
        self.application = wx.GetApp()
        self.setName(aBgRsrc.name)
        self.setImage(aBgRsrc.image)
        self.setTiled(aBgRsrc.tiled)
        self.components = WidgetDict(self)
        self.menuBar = None
        self.statusBar = None

        # override for application defined position
        position = configuration.getOption('defaultBackgroundPosition')
        if position is None:
            position = aBgRsrc.position

        # KEA 2004-01-18
        # have to explicitly declare the close box in wxPython 2.5
        if aBgRsrc.style == []:
            style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        elif aBgRsrc.style == ['resizeable']:
            style = wx.DEFAULT_FRAME_STYLE
        else:
            style = 0
            for i in aBgRsrc.style:
                try:             # intended to catch all errors !
                    style |= eval(i)
                except:
                    pass

        # First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, aParent,
                            self.id, 
                            #self.name,
                            aBgRsrc.title,
                            position,
                            aBgRsrc.size,
                            style | wx.NO_FULL_REPAINT_ON_RESIZE,
                            aBgRsrc.name)

        # KEA 2004-09-24
        # experiment to see if initialize event will
        # fire before all other events
        # also see change to wx.CallAfter in textfield, passwordfield, and textarea
        evt = wx.PyEvent()
        # this is sort of pointless, the target is always self
        # do any samples or tool refer to the target?
        evt.target = self
        wx.CallAfter(self.on_initialize, evt)
        # also changing how other background events are hooked up
        wx.CallAfter(self.OnLatentBackgroundBind, None)

        self._initLayout(aBgRsrc.components)

        # KEA 2001-08-13
        # can't set the colors until after the panel
        # has been created. this initialization should probably work differently
        self._setForegroundColor(aBgRsrc.foregroundColor)
        self._setBackgroundColor(aBgRsrc.backgroundColor)

        self._createMenus(aBgRsrc)
        self._createStatusBar(aBgRsrc)

        # AJT 20.11.2001
        # Add icon creation
        self._setIcon(aBgRsrc)

        # 2001-11-08
        # hack to preserve the statusbar text
        if self.statusBar is not None and self.menuBar is not None:
            wx.EVT_MENU_HIGHLIGHT_ALL(self, self.menuHighlight)

        if aParent is None:
            self.application.SetTopWindow(self)

        # KEA 2002-04-26
        # allow background window to remain hidden 
        if aBgRsrc.visible:
            self.Show(True)

        # RDS 2004-04-14
        # Post the Background initialization event.

##        self.EVT_OPEN_BACKGROUND_TYPE = wx.NewEventType()
##        self.id = wx.NewId()
##        self.Connect(self.GetId(), -1, 
##                     self.EVT_OPEN_BACKGROUND_TYPE, 
##                     self.on_initialize)
##                     #self._dispatchOpenBackground )
##        evt = wx.PyCommandEvent(self.EVT_OPEN_BACKGROUND_TYPE, self.GetId())
##        evt.target = self
##        wx.PostEvent(self, evt)
##        EVT_LATENT_BACKGROUNDBIND(self, self.OnLatentBackgroundBind)
##        wx.PostEvent(self, wxLatentBackgroundBindEvent())
##        # for some reason the Message Watcher isn't a listener yet
##        # so calling EventLog doesn't do anything
##        #event.EventLog.getInstance().log('initialize', self.name, True)


        self._bindWindowEvents()


    def on_initialize(self, evt):
        # override in subclass
        pass

    def on_close(self, evt):
        # override in subclass
        evt.Skip()

    def singleItemExpandingSizerLayout(self):
        """Convenience method for backgrounds with only a 
        single component on the background where the component
        should expand with the background as in an editor.
        
        Call from within the on_initialize event handler."""
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        name = self.components.order[0]
        self.sizer.Add(self.components[name], True, wx.EXPAND)
        self.sizer.Fit(self)
        self.sizer.SetSizeHints(self)
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()

    # KEA 2004-09-24
    # experiment to see if we could fit the panel
    # to the boundaries of the components with a little
    # padding to get around the problem of a static layout
    # having too much vertical space on GTK and Mac or not
    # enough vertical space on Windows if the layout was designed
    # for GTK or Mac...
    # the idea is that this would become an option in the resource
    # that could be called automatically
    # but I'm just testing now to see if it actually produces good results
    def fitToComponents(self, widthPadding=None, heightPadding=5):
        print "self.size:", self.size
        print "self.panel.size:", self.panel.size
        width = 0
        height = 0
        # height = self.panel.size
        for c in self.components.itervalues():
            print " ", c.name, c.position, c.size
            x, y = c.position
            w, h = c.size
            width = max(x + w, width)
            height = max(y + h, height)
        print "width, height", width, height
        newWidth, newHeight = self.panel.size
        if widthPadding is not None:
            newWidth = width + widthPadding
        if heightPadding is not None:
            newHeight = height + heightPadding
        print "newWidth, newHeight", newWidth, newHeight
        self.panel.SetSize((newWidth, newHeight))
        self.SetClientSize((newWidth, newHeight))

    # KEA 2004-05-09
    # this is _bindEvents taken from widget.Widget
    # so we can see how moving this to Scriptable will impact binding
    # comments have been removed
    def _bindEvents(self, eventList):
        background = wx.GetTopLevelParent(self)

        if wx.GetApp()._showDebugMenu:
            bindUnusedEvents = True
        else:
            bindUnusedEvents = False
        
        self.boundEvents = {}
        
        self.eventIdToHandler = {}
        self.wxEventIdMap = {}

        if 0:
            print "\nBINDING...", self.name

        for eventClass in eventList:
            self.wxEventIdMap[eventClass.id] = eventClass
            if issubclass(eventClass, event.CommandTypeEvent) and self.command:
                handler = background.findHandler('on_' + self.command + '_command')
                if not handler:
                    handler = background.findHandler('on_' + self.name + '_' + eventClass.name)
            else:
                handler = background.findHandler('on_' + self.name + '_' + eventClass.name)
            if not handler:
                handler = background.findHandler('on_' + eventClass.name)
            if handler or bindUnusedEvents:
                if not self.boundEvents.get(eventClass.binding, None):
                    self.Bind(eventClass.binding, self._dispatch)
                    self.boundEvents[eventClass.binding] = eventClass.name
                if handler:
                    if 0:
                        print "  binding", self.name, eventClass.name, handler.__name__, eventClass.id
                    self.eventIdToHandler[eventClass.id] = handler

        if 0:
            print "\n  boundEvents:"
            for name in self.boundEvents.values():
                print "   ", name
            print "\n\n"
            print "\n  self.eventIdToHandler:"
            for id in self.eventIdToHandler:
                print "   ", id, self.eventIdToHandler[id]
            print "\n\n"

    # KEA 2004-05-09
    # this is _dispatch taken from widget.Widget
    # so we can see how moving this to Scriptable will impact dispatch
    # comments have been removed
    # the only line I added was self.command = None
    # since I'm not sure what we should do about that attribute
    # I suspect that the if test should just be changed so that instead of
    # if self.command ...
    # we use
    # if hasattr(self, 'command') and self.command ...
    # OOPS one other change
    # we're still using unbound methods and after a close event
    # additional events will be sent as the frame is closed and destroyed
    # in particular the last event appears to be a deactivate event
    # to work around this I went ahead and added code
    def _dispatch(self, aWxEvent):
        # this is a temporary workaround, see comment above
        self.command = None
        
        eventType = aWxEvent.GetEventType()
        eventClass = self.wxEventIdMap[eventType]
        
        eventClassInstance = eventClass()
        aWxEvent = eventClassInstance.decorate(aWxEvent, self)

        if self.command and isinstance(eventClassInstance, event.CommandTypeEvent):
            eventName = 'command ' + self.command
        else:
            if isinstance(eventClassInstance, event.InsteadOfTypeEvent):
                eventType = eventClassInstance.translateEventType(aWxEvent)
            eventName = self.wxEventIdMap[eventType].name
            
        eventClass = None
        eventClassInstance = None

        handler = self.eventIdToHandler.get(eventType, None)
        if handler:
            event.EventLog.getInstance().log(eventName, self.name, True)
            if 0:
                print "dispatching", handler.__name__
            aWxEvent.skip = aWxEvent.Skip

            background = wx.GetTopLevelParent(self)

            handler(background, aWxEvent)
            
            aWxEvent.skip = None
            handler = None
            background = None
        else:
            event.EventLog.getInstance().log(eventName, self.name, False)
            aWxEvent.Skip()

        aWxEvent.target = aWxEvent.eventObject = None

    def OnLatentBackgroundBind(self, evt):
        self._bindEvents(BackgroundEvents)

    # KEA 2002-06-27
    # this is a way of loading the shell manually in an app
    # if the shell wasn't loaded at startup, so program
    # startup is quicker and take up less memory 
    # if the shell isn't needed
    def loadShell(self):
        if self.application.shell is None:
            self.application.showShell()

    def loadNamespace(self):
        self.loadShell()
        if self.application.shell is None:
            # must have been a problem loading the shell
            return
        if self.application.namespace is None:
            self.application.showNamespace()

    def setName( self, aString ) :
        self.name = aString

    def getName( self ) :
        return self.name 

    def setImage(self, aPath):
        self.image = aPath
        # Call wxPython
        #raise NotImplementedError

    def setTiled(self, aBoolean):
        if isinstance(aBoolean, str):
            if aBoolean == 'false':
                aBoolean = False
            else:
                aBoolean = True
        self.tiled = aBoolean
        # Call wxPython
        #raise NotImplementedError

    def _getName(self):
        return self.name

    def getImage(self):
        return self.image

    def getTiled(self):
        return self.tiled

    # KEA 2004-03-17
    # the get/set methods above will go away before PythonCard-1.0
    # so that we can just use new-style class properties
    
    def _getPosition(self):
        return self.GetPositionTuple()

    def _setPosition(self, aPosition):
        self.SetPosition(aPosition)

    def _getSize(self):
        return self.GetSizeTuple()

    def _setSize(self, aSize):
        self.SetSize(aSize)

    def _getBackgroundColor(self):
        return self.panel.getBackgroundColor()

    def _setBackgroundColor(self, aColor):
        self.panel.setBackgroundColor(aColor)

    def _getForegroundColor(self):
        return self.panel.getForegroundColor()

    def _setForegroundColor(self, aColor):
        self.panel.setForegroundColor(aColor)


    def enableCommand(self, aString, aBoolean=True):
        """
        Fined every component with a 'command' attribute
        that matches aString, and enable the component.
        """
        self.menuBar.enableCommand(aString, aBoolean)

        for component in self.components.itervalues():
            if component.command == aString:
                component.enabled = aBoolean

    def disableCommand(self, aString):
        """
        Fined every component with a 'command' attribute
        that matches aString, and disable the component.
        """
        self.enableCommand(aString, False)
    
    def _initLayout(self, aResourceList):
        """
        Create the gui Widgets for this Background and lay
        them out in a Frame.
        """
        self.panel = widget.Panel(self, self.image, self.tiled)

        for rsrc in aResourceList:
            self.components[rsrc.name] = rsrc

    # KEA 2002-05-02
    # always create at least a File menu with Quit on the Mac
    # so we automatically get the Apple menu...
    def _createMacMenu(self):
        mnu = wx.Menu()
        id = wx.NewId()
        mnu.Append(id, 'E&xit\tAlt+X')

        menubar = self.GetMenuBar()
        if menubar is None:
            menubar = wx.MenuBar()
            self.SetMenuBar(menubar)
        menubar.Append(mnu, 'File')
        wx.EVT_MENU(self, id, self.on_exit_command)

    def exit(self):
        """Exit the application by calling close() 
        on the main application window."""
        
        # regardless of whether this is a child window
        # or primary window of the application, this should
        # give us the right window to close to quit the application
        appWindow = self.application.getCurrentBackground()
        appWindow.close()

    def on_exit_command(self, evt):
        self.exit()

    def _createMenus(self, aResource):
        # RDS - Only create a menubar if one is defined
        #       in the stack's resource file.
        #       This is a hack, I shouldn't be accessing
        #       the stack resource's __dict)__ directly.
        if ('menubar' in aResource.__dict__) and (aResource.menubar is not None):
            self.menuBar = menu.MenuBar(self, aResource.menubar)
        elif wx.Platform == '__WXMAC__' and self.GetParent() is None:
            # always create at least a File menu with Quit on the Mac
            # so we automatically get the Apple menu...
            # KEA 2004-03-01
            # the elif was updated to make sure we only create a menubar
            # if the background has no parent, aka is the primary app window
            self._createMacMenu()

        # KEA and as a further hack, I now add a Debug menu
        # to the menubar. createMenu will create a menubar
        # if one doesn't already exist
        if self.application._showDebugMenu and self.GetParent() == None:
            self.application._debugMenu = debug.DebugMenu(self.application)
            self.application._debugMenu.createMenu(self)
            self.application._debugMenu.bindMenuEvents(self)

    # 2001-11-08
    # hack to keep the statusbar text from being wiped out
    def menuHighlight(self, event):
        self.statusBar.text = self.statusBar.text

    # KEA 2004-04-14
    # subclasses of Background can override this method
    # if they want to have a different style of statusBar
    # OnCreateStatusBar is defined for wxFrame
    # in wxWidgets, but not wxPython, so ignore OnCreateStatusBar
    # in the wxWidgets docs
    # need to verify that we don't need a more complex arg list
    # since that will impact the call in _createStatusBar below
    # this method is also defined for CustomDialog
    def createStatusBar(self):
        return statusbar.StatusBar(self)

    # KEA 2001-12-25
    # method now removes any existing statusbar if the resource
    # doesn't specify one
    # this is mostly for the resourceEditor and should have a clearer API
    def _createStatusBar( self, aResource ) :
        bar = self.GetStatusBar()
        if ('statusBar' in aResource.__dict__) and aResource.statusBar:
            if bar is None:
                self.statusBar = self.createStatusBar()
                self.SetStatusBar(self.statusBar)
                if wx.Platform == '__WXMAC__':
                    #self.statusBar.PositionStatusBar()
                    pass
        else:
            if bar is not None:
                self.SetStatusBar(None)
                bar.Destroy()
                # the statusbar changes the window size
                # so this will for it back
                #self.SetSize(self.GetSizeTuple())
                self.Fit()
            self.statusBar = None
            

    def _setIcon( self, aResource ) :
        """Set icon based on resource values"""
        if ('icon' in aResource.__dict__) and (aResource.icon is not None):
            try:
                icon = wx.Icon(aResource.icon, wx.BITMAP_TYPE_ICO)
                self.SetIcon(icon)
            except:
                pass
            

    def _bindWindowEvents(self):
        wx.EVT_CLOSE(self, self.OnClose)
        wx.EVT_WINDOW_DESTROY(self, self.OnDestroy)

    # KEA 2004-05-09
    # this is necessary so that we don't try and dispatch
    # the activate event which is sent after close
    # this might not be needed if we start using bound
    # events, but that will require more testing 
    def OnClose(self, evt):
        # this will be found when the on_close method above 
        # or override calls close so that we can still
        # disconnect the deactivateevent during close
        # otherwise trying to dispatch to 
        self.Disconnect(-1, -1, ActivateEvent.id)
        evt.Skip()

    # KEA 2002-07-09
    # make sure wxSTC text, bitmaps, etc. aren't lost
    # when the app exits
    def OnDestroy(self, evt):
        # KEA 2004-04-16
        # stopLogging prevents the OleFlushClipboard message
        # from being displayed at the console when the app quits
        if self == evt.GetEventObject():
            stopLogging = wx.LogNull()
            wx.TheClipboard.Flush()
            del stopLogging
        evt.Skip()

    def GetRestoredPosition(self):
        if self.IsIconized():
            return self._restoredPosition
        else:
            return self.GetPositionTuple()

    def GetRestoredSize(self):
        if self.IsIconized():
            return self._restoredSize
        else:
            return self.GetSizeTuple()

    def on_minimize(self, evt):
        #print "minimize", evt.Iconized()
        #print evt
        #print evt.GetTimestamp()
        #print "iconized", evt.Iconized()
        #print self.GetPositionTuple()
        #print self.GetSizeTuple()
        if evt.Iconized() and self.GetPositionTuple() != (-32000, -32000):
            self._restoredPosition = self.GetPositionTuple()
            self._restoredSize = self.GetSizeTuple()
        #print self.restoredPosition, self.restoredSize
        evt.Skip()

    # KEA 2004-04-24
    # this doesn't appear to be hooked to an event
    # did the binding get deleted or did we just
    # never decide whether we wanted to have a separate
    # event to denote exiting the app versus calling close
    # on the main background to quit the app?!
    def OnExit(self, evt):
        self.close(True)

    # KEA 2004-04-26
    # why do we need the methods below?!
    # what is the use case for them?
    # findComponentsByClass has some value
    # but any app that needs it can easily do the method itself
    # I blew away the same methods in CustomDialog
    # getComponent, getComponents, findAllComponents, findComponentsByClass
    
    # RDS = new API
    def getComponent( self, path ) :
        return eval( 'self.components.' + path )
        
    # RDS - new API
    def getComponents( self ) :
        return self.findAllComponents()
        
    # RDS - deprecated
    def findAllComponents( self ) :
        """
        Return a copy of the list of Components in this
        Background.  We're not just returning 
        self.components.values because we don't want
        someone to inadvertently whack the internal list
        of Components.
        """
        components = []
        for component in self.components.itervalues() :
            components.append( component )
        return components

    def findComponentsByClass( self, aComponentClass ) :
        """
        Return a list of Component's that are instances
        of the specified Component class.
        """
        components = []
        for component in self.components.itervalues() :
            if isinstance( component, aComponentClass ) :
                components.append( component )
        return components

    # KEA 2001-07-31
    # we may want to put this someplace else, but we do need access
    # to the componenet list
    def findFocus(self):
        # the wxPython widget that has focus
        widgetWX = wx.Window_FindFocus()
        if widgetWX is None:
            return None
        else:
            for widget in self.components.itervalues():
                if widgetWX == widget:
                    return widget
        # is this even possible? focus in another window maybe?
        return None

    # KEA 2004-03-17
    # mixedCase aliases
    close = wx.Frame.Close
    getParent = wx.Frame.GetParent
    
    # KEA 2004-03-17
    # define Python 2.2 new-style class properties
    backgroundColor = property(_getBackgroundColor, _setBackgroundColor, doc="backgroundColor of the background") 
    foregroundColor = property(_getForegroundColor, _setForegroundColor, doc="foregroundColor of the background") 
    position = property(_getPosition, _setPosition, doc="position of the background") 
    size = property(_getSize, _setSize, doc="size of the background") 
    title = property(wx.Frame.GetTitle, wx.Frame.SetTitle)
    visible = property(wx.Frame.IsShown, wx.Frame.Show, doc="whether the background window is visible") 
    maximized = property(wx.Frame.IsMaximized, wx.Frame.Maximize, doc="whether the background window is maximized") 
    minimized = property(wx.Frame.IsIconized, wx.Frame.Iconize, doc="whether the background window is minimized") 


# KEA 2004-09-28
# it appears that if you are going to use splitters
# you can't just put them a wx.Panel within a wx.Frame
# so the SplitterBackground has no self.panel
# and the question becomes how are the various splitter
# combinations specified?
# when the PageBackground children are created, they
# will need to use the correct splitters as parents
class SplitterBackground(Background):
    def _initLayout(self, aResourceList):
        # should we just set self.panel = self instead?!
        self.panel = None

    # KEA 2001-07-31
    # we may want to put this someplace else, but we do need access
    # to the componenet list
    def findFocus(self):
        # the wxPython widget that has focus
        widgetWX = wx.Window_FindFocus()
        if widgetWX is None:
            return None
        else:
            # KEA 2004-09-28
            # this needs to iterate through the splitters
            # children correctly and my brain hurts
            # too much from getting splitters working
            # to fix this ;-)
            for widget in self.components.itervalues():
                if widgetWX == widget:
                    return widget
        # is this even possible? focus in another window maybe?
        return None

    # these really don't have any purpose within the
    # context of a SplitterBackground
    # but I'll leave them here for now
    
    # there are probably additional references in Background to self.panel
    # that also need overriding methods here
    
    def _getBackgroundColor(self):
        return self.GetBackgroundColour()

    def _setBackgroundColor(self, aColor):
        self.SetBackgroundColour(aColor)

    def _getForegroundColor(self):
        return self.GetForegroundColour()

    def _setForegroundColor(self, aColor):
        self.SetForegroundColour(aColor)

    backgroundColor = property(_getBackgroundColor, _setBackgroundColor, doc="backgroundColor of the background") 
    foregroundColor = property(_getForegroundColor, _setForegroundColor, doc="foregroundColor of the background") 


PageBackgroundEvents = (
##    ActivateEvent,
##    CloseEvent,
##    DeactivateEvent,
    event.IdleEvent,
##    MaximizeEvent,
##    MinimizeEvent,
##    MoveEvent,
##    RestoreEvent,
##    SizeEvent,
)

class PageBackground(Scriptable, wx.Panel, event.EventSource):
    """
    A window that contains Widgets.
    """

    def __init__(self, aParent, aBgRsrc):
        """
        Initialize this instance.
        """
        Scriptable.__init__(self, None)
        event.EventSource.__init__(self)
        self.id = wx.NewId()
        self.resource = aBgRsrc
        self.application = wx.GetApp()
        self.setName(aBgRsrc.name)
        self.setImage(aBgRsrc.image)
        self.setTiled(aBgRsrc.tiled)
        self.components = WidgetDict(self)

##        # override for application defined position
##        position = configuration.getOption('defaultBackgroundPosition')
##        if position is None:
##            position = aBgRsrc.position

##        # KEA 2004-01-18
##        # have to explicitly declare the close box in wxPython 2.5
##        style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
##        if aBgRsrc.style == ['resizeable']:
##            style = wx.DEFAULT_FRAME_STYLE
        # First, call the base class' __init__ method to create the frame
        wx.Panel.__init__(self, aParent,
                            self.id, 
##                            aBgRsrc.title,
##                            position,
                            size=aBgRsrc.size,
##                            wx.NO_FULL_REPAINT_ON_RESIZE,
                            name=aBgRsrc.name)

        self.topLevelParent = wx.GetTopLevelParent(self)
        self.menuBar = self.topLevelParent.menuBar
        self.statusBar = self.topLevelParent.statusBar
        
        self._initLayout(aBgRsrc.components)

        # KEA 2004-09-14
        # force PageBackground to fit
        # space provided by Notebook
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self._sizer.Add(self.panel, True, wx.EXPAND)
        self._sizer.Fit(self)
        self._sizer.SetSizeHints(self)
        self.SetSizer(self._sizer)
        self.Layout()

        # KEA 2001-08-13
        # can't set the colors until after the panel
        # has been created. this initialization should probably work differently
        self._setForegroundColor(aBgRsrc.foregroundColor)
        self._setBackgroundColor(aBgRsrc.backgroundColor)

##        self._createMenus(aBgRsrc)
##        self._createStatusBar(aBgRsrc)

##        # AJT 20.11.2001
##        # Add icon creation
##        self._setIcon(aBgRsrc)

##        # 2001-11-08
##        # hack to preserve the statusbar text
##        if self.statusBar is not None and self.menuBar is not None:
##            wx.EVT_MENU_HIGHLIGHT_ALL(self, self.menuHighlight)

##        if aParent is None:
##            self.application.SetTopWindow(self)
##
##        # KEA 2002-04-26
##        # allow background window to remain hidden 
##        if aBgRsrc.visible:
##            self.Show(True)

        # RDS 2004-04-14
        # Post the Background initialization event.

        self.EVT_OPEN_BACKGROUND_TYPE = wx.NewEventType()
        self.id = wx.NewId()
        self.Connect(self.GetId(), -1, 
                     self.EVT_OPEN_BACKGROUND_TYPE, 
                     self.on_initialize)
                     #self._dispatchOpenBackground )
        evt = wx.PyCommandEvent(self.EVT_OPEN_BACKGROUND_TYPE, self.GetId())
        evt.target = self
        wx.PostEvent(self, evt)
        EVT_LATENT_BACKGROUNDBIND(self, self.OnLatentBackgroundBind)
        wx.PostEvent(self, wxLatentBackgroundBindEvent())
        # for some reason the Message Watcher isn't a listener yet
        # so calling EventLog doesn't do anything
        #event.EventLog.getInstance().log('initialize', self.name, True)

##        self._bindWindowEvents()


    def on_initialize(self, evt):
        # override in subclass
        pass

##    def on_close(self, evt):
##        # override in subclass
##        evt.Skip()

    # KEA 2004-09-14
    # this probably doesn't work, but need to test
    # since PageBackground is a wx.Panel
    # that contains a wx.Panel
    # and it contains a sizer to force it to expand to
    # the size of the Notebook set in __init__ above
    # I'm not sure if this method makes any sense for PageBackground
    def singleItemExpandingSizerLayout(self):
        """Convenience method for backgrounds with only a 
        single component on the background where the component
        should expand with the background as in an editor.
        
        Call from within the on_initialize event handler."""
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        name = self.components.order[0]
        self.sizer.Add(self.components[name], True, wx.EXPAND)
        self.sizer.Fit(self)
        self.sizer.SetSizeHints(self)
        self.panel.SetSizer(self.sizer)
        self.panel.Layout()


    # KEA 2004-05-09
    # this is _bindEvents taken from widget.Widget
    # so we can see how moving this to Scriptable will impact binding
    # comments have been removed
    def _bindEvents(self, eventList):
##        background = wx.GetTopLevelParent(self)
        background = self

        if wx.GetApp()._showDebugMenu:
            bindUnusedEvents = True
        else:
            bindUnusedEvents = False
        
        self.boundEvents = {}
        
        self.eventIdToHandler = {}
        self.wxEventIdMap = {}

        if 0:
            print "\nBINDING...", self.name

        for eventClass in eventList:
            self.wxEventIdMap[eventClass.id] = eventClass
            if issubclass(eventClass, event.CommandTypeEvent) and self.command:
                handler = background.findHandler('on_' + self.command + '_command')
                if not handler:
                    handler = background.findHandler('on_' + self.name + '_' + eventClass.name)
            else:
                handler = background.findHandler('on_' + self.name + '_' + eventClass.name)
            if not handler:
                handler = background.findHandler('on_' + eventClass.name)
            if handler or bindUnusedEvents:
                if not self.boundEvents.get(eventClass.binding, None):
                    self.Bind(eventClass.binding, self._dispatch)
                    self.boundEvents[eventClass.binding] = eventClass.name
                if handler:
                    if 0:
                        print "  binding", self.name, eventClass.name, handler.__name__, eventClass.id
                    self.eventIdToHandler[eventClass.id] = handler

        if 0:
            print "\n  boundEvents:"
            for name in self.boundEvents.values():
                print "   ", name
            print "\n\n"
            print "\n  self.eventIdToHandler:"
            for id in self.eventIdToHandler:
                print "   ", id, self.eventIdToHandler[id]
            print "\n\n"

    # KEA 2004-05-09
    # this is _dispatch taken from widget.Widget
    # so we can see how moving this to Scriptable will impact dispatch
    # comments have been removed
    # the only line I added was self.command = None
    # since I'm not sure what we should do about that attribute
    # I suspect that the if test should just be changed so that instead of
    # if self.command ...
    # we use
    # if hasattr(self, 'command') and self.command ...
    # OOPS one other change
    # we're still using unbound methods and after a close event
    # additional events will be sent as the frame is closed and destroyed
    # in particular the last event appears to be a deactivate event
    # to work around this I went ahead and added code
    def _dispatch(self, aWxEvent):
        # this is a temporary workaround, see comment above
        self.command = None
        
        eventType = aWxEvent.GetEventType()
        eventClass = self.wxEventIdMap[eventType]
        
        eventClassInstance = eventClass()
        aWxEvent = eventClassInstance.decorate(aWxEvent, self)

        if self.command and isinstance(eventClassInstance, event.CommandTypeEvent):
            eventName = 'command ' + self.command
        else:
            if isinstance(eventClassInstance, event.InsteadOfTypeEvent):
                eventType = eventClassInstance.translateEventType(aWxEvent)
            eventName = self.wxEventIdMap[eventType].name
            
        eventClass = None
        eventClassInstance = None

        handler = self.eventIdToHandler.get(eventType, None)
        if handler:
            event.EventLog.getInstance().log(eventName, self.name, True)
            if 0:
                print "dispatching", handler.__name__
            aWxEvent.skip = aWxEvent.Skip

##            background = wx.GetTopLevelParent(self)
            background = self

            handler(background, aWxEvent)
            
            aWxEvent.skip = None
            handler = None
            background = None
        else:
            event.EventLog.getInstance().log(eventName, self.name, False)
            aWxEvent.Skip()

        aWxEvent.target = aWxEvent.eventObject = None

    def OnLatentBackgroundBind(self, evt):
        self._bindEvents(PageBackgroundEvents)

    # KEA 2002-06-27
    # this is a way of loading the shell manually in an app
    # if the shell wasn't loaded at startup, so program
    # startup is quicker and take up less memory 
    # if the shell isn't needed
    def loadShell(self):
        if self.application.shell is None:
            self.application.showShell()

    def loadNamespace(self):
        self.loadShell()
        if self.application.shell is None:
            # must have been a problem loading the shell
            return
        if self.application.namespace is None:
            self.application.showNamespace()

    def setName( self, aString ) :
        self.name = aString

    def getName( self ) :
        return self.name 

    def setImage(self, aPath):
        self.image = aPath
        # Call wxPython
        #raise NotImplementedError

    def setTiled(self, aBoolean):
        if isinstance(aBoolean, str):
            if aBoolean == 'false':
                aBoolean = False
            else:
                aBoolean = True
        self.tiled = aBoolean
        # Call wxPython
        #raise NotImplementedError

    def _getName(self):
        return self.name

    def getImage(self):
        return self.image

    def getTiled(self):
        return self.tiled

    # KEA 2004-03-17
    # the get/set methods above will go away before PythonCard-1.0
    # so that we can just use new-style class properties
    
    def _getPosition(self):
        return self.GetPositionTuple()

    def _setPosition(self, aPosition):
        self.SetPosition(aPosition)

    def _getSize(self):
        return self.GetSizeTuple()

    def _setSize(self, aSize):
        self.SetSize(aSize)

    def _getBackgroundColor(self):
        return self.panel.getBackgroundColor()

    def _setBackgroundColor(self, aColor):
        self.panel.setBackgroundColor(aColor)

    def _getForegroundColor(self):
        return self.panel.getForegroundColor()

    def _setForegroundColor(self, aColor):
        self.panel.setForegroundColor(aColor)


    def enableCommand(self, aString, aBoolean=True):
        """
        Fined every component with a 'command' attribute
        that matches aString, and enable the component.
        """
        self.menuBar.enableCommand(aString, aBoolean)

        for component in self.components.itervalues():
            if component.command == aString:
                component.enabled = aBoolean

    def disableCommand(self, aString):
        """
        Fined every component with a 'command' attribute
        that matches aString, and disable the component.
        """
        self.enableCommand(aString, False)
    
    def _initLayout(self, aResourceList):
        """
        Create the gui Widgets for this Background and lay
        them out in a Frame.
        """
        self.panel = widget.Panel(self, self.image, self.tiled)

        for rsrc in aResourceList:
            self.components[rsrc.name] = rsrc

##    # KEA 2002-05-02
##    # always create at least a File menu with Quit on the Mac
##    # so we automatically get the Apple menu...
##    def _createMacMenu(self):
##        mnu = wx.Menu()
##        id = wx.NewId()
##        mnu.Append(id, 'E&xit\tAlt+X')
##
##        menubar = self.GetMenuBar()
##        if menubar is None:
##            menubar = wx.MenuBar()
##            self.SetMenuBar(menubar)
##        menubar.Append(mnu, 'File')
##        wx.EVT_MENU(self, id, self.on_exit_command)

##    def exit(self):
##        """Exit the application by calling close() 
##        on the main application window."""
##        
##        # regardless of whether this is a child window
##        # or primary window of the application, this should
##        # give us the right window to close to quit the application
##        appWindow = self.application.getCurrentBackground()
##        appWindow.close()

##    def on_exit_command(self, evt):
##        self.exit()

##    def _createMenus(self, aResource):
##        # RDS - Only create a menubar if one is defined
##        #       in the stack's resource file.
##        #       This is a hack, I shouldn't be accessing
##        #       the stack resource's __dict)__ directly.
##        if ('menubar' in aResource.__dict__) and (aResource.menubar is not None):
##            self.menuBar = menu.MenuBar(self, aResource.menubar)
##        elif wx.Platform == '__WXMAC__' and self.GetParent() is None:
##            # always create at least a File menu with Quit on the Mac
##            # so we automatically get the Apple menu...
##            # KEA 2004-03-01
##            # the elif was updated to make sure we only create a menubar
##            # if the background has no parent, aka is the primary app window
##            self._createMacMenu()
##
##        # KEA and as a further hack, I now add a Debug menu
##        # to the menubar. createMenu will create a menubar
##        # if one doesn't already exist
##        if self.application._showDebugMenu and self.GetParent() == None:
##            self.application._debugMenu = debug.DebugMenu(self.application)
##            self.application._debugMenu.createMenu(self)
##            self.application._debugMenu.bindMenuEvents(self)

##    # 2001-11-08
##    # hack to keep the statusbar text from being wiped out
##    def menuHighlight(self, event):
##        self.statusBar.text = self.statusBar.text
##
##    # KEA 2004-04-14
##    # subclasses of Background can override this method
##    # if they want to have a different style of statusBar
##    # OnCreateStatusBar is defined for wxFrame
##    # in wxWidgets, but not wxPython, so ignore OnCreateStatusBar
##    # in the wxWidgets docs
##    # need to verify that we don't need a more complex arg list
##    # since that will impact the call in _createStatusBar below
##    # this method is also defined for CustomDialog
##    def createStatusBar(self):
##        return statusbar.StatusBar(self)
##
##    # KEA 2001-12-25
##    # method now removes any existing statusbar if the resource
##    # doesn't specify one
##    # this is mostly for the resourceEditor and should have a clearer API
##    def _createStatusBar( self, aResource ) :
##        bar = self.GetStatusBar()
##        if ('statusBar' in aResource.__dict__) and aResource.statusBar:
##            if bar is None:
##                self.statusBar = self.createStatusBar()
##                self.SetStatusBar(self.statusBar)
##                if wx.Platform == '__WXMAC__':
##                    #self.statusBar.PositionStatusBar()
##                    pass
##        else:
##            if bar is not None:
##                self.SetStatusBar(None)
##                bar.Destroy()
##                # the statusbar changes the window size
##                # so this will for it back
##                #self.SetSize(self.GetSizeTuple())
##                self.Fit()
##            self.statusBar = None
##            
##
##    def _setIcon( self, aResource ) :
##        """Set icon based on resource values"""
##        if ('icon' in aResource.__dict__) and (aResource.icon is not None):
##            try:
##                icon = wx.Icon(aResource.icon, wx.BITMAP_TYPE_ICO)
##                self.SetIcon(icon)
##            except:
##                pass
            

##    def _bindWindowEvents(self):
##        wx.EVT_CLOSE(self, self.OnClose)
##        wx.EVT_WINDOW_DESTROY(self, self.OnDestroy)

##    # KEA 2004-05-09
##    # this is necessary so that we don't try and dispatch
##    # the activate event which is sent after close
##    # this might not be needed if we start using bound
##    # events, but that will require more testing 
##    def OnClose(self, evt):
##        # this will be found when the on_close method above 
##        # or override calls close so that we can still
##        # disconnect the deactivateevent during close
##        # otherwise trying to dispatch to 
##        self.Disconnect(-1, -1, ActivateEvent.id)
##        evt.Skip()

##    # KEA 2002-07-09
##    # make sure wxSTC text, bitmaps, etc. aren't lost
##    # when the app exits
##    def OnDestroy(self, evt):
##        # KEA 2004-04-16
##        # stopLogging prevents the OleFlushClipboard message
##        # from being displayed at the console when the app quits
##        if self == evt.GetEventObject():
##            stopLogging = wx.LogNull()
##            wx.TheClipboard.Flush()
##            del stopLogging
##        evt.Skip()

##    def GetRestoredPosition(self):
##        if self.IsIconized():
##            return self._restoredPosition
##        else:
##            return self.GetPositionTuple()

##    def GetRestoredSize(self):
##        if self.IsIconized():
##            return self._restoredSize
##        else:
##            return self.GetSizeTuple()

##    def on_minimize(self, evt):
##        #print "minimize", evt.Iconized()
##        #print evt
##        #print evt.GetTimestamp()
##        #print "iconized", evt.Iconized()
##        #print self.GetPositionTuple()
##        #print self.GetSizeTuple()
##        if evt.Iconized() and self.GetPositionTuple() != (-32000, -32000):
##            self._restoredPosition = self.GetPositionTuple()
##            self._restoredSize = self.GetSizeTuple()
##        #print self.restoredPosition, self.restoredSize
##        evt.Skip()

##    # KEA 2004-04-24
##    # this doesn't appear to be hooked to an event
##    # did the binding get deleted or did we just
##    # never decide whether we wanted to have a separate
##    # event to denote exiting the app versus calling close
##    # on the main background to quit the app?!
##    def OnExit(self, evt):
##        self.close(True)

    # KEA 2004-04-26
    # why do we need the methods below?!
    # what is the use case for them?
    # findComponentsByClass has some value
    # but any app that needs it can easily do the method itself
    # I blew away the same methods in CustomDialog
    # getComponent, getComponents, findAllComponents, findComponentsByClass
    
    # RDS = new API
    def getComponent( self, path ) :
        return eval( 'self.components.' + path )
        
    # RDS - new API
    def getComponents( self ) :
        return self.findAllComponents()
        
    # RDS - deprecated
    def findAllComponents( self ) :
        """
        Return a copy of the list of Components in this
        Background.  We're not just returning 
        self.components.values because we don't want
        someone to inadvertently whack the internal list
        of Components.
        """
        components = []
        for component in self.components.itervalues() :
            components.append( component )
        return components

    def findComponentsByClass( self, aComponentClass ) :
        """
        Return a list of Component's that are instances
        of the specified Component class.
        """
        components = []
        for component in self.components.itervalues() :
            if isinstance( component, aComponentClass ) :
                components.append( component )
        return components

    # KEA 2001-07-31
    # we may want to put this someplace else, but we do need access
    # to the componenet list
    def findFocus(self):
        # the wxPython widget that has focus
        widgetWX = wx.Window_FindFocus()
        if widgetWX is None:
            return None
        else:
            for widget in self.components.itervalues():
                if widgetWX == widget:
                    return widget
        # is this even possible? focus in another window maybe?
        return None

##    # KEA 2004-03-17
##    # mixedCase aliases
##    close = wx.Frame.Close
##    getParent = wx.Frame.GetParent

    def _getTitle(self):
        return wx.GetTopLevelParent(self).GetTitle()

    def _setTitle(self, aString):
        wx.GetTopLevelParent(self).SetTitle(aString)

    # KEA 2004-03-17
    # define Python 2.2 new-style class properties
    backgroundColor = property(_getBackgroundColor, _setBackgroundColor, doc="backgroundColor of the background") 
    foregroundColor = property(_getForegroundColor, _setForegroundColor, doc="foregroundColor of the background") 
    position = property(_getPosition, _setPosition, doc="position of the background") 
    size = property(_getSize, _setSize, doc="size of the background") 
    title = property(_getTitle, _setTitle, doc="title of the background")
    visible = property(wx.Frame.IsShown, wx.Frame.Show, doc="whether the background window is visible") 


class CustomDialog( Scriptable, wx.Dialog, event.EventSource):
    """The dialog class used by all custom dialogs."""

    def __init__(self, aBg, aDialogRsrc=None):
        """
        Initialize this instance.
        """
        Scriptable.__init__( self, None)

        self.parent = aBg
        self.application = wx.GetApp()

        # KEA 2002-09-13
        # if a resource isn't provided, try and load
        # a default based on the name
        if aDialogRsrc is None:
            if util.main_is_frozen():
                # KEA 2004-05-20
                # running standalone
                # need to support py2exe differently than bundlebuilder and mcmillan probably
                # but this is the py2exe 0.5 way
                # figure out the .rsrc.py filename based on the module name stored in library.zip
                filename = os.path.split(sys.modules[self.__class__.__module__].__file__)[1]
                filename = os.path.join(self.parent.application.applicationDirectory, filename)
            else:
                # figure out the .rsrc.py filename based on the module name
                filename = sys.modules[self.__class__.__module__].__file__
            # chop the .pyc or .pyo from the end
            base, ext = os.path.splitext(filename)
            filename = internationalResourceName(base)
            aDialogRsrc = resource.ResourceFile(filename).getResource()
        else:
            if isinstance(aDialogRsrc, dict):
                aDialogRsrc = resource.Resource(aDialogRsrc)
        
        self.resource = aDialogRsrc

        self.id = wx.NewId()
        self.setName( aDialogRsrc.name )
        self.components = WidgetDict(self)

        # First, call the base class' __init__ method to create the dialog
        wx.Dialog.__init__( self, self.parent,   
                          -1, 
                          aDialogRsrc.title,
                          aDialogRsrc.position, 
                          aDialogRsrc.size )

        self._initLayout( aDialogRsrc.components )

    # this allows the labels to be something other than Ok, Cancel, No, etc.
    def _returnedString(self, returned):
        for w in self.components.itervalues():
            if returned == w.GetId():
                return w.label

    def showModal(self):
        result = dialog.DialogResults(self.ShowModal())
        result.returnedString = self._returnedString(result.returned)
        return result

    def destroy(self):
        self.Destroy()


    def setName( self, aString ) :
        self.name = aString
    
    def getName( self ) :
        return self.name

    # KEA 2004-03-17
    # the get/set methods above will go away before PythonCard-1.0
    # so that we can just use new-style class properties
    
    def _getPosition(self):
        return self.GetPositionTuple()

    def _setPosition(self, aPosition):
        self.SetPosition(aPosition)

    def _getSize(self):
        return self.GetSizeTuple()

    def _setSize(self, aSize):
        self.SetSize(aSize)


    def enableCommand(self, aString, aBoolean=True):
        """
        Fined every component with a 'command' attribute
        that matches aString, and enable the component.
        """
        for component in self.components.itervalues():
            if component.command == aString:
                component.enabled = aBoolean

    def disableCommand(self, aString):
        """
        Fined every component with a 'command' attribute
        that matches aString, and disable the component.
        """
        self.enableCommand(aString, False)

    
    def _initLayout( self, aResourceList ) :
        """
        Create the gui Widgets for this Dialog and lay
        them out in the panel.
        """
        self.panel = self
        for rsrc in aResourceList:
            self.components[rsrc.name] = rsrc

    def createStatusBar(self):
        return statusbar.StatusBar(self)

    def _createStatusBar( self, aResource ) :
        if ('statusBar' in aResource.application.__dict__) and aResource.application.statusBar:
            self.statusBar = self.createStatusBar(self)
            self.SetStatusBar(self.statusBar)


    def _bindWindowEvents( self ) :
        # Associate some events with methods of this class
        # KEA 2002-06-10
        # this shouldn't be bound, should it?!
        #EVT_CLOSE(self, self.OnCloseWindow) # KEA 2001-08-06
        pass

    # KEA 2001-07-31
    # we may want to put this someplace else, but we do need access
    # to the componenet list
    def findFocus(self):
        # the wxPython widget that has focus
        widgetWX = wx.Window_FindFocus()
        for widget in self.components.itervalues():
            if widgetWx == widget:
                return widget
        # is this even possible? focus in another window maybe?
        return None

    # these shouldn't be necessary
    # but I haven't taken the time to figure out what is messed up in
    # the event dispatch that keeps event.Skip from being called automatically
    # there might be a problem specific to wxDialog
    def on_mouseClick(self, event):
        event.Skip()

    # KEA 2004-03-17
    # mixedCase aliases
    getParent = wx.Dialog.GetParent

    # KEA 2004-03-17
    # define Python 2.2 new-style class properties
    position = property(_getPosition, _setPosition, doc="position of the dialog") 
    size = property(_getSize, _setSize, doc="size of the dialog") 
    title = property(wx.Dialog.GetTitle, wx.Dialog.SetTitle)
    visible = property(wx.Dialog.IsShown, wx.Dialog.Show, doc="whether the dialog is visible") 

