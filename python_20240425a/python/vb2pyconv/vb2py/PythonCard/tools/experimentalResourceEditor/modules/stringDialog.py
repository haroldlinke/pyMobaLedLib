
"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/10/24 19:21:46 $"
"""

from PythonCard import log, model, resource
import os
import wx

NEWSTRING = 'newString'
SPACER = '  :  '

def stringResourceFromList(stringList):
    desc = "         {\n"

    for s in stringList:
        desc += """         %s:%s,\n""" % (repr(s), repr(stringList[s]))

    # close strings
    desc += "         }\n"
    d = eval(desc)
    return resource.Resource(d)


class StringDialog(model.CustomDialog):
    def __init__(self, aBg, stringList):        
        model.CustomDialog.__init__(self, aBg)
        
        self.parent = aBg
        
        """
        # KEA 2004-08-22
        # workaround/hack to make sure closeField message
        # is processed prior to the dialog being closed
        # this occurs when one of the fields are edited and then
        # the user clicks Ok
        # this hack works because we don't process on_close
        # the first time, but rather delay it by posting a second close message
        self.closeDialog = False
        """
        
        # if some special setup is necessary, do it here
        self.stringList = stringList
        sortedStrings = self.stringList.keys()
        sortedStrings.sort()
        for s in sortedStrings:
            label = self.getLabelFromKey(s)
            self.components.listStrings.append(label)

    def parseStrings(self, rsrc):
        stringList = {}
        for s in rsrc.__dict__:
            stringList[s] = rsrc.__dict__[s]
        return stringList

    def getLabelFromKey(self, key):
        return key + SPACER + self.stringList[key].split('\n')[0]

    def updateItemLabel(self, n, key):
        label = self.getLabelFromKey(key)
        self.components.listStrings.setString(n, label)

    def getStringSelectionKey(self):
        return self.components.listStrings.stringSelection.split()[0]

    def on_fldName_closeField(self, event):
        print "closeField fldName", event.target.text
        newName = event.target.text
        previousName = self.getStringSelectionKey()
        # if the name changes then we have to check to see
        # if the dictionary already has a key with the new
        # name
        if newName in self.stringList:
            # replace?
            pass
        else:
            sel = self.components.listStrings.selection
            self.stringList[newName] = self.stringList[previousName]
            del self.stringList[previousName]
            #self.components.listStrings.setString(sel, newName)
            self.updateItemLabel(sel, newName)

    def on_fldValue_closeField(self, event):
        print "closeField fldValue", event.target.text
        sel = self.components.listStrings.selection
        name = self.getStringSelectionKey()
        self.stringList[name] = event.target.text
        self.updateItemLabel(sel, name)

    def displayItemAttributes(self, s):
        self.components.fldName.text = s
        self.components.fldValue.text = self.stringList[s]

    def on_listStrings_select(self, event):
        self.displayItemAttributes(self.getStringSelectionKey())
            
    def on_btnDelete_mouseClick(self, event):
        sel = self.components.listStrings.selection
        name = self.getStringSelectionKey()
        if sel != -1:
            del self.stringList[name]
            self.components.listStrings.delete(sel)
            if len(self.stringList) > 0:
                if sel > len(self.stringList) - 1:
                    sel = sel - 1
                self.components.listStrings.selection = sel
                self.displayItemAttributes(self.getStringSelectionKey())

    def on_btnNew_mouseClick(self, event):
        s = NEWSTRING
        if s in self.stringList:
            self.components.listStrings.stringSelection = self.getLabelFromKey(s)
        else:
            self.stringList[s] = ''
            sel = len(self.stringList) - 1
            self.components.listStrings.append(s)
            self.components.listStrings.stringSelection = s
            self.updateItemLabel(sel, s)
        self.displayItemAttributes(self.getStringSelectionKey())

    """
    # KEA 2004-08-22
    # experiment to workaround Mac closeField bug
    # ignore for now along with the extra debug print statements in closeField
    # event handlers above
    def on_mouseClick(self, event):
        try:
            print self.closeDialog
            print event.target.name
            print event.target.id
        except:
            pass
        if self.closeDialog:
            event.skip()
        else:
            self.closeDialog = True
            wx.PostEvent(self, event)
    """
        

def stringDialog(parent, rsrc):
    dlg = StringDialog(parent, rsrc)
    result = dlg.showModal()
    if result.accepted:
        result.stringList = stringResourceFromList(dlg.stringList)
    dlg.destroy()
    return result

