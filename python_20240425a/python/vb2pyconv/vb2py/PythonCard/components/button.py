
"""
__version__ = "$Revision: 1.31 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx
from PythonCard import event, widget

class ButtonMouseClickEvent(event.MouseClickEvent):
    binding = wx.EVT_BUTTON
    id = wx.wxEVT_COMMAND_BUTTON_CLICKED

ButtonEvents = (ButtonMouseClickEvent,)
#ButtonEvents = [ButtonMouseClickEvent]

class ButtonSpec(widget.WidgetSpec):
    def __init__(self):
        # KEA 2004-04-26
        # test to use new event classes
        events = list(ButtonEvents)
        #events = ButtonEvents
##        events = [event.MouseClickEvent]
        attributes = {
            'label' : { 'presence' : 'optional', 'default':'Button' },
            # KEA don't need style for Button unless we are going to support
            # Win32-specific attributes
            #'style':{'presence':'optional', 'default':'3d', 'values':['3d', 'none']},
            'default':{'presence':'optional', 'default':0} }
        widget.WidgetSpec.__init__(self, 'Button', 'Widget', events, attributes )

    # KEA 2004-05-12
    # this is here just so I have an example of a subclass
    # using getMinimalResourceDict
    
    def getMinimalResourceDict(self, name):
        d = widget.WidgetSpec.getMinimalResourceDict(self, name)
        d['label'] = d['name']
        return d


class Button(widget.Widget, wx.Button):
    """
    A simple push-button with a label.
    """

    _spec = ButtonSpec()

    def __init__(self, aParent,  aResource):
        wx.Button.__init__(self,
                    aParent,
                    widget.makeNewId(aResource.id),
                    aResource.label,
                    aResource.position,
                    aResource.size,
                    style = wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
                    name = aResource.name
                   )

        widget.Widget.__init__(self, aParent, aResource)

        self._setDefault(self._resource.default)
        
        self._bindEvents(event.WIDGET_EVENTS + ButtonEvents)

    def _getDefault(self):
        #return self == self._parent.GetDefaultItem()
        # KEA 2002-03-26
        # for some reason wxDialog doesn't have a
        # GetDefaultItem and SetDefaultItem
        try:
            return (self == self._parent.GetDefaultItem()) and self._default
        except:
            return self._default

    def _setDefault(self, aBoolean):
        self._default = aBoolean
        if aBoolean:
            self.SetDefault()
        else:
            # KEA 2002-03-26
            # for some reason wxDialog doesn't have a
            # GetDefaultItem and SetDefaultItem
            try:
                if self == self._parent.GetDefaultItem():
                    self._parent.SetDefaultItem(None)
            except:
                pass


    default = property(_getDefault, _setDefault)
    label = property(wx.Button.GetLabel, wx.Button.SetLabel)


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
registry.Registry.getInstance().register(sys.modules[__name__].Button)


if __name__ == "__main__":
    import pprint
    
    b = ButtonSpec()
    pprint.pprint(b.name)
    pprint.pprint(b.parent)
    pprint.pprint(b.events)
    pprint.pprint(b._attributes)
