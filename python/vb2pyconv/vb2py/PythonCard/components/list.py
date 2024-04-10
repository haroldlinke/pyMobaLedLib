
"""
__version__ = "$Revision: 1.29 $"
__date__ = "$Date: 2005/12/25 13:44:50 $"
"""

import wx
from PythonCard import event, widget

class ContainerMixin:
    def _getSelection(self):
        return self.GetSelection()

    def _setSelection(self, index):
        self.SetSelection(index)

    def _getStringSelection(self):
        return self.GetStringSelection()

    def _setStringSelection(self, s):
        # an arg of None or empty string will remove the selection
        if s is None or s == '':
            self.SetSelection(-1)
        else:
            self.SetStringSelection(s)

    selection = property(_getSelection, _setSelection)
    stringSelection = property(_getStringSelection, _setStringSelection)


class ListSelectEvent(event.SelectEvent):
    name = 'select'
    binding = wx.EVT_LISTBOX
    id = wx.wxEVT_COMMAND_LISTBOX_SELECTED

# can only have one CommandTypeEvent per component
class ListMouseDoubleClickEvent(event.Event):
    name = 'mouseDoubleClick'
    binding = wx.EVT_LISTBOX_DCLICK
    id = wx.wxEVT_COMMAND_LISTBOX_DOUBLECLICKED

ListEvents = (ListSelectEvent, ListMouseDoubleClickEvent)


class ListSpec(widget.WidgetSpec):
    def __init__(self):
##        events = [event.SelectEvent]
        # KEA 2004-05-03
        # how do we cleanly remove the MouseDoubleClickEvent
        # which the subclass is automatically going to add?
        events = list(ListEvents)
        attributes = { 
            'items' : { 'presence' : 'optional', 'default' : [] },
            'stringSelection' : { 'presence' : 'optional', 'default' : None } 
        }
        widget.WidgetSpec.__init__( self, 'List', 'Widget', events, attributes )
        # KEA 2004-09-04
        # this isn't particularly clean, but it does remove the extra event class
        # and since events unlike attributes don't get any further processing
        # in the spec this should be okay 
        self._events.remove(event.MouseDoubleClickEvent)


class List(widget.Widget, wx.ListBox, ContainerMixin):
    """
    A list that only allows a single item to be selected.
    """
    
    _spec = ListSpec()

    def __init__(self, aParent, aResource):
        wx.ListBox.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.position, 
            aResource.size, 
            aResource.items,
            style = wx.LB_SINGLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name
        )

        widget.Widget.__init__(self, aParent, aResource)

        if aResource.stringSelection:
            self._setStringSelection(aResource.stringSelection)

        self._bindEvents(self._spec._events)

    def _getItems(self):
        items = []
        for i in range(self.GetCount()):
            items.append(self.GetString(i))
        return items

    def _setItems( self, aList ) :
        self.Set(aList)

    def append(self, aString):
        self.Append(aString)

    def appendItems(self, aList):
        self.AppendItems(aList)

    def clear( self ) :
        self.Clear()

    def delete( self, aPosition ) :
        self.Delete( aPosition )

    def findString( self, aString ) :
        return self.FindString( aString )

    def getString( self, aPosition ) :
        return self.GetString( aPosition )

    def insertItems( self, aList, aPosition ) :
        self.InsertItems( aList, aPosition )

    def getCount(self):
        return self.GetCount()

    # KEA was getSelected
    def isSelected(self, aPosition):
        """Determines whether an item is selected.
        aPosition is the zero-based item index
        Returns True if the given item is selected, False otherwise.
        """
        return self.IsSelected(aPosition)

    def setString( self, n, aString ) :
        self.SetString( n, aString )

    items = property(_getItems, _setItems)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].List)

