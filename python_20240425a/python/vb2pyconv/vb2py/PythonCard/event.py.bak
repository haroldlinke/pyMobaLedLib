"""
__version__ = "$Revision: 1.70 $"
__date__ = "$Date: 2004/10/05 00:43:40 $"
"""

import error
import singleton
import sys
import wx


callAfter = wx.CallAfter
futureCall = wx.FutureCall

class EventHandler:
    """
    RDS - 2004-05-02
    Future replacement for Handler.
    Maps a function name to an instance method.
    """
    def __init__( self, method ) :

        # Grab the method object.
        self._method = method
        # Hold on to the full name.
        self._name = method.__name__
        # Parse the function/method name.
        parts = self._name.split('_')
        # The 'on' prefix, i.e. on_button1_click  
        self._prefix = parts[ 0 ] 

        if len( parts ) == 3 :
            # The name of the Widget instance that is the target.
            self._sourceName = parts[ 1 ]
            # The Event class identifier.
            self._eventName = parts[ 2 ]
        else:
            # KEA 2001-09-06
            # need to pass in the name of the Background subclass instance ?
            # RDS 2004-05-02
            # What?
            self._sourceName = ''
            self._eventName = parts[ 1 ]
        
    def getName( self ) :
        return self._name 
        
    def getSourceName( self ) :
        return self._sourceName

    def getEventName( self ) :
        return self._eventName
        
    def execute( self, event ) :
        """
        RDS - 2004-05-02
        Added to support new Scriptable design in
        component.Scriptable.  Ask the Handler to
        execute itself instead of getting it's 
        function and calling it.
        """
        self._method( event )
        
    def __repr__( self ) :
        return str( self.__dict__ )



# KEA 2004-05-04
# I don't think this is needed, but I'm leaving it in for now
# with the previous code in model.py, widget.py, menu.py, and iehtmlwindow.py
# that use Handler and getFunction() commented with the replacement
# code in use

##class Handler:
##    """
##    Maps a function name to a function, parsing the
##    PythonCard-specific name into meaningful parts.
##    """
##    def __init__(self, aFunctionObject):
##
##        # Hold on to the full name.
##        self._name = aFunctionObject.__name__
##        # Parse the function/method name.
##        parts = self._name.split('_')
##        # The 'on' prefix, i.e. on_button1_click  
##        self._prefix = parts[ 0 ] 
##
##        if len(parts) == 3:
##            # The name of the Widget instance that is the target.
##            self._sourceName = parts[ 1 ]
##            # The Event class identifier.
##            self._eventName = parts[ 2 ]
##        else:
##            # KEA 2001-09-06
##            # need to pass in the name of the Background subclass instance ?
##            self._sourceName = ''
##            self._eventName = parts[ 1 ]
##
##        # Grab the function/method object.
##        self._function = aFunctionObject
##        
##    def getName( self ) :
##        return self._name 
##        
##    def getSourceName( self ) :
##        return self._sourceName
##
##    def getEventName( self ) :
##        return self._eventName
##
##    def getFunction( self ) :
##        """
##        RDS - 2004-05-02
##        Once we've switched to the new component.Scriptable
##        design, remove this method and all references to it.
##        """
##        return self._function
##
##    def execute( self, target, event ) :
##        """
##        RDS - 2004-05-02
##        Added to support new Scriptable design in
##        component.Scriptable.  Ask the Handler to
##        execute itself instead of getting it's 
##        function and calling it.
##        """
##        self._function( target, event )
##        
##    def __repr__( self ) :
##        return str( self.__dict__ )


class ChangeEvent :
    """
    A ChangeEvent indicates that some attribute of
    and object has changed.  The event carries a
    reference to the object, and the attribute
    value that changed.
    """
    def __init__( self, aObject, aOldValue ) :
        """
        Initialize this instance.
        """
        self._object = aObject
        self._oldValue = aOldValue

    def getChangedObject( self ) :
        """
        Get a reference to the object that was modified.
        """
        return self._object 

    def getOldValue( self ) :
        """
        Get the old attribute value that changed.
        NOTE: We'll probably need to provide a
        getAttributeName() method to identify the
        actual value that changed within the object.
        """
        return self._oldValue


class ChangeListener :
    """
    Defines an interface that must be implemented
    by classes that want to listen for ChangeEvents.
    """
    def changed( self, aChangeEvent ) :
        """
        Called by a Changeable object when it's
        contents are modified.
        """
        raise error.AbstractMethodException( self.changed )


class Changeable :
    """
    Defines an interface that must be implemented by
    classes that want to generate a notification when
    their contents change.
    """

    def __init__( self ) :
        """
        Initialize this instance.
        """
        self._listeners = []

    def addChangeEventListener( self, aChangeListener ) :
        """
        Add a ChangeListener to this Changeable object's
        list of interested listeners.
        """
        self._listeners.append( aChangeListener )

    def fireChanged( self, oldValue ) :
        """
        Broadcast a ChangeEvent to all registered ChangeListeners.
        """
        evt = ChangeEvent( self, oldValue )
        for listener in self._listeners :
            listener.changed( evt )

