
"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/08/12 19:12:39 $"
"""

from PythonCard import dialog, model

class FindDialog(model.CustomDialog):
    def __init__(self, aBg, searchText='', wholeWordsOnly=0, caseSensitive=0, 
                    searchField=None, searchableFields=None):
        model.CustomDialog.__init__(self, aBg)
        
        self.parent = aBg
        
        # if some special setup is necessary, do it here
        self.components.fldFind.text = searchText
        self.components.chkMatchWholeWordOnly.checked = wholeWordsOnly
        self.components.chkMatchCase.checked = caseSensitive
        if searchableFields is None:
            self.components.popSearchField.visible = False
        else:
            searchableFields.insert(0, 'All')
            self.components.popSearchField.items = searchableFields
            if searchField is None:
                self.components.popSearchField.stringSelection = 'All'
            else:
                self.components.popSearchField.stringSelection = searchField
        self.components.fldFind.setSelection(0, len(self.components.fldFind.text))
        #self.components.fldFind.SetMark(-1, -1)
        self.components.fldFind.setFocus()

def findDialog(parent, searchText='', wholeWordsOnly=0, caseSensitive=0, 
                searchField=None, searchableFields=None):
    dlg = FindDialog(parent, searchText, wholeWordsOnly, caseSensitive, 
                        searchField, searchableFields)
    result = dlg.showModal()
    result.searchText= dlg.components.fldFind.text
    result.wholeWordsOnly = dlg.components.chkMatchWholeWordOnly.checked
    result.caseSensitive = dlg.components.chkMatchCase.checked
    sel = dlg.components.popSearchField.stringSelection
    if searchableFields is None or sel == 'All':
        result.searchField = None
    else:
        result.searchField = sel
    dlg.destroy()
    return result

