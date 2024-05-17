
"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/10/24 19:21:46 $"
"""

from PythonCard import model
import os

class StackInfoDialog(model.CustomDialog):
    def __init__(self, aBg, rsrc):        
        model.CustomDialog.__init__(self, aBg)
        
        self.parent = aBg
        
        # if some special setup is necessary, do it here
        self.components.fldName.text = rsrc.application.name

def stackInfoDialog(parent):
    dlg = StackInfoDialog(parent, parent.rsrc)
    result = dlg.showModal()
    result.text = dlg.components.fldName.text
    dlg.destroy()
    return result
