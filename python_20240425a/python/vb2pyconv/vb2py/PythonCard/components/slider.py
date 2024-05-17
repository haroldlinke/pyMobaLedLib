
"""
__version__ = "$Revision: 1.19 $"
__date__ = "$Date: 2004/05/09 04:11:28 $"
"""

import wx
from PythonCard import event, widget

class SliderSelectEvent(event.SelectEvent):
    binding = wx.EVT_SLIDER
    id = wx.wxEVT_COMMAND_SLIDER_UPDATED

SliderEvents = (SliderSelectEvent,)

class SliderSpec(widget.WidgetSpec):
    def __init__(self):
        events = list(SliderEvents)
##        events = [event.SelectEvent]
        attributes = { 
            'layout' : { 'presence' : 'optional', 'default' : 'horizontal', 'values' : [ 'horizontal', 'vertical' ]  },
            'labels' : { 'presence' : 'optional', 'default' : False },
            'ticks' : { 'presence' : 'optional', 'default' : False },
            'tickFrequency' : { 'presence' : 'optional', 'default' : 0 }, 
            'min' : { 'presence' : 'optional', 'default' : 0 }, 
            'max' : { 'presence' : 'optional', 'default' : 100 }, 
            'value' : { 'presence' : 'optional', 'default' : 0 } 
        }
        widget.WidgetSpec.__init__( self, 'Slider', 'Widget', events, attributes )


class Slider(widget.Widget, wx.Slider):
    """
    A slider component.
    """

    _spec = SliderSpec()
    
    def __init__( self, aParent, aResource ) :
        wx.Slider.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.value, aResource.min, aResource.max,
            aResource.position, 
            aResource.size, 
            style= self.__getLayout(aResource.layout) | \
                self.__getLabels(aResource.labels) | \
                self.__getTicks(aResource.ticks) | \
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )
        
        widget.Widget.__init__( self, aParent, aResource )

        self._layout = aResource.layout
        self._labels = aResource.labels
        self._ticks = aResource.ticks
        if aResource.ticks and aResource.tickFrequency:
            self._setTickFrequency(aResource.tickFrequency)
        
        self._bindEvents(event.WIDGET_EVENTS + SliderEvents)

    def __getLayout( self, aString  ) :
        if aString == 'horizontal' :
            return wx.SL_HORIZONTAL
        elif aString == 'vertical' :
            return wx.SL_VERTICAL
        else :
            raise 'invalid Slider.layout value: ', aString

    def __getLabels(self, aBoolean):
        if aBoolean:
            return wx.SL_LABELS 
        else :
            return 0

    def __getTicks(self, aBoolean):
        if aBoolean:
            return wx.SL_AUTOTICKS
        else :
            return 0

    def setRange( self, aMin, aMax ) :
        self.SetRange( aMin, aMax )

    def _setMin( self, aMin ) :
        self.SetRange( aMin, self.GetMax() )

    def _setMax( self, aMax ) :
        self.SetRange( self.GetMin(), aMax )

    def _getLayout( self ) :
        return self._layout

    def _setLayout( self, aString ) :
        raise AttributeError, "layout attribute is read-only"

    def _getLabels(self):
        return self._labels

    def _setLabels(self, aBoolean):
        raise AttributeError, "labels attribute is read-only"

    def _getTicks(self):
        return self._ticks

    def _setTicks(self, aBoolean):
        raise AttributeError, "ticks attribute is read-only"

    def _getTickFrequency(self):
        return self.GetTickFreq()

    def _setTickFrequency(self, aInteger):
        self.SetTickFreq(aInteger, 1)
        
    layout = property(_getLayout, _setLayout)
    labels = property(_getLabels, _setLabels)
    ticks = property(_getTicks, _setTicks)
    tickFrequency = property(_getTickFrequency, _setTickFrequency)
    max = property(wx.Slider.GetMax, _setMax)
    min = property(wx.Slider.GetMin, _setMin)
    value = property(wx.Slider.GetValue, wx.Slider.SetValue)


import sys
from PythonCard import registry
registry.Registry.getInstance().register( sys.modules[__name__].Slider )
