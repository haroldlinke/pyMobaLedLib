# inserts "\t* " before each line in the selection
text = self.currentDocument.GetSelectedText()
unorderedList = ""
for i in text.splitlines(1):
    unorderedList += "\t* " + i

self.currentDocument.ReplaceSelection(unorderedList)
