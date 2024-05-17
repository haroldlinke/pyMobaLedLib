
"""
__version__ = "$Revision: 1.7 $"
__date__ = "$Date: 2004/08/22 19:11:35 $"
"""

from PythonCard import dialog, model
import os

class DialogInfoDialog(model.CustomDialog):
    def __init__(self, aBg, rsrc):
        model.CustomDialog.__init__(self, aBg)
        
        self.parent = aBg
        
        # if some special setup is necessary, do it here
        self.components.fldName.text = rsrc.name
        self.components.fldTitle.text = rsrc.title
        self.components.fldPosition.text = str(rsrc.position)
        self.components.fldSize.text = str(rsrc.size)        

def dialogInfoDialog(parent, rsrc):
    dlg = DialogInfoDialog(parent, rsrc)
    result = dlg.showModal()
    if result.accepted:
        result.name = dlg.components.fldName.text
        result.title = dlg.components.fldTitle.text
        result.position = eval(dlg.components.fldPosition.text)
        result.size = eval(dlg.components.fldSize.text)
    dlg.destroy()
    return result
