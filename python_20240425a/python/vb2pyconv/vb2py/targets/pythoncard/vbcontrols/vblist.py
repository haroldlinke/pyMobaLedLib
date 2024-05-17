from vb2py.targets.vb2py.PythonCard.controlclasses import VBWrapped, VBWidget
from vb2py.targets.vb2py.PythonCard import Register
import vb2py.logger
log = vb2py.logger.getLogger("VBListBox")

from vb2py.PythonCard.components import list
from wxPython import wx
import sys
from vb2py.PythonCard import event, registry, widget


class VBList(VBWidget): 
    __metaclass__ = VBWrapped 

    _translations = { 
            "Text" : "text", 
            "Enabled" : "enabled", 
            "Visible" : "visible", 
            "List" : "items",
    } 

    _name_to_method_translations = {
            "ListCount" : ("getNumber", None),
            "ListIndex" : ("getSelectionIndex", None),
    }

    _indexed_translations = { 
            "Left" : ("position", 0), 
            "Top" : ("position", 1), 
            "Width" : ("size", 0), 
            "Height" : ("size", 1), 
    } 

    _method_translations = {			
            "Clear" : "clear",
            "RemoveItem" : "delete",	
    }

    _proxy_for = list.List

    # << VBList methods >>
    def AddItem(self, item, position=None):
        """Add an item to the list

        We cannot just map this to a vb2py.PythonCard control event because it only has
        an 'append' and an 'insertItems' method, which isn't exactly the same

        """
        if position is None:
            self.append(item)
        else:
            self.insertItems([item], position)
    # -- end -- << VBList methods >>   

log.debug("Registering VBList as '%s'" % sys.modules[__name__].VBList)
Register(VBList)
