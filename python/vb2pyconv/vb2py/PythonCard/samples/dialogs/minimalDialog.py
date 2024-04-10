
"""
__version__ = "$Revision: 1.7 $"
__date__ = "$Date: 2004/08/12 19:18:51 $"
"""

from PythonCard import model

class MinimalDialog(model.CustomDialog):
    def __init__(self, parent, txt=''):
        model.CustomDialog.__init__(self, parent)
        
        # if some special setup is necessary, do it here
        self.components.field1.text = txt

def minimalDialog(parent, txt):
    dlg = MinimalDialog(parent, txt)
    result = dlg.showModal()
    result.text = dlg.components.field1.text
    dlg.destroy()
    return result
