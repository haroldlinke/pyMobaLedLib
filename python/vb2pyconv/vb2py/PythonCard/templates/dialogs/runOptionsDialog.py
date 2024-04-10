
"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/08/12 19:12:39 $"
"""

from PythonCard import model
import os
import wx

class RunOptionsDialog(model.CustomDialog):
    def __init__(self, aBg, cmdLineArgs):
        model.CustomDialog.__init__(self, aBg)
        
        self.parent = aBg
        
        self.components.chkDebugMenu.checked = cmdLineArgs['debugmenu']
        self.components.chkLogging.checked = cmdLineArgs['logging']
        self.components.chkMessageWatcher.checked = cmdLineArgs['messagewatcher']
        self.components.chkNamespaceViewer.checked = cmdLineArgs['namespaceviewer']
        self.components.chkPropertyEditor.checked = cmdLineArgs['propertyeditor']
        self.components.chkShell.checked = cmdLineArgs['shell']
        self.components.fldOtherArgs.text = cmdLineArgs['otherargs']

        self.initSizers()

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        comp = self.components
        
        btnFlags = wx.LEFT | wx.ALIGN_BOTTOM
        vertFlags = wx.LEFT | wx.TOP | wx.ALIGN_LEFT
        fldFlags = wx.LEFT | wx.TOP | wx.ALIGN_CENTER

        sizer4.Add(comp.stcOtherArgs, 0, fldFlags, 5)
        sizer4.Add(comp.fldOtherArgs, 1, fldFlags, 5)

        sizer3.Add(comp.btnOK, 0, btnFlags, 5)
        sizer3.Add(comp.btnCancel, 0, btnFlags, 5)

        sizer2.Add(comp.stcCmdLineArgs, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_TOP, 5)
        sizer2.Add(comp.chkDebugMenu, 0, vertFlags, 5)
        sizer2.Add(comp.chkLogging, 0, vertFlags, 5)
        sizer2.Add(comp.chkMessageWatcher, 0, vertFlags, 5)
        sizer2.Add(comp.chkNamespaceViewer, 0, vertFlags, 5)
        sizer2.Add(comp.chkPropertyEditor, 0, vertFlags, 5)
        sizer2.Add(comp.chkShell, 0, vertFlags, 5)
        sizer2.Add(sizer4, 0, vertFlags)
        sizer2.Add((5, 5), 1)  # spacer
        sizer2.Add(sizer3, 1, wx.ALIGN_BOTTOM)

        sizer1.Add(sizer2, 0, vertFlags)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

def runOptionsDialog(parent, cmdLineArgs):
    dlg = RunOptionsDialog(parent, cmdLineArgs)
    result = dlg.showModal()
    if result.accepted:
        result.debugmenu = dlg.components.chkDebugMenu.checked
        result.logging = dlg.components.chkLogging.checked
        result.messagewatcher= dlg.components.chkMessageWatcher.checked
        result.namespaceviewer = dlg.components.chkNamespaceViewer.checked
        result.propertyeditor = dlg.components.chkPropertyEditor.checked
        result.shell = dlg.components.chkShell.checked
        result.otherargs = dlg.components.fldOtherArgs.text
    dlg.destroy()
    return result
