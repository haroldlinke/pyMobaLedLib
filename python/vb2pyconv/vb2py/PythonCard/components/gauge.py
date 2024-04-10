
"""
__version__ = "$Revision: 1.12 $"
__date__ = "$Date: 2004/05/04 17:15:42 $"
"""

import wx
from PythonCard import event, widget

class GaugeSpec(widget.WidgetSpec):
    def __init__(self):
        events = []
        attributes = { 
            'layout' : { 'presence' : 'optional', 'default' : 'horizontal', 'values' : [ 'horizontal', 'vertical' ]  },
            'max' : { 'presence' : 'optional', 'default' : 100 }, 
            'value' : { 'presence' : 'optional', 'default' : 0 } 
        }
        widget.WidgetSpec.__init__(self, 'Gauge', 'Widget', events, attributes)


class Gauge(widget.Widget, wx.Gauge):
    """
    A gauge component.
    """

    _spec = GaugeSpec()
    
    def __init__( self, aParent, aResource ) :
        wx.Gauge.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.max,
            aResource.position, 
            aResource.size, 
            style= self.__getLayout( aResource.layout ) | wx.GA_SMOOTH | 
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )
        
        widget.Widget.__init__( self, aParent, aResource )        

        self.SetValue(aResource.value)
        self._layout = aResource.layout
        
        self._bindEvents(event.WIDGET_EVENTS)

    def __getLayout( self, aString  ) :
        if aString == 'horizontal' :
            return wx.GA_HORIZONTAL
        elif aString == 'vertical' :
            return wx.GA_VERTICAL
        else :
            raise 'invalid Gauge.layout value: ', aString
            
    def _getLayout( self ) :
        return self._layout

    def _setLayout( self, aString ) :
        raise AttributeError, "layout attribute is read-only"

    layout = property(_getLayout, _setLayout)
    max = property(wx.Gauge.GetRange, wx.Gauge.SetRange)
    value = property(wx.Gauge.GetValue, wx.Gauge.SetValue)
    

import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Gauge)
