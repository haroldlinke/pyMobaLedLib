
"""
__version__ = "$Revision: 1.17 $"
__date__ = "$Date: 2005/11/02 12:14:33 $"
"""

from PythonCard import dialog, model, util, helpful
import os

import wx

### map wxWindowStyle constants to nice strings
styleNames = [ ('wx.MINIMIZE_BOX', 'Include Minimize box'),
               ('wx.CAPTION', 'Include Caption'),
               ('wx.MAXIMIZE_BOX', 'Include Maximize box'),
               ('wx.CLOSE_BOX', 'Include Close box'),
               ('wx.STAY_ON_TOP', 'Stay on top'),
               ('wx.SYSTEM_MENU', 'Include System Menu'),
               ('wx.RESIZE_BORDER', 'Include resize border'),
               ('wx.FRAME_TOOL_WINDOW', 'Toolbar size frame'),
               ('wx.FRAME_SHAPED', 'Frame can be shaped') ]
              

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
        self.components.btnCustomize.visible = False
        self.components.btnCustomize.enabled = False
        if rsrc.style == []:
            self.components.windowStyle.stringSelection = 'Static'
        elif rsrc.style == ['resizeable']:
            self.components.windowStyle.stringSelection = 'Resizeable'
        else:
            self.components.windowStyle.stringSelection = 'Custom'
            self.components.btnCustomize.visible = True
            self.components.btnCustomize.enabled = True
        self.style = rsrc.style

        if rsrc.icon is not None:
            self.components.fldIcon.text = rsrc.icon

    def on_windowStyle_select(self, event):
        if self.components.windowStyle.stringSelection <> 'Custom':
            self.components.btnCustomize.visible = False
            self.components.btnCustomize.enabled = False
            return
        self.components.btnCustomize.visible = True
        self.components.btnCustomize.enabled = True
        self.on_btnCustomize_mouseClick(event)

    def on_btnCustomize_mouseClick(self, event):
        styleBoxes = []
        for s,text in styleNames:
            styleBoxes.append( (s, s in self.style, text) )
        
        result = helpful.multiCheckBoxDialog(self, styleBoxes, "Define Custom Window Styles")
        if result.accepted:
            self.style = []
            for s,val  in result.boxes.iteritems():
                if val: self.style.append( s )
    
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
        if dlg.components.windowStyle.stringSelection == 'Static':
            result.style = []
        elif dlg.components.windowStyle.stringSelection == 'Resizeable':
            result.style = ['resizeable']
        else:
            result.style = dlg.style
        if dlg.components.fldIcon.text != '':
            result.icon = dlg.components.fldIcon.text
        else:
            result.icon = None
    dlg.destroy()
    return result
