
"""
__version__ = "$Revision: 1.28 $"
__date__ = "$Date: 2004/07/21 20:09:04 $"
"""

import wx

import sys
from PythonCard import event, widget
from list import ContainerMixin

class ComboBoxSelectEvent(event.SelectEvent):
    binding = wx.EVT_COMBOBOX
    id = wx.wxEVT_COMMAND_COMBOBOX_SELECTED

# KEA 2004-05-04
# dropped TextEnterEvent since I'm not sure it is needed
# use keyPress handler instead
ComboBoxEvents = (
            event.KeyPressEvent,
            event.KeyDownEvent,
            event.KeyUpEvent,
            #event.TextEnterEvent,
            event.TextUpdateEvent,
            ComboBoxSelectEvent
            )

class ComboBoxSpec(widget.WidgetSpec):
    def __init__(self):
        events = list(ComboBoxEvents)
##        events = [event.SelectEvent,
##                            event.KeyPressEvent,
##                            event.KeyDownEvent, 
##                            event.KeyUpEvent,
##                            event.TextEnterEvent,
##                            event.TextUpdateEvent]
        attributes = { 
            'text' : { 'presence' : 'optional', 'default' : '' },
            'items' : { 'presence' : 'optional', 'default' : [] },
            'stringSelection' : { 'presence' : 'optional', 'default' : None }
        }        
        widget.WidgetSpec.__init__(self, 'ComboBox', 'Widget', events, attributes)


class ComboBox(widget.Widget, wx.ComboBox, ContainerMixin):
    """
    A combobox menu.
    """

    _spec = ComboBoxSpec()

    def __init__( self, aParent, aResource ) :
        wx.ComboBox.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id),
            '',
            aResource.position, 
            aResource.size, 
            aResource.items,
            style = wx.CB_DROPDOWN  | wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )

        widget.Widget.__init__( self, aParent, aResource )
        
        # KEA 2001-08-12
        # need to fix this, these are supposed to be optional
        if aResource.stringSelection:
            self._setStringSelection(aResource.stringSelection)
        if aResource.text != '':
            self.SetValue(aResource.text)

        self._bindEvents(event.WIDGET_EVENTS + ComboBoxEvents)

    def _getItems(self):
        items = []
        try:
            for i in range(self.GetCount()):
                items.append(self.GetString(i))
        except:
            pass
        return items

    def _setItems(self, items):
        self.Clear()
        self.AppendItems(items)

    def append( self, aString ) :
        self.Append( aString )

    def appendItems(self, aList):
        self.AppendItems(aList)

    items = property(_getItems, _setItems)
    text = property(wx.ComboBox.GetValue, wx.ComboBox.SetValue)
    # KEA 2004-04-24
    # wxPython 2.5.1.5 workaround
    # Mac ComboBox is missing SetStringSelection
    if wx.Platform == '__WXMAC__':
        def _setStringSelection(self, s):
            self.SetSelection(self.FindString(s))
        stringSelection = property(ContainerMixin._getStringSelection, _setStringSelection)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].ComboBox)


