
"""
__version__ = "$Revision: 1.20 $"
__date__ = "$Date: 2004/07/21 20:09:04 $"
"""

import wx
from PythonCard import event, widget
from list import ContainerMixin

class ChoiceSelectEvent(event.SelectEvent):
    binding = wx.EVT_CHOICE
    id = wx.wxEVT_COMMAND_CHOICE_SELECTED

ChoiceEvents = (ChoiceSelectEvent,)

class ChoiceSpec(widget.WidgetSpec):
    def __init__(self):        
        events = list(ChoiceEvents)
##        events = [ event.SelectEvent ]
        attributes = { 
            'items' : { 'presence' : 'optional', 'default' : [] },
            'stringSelection' : { 'presence' : 'optional', 'default' : None } }
        widget.WidgetSpec.__init__(self, 'Choice', 'Widget', events, attributes )


class Choice(widget.Widget, wx.Choice, ContainerMixin):
    """
    A popup menu.
    """

    _spec = ChoiceSpec()

    def __init__( self, aParent, aResource ) :
        wx.Choice.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.position, 
            aResource.size, 
            aResource.items,
            style =  wx.CLIP_SIBLINGS | wx.NO_FULL_REPAINT_ON_RESIZE,
            name = aResource.name 
        )
        
        widget.Widget.__init__( self, aParent, aResource )        
        
        if aResource.stringSelection:
            self._setStringSelection(aResource.stringSelection)
        
        self._bindEvents(event.WIDGET_EVENTS + ChoiceEvents)

    def _getItems(self):
        if self.IsEmpty():
            return []
        else:
            items = []
            for i in range(self.GetCount()):
                items.append(self.GetString(i))
            return items

    def _setItems(self, items):
        self.Clear()
        self.AppendItems(items)

    def append(self, aString):
        self.Append(aString)

    def appendItems(self, aList):
        self.AppendItems(aList)

    items = property(_getItems, _setItems)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Choice)


