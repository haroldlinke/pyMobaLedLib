
"""
__version__ = "$Revision:$"
__date__ = "$Date:$"
"""

import wx
from PythonCard import event, widget, model

class ContainerSpec( widget.WidgetSpec ) :
    def __init__( self ) :
        events = [ event.MouseClickEvent ]
        attributes = {}
        widget.WidgetSpec.__init__( self, 'Container', 'Widget', events, attributes )
 

class Container( widget.Widget, model.Scriptable, wx.Panel ) :
    """
    A container panel for composite components.
    """

    _spec = ContainerSpec()

    def __init__( self, aParent,  aResource ) :
        model.Scriptable.__init__( self, aParent )     
        wx.Panel.__init__(
            self, aParent, widget.makeNewId(aResource.id), 
            aResource.position,
            aResource.size,
            style = wx.CLIP_SIBLINGS,
            name = aResource.name
        )
        widget.Widget.__init__( self, aParent, aResource )
        
        adapter = event.DefaultEventBinding( self )
        adapter.bindEvents()

# KEA 2001-12-09
# the registry could contain a dictionary of the class, its EventBinding, spec, etc.
# some of those references could be class attributes instead
# it seems like the spec for the class should be part of the class itself
# RDS 2001-16-01
# A new module, registry, contains the Registry class.  A Component's
# class now contains it's spec, which contains meta data for it's events
# and attributes.  Components register with the ComponentRegistry.

import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Container)
