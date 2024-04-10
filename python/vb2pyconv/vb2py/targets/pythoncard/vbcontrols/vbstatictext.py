from vb2py.targets.vb2py.PythonCard.controlclasses import VBWrapped, VBWidget
from vb2py.targets.vb2py.PythonCard import Register
import vb2py.logger
log = vb2py.logger.getLogger("VBStaticText")

from vb2py.PythonCard.components import statictext
from wxPython import wx
import sys
from vb2py.PythonCard import event, registry, widget


class VBStaticText(VBWidget): 
    __metaclass__ = VBWrapped 

    _translations = { 
            "Caption" : "text", 
            "Enabled" : "enabled", 
            "Visible" : "visible", 
        } 

    _indexed_translations = { 
            "Left" : ("position", 0), 
            "Top" : ("position", 1), 
            "Width" : ("size", 0), 
            "Height" : ("size", 1), 
        } 

    _proxy_for = statictext.StaticText




log.debug("Registering VBStaticText as '%s'" % sys.modules[__name__].VBStaticText)
Register(VBStaticText)
