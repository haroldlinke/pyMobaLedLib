#!/usr/bin/python

"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2005/12/26 19:08:03 $"
"""

# sample to demonstrate usage of the "helpful" wrappers in helpful.py
from PythonCard import model, helpful

rsrc = {'application':{'type':'Application',
          'name':'testmultibuttondialog',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'Demo of Helpful wrappers',
          'size':(300, 100),
         'components': [

       {'type':'Button',
           'name':'popup',
           'position':(100,10),
           'label':'Test pop-ups!',
           'toolTip':'try this - context-click and the pop-up will appear',
           },

       {'type':'Button',
           'name':'buttons',
           'position':(50,50),
           'label':'Test buttons!',
           },

       {'type':'Button',
           'name':'boxes',
           'position':(150,50),
           'label':'Test boxes!',
           },


] # end components
} # end background
] # end backgrounds
} }

class MyBackground(model.Background):

    def on_initialize(self, event):
        self.boxes = [ ("already", False, 'already has a tooltip'), ("later", True), ("a long string to check sizing", True), "just a string", ("c", True), ("d", True), ("a1", True), ("a2", True), ("a3", True) ]
        pass

    def on_popup_mouseClick(self, event):
        print self.boxes

    def on_popup_mouseContextDown(self, event):
        selected = helpful.popUpMenu(self, ['this', 'set', 'of', 'strings'], self.components.popup.position)
        if selected:
            print "Selected item was '"+selected+"'"
        else:
            print "Nothing selected."

    def on_buttons_mouseClick(self, event):
        result = helpful.multiButtonDialog(self, 'some question', ['OK', 'Not OK', "Cancel"], "Test Dialog Title")
        print "Dialog result:\naccepted: %s\ntext: %s" % (result.accepted, result.text)
        
        result = helpful.multiButtonDialog(self, 'Dad, can I go to the movies tonight', \
               ['Yes', 'No', 'Maybe', ('Ask me later', 'procrastination will be better tomorrow'), 'Ask your mum'], "Movies Dialog Title")
        print "Dialog result:\naccepted: %s\ntext: %s" % (result.accepted, result.text)


    def on_boxes_mouseClick(self, event):
        boxes = [ ("already", False), ("later", True) ]
        result = helpful.multiCheckBoxDialog(self, boxes, "Test Boxes Dialog Title")
        print "Dialog result:\naccepted: %s\n" % (result.accepted), result.boxes
        
        result = helpful.multiCheckBoxDialog(self, self.boxes, "Test Boxes Dialog Title")
        print "Dialog result:\naccepted: %s\n" % (result.accepted), result.boxes
        self.boxes = result.boxes


if __name__ == '__main__':
   app = model.Application(MyBackground, None, rsrc)
   app.MainLoop()
