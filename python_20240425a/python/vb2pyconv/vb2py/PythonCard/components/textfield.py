
"""
__version__ = "$Revision: 1.31 $"
__date__ = "$Date: 2005/03/28 17:29:39 $"
"""

import wx
from PythonCard import event, widget

# KEA 2002-04-04
# custom event posted after loseFocus when a field
# has been changed
wxEVT_CLOSE_FIELD = wx.NewEventType()

##def EVT_CLOSE_FIELD(win, id, func):
##    win.Connect(id, -1, wxEVT_CLOSE_FIELD, func)
# use the new PyEventBinder in 2.5.x
EVT_CLOSE_FIELD = wx.PyEventBinder(wxEVT_CLOSE_FIELD)
        
class CloseFieldEvent(event.Event):
    name = 'closeField'
    binding = EVT_CLOSE_FIELD
    id = wxEVT_CLOSE_FIELD


TextFieldEvents = (
            event.KeyPressEvent, 
            event.KeyDownEvent, 
            event.KeyUpEvent, 
            event.TextUpdateEvent,
            CloseFieldEvent
            )

class TextFieldSpec(widget.WidgetSpec):
    def __init__( self ) :
        events = list(TextFieldEvents)       
        attributes = {
            'text' : {'presence' : 'optional', 'default' : ''},
            'editable' : {'presence' : 'optional', 'default' : 1},
            'alignment' : {'presence' : 'optional', 'default' : 'left', 'values' :['left', 'right', 'center']},
            'border' : {'presence' : 'optional', 'default' : '3d', 'values' : ['3d', 'none']}
        }                
        widget.WidgetSpec.__init__( self, 'TextField', 'Widget' , events, attributes )


def getAlignment(aString):
    if aString == 'left':
        return wx.TE_LEFT
    elif aString == 'center':
        return wx.TE_CENTRE
    elif aString == 'right':
        return wx.TE_RIGHT
    else :
        raise 'invalid TextField.alignment value:', aString

class TextField(widget.Widget, wx.TextCtrl):
    """
    A text field.
    """

    _spec = TextFieldSpec()

    def __init__(self, aParent,  aResource):
        self._border = aResource.border

        if aResource.border == 'none':
            borderStyle = wx.NO_BORDER
        else:
            borderStyle = 0

        self._alignment = aResource.alignment

        wx.TextCtrl.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id),
            aResource.text, 
            aResource.position, 
            aResource.size, 
            #style = wxTE_PROCESS_ENTER | borderStyle | wxCLIP_SIBLINGS,
            style = borderStyle | getAlignment(aResource.alignment) | \
                wx.CLIP_SIBLINGS | wx.NO_FULL_REPAINT_ON_RESIZE,
            name = aResource.name)

        widget.Widget.__init__(self, aParent, aResource)

        if not aResource.editable:
            self.SetEditable(False)

        if aResource.border == 'none':
            # the erase background event doesn't appear to make the control
            # transparent, so further investigation is required
            #EVT_ERASE_BACKGROUND(delegate, lambda evt: None)
            self.SetBackgroundColour(self.GetParent().GetBackgroundColour())

        #adapter = TextFieldEventBinding(self)
        #adapter.bindEvents()