class EventSource( object ) :
    """
    Provides support for adding event listeners
    and notifying listeners when an event occurs.
    """
    def __init__( self ) :
        self._listeners = []
        
    def addEventListener(self, listener):
        """
        Add an EventListener as an observer of this object.
        """
        if listener.__class__.__name__ == 'MessageWatcher':
            self._listeners.insert(0, listener)
        else: 
            self._listeners.append(listener)

    # KEA 2004-04-24
    # need this to disconnect the Message Watcher
    def removeEventListener(self, listener):
        self._listeners.remove(listener)

    def notifyEventListeners( self, event ) :
        """
        Notify all of our EventListeners that an event has occured.
        """
        for listener in self._listeners :
            listener.eventOccurred( event )


class EventListener :
    """
    ABSTRACT INTERFACE

    Define an interface that clients can implement in order
    to act as observers of the EventQueue.
    """

    # I don't know if it's possible to make a method
    # 'abstract' in python, i.e. specify that it MUST
    # be overridden?

    def eventOccurred( self, event ) :
        raise error.AbstractMethodException( self.eventOccurred )


# base event classes

class Event :
    """
    Superclass of all event classes.
    """

    def decorate(self, aWxEvent, source):
        aWxEvent.target = aWxEvent.eventObject = source
        return aWxEvent

# mixin for MouseClickEvent, SelectEvent
# the classname can be changed, I just didn't want
# to conflict with CommandEvent above
class CommandTypeEvent:
    pass
    
# mixin for RestoreEvent, DeactivateEvent, MouseDragEvent
# CloseFieldEvent isn't virtual because
# LoseFocus is still sent
# probably need a better descriptor than "virtual" or "instead of"
class InsteadOfTypeEvent:
    pass

class MouseClickEvent(Event, CommandTypeEvent):
    name = 'mouseClick'

class SelectEvent(Event, CommandTypeEvent):
    name = 'select'

    def decorate(self, aWxEvent, source):
        aWxEvent = Event.decorate(self, aWxEvent, source)
        try:
            aWxEvent.selection = aWxEvent.GetSelection()
        except:
            pass
        try:
            aWxEvent.stringSelection = aWxEvent.GetString()
        except:
            pass
        return aWxEvent

# KEA 2004-05-09
# this is referenced in debug.py
# and I don't want to create a circular import
# with model.py, so I'm going to go ahead
# and leave this in event.py
# this might actually be better as an app level
# event anyway, since I'm not sure every Background
# should receive a separate idle event?!
# need to test/experiment
class IdleEvent(Event):
    name = 'idle'
    binding = wx.EVT_IDLE
    id = wx.wxEVT_IDLE

# focus events

class GainFocusEvent(Event):
    name = 'gainFocus'
    binding = wx.EVT_SET_FOCUS
    id = wx.wxEVT_SET_FOCUS

class LoseFocusEvent(Event):
    name = 'loseFocus'
    binding = wx.EVT_KILL_FOCUS
    id = wx.wxEVT_KILL_FOCUS


# timer event

class TimerEvent(Event):
    name = 'timer'
    binding = wx.EVT_TIMER
    id = wx.wxEVT_TIMER

    def decorate(self, aWxEvent, source):
        aWxEvent = Event.decorate(self, aWxEvent, source)
        aWxEvent.interval = aWxEvent.GetInterval()
        return aWxEvent


# key events and text update

class KeyEvent(Event):
    def decorate(self, aWxEvent, source):
        aWxEvent = Event.decorate(self, aWxEvent, source)
        
        # this is basically the same block as MouseEvent.decorate
        # but it seems wrong to have KeyEvent be a subclass of MouseEvent
        aWxEvent.position = tuple(aWxEvent.GetPosition())
        aWxEvent.x = aWxEvent.GetX()
        aWxEvent.y = aWxEvent.GetY()
        aWxEvent.altDown = aWxEvent.AltDown()
        aWxEvent.controlDown = aWxEvent.ControlDown()
        aWxEvent.shiftDown = aWxEvent.ShiftDown()
        
        aWxEvent.keyCode = aWxEvent.GetKeyCode()
        return aWxEvent

class KeyDownEvent(KeyEvent):
    name = 'keyDown'
    binding = wx.EVT_KEY_DOWN
    id = wx.wxEVT_KEY_DOWN

class KeyPressEvent(KeyEvent):    
    name = 'keyPress'
    binding = wx.EVT_CHAR
    id = wx.wxEVT_CHAR

class KeyUpEvent(KeyEvent):
    name = 'keyUp'
    binding = wx.EVT_KEY_UP
    id = wx.wxEVT_KEY_UP

