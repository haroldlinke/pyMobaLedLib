from PythonCard import dialog

alertDialogTemplate = """result = dialog.alertDialog(self, 'a message', 'a title')
if result.accepted:
    returned = result.returnedString
"""

colorDialogTemplate = """result = dialog.colorDialog(self)
if result.accepted:
    color = result.color
"""

directoryDialogTemplate = """result = dialog.directoryDialog(self, 'Choose a directory', '')
if result.accepted:
    path = result.path
"""

findDialogTemplate = """result = dialog.findDialog(self)
if result.accepted:
    searchText = result.searchText
    wholeWordsOnly = result.wholeWordsOnly
    caseSensitive = result.caseSensitive
"""

fontDialogTemplate = """result = dialog.fontDialog(self)
if result.accepted:
    color = result.color
    font = result.font
"""

messageDialogTemplate = """result = dialog.messageDialog(self, 'a message', 'a title',
    wx.ICON_INFORMATION | wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL)
if result.accepted:
    returned = result.returnedString
"""

multipleChoiceDialogTemplate = """result = dialog.multipleChoiceDialog(self, "message", "title", ['one', 'two', 'three'])
if result.accepted:
    sel = result.selection
"""

openFileDialogTemplate = """wildcard = "JPG files (*.jpg;*.jpeg)|*.jpg;*.jpeg;*.JPG;*.JPEG|GIF files (*.gif)|*.gif;*.GIF|All Files (*.*)|*.*"
result = dialog.openFileDialog(self, 'Open', '', '', wildcard )
if result.accepted:
    path = result.paths[0]
"""

saveFileDialogTemplate = """wildcard = "JPG files (*.jpg;*.jpeg)|*.jpg;*.jpeg;*.JPG;*.JPEG|GIF files (*.gif)|*.gif;*.GIF|All Files (*.*)|*.*"
result = dialog.saveFileDialog(self, 'Save', '', '', wildcard )
if result.accepted:
    path = result.paths[0]
"""

scrolledMessageDialogTemplate = """dialog.scrolledMessageDialog(self, 'message', 'title')
if result.accepted:
    # you don't really need the accepted test, since there isn't a result
    # to check for a scrolledMessageDialog
    pass
"""

singleChoiceDialogTemplate = """result = dialog.singleChoiceDialog(self, "message", "title", ['one', 'two', 'three'])
if result.accepted:
    sel = result.selection
"""

textEntryDialogTemplate = """result = dialog.textEntryDialog(self, 'message', 'title', 'text')
if result.accepted:
    returned = result.returnedString
    text = result.text
"""


dialogsList = ['alertDialog', 'colorDialog', 'directoryDialog', 
    'findDialog', 'fontDialog', 'messageDialog', 
    'multipleChoiceDialog', 'openFileDialog', 'saveFileDialog', 
    'scrolledMessageDialog', 'singleChoiceDialog', 
    'textEntryDialog']
dialogsList.sort()

result = dialog.singleChoiceDialog(None, "Pick a dialog:", "Dialogs", dialogsList)
if result.accepted:
    dialogText = eval(result.selection + 'Template')
    # could get the current indent and insert the appropriate
    # number of spaces before each line of the template here
    comp.document.ReplaceSelection(dialogText)