##        self._bindEvents(event.WIDGET_EVENTS + TextFieldEvents)
        # KEA 2004-09-24
        # changing to CallAfter to force the gainFocus
        # event to occur after the initialize event
        wx.CallAfter(self._bindEvents, event.WIDGET_EVENTS + TextFieldEvents)

    def _getAlignment(self):
        return self._alignment

    def _setAlignment(self, aString):
        raise AttributeError, "alignment attribute is read-only"

    def ClearSelection(self):
        if self.CanCut():
            # delete the current selection,
            # if we can't do a Cut we shouldn't be able to delete either
            # which is why i used the test above
            sel = self.replaceSelection('')
        else:
            ins = self.GetInsertionPoint()
            try:
                self.replace(ins, ins + 1, '')
            except:
                pass

    # KEA the methods for retrieving and manipulating the text
    # has to be greatly expanded to match wxPython
    # capabilities or more


    # KEA new methods to mirror wxPython wxTextCtrl capabilities
    def appendText( self, aString ) :
        """Appends the text to the end of the text widget.
        After the text is appended, the insertion point will be at the end
        of the text widget. If this behavior is not desired, the programmer
        should use getInsertionPoint and setInsertionPoint."""
        self.AppendText( aString )

    def canCopy( self ) :
        return self.CanCopy()

    def canCut( self ) :
        return self.CanCut()

    def canPaste( self ) :
        return self.CanPaste()

    def canRedo( self ) :
        return self.CanRedo()

    def canUndo( self ) :
        return self.CanUndo()

    def clear( self ) :
        self.Clear()

    def copy( self ) :
        self.Copy()

    def cut( self ) :
        self.Cut()

    def discardEdits( self ) :
        self.DiscardEdits()
    
    def getInsertionPoint( self ) :
        return self.GetInsertionPoint()

    def getLastPosition( self ) :
        return self.GetLastPosition()

    def getLineLength( self, aLineNumber ) :
        return self.GetLineLength( aLineNumber )

    def getLineText( self, aLineNumber ) :
        return self.GetLineText( aLineNumber )

    def getNumberOfLines( self ) :
        return self.GetNumberOfLines()

    def getSelection( self ) :
        return self.GetSelection()

    def getNumberOfLines( self ) :
        return self.GetNumberOfLines()

    # KEA rename to getModified?
    def isModified( self ) :
        """Returns 1 if the text has been modified, 0 otherwise."""
        return self.IsModified()

    # KEA support LoadFile? If so, it only makes sense for TextArea
    # many of the other methods only make sense for the multiline TextArea
    # not TextField and PasswordField

    # KEA OnChar ties into our user code handlers and our events,
    # need to think about this one some more

    # KEA OnDropFiles is windows-specific, if you try and call it under *nix
    # what happens? just an exception?

    def paste( self ) :
        self.Paste()

    def positionToXY(self, aPosition):
        result = self.PositionToXY(aPosition)
        if len(result) == 2:
            return result
        else:
            # workaround for wxPython 2.3.2.1
            return (result[1], result[2])

    def redo( self ) :
        self.Redo()

    def remove( self, aFrom, aTo ) :
        self.Remove( aFrom, aTo )

    def replace( self, aFrom, aTo, aString ) :
        # KEA workaround for Replace bug, has the side effect of
        # possibly changing the insertion point
        #self._delegate.Replace( aFrom, aTo, aString )
        i = self.GetInsertionPoint()
        self.Remove( aFrom, aTo )
        self.SetInsertionPoint( aFrom )
        self.WriteText( aString )
        self.SetInsertionPoint( i )

    def replaceSelection(self, aString, select=0):
        sel = self.GetSelection()
        self.Remove(sel[0], sel[1])
        self.WriteText(aString)
        if select:
            self.SetSelection(sel[0], sel[0] + len(aString))

    # KEA support SaveFile?

    def setInsertionPoint( self, aPosition ) :
        self.SetInsertionPoint( aPosition )

    def setInsertionPointEnd( self ) :
        self.SetInsertionPointEnd()

    def setSelection( self, aFrom, aTo ) :
        self.SetSelection( aFrom, aTo )

    def showPosition( self, aPosition ) :
        self.ShowPosition( aPosition )

    def undo( self ) :
        self.Undo()

    def writeText( self, aString ) :
        self.WriteText( aString )

    def xyToPosition( self, aX, aY ) :
        return self.XYToPosition( aX, aY )

    def _getBorder( self ) :
        return self._border

    def _setBorder( self, aString ) :
        raise AttributeError, "border attribute is read-only"

    getStringSelection = wx.TextCtrl.GetStringSelection
    
    def getString(self, aFrom, aTo):
        return self.GetValue()[aFrom:aTo]

    # mimic wxSTC method
    ClearAll = wx.TextCtrl.Clear

    def _bindEvents(self, eventList):
        widget.Widget._bindEvents(self, eventList)

        # in order for closeField to work properly
        # both gainFocus and loseFocus have to be bound to _dispatch
        # regardless of whether they have handlers or not
        for eventClass in [event.GainFocusEvent, event.LoseFocusEvent]:
            if not self.boundEvents.get(eventClass.binding, None):
                self.Bind(eventClass.binding, self._dispatch)
                self.boundEvents[eventClass.binding] = eventClass.name

        # calling widget.Widget._bindEvents after instead of before
        # our component specific initialization would mean any log debug
        # statements like this could just be in Widget_bindEvents
        # however, until we convert all the components I'm not sure 
        # that changing the order will always work
        if 0:
            print "\n  boundEvents:"
            for name in self.boundEvents.values():
                print "   ", name
            print "\n\n"
            print "\n  self.eventIdToHandler:"
            for id in self.eventIdToHandler:
                print "   ", id, self.eventIdToHandler[id]._function
            print "\n\n"

    def _dispatch(self, aWxEvent):
        eventType = aWxEvent.GetEventType()
                    
        # TextField specific stuff
        # the question is how we either call the generic stuff above
        # due to the try/except blocks this code would probably
        # work in the generic event handling but that would be unclean <wink>
        if eventType == wx.wxEVT_SET_FOCUS:
            try:
                aWxEvent.GetEventObject().DiscardEdits()
            except:
                pass
        elif eventType == wx.wxEVT_KILL_FOCUS:
            try:
                aWxEvent.target = aWxEvent.GetEventObject()
                # only wxTextCtrl should have IsModified
                # so an exception will be thrown and the event won't be posted
                # for other components, but they shouldn't be binding to these
                # handlers anyway, so I'm just being overly defensive
                # same with DiscardEdits() above
                #modified = obj.IsModified()
                if not aWxEvent.target.IsBeingDeleted() and aWxEvent.target.IsModified():
                    #closeFieldEvent = aWxEvent.Clone()
                    #closeFieldEvent.SetEventType(event.wxEVT_CLOSE_FIELD)
                    # should I be using wx.PyEvent() instead?
                    closeFieldEvent = wx.WindowCreateEvent()
                    closeFieldEvent.SetEventType(wxEVT_CLOSE_FIELD)
                    closeFieldEvent.SetEventObject(aWxEvent.target)
                    closeFieldEvent.SetId(aWxEvent.GetId())
                    closeFieldEvent.SetTimestamp(aWxEvent.GetTimestamp())
                    # this is what Robin suggested instead, see:
                    # http://aspn.activestate.com/ASPN/Mail/Message/wxPython-users/1103427
                    #obj.GetParent().GetEventHandler().ProcessEvent(closeFieldEvent)
                    # KEA 2004-04-30
                    # ProcessEvent will cause closeField to occur before loseFocus and
                    # gainFocus messages, so should we do a wxCallAfter instead?
                    # in the case of fields should closeField be an InsteadOfTypeEvent
                    # and replace the loseFocus event? probably not since they mean
                    # different things
                    aWxEvent.target.GetEventHandler().ProcessEvent(closeFieldEvent)
                    #wx.PostEvent(obj.GetParent(), evt)
                    #print 'posted closeField'
            except:
                pass

        # rest of the dispatch is standard
        widget.Widget._dispatch(self, aWxEvent)


    alignment = property(_getAlignment, _setAlignment)
    border = property(_getBorder, _setBorder)
    editable = property(wx.TextCtrl.IsEditable, wx.TextCtrl.SetEditable)
    text = property(wx.TextCtrl.GetValue, wx.TextCtrl.SetValue)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].TextField)
