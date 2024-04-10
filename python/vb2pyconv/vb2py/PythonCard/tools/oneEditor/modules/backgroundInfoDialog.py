
"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/10/03 23:58:01 $"
"""

from PythonCard import dialog, model, util
import os

class BackgroundInfoDialog(model.CustomDialog):
    def __init__(self, aBg, rsrc):
        model.CustomDialog.__init__(self, aBg)
        
        self.parent = aBg
        
        # if some special setup is necessary, do it here
        self.components.fldName.text = rsrc.name
        self.components.fldTitle.text = rsrc.title
        self.components.fldPosition.text = str(rsrc.position)
        self.components.fldSize.text = str(rsrc.size)
        self.components.chkStatusBar.checked = rsrc.statusBar
        if rsrc.foregroundColor is not None:
            #self.components.fldForegroundColor.text = colorDescription(rsrc.foregroundColor)
            self.components.fldForegroundColor.text = str(rsrc.foregroundColor)
        if rsrc.backgroundColor is not None:
            #self.components.fldBackgroundColor.text = colorDescription(rsrc.backgroundColor)
            self.components.fldBackgroundColor.text = str(rsrc.backgroundColor)
        if rsrc.image is not None:
            self.components.fldImage.text = rsrc.image
        self.components.chkTiled.checked = rsrc.tiled
        self.components.chkVisible.checked = rsrc.visible
        self.components.chkResizeable.checked = (rsrc.style != [])
            
        if rsrc.icon is not None:
            self.components.fldIcon.text = rsrc.icon

    def on_btnForegroundColor_mouseClick(self, event):
        result = dialog.colorDialog(self, color=util.colorFromString(self.components.fldForegroundColor.text))
        if result.accepted:
            self.components.fldForegroundColor.text = str(result.color)

    def on_btnBackgroundColor_mouseClick(self, event):
        result = dialog.colorDialog(self, color=util.colorFromString(self.components.fldBackgroundColor.text))
        if result.accepted:
            self.components.fldBackgroundColor.text = str(result.color)

    def on_btnFile_mouseClick(self, event):
        result = dialog.openFileDialog()
        if result.accepted:
            path = result.paths[0]
            filename = util.relativePath(self.parent.filename, path)
            self.components.fldImage.text = filename

    def on_btnIconFile_mouseClick(self, event):
        wildcard = "Icon Files (*.ico)|*.ico|XPM Files (*.xpm)|*.xpm|All Files (*.*)|*.*"
        result = dialog.openFileDialog(wildcard=wildcard)
        if result.accepted:
            path = result.paths[0]
            filename = util.relativePath(self.parent.filename, path)
            self.components.fldIcon.text = filename
        

def backgroundInfoDialog(parent, rsrc):
    dlg = BackgroundInfoDialog(parent, rsrc)
    result = dlg.showModal()
    if result.accepted:
        result.name = dlg.components.fldName.text
        result.title = dlg.components.fldTitle.text
        result.position = eval(dlg.components.fldPosition.text)
        result.size = eval(dlg.components.fldSize.text)
        result.statusBar = dlg.components.chkStatusBar.checked
        result.foregroundColor = util.colorFromString(dlg.components.fldForegroundColor.text)
        result.backgroundColor = util.colorFromString(dlg.components.fldBackgroundColor.text)
        if dlg.components.fldImage.text != '':
            result.image = dlg.components.fldImage.text
        else:
            result.image = None
        result.tiled = dlg.components.chkTiled.checked
        result.visible = dlg.components.chkVisible.checked
        if dlg.components.chkResizeable.checked:
            result.style = ['resizeable']
        else:
            result.style = []
        if dlg.components.fldIcon.text != '':
            result.icon = dlg.components.fldIcon.text
        else:
            result.icon = None
    dlg.destroy()
    return result
