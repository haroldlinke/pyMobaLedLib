
"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx
from PythonCard import event, widget

# KEA 2004-05-06
# expose the same interface as CheckBox

class ToggleButtonMouseClickEvent(event.MouseClickEvent):
    binding = wx.EVT_TOGGLEBUTTON
    id = wx.wxEVT_COMMAND_TOGGLEBUTTON_CLICKED

ToggleButtonEvents = (ToggleButtonMouseClickEvent,)

class ToggleButtonSpec(widget.WidgetSpec):
    def __init__(self):
        events = list(ToggleButtonEvents)
        attributes = {
            'label' : { 'presence' : 'optional', 'default':'ToggleButton' },
            'checked' : { 'presence' : 'optional', 'default' : 0 } }
        widget.WidgetSpec.__init__(self, 'ToggleButton', 'Widget', events, attributes )


class ToggleButton(widget.Widget, wx.ToggleButton):
    """
    A toggle button.
    """

    _spec = ToggleButtonSpec()

    def __init__( self, aParent,  aResource ) :
        wx.ToggleButton.__init__(
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

        self._bindEvents(event.WIDGET_EVENTS + ToggleButtonEvents)
    
    checked = property(wx.ToggleButton.GetValue, wx.ToggleButton.SetValue)
    label = property(wx.ToggleButton.GetLabel, wx.ToggleButton.SetLabel)

    # KEA 2004-05-06
    # you can't actually set the foregroundColor and backgroundColor of
    # a ToggleButton so I wonder whether we should have those as valid
    # attributes? The same goes for other components where some of our
    # base attributes don't make any sense. OTOH, having the attribute
    # which fails silently when it tries to set it gives some symmetry
    # to the components and gets rid of the need for try/except blocks
    # when processing a group of component attributes.


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].ToggleButton)

