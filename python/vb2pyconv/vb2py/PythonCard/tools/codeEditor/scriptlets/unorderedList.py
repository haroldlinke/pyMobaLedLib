# inserts "\t* " before each line in the selection
text = bg.components.document.GetSelectedText()
unorderedList = ""
for i in text.splitlines(1):
    unorderedList += "\t* " + i

bg.components.document.ReplaceSelection(unorderedList)
