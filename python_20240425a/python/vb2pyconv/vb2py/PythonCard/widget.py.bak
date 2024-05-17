
"""
__version__ = "$Revision: 1.136 $"
__date__ = "$Date: 2005/03/28 17:29:37 $"
"""

import wx
import event
import error
import font
import graphic
import component


def makeNewId(id):
    if id == -1:
        return wx.NewId()
    else:
        return id


class WidgetSpec( component.ComponentSpec ) :
    def __init__( self, name, parent, events, subclassAttributes ) :
        events.extend( event.WIDGET_EVENTS )
        attributes = {
            'id':{'presence':'optional', 'default':-1},
            'enabled' : { 'presence' : 'optional', 'default' : 1 },
            'visible' : { 'presence' : 'optional', 'default' : 1 },
            'foregroundColor' : { 'presence' : 'optional', 'default' : None },
            'backgroundColor' : { 'presence' : 'optional', 'default' : None },
            #'helpText' : { 'presence' : 'optional', 'default' : '' },
            'toolTip' : { 'presence' : 'optional', 'default' : '' },
            'font' : { 'presence' : 'optional', 'default' : None },
            'position' : { 'presence' : 'optional', 'default' : [ -1, -1 ] },
            'size' : { 'presence' : 'optional', 'default' : [ -1, -1 ] },
            'userdata' : {'presence':'optional', 'default':''}
            }
        attributes.update(subclassAttributes)
        component.ComponentSpec.__init__( self, name, parent, events, attributes )        
       

