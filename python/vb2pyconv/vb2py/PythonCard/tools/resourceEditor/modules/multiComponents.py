#!/usr/bin/python

"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2005/07/27 21:49:41 $"
"""

from PythonCard import dialog, font, model, registry, util
from PythonCard.event import ChangeListener
import resourceOutput
import time
import os
import string

import wx

class MultiComponents(model.Background, ChangeListener):

    def on_initialize(self, event):
        self._parent = self.GetParent()
        self._comp = self._parent.components
        self._updatingComponent = 0
        ##self.components.addChangeEventListener(self)
        self._comp.addChangeEventListener(self)
                
        #self.displayComponents(self.components)
        self.displayComponents(self._comp)
        self.visible = True


    def on_componentSendBack_command(self, event):
        print "no re-layering yet"
        return
        self._parent.on_componentSendBack_command(event)
        
    def on_componentMoveBack_command(self, event):
        print "no re-layering yet"
        return
        self._parent.on_componentMoveBack_command(event)
        
    def on_componentMoveForward_command(self, event):
        print "no re-layering yet"
        return
        self._parent.on_componentMoveForward_command(event)
        
    def on_componentBringFront_command(self, event):
        print "no re-layering yet"
        return
        self._parent.on_componentBringFront_command(event)
        



    def addWidgetToComponentList(self, widget):
        wName = widget.name
        wClass = widget.__class__.__name__
        self.components.wComponentList.Append(wName + "  :  " + wClass)

    # KEA 2002-02-23
    # need to redo the logic below to avoid asserts in hybrid
    # versions of wxPython, but also be cleaner
    def deleteWidgetFromComponentList(self, wName, wClass):
        i = self.components.wComponentList.GetSelection()
        j = self.components.wComponentList.FindString(wName + "  :  " + wClass)
        if i == -1 or i != j:
            if j != -1: 
                self.components.wComponentList.Delete(j)
        else:
            if j > 0:
                self.components.wComponentList.SetSelection(j - 1)
            if j != -1:
                self.components.wComponentList.Delete(j)
            if self.components.wComponentList.GetSelection() == -1:
                self.setValidProps("")
            else:
                wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
                # deselect the name from properties list
                self.setValidProps(wClass)
                self.displayProperties(wName, wClass)

    def changed(self, event):
        print "multi changed", self._parent.multipleSelected, self._parent.multipleComponents


    def clearComponentList(self):
        self.components.wComponentList.Clear()
        self.statusBar.text = ''

    def displayComponents(self, components):
        self.components.wComponentList.Freeze()
        self.components.wComponentList.Clear()
        self._comp = components
        for c in components.order:
            #print "display", c, self._parent.isSizingHandle(c)
            if c not in self._parent.sizingHandleNames and not self._parent.isSizingHandle(c):
                self.addWidgetToComponentList(components[c])
        self.components.wComponentList.Thaw()
        self.components.wComponentList.Refresh()
        self.components.wComponentList.Update()

    def on_close(self, event):
        self.visible = False
        parent = self.GetParent()
        parent.menuBar.setChecked('menuViewPropertyEditor', 0)
