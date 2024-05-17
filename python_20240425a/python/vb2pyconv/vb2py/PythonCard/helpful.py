"""
__version__ = "$Revision: 1.5 $"
__date__ = "$Date: 2006/01/14 12:11:49 $"
"""

# Assorted helpful wrappers.

from PythonCard import model

import wx
import string, copy
import types


# AGT This could probably be generalized some more - but it handles current
#   needs within this wrapper collection of cloning buttons and checkboxes.

# utility functions to manipulate controls at run time
class copyControl:
    def __init__(self, aBg, Name, newname, Text=""):
        Flds = ['position', 'size', 'backgroundColor', 'foregroundColor', 'command', 'font']
        aWidget = aBg.components[Name]
        d = {}
        d['type'] = aWidget.__class__.__name__
        for key in Flds: # attributes
            # I'm not exactly sure why I have to special-case these tuples
            if key == 'bitmap':
                # this should get recreated from the file attribute
                pass
            elif key in ['position', 'size']:
                d[key] = getattr(aWidget, key)
            elif getattr(aWidget, key) is not None:
                d[key] = getattr(aWidget, key)
        if Text == "": Text = newname
        d['label'] = Text
        d['name'] = newname
        aBg.components[newname] = d
        self.name = newname 
       
       
# dialog to present a block of text and a number of alternative buttons
class MultiButtonDialog(model.CustomDialog):
    
    def __init__(self, parent, txt, buttons, rsrc):
        model.CustomDialog.__init__(self, parent, rsrc)
        self.components.Text.text = txt
        self.components.Button.visible = False
        self.components.Button.enabled = False
        if len(buttons) == 0: buttons = ["OK"]
        bx, by = self.components.Button.size
        for b in buttons:
            if isinstance(b, (str,)):
                self.components.Button.label = b
            else:
                self.components.Button.label = b[0]
            
            newx, newy = self.components.Button.GetBestSize()
            bx = max(bx, newx)
            by = max(by, newy)
        self.components.Button.size = (bx, newy)
        dx = bx + 20
        # check if all buttons will fit in window
        owx, owy = self.size
        startx, starty = self.components.Button.position
        if len(buttons)*dx + bx + 40 > owx:
            wx = len(buttons)*dx + bx + 40
            self.size = (wx, owy)
            startx, starty = (wx-bx-20, owy-by-30)   # AGT - why 30 ??
            tsx, tsy = self.components.Text.size
            self.components.Text.size = (wx-20, tsy)
        localbuttons = buttons
        localbuttons.reverse()
        count = 0
        for b in localbuttons:
            if isinstance(b, (str,)):
                theName = b
                theToolTip = ''
            else:
                theName = b[0]
                theToolTip = b[1]
            n = copyControl(self, "Button", "Button"+str(count), theName)
            self.components[n.name].position = startx-count*dx, starty
            self.components[n.name].visible = True
            self.components[n.name].enabled = True
            self.components[n.name].toolTip = theToolTip
            count += 1
        self.accepted = False
        self.text = ""
   
    def on_mouseClick(self, event):
        self.text = event.target.label
        if self.text == "Cancel":
            self.accepted = False
        else:
            self.accepted = True
        self.Close()

def multiButtonDialog(parent, txt, buttons, title=""):
    rsrc = {'type':'CustomDialog',
        'name':'Template',
        'title':'Template',
        'position':(176, 176),
        'size':(367, 230),
        'components': [

        {'type':'StaticText',
            'name':'Text',
            'position':(10, 10),
            'size':(341, 123),
            'actionBindings':{},
            },

        {'type':'Button',
           'name':'Button',
           'position':(269, 145),
           'actionBindings':{},
           'label':'template',
           },

        ] # end components
    } # end CustomDialog
    rsrc["title"] = title
    dlg = MultiButtonDialog(parent, txt, buttons, rsrc)
    result = dlg.showModal()
    result.accepted = dlg.accepted
    result.text = dlg.text
    dlg.destroy()
    return result


