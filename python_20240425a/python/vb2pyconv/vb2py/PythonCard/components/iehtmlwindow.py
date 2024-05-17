
"""
__version__ = "$Revision: 1.19 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx

if wx.Platform == '__WXMSW__':
    from wx.lib import iewin
else:
    # need a graceful exit
    pass

from PythonCard import event, log, widget

"""
        # Hook up the event handlers for the IE window
        self.Bind(iewin.EVT_BeforeNavigate2, self.OnBeforeNavigate2, self.ie)
        self.Bind(iewin.EVT_NewWindow2, self.OnNewWindow2, self.ie)
        self.Bind(iewin.EVT_DocumentComplete, self.OnDocumentComplete, self.ie)
        ##self.Bind(iewin.EVT_ProgressChange,  self.OnProgressChange, self.ie)
        self.Bind(iewin.EVT_StatusTextChange, self.OnStatusTextChange, self.ie)
        self.Bind(iewin.EVT_TitleChange, self.OnTitleChange, self.ie)
"""

class IEHtmlTitleChangeEvent(event.Event):
    name = 'titleChange'
    binding = iewin.EVT_TitleChange
    id = iewin.wxEVT_TitleChange

class IEHtmlStatusTextChangeEvent(event.Event):
    name = 'statusTextChange'
    binding = iewin.EVT_StatusTextChange
    id = iewin.wxEVT_StatusTextChange

class IEHtmlDocumentCompleteEvent(event.Event):
    name = 'documentComplete'
    binding = iewin.EVT_DocumentComplete
    id = iewin.wxEVT_DocumentComplete

IEHtmlWindowEvents = (
            IEHtmlTitleChangeEvent,
            IEHtmlStatusTextChangeEvent,
            IEHtmlDocumentCompleteEvent,
            )

class IEHtmlWindowSpec(widget.WidgetSpec):
    def __init__(self):
        self.name = 'IEHtmlWindow'
        self.parent = 'Widget'
        events = list(IEHtmlWindowEvents)
##        events = [event.IEHtmlTitleChangeEvent,
##                            event.IEHtmlStatusTextChangeEvent,
##                            event.IEHtmlDocumentCompleteEvent,
##                            ]
        attributes = {
            'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
            'text' : { 'presence' : 'optional', 'default' : '' },
        }
        widget.WidgetSpec.__init__(self, 'IEHtmlWindow', 'Widget', events, attributes )
       

class IEHtmlWindow(widget.Widget, iewin.IEHtmlWindow):
    """
    An HTML window using the MS HTML control.
    """

    _spec = IEHtmlWindowSpec()

    def __init__(self, aParent, aResource):
        iewin.IEHtmlWindow.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.position, 
            aResource.size,
            style = wx.CLIP_SIBLINGS | wx.NO_FULL_REPAINT_ON_RESIZE,
            name = aResource.name 
        )

        widget.Widget.__init__(self, aParent, aResource)

        self._setText(aResource.text)

        self._bindEvents(event.WIDGET_EVENTS + IEHtmlWindowEvents)

    def _getText(self) :
        #return self.GetOpenedPage()
        return self.GetText()

    def _setText(self, aString):
        if aString == '' or aString[0] == '<':
            self.LoadString(aString)
        else:
            # filename or URL
            self.LoadUrl(aString)

    text = property(_getText, _setText)

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
        
        #background = self.GetParent().GetParent()
        background = wx.GetTopLevelParent(self)

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
                    background.Bind(eventClass.binding, self._dispatch, self)
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


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].IEHtmlWindow)

