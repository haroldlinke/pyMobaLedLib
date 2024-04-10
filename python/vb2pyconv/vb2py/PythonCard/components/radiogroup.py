
"""
__version__ = "$Revision: 1.25 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx
from PythonCard import event, widget
from list import ContainerMixin

class RadioGroupSelectEvent(event.SelectEvent):
    binding = wx.EVT_RADIOBOX
    id = wx.wxEVT_COMMAND_RADIOBOX_SELECTED

RadioGroupEvents = (RadioGroupSelectEvent,)

class RadioGroupSpec(widget.WidgetSpec):
    def __init__(self):
        events = list(RadioGroupEvents)
##        events = [event.SelectEvent]
        attributes = { 
            'label' : { 'presence' : 'optional', 'default' : '' },
            'items' : { 'presence' : 'optional', 'default' : ['one'] },
            'stringSelection' : { 'presence' : 'optional', 'default' : 'one' },
            'layout' : { 'presence' : 'optional', 'default' : 'vertical', 'values' : [ 'horizontal', 'vertical' ] },
            'max' : { 'presence' : 'optional', 'default' : 1 }
            # KEA we can't control the border of a wxRadioBox as far as I can tell
            #'border' : { 'presence' : 'optional', 'default' : None }        
        }
        widget.WidgetSpec.__init__( self, 'RadioGroup', 'Widget', events, attributes )


class RadioGroup(widget.Widget, wx.RadioBox, ContainerMixin):
    """
    A group of radio buttons.
    """

    _spec = RadioGroupSpec()

    def __init__(self, aParent, aResource):
        wx.RadioBox.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.label, 
            aResource.position, 
            aResource.size, 
            aResource.items,
            aResource.max,
            self.__getLayout(aResource.layout) | \
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name=aResource.name
            )

        widget.Widget.__init__(self, aParent, aResource)

        self._labels = aResource.items
        self._layout = aResource.layout
        self._max = aResource.max
        if aResource.stringSelection:
            self._setStringSelection(aResource.stringSelection)
        
        self._bindEvents(event.WIDGET_EVENTS + RadioGroupEvents)

    def __getLayout(self, aString):
        if aString == 'vertical':
            return wx.RA_SPECIFY_COLS
        elif aString == 'horizontal':
            return wx.RA_SPECIFY_ROWS
        else:
            raise 'invalid RadioGroup.layout value: ', aString

    def _getItems(self):
        return self._labels

    # KEA 2004-04-23
    # I could probably manually call SetItemLabel(n, string)
    # to replace all the radio button lables but only
    # if there was the same number of items as radio buttons
    def _setItems(self, aList):
        raise NotImplementedError

    def _getLayout(self):
        return self._layout

    def _setLayout(self, aString):
        raise AttributeError, "layout attribute is read-only"

    def _getMax(self):
        return self._max

    def _setMax(self, aMax):
        raise AttributeError, "max attribute is read-only"

    items = property(_getItems, _setItems)
    label = property(wx.RadioBox.GetLabel, wx.RadioBox.SetLabel)
    layout = property(_getLayout, _setLayout)
    max = property(_getMax, _setMax)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].RadioGroup)
