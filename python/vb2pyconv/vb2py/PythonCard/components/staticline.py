
"""
__version__ = "$Revision: 1.13 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx
from PythonCard import event, widget


class StaticLineSpec(widget.WidgetSpec):
    def __init__(self):
        attributes = {
            'layout' : { 'presence' : 'optional', 'default' : 'horizontal', 'values' : [ 'horizontal', 'vertical' ]  },
            'size' : { 'presence' : 'optional', 'default' : [ 50, -1 ] },
        }
        widget.WidgetSpec.__init__( self, 'StaticLine', 'Widget', [], attributes )

class StaticLine(widget.Widget, wx.StaticLine):
    """
    A static line is just a line which may be used to separate
    a groups of controls. The line may be only vertical or horizontal.
    """

    _spec = StaticLineSpec()

    def __init__( self, aParent, aResource ) :
        wx.StaticLine.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.position, 
            aResource.size,
            style = self.__getLayout( aResource.layout ) | 
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )
        
        widget.Widget.__init__( self, aParent, aResource )

        # set attributes directly that can only be set at initialization
        self._layout = aResource.layout
        
        self._bindEvents(event.WIDGET_EVENTS)

    def __getLayout( self, aString  ) :
        if aString == 'horizontal' :
            return wx.LI_HORIZONTAL
        elif aString == 'vertical' :
            return wx.LI_VERTICAL
        else :
            raise 'invalid StaticLine.layout value: ', aString

    #def _setHelpText( self, aString ) :
    #    pass

    def _setLayout( self, aString ) :
        raise AttributeError, "layout attribute is read-only"

    def _getLayout( self ) :
        return self._layout

    layout = property(_getLayout, _setLayout)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].StaticLine)