# dialog to present a number of on/off checkboxes
class MultiCheckBoxDialog(model.CustomDialog):
    
    # boxes is a list of (name, value) pairs, not a dictionary
    # because a dictionary didn't allow the caller to control the order of presentation
    def __init__(self, parent, boxes, rsrc):
        model.CustomDialog.__init__(self, parent, rsrc)
        self.components.box.visible = False
        self.components.box.enabled = False
        self.components.box.checked = False
        # check if all buttons will fit in window
        owx, owy = self.size
        startx, starty = self.components.box.position
        sx,sy = self.components.box.GetBestSize()
        #rint starty, len(boxes), sy, (len(boxes)-1) * (sy+20), owy
        wy = (len(boxes)+1) * (sy+20) + 30
        self.size = (owx, wy)
            
        count = 0
        self.boxes = {}
        for b in boxes:
            val = False
            toolTip = ''
            if isinstance(b, (str,)):
                key = b
            else:
                key = b[0]
                if len(b) > 1: val = b[1]
                if len(b) > 2: toolTip = b[2]
            n = copyControl(self, "box", "Box"+str(count), key)
            self.components[n.name].position = startx, starty+count*(sy+20)
            self.components[n.name].visible = True
            self.components[n.name].enabled = True
            self.components[n.name].checked = val
            self.components[n.name].toolTip = toolTip
            self.boxes[key] = val
            count += 1
        self.components.btnOK.position = (150, starty+count*(sy+20))
        self.components.btnCancel.position = (250, starty+count*(sy+20))
        self.accepted = False
   
    def on_btnOK_mouseClick(self, event):
        self.accepted = True

        for count in range(len(self.boxes)):
            name = "Box"+str(count)
            self.boxes[self.components[name].label] = self.components[name].checked
        
        self.Close()

    def on_btnCancel_mouseClick(self, event):
        self.accepted = False
        self.Close()

def multiCheckBoxDialog(parent, boxes, title=""):
    rsrc = {'type':'CustomDialog',
        'name':'Template',
        'title':'Template',
        'position':(176, 176),
        'size':(340, 230),
        'components': [

        {'type':'CheckBox',
           'name':'box',
           'position':(50, 15),
           'size':(250,20),
           'actionBindings':{},
           'label':'template',
           },

        {'type':'Button',
           'name':'btnOK',
           'position':(250, 0),
           'actionBindings':{},
           'label':'OK',
           },

        {'type':'Button',
           'name':'btnCancel',
           'position':(320, 0),
           'actionBindings':{},
           'label':'Cancel',
           },

        ] # end components
    } # end CustomDialog
    rsrc["title"] = title
    dlg = MultiCheckBoxDialog(parent, boxes, rsrc)
    result = dlg.showModal()
    result.accepted = dlg.accepted
    result.boxes = dlg.boxes
    dlg.destroy()
    return result

# wrapper to help with pop up menus

class PopUpMenu:
    def __init__(self, aBg, items, pos):
        # Yet another alternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity. 
        self.popup = {}
        self.reverse = {}
        self.selected = None
        # make a menu
        self.menu = wx.Menu()
        # add the items
        for it in items:
            if isinstance(it, (str,)):
                Id = wx.NewId()
                self.popup[it] = Id
                self.reverse[Id] = it
                aBg.Bind(wx.EVT_MENU, self.OnPopup, id=self.popup[it])
                self.menu.Append(self.popup[it], it)
            else:
                # make a menu
                submenu = wx.Menu()
                Id = wx.NewId()
                aBg.Bind(wx.EVT_MENU, self.OnPopup, id=Id)
                for that in it:
                    if isinstance(that, (str,)):
                        Id = wx.NewId()
                        self.popup[that] = Id
                        self.reverse[Id] = that
                        aBg.Bind(wx.EVT_MENU, self.OnPopup, id=self.popup[that])
                        submenu.Append(self.popup[that], that)
                        
                self.menu.AppendMenu(Id, "Test Submenu", submenu)

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        aBg.PopupMenu(self.menu, pos)
        self.menu.Destroy()
               
    def OnPopup(self, event):
        self.selected = self.reverse[event.GetId()]

def popUpMenu(aBg, items, pos):
    menu = PopUpMenu(aBg, items, pos)
    
    return menu.selected
       
