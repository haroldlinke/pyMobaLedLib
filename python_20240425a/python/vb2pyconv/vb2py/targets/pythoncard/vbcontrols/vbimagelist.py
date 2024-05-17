from vb2py.targets.vb2py.PythonCard.controlclasses import VBWrapped, VBWidget
from vb2py.targets.vb2py.PythonCard import Register
import vb2py.logger
log = vb2py.logger.getLogger("VBImageList")

from vb2py.PythonCard.components import statictext
from wxPython import wx
import sys
from vb2py.PythonCard import event, registry, widget


class VBImageList(VBWidget): 
    __metaclass__ = VBWrapped 

    _translations = { 
            "ListImages" : "items",
    } 

    _name_to_method_translations = {
            "ListCount" : ("getNumber", None),
            "ListIndex" : ("getSelectionIndex", None),
    }

    _indexed_translations = { 
    } 

    _method_translations = {			
    }

    _proxy_for = statictext.StaticText # Not a vb2py.PythonCard object at all but this at least works!

    # << VBImageList methods >>
    pass
    # -- end -- << VBImageList methods >>   

log.debug("Registering VBImageList as '%s'" % sys.modules[__name__].VBImageList)
Register(VBImageList)
