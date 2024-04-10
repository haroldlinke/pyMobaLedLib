
"""
__version__ = "$Revision: 1.12 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx
from PythonCard import event, widget


class StaticBoxSpec(widget.WidgetSpec):
    def __init__(self):
        attributes = {
            'label' : { 'presence' : 'optional', 'default' : '' },
            'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
        }
        widget.WidgetSpec.__init__( self, 'StaticBox', 'Widget', [], attributes )


class StaticBox(widget.Widget, wx.StaticBox):
    """
    A static box is just a box which may be used to group
    controls. The box may have a label.
    """

    _spec = StaticBoxSpec()

    def __init__( self, aParent, aResource ) :
        wx.StaticBox.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id),
            aResource.label,
            aResource.position, 
            aResource.size,
            style = wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )

        widget.Widget.__init__( self, aParent, aResource )

        self._bindEvents(event.WIDGET_EVENTS)

    """
    # KEA 2002-03-25
    # this works, but is too much of a hack, wxWindows needs to be fixed
    def _setPosition(self, position):
        self.Move(position)
        size = self.GetSize()
        self.SetSize((size[0], size[1] - 1))
        self.SetSize(size)
    """
    
    label = property(wx.StaticBox.GetLabel, wx.StaticBox.SetLabel)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].StaticBox)