class Widget(component.Component):
    """
    The base class for all of our GUI controls.
    Each Widget must bind itself to the wxPython
    event model.  When it receives an event
    from wxPython, it will convert the event
    to a PythonCArd event.Event ( SelectEvent, ClickEvent,
     etc ) and post the event to the EventQueue.
    """
   # _spec = WidgetSpec()

    def __init__(self, aParent, aResource):
        component.Component.__init__(self, aResource)
        self._parent = aParent
        self._resource = aResource
        self._setUserdata(self._resource.userdata)
        # KEA 2004-04-23
        # Controls are enabled and visible by default
        # so no need to enable and call Show unless False.
        if not self._resource.enabled:
            self._setEnabled(self._resource.enabled)
        if not self._resource.visible:
            self._setVisible(self._resource.visible)
        if self._resource.foregroundColor is not None:
            self._setForegroundColor(self._resource.foregroundColor)
        if self._resource.backgroundColor is not None:
            self._setBackgroundColor(self._resource.backgroundColor)
        if self._resource.toolTip != "":
            self._setToolTip(self._resource.toolTip)
        if self._resource.font is None:
            self._font = None
        else:
            self._setFont(font.Font(self._resource.font, self))

    def __repr__(self):
        return str(self.__dict__)

    def _getId(self):
        # KEA 2004-04-20
        # the id is generated using makeNewId by the base wxPython control
        return self.GetId()

    def _setId(self, id):
        raise AttributeError, "id attribute is read-only"

    # KEA 2004-04-21
    # finding the parent is probably going to be a common task
    # I'm tempted to make this a read-only attribute like id
    # but the user would never specify it, so it won't show up
    # in the spec, but before that is done the framework, samples,
    # and tools have to be checked for use of a parent variable
    def getParent(self):
        return self.GetParent() 
    
    def _getToolTip(self):
        try:
            return self.GetToolTip().GetTip()
        except:
            return ""
    
    def _getFont(self):
        if self._font is None:
            desc = font.fontDescription(self.GetFont())
            self._font = font.Font(desc)
        return self._font
    
    def _setForegroundColor( self, aColor ) :
        aColor = self._getDefaultColor( aColor )
        self.SetForegroundColour( aColor )
        self.Refresh()   # KEA wxPython bug?
    
    def _setBackgroundColor( self, aColor ) :
        aColor = self._getDefaultColor( aColor )
        self.SetBackgroundColour( aColor )
        self.Refresh()   # KEA wxPython bug?
        
    def _setToolTip(self, aString):
        toolTip = wx.ToolTip(aString)
        self.SetToolTip(toolTip)
    
    def _setFont(self, aFont):
        if isinstance(aFont, dict):
            aFont = font.Font(aFont, aParent=self)
        else: # Bind the font to this widget.
            aFont._parent = self
        self._font = aFont
        aWxFont = aFont._getFont()
        self.SetFont( aWxFont )

    def _getUserdata(self):
        return self._userdata 

    def _setUserdata(self, aString):
        self._userdata = aString

    def _getDefaultColor( self, aColor ) :
        if aColor is None :
            return wx.NullColour
        else :
            # KEA 2001-07-27
            # is the right place for this check?
            if isinstance(aColor, tuple) and len(aColor) == 3:
                return wx.Colour(aColor[0], aColor[1], aColor[2])
            else:
                return aColor

    # KEA 2004-04-16
    # can the method below be replaced with
    #setFocus = wx.Window.SetFocus
    # even if Widget doesn't subclass wx.Window?
    # the same issue applies to other aliases that might be created
    # above and below
    # if not perhaps Widget should subclass wx.Window?
    def setFocus(self):
        self.SetFocus()

    def _getPosition(self):
        # get the actual position, not (-1, -1)
        return self.GetPositionTuple()  

    def _setPosition(self, aPosition):
        self.Move(aPosition)

    def _getSize(self):
        # return the actual size, not (-1, -1)
        return self.GetSizeTuple()

    def _setSize(self, aSize):
        self.SetSize(aSize)

    def _getEnabled(self):
        return self.IsEnabled()

    def _setEnabled(self, aBoolean):
        self.Enable(aBoolean)

    def _getVisible(self):
        return self.IsShown()

    def _setVisible(self, aBoolean):
        self.Show(aBoolean)

    def _getForegroundColor(self):
        return self.GetForegroundColour()

    def _getBackgroundColor(self):
        return self.GetBackgroundColour()

    def redraw(self):
        """Force an immediate redraw without waiting for an event handler to finish."""
        self.Refresh()
        self.Update()

    # KEA 2004-04-16
    # if a subclass overrides any of the methods below then it needs to
    # set the property as well so the appropriate method gets used
    backgroundColor = property(_getBackgroundColor, _setBackgroundColor)
    font = property(_getFont, _setFont)
    foregroundColor = property(_getForegroundColor, _setForegroundColor)
    enabled = property(_getEnabled, _setEnabled)
    id = property(_getId, _setId)
    #position = property(wx.Window.GetPositionTuple, wx.Window.Move)
    position = property(_getPosition, _setPosition)
    size = property(_getSize, _setSize)
    toolTip = property(_getToolTip, _setToolTip)
    userdata = property(_getUserdata, _setUserdata)
    visible = property(_getVisible, _setVisible)

    # KEA 2004-05-02
    # this will probably end up in Scriptable or Component
    # it should be completely generic
    # the only problem part would be the reference to the parent (background)
    # where the events are actually defined which would make this problematic
    # for a compound component or events bound to a Panel
    # what we really want is a reference to the application instance
    # there is probably some method to give us that in wxWidgets
    # UPDATE - I think GetTopLevelParent is what I was looking for
    def _bindEvents(self, eventList):
        # shouldn't components be subclasses of Scriptable?
        # components would have their own handlers but when
        # looking for a handler match it will search the parents
        # for now just grab handlers from the background
        
        # the references below would be self.findHandler instead of
        # background.findHandler
        
        # KEA 2004-09-13
        # switching back to the earlier hack for finding the parent background
        # in order to support the PageBackground experiments
        #background = self.GetParent().GetParent()
        parent = self.GetParent()
        if isinstance(parent, wx.Dialog):
            background = parent
        else:
            background = parent.GetParent()

        if wx.GetApp()._showDebugMenu:
            bindUnusedEvents = True
        else:
            bindUnusedEvents = False
        
        # helper variable to simplify test for whether to bind InsteadOfTypeEvents
        # there is a good chance we will need to know
        # which events are bound, if we want to dynamically add or remove
        # events later, so go ahead and keep a reference to the list
        self.boundEvents = {}
        
        self.eventIdToHandler = {}
        self.wxEventIdMap = {}

        if 0:
            print "\nBINDING...", self.name

        actionBindings = {}
        if self.actionBindings is not None:
            actionBindings = self.actionBindings
        for eventClass in eventList:
        #for eventClass in ButtonEvents:
            # need to figure out a way to avoid the need
            # for this id to class mapping which is used in _dispatch below
            self.wxEventIdMap[eventClass.id] = eventClass
            # command handler overrides normal mouseClick or select handler
            # so dispatch will automatically dispatch to the command handler
            # by looking up the handler this way
            # it also means that if there is a command association with this component
            # then the regular mouseClick or select handler will never be bound, just ignored
            if issubclass(eventClass, event.CommandTypeEvent) and self.command:
                handler = background.findHandler('on_' + self.command + '_command')
                if not handler:
                    handler = background.findHandler('on_' + self.name + '_' + eventClass.name)
            else:
                handler = background.findHandler('on_' + self.name + '_' + eventClass.name)
            if not handler:
                handler = background.findHandler('on_' + eventClass.name)
            if not handler:
                handlerData = actionBindings.get(eventClass.name)
                if handlerData is not None:
                    handlerObjectName, handlerFunction = handlerData
                    handlerObject = background.components.get(handlerObjectName)
                    if handlerObject is not None:
                        handler = getattr(handlerObject, handlerFunction, None)
                    if not handler:
                        handler = background.findHandler('on_' + handlerObjectName + '_' + handlerFunction)
            if handler or bindUnusedEvents:
                # only bind events that have an event handler
                # in this scenario unused events are never bound
                # which is more efficient, but the Message Watcher needs
                # to be changed
                # alternatively we can bind everything and then in _dispatch
                # if there isn't a match in eventIdToHandler then we know
                # the event isn't used and we can set used to False
                # the complication would be that we probably have to have to
                # always call Skip() which may or may not be a hassle with components
                
                # this doesn't bind command events
                # they would be of the form on_somename_command
                # or perhaps on_command but I don't think we would want
                # to support that
                # the event binding would be specific to a component
                # since on dispatch command overrides something like mouseClickEvent
                # but the name of the command is not related to the component
                # need to look at whether self.command has a value and then bind
                # with ButtonMouseClickEvent.binding if that isn't already bound
                # then in dispatch have to check again I think
                
                # need to avoid double binding
                # also binding shouldn't be order-specific
                # so how to avoid binding mouseDrag to _dispatch
                # if mouseMove is already bound or if binding mouseMove
                # not rebinding if mouseDrag is already bound
                # perhaps MouseDragEvent keeps a reference to MouseMoveEvent
                # and that is inserted into boundEvents, then we check boundEvents
                # prior to rebinding?
                if not self.boundEvents.get(eventClass.binding, None):
                    self.Bind(eventClass.binding, self._dispatch)
                    self.boundEvents[eventClass.binding] = eventClass.name
                if handler:
                    if 0:
                        print "  binding", self.name, eventClass.name, handler.__name__, eventClass.id
                    # KEA 2004-05-02
                    # change to just using the method directly, Handler class not needed
                    # actually the Handler class isn't needed at all
                    # so if the initial list built to simplify findHandler
                    # just stores a reference to the method that would be fine
                    # as long as the whole system uses that
                    # the only reason we don't just build the list ourselves
                    # in _bindEvents is that every component needs to do findHandler
                    # so it is more efficient to do once when the Scriptable object
                    # is created than to reparse for each component
                    #self.eventIdToHandler[eventClass.id] = handler
                    #self.eventIdToHandler[eventClass.id] = handler.getFunction()
                    self.eventIdToHandler[eventClass.id] = handler

        if 0:
            print "\n  boundEvents:"
            for name in self.boundEvents.values():
                print "   ", name
            print "\n\n"
            print "\n  self.eventIdToHandler:"
            for id in self.eventIdToHandler:
                # KEA 2004-05-02
                # change to just using the method directly, Handler class not needed
                #print "   ", id, self.eventIdToHandler[id]._function
                print "   ", id, self.eventIdToHandler[id]
            print "\n\n"

    def _dispatch(self, aWxEvent):
        eventType = aWxEvent.GetEventType()
        eventClass = self.wxEventIdMap[eventType]
        
        eventClassInstance = eventClass()
        # decorate will add the relevant event attributes
        aWxEvent = eventClassInstance.decorate(aWxEvent, self)

        if self.command and isinstance(eventClassInstance, event.CommandTypeEvent):
            # need to report the name for the handler if it exists
            eventName = 'command ' + self.command
        else:
            if isinstance(eventClassInstance, event.InsteadOfTypeEvent):
                # changes eventType if needed
                # e.g. mouseDrag instead of mouseMove
                eventType = eventClassInstance.translateEventType(aWxEvent)
            eventName = self.wxEventIdMap[eventType].name
            
        # cleanup
        eventClass = None
        eventClassInstance = None

        # it shouldn't be possible to be in _dispatch for an event
        # that wasn't bound above, but just in case...
        # KEA 2004-05-02
        # change to just using the method directly, Handler class not needed
        #handler = self.eventIdToHandler.get(eventType, None)
        handler = self.eventIdToHandler.get(eventType, None)
        # KEA 2005-03-28
        # don't fire events when objects are in the process of being deleted
        if handler and not aWxEvent.target.IsBeingDeleted():
            event.EventLog.getInstance().log(eventName, self.name, True)
            if 0:
                print "dispatching", handler.__name__
            # make a lowercase alias
            aWxEvent.skip = aWxEvent.Skip

            # the event handlers are part of the Background so
            # we have to have a reference to call the handler below
            
            # if Scriptable takes over the dispatch then
            # this would need to work differently if the actual
            # handler could be somewhere else
            
            # KEA 2004-09-13
            # switching back to the earlier hack for finding the parent background
            # in order to support the PageBackground experiments
            #background = self.GetParent().GetParent()
