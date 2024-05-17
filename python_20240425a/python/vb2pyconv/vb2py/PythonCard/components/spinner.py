
"""
__version__ = "$Revision: 1.16 $"
__date__ = "$Date: 2004/05/04 17:15:42 $"
"""

import wx
from PythonCard import event, widget

# KEA 2004-05-04
# dropped TextEnterEvent since I'm not sure it is needed
# use keyPress handler instead
SpinnerEvents = (
            event.KeyPressEvent,
            event.KeyDownEvent,
            event.KeyUpEvent,
            #event.TextEnterEvent,
            event.TextUpdateEvent,
            )

class SpinnerSpec(widget.WidgetSpec):
    def __init__(self):
        events = list(SpinnerEvents)
##        events = [event.KeyPressEvent,
##                            event.KeyDownEvent, 
##                            event.KeyUpEvent,
##                            event.TextEnterEvent,
##                            event.TextUpdateEvent,
##                            #event.SpinUpEvent,
##                            #event.SpinDownEvent
##                            ]
        attributes = { 
            'min' : { 'presence' : 'optional', 'default' : 0 }, 
            'max' : { 'presence' : 'optional', 'default' : 100 }, 
            'value' : { 'presence' : 'optional', 'default' : 0 } 
        }
        widget.WidgetSpec.__init__( self, 'Spinner', 'Widget', events, attributes )


class Spinner(widget.Widget, wx.SpinCtrl):
    """
    A Spinner component.
    """

    _spec = SpinnerSpec()
    
    def __init__( self, aParent, aResource ) :
        wx.SpinCtrl.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            str(aResource.value),
            aResource.position, 
            aResource.size, 
            style = wx.SP_ARROW_KEYS | wx.SP_WRAP | \
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            min = aResource.min,
            max = aResource.max,
            initial = aResource.value,
            name = aResource.name 
        )

        widget.Widget.__init__( self, aParent, aResource )

        self._bindEvents(event.WIDGET_EVENTS + SpinnerEvents)
            
    def setRange( self, aMin, aMax ) :
        self.SetRange( aMin, aMax )

    def _setMin( self, aMin ) :
        self.SetRange( aMin, self.GetMax() )

    def _setMax( self, aMax ) :
        self.SetRange( self.GetMin(), aMax )

    max = property(wx.SpinCtrl.GetMax, _setMax)
    min = property(wx.SpinCtrl.GetMin, _setMin)
    value = property(wx.SpinCtrl.GetValue, wx.SpinCtrl.SetValue)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Spinner)