class TextEnterEvent( Event ) :
    name = 'textEnter'
    binding = wx.EVT_TEXT_ENTER
    id = wx.wxEVT_COMMAND_TEXT_ENTER
    
class TextUpdateEvent( Event ) :
    name = 'textUpdate'
    binding = wx.EVT_TEXT
    id = wx.wxEVT_COMMAND_TEXT_UPDATED


# mouse events

class MouseEvent(Event):
    def decorate(self, aWxEvent, source):
        aWxEvent = Event.decorate(self, aWxEvent, source)
        
        aWxEvent.position = tuple(aWxEvent.GetPosition())
        aWxEvent.x = aWxEvent.GetX()
        aWxEvent.y = aWxEvent.GetY()
        aWxEvent.altDown = aWxEvent.AltDown()
        aWxEvent.controlDown = aWxEvent.ControlDown()
        aWxEvent.shiftDown = aWxEvent.ShiftDown()
        return aWxEvent
        
class MouseContextDoubleClickEvent(MouseEvent):
    name = 'mouseContextDoubleClick'
    binding = wx.EVT_RIGHT_DCLICK
    id = wx.wxEVT_RIGHT_DCLICK

class MouseContextDownEvent(MouseEvent):
    name = 'mouseContextDown'
    binding = wx.EVT_RIGHT_DOWN
    id = wx.wxEVT_RIGHT_DOWN

class MouseContextUpEvent(MouseEvent):
    name = 'mouseContextUp'
    binding = wx.EVT_RIGHT_UP
    id = wx.wxEVT_RIGHT_UP

class MouseDoubleClickEvent(MouseEvent):
    name = 'mouseDoubleClick'
    binding = wx.EVT_LEFT_DCLICK
    id = wx.wxEVT_LEFT_DCLICK

class MouseDownEvent(MouseEvent):
    name = 'mouseDown'
    binding = wx.EVT_LEFT_DOWN
    id = wx.wxEVT_LEFT_DOWN

class MouseEnterEvent(MouseEvent):
    name = 'mouseEnter'
    binding = wx.EVT_ENTER_WINDOW
    id = wx.wxEVT_ENTER_WINDOW

class MouseLeaveEvent(MouseEvent):
    name = 'mouseLeave'
    binding = wx.EVT_LEAVE_WINDOW
    id = wx.wxEVT_LEAVE_WINDOW

class MouseMiddleDoubleClickEvent(MouseEvent):
    name = 'mouseMiddleDoubleClick'
    binding = wx.EVT_MIDDLE_DCLICK
    id = wx.wxEVT_MIDDLE_DCLICK

class MouseMiddleDownEvent(MouseEvent):
    name = 'mouseMiddleDown'
    binding = wx.EVT_MIDDLE_DOWN
    id = wx.wxEVT_MIDDLE_DOWN

class MouseMiddleUpEvent(MouseEvent):
    name = 'mouseMiddleUp'
    binding = wx.EVT_MIDDLE_UP
    id = wx.wxEVT_MIDDLE_UP

class MouseMoveEvent(MouseEvent, InsteadOfTypeEvent):
    name = 'mouseMove'
    binding = wx.EVT_MOTION
    id = wx.wxEVT_MOTION

    def translateEventType(self, aWxEvent):
        if aWxEvent.Dragging():
            return MouseDragEvent.id
        else:
            return self.id

class MouseDragEvent(MouseMoveEvent):
    name = 'mouseDrag'
    id = wx.NewEventType()

class MouseUpEvent(MouseEvent):
    name = 'mouseUp'
    binding = wx.EVT_LEFT_UP
    id = wx.wxEVT_LEFT_UP


FOCUS_EVENTS = (
    GainFocusEvent,
    LoseFocusEvent,
)

MOUSE_EVENTS = (
    MouseContextDoubleClickEvent,
    MouseContextDownEvent,
    MouseContextUpEvent,
    MouseDoubleClickEvent,
    MouseDownEvent,
    MouseDragEvent,
    MouseEnterEvent,
    MouseLeaveEvent,
    MouseMiddleDownEvent,
    MouseMiddleDoubleClickEvent,
    MouseMiddleUpEvent,
    MouseMoveEvent,
    MouseUpEvent,
)

WIDGET_EVENTS = MOUSE_EVENTS + FOCUS_EVENTS + (TimerEvent,)


class EventLog( singleton.Singleton, EventSource ) :
    """
    All events are reported to the EventLog.  Any interested
    parties may register as listeners.
    """
    def __init__( self ) :
        singleton.Singleton.__init__( self )
        EventSource.__init__( self )

    def log( self, eventName, sourceName, used ) :
        """
        Broadcast the event to all listeners.
        """
        self.notifyEventListeners( ( eventName, sourceName, used ) )
        
