
"""
__version__ = "$Revision: 1.17 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx
from PythonCard import event, widget

class StaticTextSpec(widget.WidgetSpec):
    def __init__(self):
        attributes = {
            'text' : { 'presence' : 'optional', 'default' : 'StaticText' },
            'alignment' : { 'presence' : 'optional', 'default' : 'left', 'values' :[ 'left', 'right', 'center' ] }
        }
        widget.WidgetSpec.__init__( self, 'StaticText', 'Widget', [], attributes )


class StaticText(widget.Widget, wx.StaticText):
    """
    An uneditable block of text.
    """

    _spec = StaticTextSpec()

    def __init__( self, aParent, aResource ) :
        wx.StaticText.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.text, 
            aResource.position, 
            aResource.size,
            style = self.__getAlignment(aResource.alignment) | \
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )
        
        widget.Widget.__init__( self, aParent, aResource )
        
        self._alignment = aResource.alignment
        
        self._bindEvents(event.WIDGET_EVENTS)

    def __getAlignment( self, aString  ) :
        if aString == 'left' :
            return wx.ALIGN_LEFT
        elif aString == 'center' :
            return wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE
        elif aString == 'right' :
            return wx.ALIGN_RIGHT | wx.ST_NO_AUTORESIZE
        else :
            raise 'invalid StaticText.alignment value: ', aString

    def _setText( self, aString):
        self.SetLabel(aString)
        self.Refresh()
        self.Update()

    def _getAlignment( self ) :
        return self._alignment

    def _setAlignment( self, aString ) :
        raise AttributeError, "alignment attribute is read-only"

    alignment = property(_getAlignment, _setAlignment)
    text = property(wx.StaticText.GetLabel, _setText)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].StaticText)
