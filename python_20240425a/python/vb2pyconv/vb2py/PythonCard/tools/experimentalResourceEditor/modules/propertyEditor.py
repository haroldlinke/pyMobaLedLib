#!/usr/bin/python

"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/12/31 20:44:29 $"
"""

from PythonCard import dialog, font, model, registry, util
from PythonCard.event import ChangeListener
import resourceOutput
import time
import os
import string

import wx

# KEA this is a load of dingos' kidneys and needs to be rewritten
# 2002-02-22
# now I'm compounding the problem by porting from the original
# Property Editor to a PythonCard background
class PropertyEditor(model.Background, ChangeListener):

    def on_initialize(self, event):
        self._parent = self.GetParent()
        self._comp = self._parent.components
        self._updatingComponent = 0
        self.autoAttributeUpdate = True
        ##self.components.addChangeEventListener(self)
        self._comp.addChangeEventListener(self)
        
        self.checkItems = ['enabled', 'visible', 'editable', 'checked', 'default', \
            'rules', 'labels', 'ticks', 'horizontalScrollbar']
        self.popItems = ['layout', 'border', 'style', 'alignment', 'stringSelection']
        self.cantModify = ['id', 'name', 'alignment', 'layout', 'style', 'border', \
            'horizontalScrollbar', 'min', 'max', 'columns', 'rules', 'labels', 'ticks']

        self.editItems = [self.components.wField, self.components.wColor,
                          self.components.wFont, self.components.wTextArea,
                          self.components.wChecked, self.components.wPop,
                          self.components.wFile,]        

        # KEA 2001-08-14
        # this was causing an assertion error with the hybrid wxPython
        #self.components.wComponentList.SetSelection(0)
        if self.components.wComponentList.stringSelection == "":
            wClass = ""
        else:
            wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
        self.setValidProps(wClass)
        
        #self.displayComponents(self.components)
        self.displayComponents(self._comp)
        self.visible = True

    # KEA 2004-08-23
    # support updating of attributes without the need
    # for clicking the Update button
    def on_wField_closeField(self, event):
        if self.autoAttributeUpdate:
            self.updateComponent()

    def on_wTextArea_closeField(self, event):
        if self.autoAttributeUpdate:
            self.updateComponent()

    def on_wChecked_mouseClick(self, event):
        if self.autoAttributeUpdate:
            self.updateComponent()

    def on_wPop_select(self, event):
        if self.autoAttributeUpdate:
            self.updateComponent()

    def on_wColor_mouseClick(self, event):
        result = dialog.colorDialog(self, color=util.colorFromString(self.components.wField.text))
        if result.accepted:
            self.components.wField.text = str(result.color)
            if self.autoAttributeUpdate:
                self.updateComponent()

    def on_wFont_mouseClick(self, event):
        wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
        ##widget = self.components[wName]
        widget = self._comp[wName]
        f = widget.font
        if f is None:
            desc = font.fontDescription(widget.GetFont())
            f = font.Font(desc)
        result = dialog.fontDialog(self, f)
        if result.accepted:
            #color = dlg.getColor()
            f = result.font
            #self.components.wField.SetValue("%s;%s" % (f, color))
            self.components.wField.text = "%s" % f
            if self.autoAttributeUpdate:
                self.updateComponent()

    def on_wFile_mouseClick(self, event):
        path, filename = os.path.split(self.components.wField.text)
        result = dialog.openFileDialog(self, directory=path, filename=filename)
        if result.accepted:
            self.components.wField.text = util.relativePath(self._parent.filename, result.paths[0])
            if self.autoAttributeUpdate:
                self.updateComponent()


    def addWidgetToComponentList(self, widget):
        wName = widget.name
        # KEA 2004-01-25
        # just use __name__, the other code must have been something from wxPython 2.3
        #wClass = str(widget.__class__).split('.')
        #self.components.wComponentList.Append(wName + "  :  " + wClass[len(wClass) - 1])
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
                self.hideAllBut(self.components.wField)
            else:
                wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
                # deselect the name from properties list
                self.setValidProps(wClass)
                propName = self.components.wPropertyList.stringSelection
                if propName == "":
                    propName = "name"
                    self.components.wPropertyList.stringSelection = "name"
                self.displayProperty(wName, wClass, propName)

    def selectComponentList(self, wName, wClass):
        self.components.wComponentList.stringSelection = wName + "  :  " + wClass
        self.setValidProps(wClass)
        propName = self.components.wPropertyList.stringSelection
        #print propName
        if propName == "":
            propName = "name"
            self.components.wPropertyList.stringSelection = "name"
        self.displayProperty(wName, wClass, propName)
        c = self._parent.components[wName]
        if hasattr(c, 'position'):
            # AB 2004-12-31
            # Don't set a tooltip pos for components that don't have a pos - they aren't displayed.
            self._parent.setToolTipDrag(wName, c.position, c.size)

    def changed(self, event):
        ##comp = self.components
        if self._updatingComponent:
            # KEA 2003-01-04
            # hack to speed up updates in place
            return

        comp = self._comp
        wName, wClass = event.getOldValue().split(",")
        if wName in comp:
            # new item added
            self.addWidgetToComponentList(comp[wName])
        else:
            # item deleted
            self.deleteWidgetFromComponentList(wName, wClass)

    """
    def on_wCopy_mouseClick(self, event):
        wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
        # what needs to happen here is to have a method for the Widget class that
        # will provide a valid resource description, each subclass of widget would
        # override the method to deal with their specific resource attributes
        # the Widget class should provide some ordering so that 'type',
        # 'position', 'size' comes before less commonly used items, the actual
        # ordering could just be defined in a list, so it is easy to change
        # also, if the current values match the defaults for a widget attribute
        # then that attribute should not be provided as part of the output
        print "this is just a placeholder method right now,"
        print "the resource is not actually copied to the clipboard yet"
        pprint.pprint(self._comp[wName])
    """

    def on_wUpdate_mouseClick(self, event):
        self.updateComponent()

    def updateComponent(self):
        wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
        propName = self.components.wPropertyList.stringSelection
        
        if propName in self.checkItems:
            value = self.components.wChecked.checked
        elif propName in self.popItems:
            value = self.components.wPop.stringSelection
        elif propName in ('items', 'userdata') or (wClass == 'TextArea' and propName == 'text'):
            value = self.components.wTextArea.text
        else:
            #value = self.components.wField.GetValue()
            value = self.components.wField.text

        if propName not in ['label', 'stringSelection', 'text', 'toolTip', 'userdata']:
            try:
                value = eval(value)
            except:
                pass

        # KEA 2004-05-10
        # need to figure out where to stick validation code
        # but for now just need to make sure that if we're changing the name
        # attribute that it is valid, but similar checks will be necessary for
        # integer fields, a list of items, etc.
        # also maybe each attribute should have a doc or help string displayed
        # saying what the attribute does, example values, etc.
        if propName == 'name':
            badValue = False
            # if it isn't valid then display an alert and exit
            # must start with a letter and only contain alphanumeric characters
            if value == "" or value[0] not in string.ascii_letters:
                badValue = True
            else:
                alphanumeric = string.ascii_letters + string.digits
                for c in value:
                    if c not in alphanumeric:
                        badValue = True
                        break
            if badValue:
                dialog.alertDialog(None, "Name must start with a letter and only contain letters and numbers.", 'Error: Name is invalid')
                self.components.wField.setFocus()
                self.components.wField.setSelection(-1, -1)
                return
            # check for duplicate names is done below

        ##widget = self.components[wName]
        widget = self._comp[wName]

        # KEA 2002-02-23
        # I can't remember why this is actually necessary
        if propName == 'size':
            width, height = value
            if wClass not in ['BitmapCanvas', 'HtmlWindow']:
                bestWidth, bestHeight = widget.GetBestSize()
                if width == -1:
                    width = bestWidth
                if height == -1:
                    height = bestHeight
            widget.size = (width, height)
            #setattr(widget, propName, (width, height))
            #print widget.size, propName, width, height
        else:
            if (propName in self.cantModify) or \
               (propName == 'items' and wClass == 'RadioGroup'):
                order = self._comp.order.index(wName)
                desc = resourceOutput.widgetAttributes(self._parent, widget)
                if desc.endswith(',\n'):
                    desc = eval(desc[:-2])
                else:
                    desc = eval(desc)

                if propName == 'name':
                    if value == wName:
                        # user didn't actually change the name
                        return
                    elif value in self._comp:
                        # we already have a component with that name
                        dialog.alertDialog(self, 'Another component already exists with the name ' + value,
                                           'Error: unable to rename component')
                        return
                if value is None:
                    desc[propName] = 'none'
                elif propName in ['min', 'max']:
                    desc[propName] = int(value)
                else:
                    desc[propName] = value

                # need to experiment with freeze and thaw to avoid
                # a lot of update events
                startTime = time.time()

                # this is going to trigger a changed event
                # as we delete the old component
                self._updatingComponent = True
                del self._comp[wName]
                if propName == 'name':
                    wName = value
                # this is going to trigger another changed event
                # as we create a new component with the changed attribute
                self._comp[wName] = desc
                c = self._comp[wName]
                wx.EVT_LEFT_DOWN(c, self._parent.on_mouseDown)
                wx.EVT_LEFT_UP(c, self._parent.on_mouseUp)
                wx.EVT_MOTION(c, self._parent.on_mouseDrag)


                # now restore the order of the component
                # have to update the startName in case the name was updated
                if propName == 'name':
                    self._parent.startName = wName
                self._comp.order.remove(wName)
                self._comp.order.insert(order, wName)

                self._parent.fixComponentOrder(wName)

                self._updatingComponent = False
                
                endTime = time.time()
                #print "attribute change took:", endTime - startTime
            else:
                if wClass in ['Image', 'ImageButton'] and propName == 'file':
                    cwd = os.getcwd()
                    try:
                        os.chdir(self._parent.filename)
                    except:
                        pass
                    setattr(widget, propName, value)
                    os.chdir(cwd)
                else:
                    setattr(widget, propName, value)
                    #print propName, value
        # KEA 2002-02-23
        self._parent.showSizingHandles(wName)

    def setValidProps(self, wClass):
        #print "setValidProps", wClass
        oldProp = self.components.wPropertyList.stringSelection
        if wClass == "":
            self.components.wPropertyList.Clear()
        else:
            ##props = self.propList + self.optionalProps[wClass]
            ##props.sort()
            ##print "props", props
            # get the property (attribute) list from the spec
            klass = registry.Registry.getInstance().getComponentClass(wClass)
            props = klass._spec.getAttributes().keys()

            # KEA 2002-03-24
            # only show the 'id' attribute for Button
            # and only when displaying dialog properties
            if not (self._parent.editingDialog and wClass == 'Button'):
                # AB 2004-12-31
                # The id attrib is optional, and may not be present. All widgets will have
                # IDs, but Components may not. If it is not present, then we don't need to remove it.
                if 'id' in props:
                    props.remove('id')
            
            # AB 2004-12-31
            # Don't show the action bindings at all. Edit them only via the action binding dialog.
            if 'actionBindings' in props:
                props.remove('actionBindings')
            props.sort()
            ##print "spec props", specProps
            
            self.components.wPropertyList.Clear()
            self.components.wPropertyList.InsertItems(props, 0)
            if oldProp in props:
                self.components.wPropertyList.stringSelection = oldProp

    def hideAllBut(self, widget):
        for w in self.editItems:
            if widget.id != w.id:
                w.visible = False

    def displayProperty(self, wName, wClass, propName):
        self.components.wName.text = propName + ":"
        ##widget = self.components[wName]
        widget = self._comp[wName]
        if propName in ['label', 'stringSelection', 'text', 'toolTip'] or propName in self.checkItems:
            value = getattr(widget, propName)
        else:
            value = str(getattr(widget, propName))
        
        if propName in self.checkItems:
            self.hideAllBut(self.components.wChecked)
            self.components.wChecked.visible = True
            self.components.wChecked.checked = value
        elif propName in self.popItems:
            self.hideAllBut(self.components.wPop)
            self.components.wPop.visible = True
            self.components.wPop.Clear()
            if propName == 'stringSelection':
                for v in widget.items:
                    self.components.wPop.Append(v)
            else:
                for v in widget._spec.getAttributes()[propName].values:
                    self.components.wPop.Append(v)
            try:
                self.components.wPop.stringSelection = value
            except:
                # if value is empty or doesn't already exist
                pass
        elif propName in ('items', 'userdata') or (wClass == 'TextArea' and propName == 'text'):
            #print 'displaying TextArea'
            self.hideAllBut(self.components.wTextArea)
            self.components.wTextArea.visible = True
            self.components.wTextArea.text = value
        else:
            self.hideAllBut(self.components.wField)
            self.components.wField.visible = True
            if propName == 'foregroundColor' or propName == 'backgroundColor':
                self.components.wColor.visible = True
            elif propName == 'font':
                self.components.wFont.visible = True
            elif propName == 'file':
                self.components.wFile.visible = True
            self.components.wName.text = propName + ":"
                    
            # KEA 2002-02-23
            # I can't remember why this is actually necessary
            if propName == 'size':
                width, height = getattr(widget, propName)
                if wClass not in ['BitmapCanvas', 'HtmlWindow']:
                    bestWidth, bestHeight = widget.GetBestSize()
                    if width == bestWidth:
                        width = -1
                    if height == bestHeight:
                        height = -1
                size = (width, height)
                value = str(size)

            self.components.wField.text = value
        # this should only display if the attribute is settable
        # so name, alignment, and others are read-only
        # KEA 2002-02-23
        # wUpdate is always visible now
        self.components.wUpdate.visible = True

    def on_wComponentList_select(self, event):
        #print 'selectComponentListEvent: %s\n' % event.GetString()
        wName, wClass = event.GetString().split("  :  ")
        # change the wPropertiesList to only show relevant properties
        # either display the name by default or try and preserve the
        # wPropertiesList selection and display that item, so for example
        # you could look at size for all widgets, simply by going up and down
        # the components list
        self.setValidProps(wClass)
        propName = self.components.wPropertyList.stringSelection
        #print propName
        if propName == "":
            propName = "name"
            self.components.wPropertyList.stringSelection = "name"
        self.displayProperty(wName, wClass, propName)
        c = self._parent.components[wName]
        if hasattr(c, 'position'):
            self._parent.showSizingHandles(wName)
            self._parent.setToolTipDrag(wName, c.position, c.size)

    def on_wPropertyList_select(self, event):
        propName = event.GetString()
        wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
        if wName != "":
            self.displayProperty(wName, wClass, propName)

    def clearComponentList(self):
        self.components.wComponentList.Clear()
        self.statusBar.text = ''

    def clearPropertyList(self):
        self.components.wPropertyList.Clear()

    def displayComponents(self, components):
        self.components.wComponentList.Freeze()
        self.components.wComponentList.Clear()
        self._comp = components
        for c in components.order:
            if c not in self._parent.sizingHandleNames:
                self.addWidgetToComponentList(components[c])
        self.components.wComponentList.Thaw()
        self.components.wComponentList.Refresh()
        self.components.wComponentList.Update()

    def on_close(self, event):
        self.visible = False
        parent = self.GetParent()
        parent.menuBar.setChecked('menuViewPropertyEditor', 0)
