
"""
+__version__ = "$Revision: 1.3 $"
+__date__ = "$Date: 2005/10/27 23:51:14 $"
"""

import wx
from PythonCard import widget

try:
    # I have to do this rename to avoid a name collision
    from wx.lib.floatcanvas import FloatCanvas as FCanvas
    FLOATCANVAS_LOADED = True

    # what is a better way of dealing with this error
    # caused by NumPy not being installed?
    # we don't want the component showing up in the resourceEditor
    # but the error message you get if you try and use an
    # application that requires the component isn't very meaningful

    class FloatCanvasSpec(widget.WidgetSpec):
        def __init__(self):
            events = []
            attributes = {
                'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
            }
            widget.WidgetSpec.__init__(self, 'FloatCanvas', 'Widget', events, attributes )
    
    
    class FloatCanvas(widget.Widget, FCanvas.FloatCanvas):
    
        _spec = FloatCanvasSpec()
    
        def __init__( self, aParent, aResource ) :
    
            FCanvas.FloatCanvas.__init__(
                self,
                aParent,
                widget.makeNewId(aResource.id),
                #wx.wxPoint(aResource.position[0], aResource.position[1]),
                size=aResource.size,
                #aResource.items,
                #style = wx.wxCLIP_SIBLINGS,
                #name = aResource.name,
                ProjectionFun = None,
                BackgroundColor = "WHITE",
                Debug = False,
                )
    
            widget.Widget.__init__( self, aParent, aResource )
            widget.Widget._setPosition(self, aResource.position)
    
            # if there are any events to bind this is where we would do it
            #self._bindEvents(event.WIDGET_EVENTS + CanvasEvents)
    
        # I don't think we need this anymore
        
        """
        def __getattr__(self, name):
            if name[:3] == "Add":
                return FloatCanvas.FloatCanvas.__getattr__(self, name)
            else:
                return widget.Widget.__getattr__(self, name)
        """
    
    
    import sys
    from PythonCard import registry
    registry.Registry.getInstance().register(sys.modules[__name__].FloatCanvas)

except ImportError:
    FLOATCANVAS_LOADED = False
