
"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/12/31 20:44:29 $"
"""

from PythonCard import model

class ActionBinderDialog(model.CustomDialog):
    def __init__(self, parent):
        model.CustomDialog.__init__(self, parent)
        self.resource_editor = parent
        
        for inst in self.resource_editor.components.keys():
            if inst not in self.resource_editor.sizingHandleNames:
                self.components.sourceComponent.append(inst)
                self.components.destinationComponent.append(inst)
        
        # if some special setup is necessary, do it here
        # example from samples/dialogs/minimalDialog.py
        # self.components.field1.text = txt

    def on_sourceComponent_select(self, wx_event):
        the_widget = self.resource_editor.components[wx_event.stringSelection]
        self.components.sourceEvent.clear()
        for evt in the_widget._spec.getEventNames():
            self.components.sourceEvent.append(evt)
        self.components.sourceComponent.selected = wx_event.stringSelection
    
    def on_btnApply_mouseClick(self, wx_event):
        sourceComponent = self.components.sourceComponent.stringSelection
        sourceEvent = self.components.sourceEvent.stringSelection
        destinationComponent = self.components.destinationComponent.stringSelection
        destinationFunction = self.components.destinationFunction.text
        if max(len(sourceComponent), len(sourceEvent),
            len(destinationComponent), len(destinationFunction)) == 0:
                return
            
        the_widget = self.resource_editor.components[sourceComponent]
        actionBindings = the_widget.actionBindings
        actionBindings[sourceEvent] = (destinationComponent, destinationFunction)
        self.resource_editor.documentChanged = True

def runDialog(parent):
    dlg = ActionBinderDialog(parent)
    result = dlg.showModal()
    # stick your results into the result dictionary here
    # example from samples/dialogs/minimalDialog.py
    # result.text = dlg.components.field1.text
    dlg.destroy()
    return result
