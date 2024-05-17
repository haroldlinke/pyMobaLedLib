
"""
__version__ = "$Revision: 1.39 $"
__date__ = "$Date: 2004/09/25 15:37:40 $"
"""

import wx
from wx.lib import dialogs
from font import Font, fontDescription


DialogResults = dialogs.DialogResults

findDialog = dialogs.findDialog
colorDialog = dialogs.colorDialog

def fontDialog(parent, aFont=None):
    if aFont is not None:
        aFont = aFont._getFont()
    result = dialogs.fontDialog(parent, font=aFont)
    if result.accepted:
        fontData = result.fontData
        result.color = result.fontData.GetColour().Get()
        fontWx = result.fontData.GetChosenFont()
        result.fontDescription = fontDescription(fontWx)
        fontWx = None
        result.font = Font(result.fontDescription)
    return result

def passwordTextEntryDialog(parent=None, message='', title='', defaultText='',
                    style=wx.TE_PASSWORD | wx.OK | wx.CANCEL):
    return dialogs.textEntryDialog(parent, message, title, defaultText, style)

def multilineTextEntryDialog(parent=None, message='', title='', defaultText='',
                    style=wx.TE_MULTILINE | wx.OK | wx.CANCEL):
    result = dialogs.textEntryDialog(parent, message, title, defaultText, style)
    # workaround for Mac OS X
    result.text = '\n'.join(result.text.splitlines())
    return result

textEntryDialog = dialogs.textEntryDialog
messageDialog = dialogs.messageDialog
alertDialog = dialogs.alertDialog
scrolledMessageDialog = dialogs.scrolledMessageDialog
fileDialog = dialogs.fileDialog
openFileDialog = dialogs.openFileDialog
saveFileDialog = dialogs.saveFileDialog
directoryDialog = dialogs.directoryDialog
singleChoiceDialog = dialogs.singleChoiceDialog
multipleChoiceDialog = dialogs.multipleChoiceDialog

