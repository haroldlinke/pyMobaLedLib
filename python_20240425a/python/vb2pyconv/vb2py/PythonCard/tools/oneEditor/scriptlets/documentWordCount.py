import wx
from PythonCard import dialog, util

def wordCount(text):
    chars = len(text)
    words = len(text.split())
    # this doesn't always match the getNumberOfLines() method
    # so this should probably be changed
    lines = len(text.splitlines())
    return chars, words, lines

if self.currentPage.documentPath is None:
    filename = 'Untitled'
else:
    filename = os.path.basename(self.currentPage.documentPath)

dialog.messageDialog(self, "Document: %s\n" % filename + "%d chars, %d words, %d lines" % wordCount(util.normalizeEOL(self.currentDocument.text)), 'Word Count', wx.ICON_INFORMATION | wx.OK)
