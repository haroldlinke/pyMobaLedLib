# inserts "\t* " before each line in the selection
text = bg.components.fldDocument.getStringSelection()
unorderedList = ""
for i in text.splitlines(1):
    unorderedList += "\t* " + i

bg.components.fldDocument.replaceSelection(unorderedList)
