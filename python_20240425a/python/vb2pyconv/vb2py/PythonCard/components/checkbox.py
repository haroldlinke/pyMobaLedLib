
"""
__version__ = "$Revision: 1.19 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx
from PythonCard import event, widget

class CheckBoxMouseClickEvent(event.MouseClickEvent):
    binding = wx.EVT_CHECKBOX
    id = wx.wxEVT_COMMAND_CHECKBOX_CLICKED

CheckBoxEvents = (CheckBoxMouseClickEvent,)

class CheckBoxSpec(widget.WidgetSpec):
    def __init__(self):
##        events = [event.MouseClickEvent ]
        events = list(CheckBoxEvents)
        attributes = {
            'label' : { 'presence' : 'optional', 'default':'CheckBox' },
            'checked' : { 'presence' : 'optional', 'default' : 0 } }
        widget.WidgetSpec.__init__(self, 'CheckBox', 'Widget', events, attributes )


class CheckBox(widget.Widget, wx.CheckBox):
    """
    A check box.
    """

    _spec = CheckBoxSpec()

    def __init__( self, aParent,  aResource ) :
        wx.CheckBox.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id),
            aResource.label, 
            aResource.position, 
            aResource.size,
            style = wx.CLIP_SIBLINGS | wx.NO_FULL_REPAINT_ON_RESIZE,
            name = aResource.name 
            )

        widget.Widget.__init__( self, aParent, aResource)

        if aResource.checked:
            self.SetValue(True)

        self._bindEvents(event.WIDGET_EVENTS + CheckBoxEvents)
    
    checked = property(wx.CheckBox.GetValue, wx.CheckBox.SetValue)
    label = property(wx.CheckBox.GetLabel, wx.CheckBox.SetLabel)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].CheckBox)

