
"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/10/03 23:58:01 $"
"""

from PythonCard import model

class NewComponentDialog(model.CustomDialog):
    def __init__(self, aBg, original, attributes, offsets, title):
        model.CustomDialog.__init__(self, aBg)
        
        self.parent = aBg
        
        self.title = title
        if title.startswith("New"):
            add = ""
        else:
            add = "Copy"
        self.components.fldName.text = original['name'] + add
        if "label" in attributes:
            self.components.lblLabelOrText.text = "Label:"
            if "label" in original.keys():
                self.components.fldLabelOrText.text = original['label'] + add
            else:
                self.components.fldLabelOrText.text = original['name'] + add
        elif "text" in attributes:
            self.components.lblLabelOrText.text = "Text:"
            if "text" in original.keys():
                self.components.fldLabelOrText.text = original['text'] + add
            else:
                self.components.fldLabelOrText.text = original['name'] + add
        else:
            self.components.lblLabelOrText.visible = False
            self.components.fldLabelOrText.visible = False
            self.components.fldLabelOrText.enabled = False
            
        self.components.chkHorizontal.visible = offsets
        self.components.chkVertical.visible = offsets
    
def newComponentDialog(aBg, original, attributes, offsets, title):
    dlg = NewComponentDialog(aBg, original, attributes, offsets, title)
    result = dlg.showModal()
    if result.accepted:
        result.name = dlg.components.fldName.text
        result.labelortext = dlg.components.fldLabelOrText.text
        result.horizontal = dlg.components.chkHorizontal.checked
        result.vertical = dlg.components.chkVertical.checked
    dlg.destroy()
    return result

