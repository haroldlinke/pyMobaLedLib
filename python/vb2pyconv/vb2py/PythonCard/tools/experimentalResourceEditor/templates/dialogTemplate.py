
"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/10/24 19:21:46 $"
"""

from PythonCard import model

class MyDialog(model.CustomDialog):
    def __init__(self, parent, txt=''):
        model.CustomDialog.__init__(self, parent)
        
        # if some special setup is necessary, do it here
        # example from samples/dialogs/minimalDialog.py
        # self.components.field1.text = txt

#def myDialog(parent, txt):
def myDialog(parent):
    dlg = MyDialog(parent, txt)
    result = dlg.showModal()
    # stick your results into the result dictionary here
    # example from samples/dialogs/minimalDialog.py
    # result.text = dlg.components.field1.text
    dlg.destroy()
    return result