##            background = wx.GetTopLevelParent(self)
            parent = self.GetParent()
            if isinstance(parent, wx.Dialog):
                background = parent
            else:
                background = parent.GetParent()

            # this is what is in event.py
            # aHandler.getFunction()( aOwner, self.getSource(), self )
            # KEA 2004-05-02
            # change to just using the method directly, Handler class not needed
            #handler.getFunction()(background, aWxEvent)
            handler(background, aWxEvent)
            
            # do we have to clean up this alias?
            aWxEvent.skip = None
            # how about this local reference to handler?
            handler = None
            background = None
        else:
            event.EventLog.getInstance().log(eventName, self.name, False)
            # hopefully this is all we need to do for "unused events"
            aWxEvent.Skip()

        # cleanup
        aWxEvent.target = aWxEvent.eventObject = None


class Panel(wx.Panel):

    def __init__(self, aParent, imageFile, tiled):
        wx.Panel.__init__(self, aParent, -1, 
            style=wx.TAB_TRAVERSAL | wx.NO_FULL_REPAINT_ON_RESIZE)
        self._frame = aParent
        self._imageFile = imageFile
        self._backgroundTiling = tiled
        # KEA 2001-07-27
        # Load the bitmap once and keep it around
        # this could fail, so should be a try/except.
        if imageFile is not None :
            self._bitmap = graphic.Bitmap(imageFile)
            wx.EVT_ERASE_BACKGROUND( self, self.onEraseBackground )
            
        wx.EVT_WINDOW_DESTROY(self, self._OnDestroy)

    def _OnDestroy(self, event):
        # memory leak cleanup
        self._bitmap = None

    def tileBackground(self, deviceContext):
        # tile the background bitmap
        sz = self.GetClientSize()
        bmp = self._bitmap.getBits()
        w = bmp.GetWidth()
        h = bmp.GetHeight()

        if isinstance(self, wx.ScrolledWindow):
            # adjust for scrolled position
            spx, spy = self.GetScrollPixelsPerUnit()
            vsx, vsy = self.GetViewStart()
            dx,  dy  = (spx * vsx) % w, (spy * vsy) % h
        else:
            dx, dy = (w, h)

        x = -dx
        while x < sz.width:
            y = -dy
            while y < sz.height:
                deviceContext.DrawBitmapPoint(bmp, (x, y))
                y = y + h
            x = x + w

    def getForegroundColor(self):
        return self.GetForegroundColour()

    def getBackgroundColor(self):
        return self.GetBackgroundColour()

    def _getDefaultColor(self, aColor):
        if aColor is None :
            return wx.NullColour
        else :
            # KEA 2001-07-27
            # is the right place for this check?
            if isinstance(aColor, tuple) and len(aColor) == 3:
                return wx.Colour(aColor[0], aColor[1], aColor[2])
            else:
                return aColor
            
    def setForegroundColor(self, aColor):
        aColor = self._getDefaultColor(aColor)
        self.SetForegroundColour(aColor)
        self.Refresh()   # KEA wxPython bug?
    
    def setBackgroundColor(self, aColor):
        aColor = self._getDefaultColor(aColor)
        self.SetBackgroundColour(aColor)
        self.Refresh()   # KEA wxPython bug?

    def onEraseBackground(self, aWxEvent):
        deviceContext = aWxEvent.GetDC()
        
        if not deviceContext :
            deviceContext = wx.ClientDC(self)
            r = self.GetUpdateRegion().GetBox()
            deviceContext.SetClippingRegion(r.x, r.y, r.width, r.height)
                                                       
        if self._backgroundTiling:
            self.tileBackground( deviceContext )
        else:
            deviceContext.DrawBitmapPoint(self._bitmap.getBits(), (0, 0))

    position = property(wx.Panel.GetPositionTuple, wx.Panel.SetPosition, doc="position of the panel") 
    size = property(wx.Panel.GetSizeTuple, wx.Panel.SetSize, doc="size of the panel") 
