#!/usr/bin/python

"""
__version__ = "$Revision: 1.5 $"
__date__ = "$Date: 2005/10/27 22:54:41 $"
"""

from PythonCard import dialog, font, model, registry, util
from PythonCard.event import ChangeListener
import multiresourceOutput
import time
import os
import string

import wx

DO_TRICKY_NAME_DERIVATIONS = True

# KEA this is a load of dingos' kidneys and needs to be rewritten
# 2002-02-22
# now I'm compounding the problem by porting from the original
# Property Editor to a PythonCard background
class PropertyEditor(model.Background, ChangeListener):

    def on_initialize(self, event):
        self._parent = self.GetParent()
        self._comp = self._parent.components
        self._updatingComponent = 0
        ##self.components.addChangeEventListener(self)
        self._comp.addChangeEventListener(self)

        self.checkItems = ['enabled', 'visible', 'editable', 'checked', 'default', \
                            'allowNameLabelVariation', \
                            'rules', 'labels', 'ticks', 'horizontalScrollbar']
        self.popItems = ['layout', 'border', 'style', 'alignment', 'stringSelection']
        self.cantModify = ['id', 'name', 'alignment', 'layout', 'style', 'border', \
            'horizontalScrollbar', 'min', 'max', 'columns', 'rules', 'labels', 'ticks']

        self.standardProps = ['name', 'allowNameLabelVariation', \
                            'enabled', 'visible', 'checked', 'backgroundColor', 'foregroundColor',
                            'font', 'position', 'size', 'label', 'text']

        self.standardPrefixes = ["txt", "fld", "btn", "chk", "pop", "clr", "fnt"]
        
        self.compOrderControls = ['SendToBack', 'MoveBack', 
                                  'reLayer', 'MoveTogether', 
                                  'MoveForward', 'SendToFront']
        
        self.multiCompControls = ['stbAlign', 
                                'alignRight', 'alignLeft', 'alignTop', 'alignBottom', 
                                'alignVerticalCentres','alignHorizontalCentres',
                                'stbEqualize',
                                'equalWidth', 'equalHeight', 'equalBoth',
                                'stbDistribute', 
                                'distHorizFirstLast', 'distHorizEdge', 
                                'distVertFirstLast', 'distVertEdge', ]
##                                'stbNudge', 'nudgeDistance',
##                                'nudgeLeft', 'nudgeRight',
##                                'nudgeUp', 'nudgeDown'
##                                ]

        # KEA 2001-08-14
        # this was causing an assertion error with the hybrid wxPython
        #self.components.wComponentList.SetSelection(0)
        if self.components.wComponentList.stringSelection == "":
#multicol        if self.components.wComponentList.getStringSelection() == []:
            wClass = ""
        else:
            wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
#multicol            wName, wClass = self.components.wComponentList.getStringSelection()[0].split("  :  ")
        self.setValidProps(wClass)
                
        #self.displayComponents(self.components)
        self.displayComponents(self._comp)
        self.visible = True

    # these functions for adding dynamically any property fields
    # not used for "standard" items, and used once only for others
    #  thereafter, use hiding and repositioning. 
    def add_field(self, pType, name, pos, siz, text, align):
        self.components[name] = {'type':pType,
                                 'name':name,
                                 'position':pos,
                                 'size':siz,
                                 'alignment':align,
                                 'text':text}

    def add_chk(self, name, pos, siz):
        # NB - set the command option to trigger the event
        self.components[name] = {'type':"CheckBox",
                                 'name':name,
                                 'position':pos,
                                 'command':'checkedProperty',
                                 'size':siz}

    def add_pop(self, name, pos, siz):
        #rint "add_pop", name, pos, siz
        self.components[name] = {'type':"Choice",
                                 'name':name,
                                 'position':pos,
                                 'size':siz}

    def add_btnFile(self, name, pos, siz):
        # NB - set the command option to trigger the event
        self.components[name] = {'type':"Button",
                                 'name':name,
                                 'position':pos,
                                 'label':"File...",
                                 'command':'btnFile',
                                 'size':siz}


    def on_componentSendBack_command(self, event):
        self._parent.on_componentSendBack_command(event)
        
    def on_componentMoveBack_command(self, event):
        self._parent.on_componentMoveBack_command(event)
 
    def on_componentMoveTogether_command(self, event):
        self._parent.on_componentMoveTogether_command(event)
        
    def on_componentRelayer_command(self, event):
        self._parent.on_componentRelayer_command(event)

    def on_componentMoveForward_command(self, event):
        self._parent.on_componentMoveForward_command(event)
        
    def on_componentBringFront_command(self, event):
        self._parent.on_componentBringFront_command(event)
        

    # KEA 2004-08-23
    # support updating of attributes without the need
    # for clicking the (no longer existent) Update button   
    def on_closeField(self, event):
        which = event.target.name.replace("fld", "")
        self.updateComponent(which)

    def on_checkedProperty_command(self, event):
        which = event.target.name.replace("chk", "")
        self.updateComponent(which)

    def on_select(self, event):
        which = event.target.name.replace("pop", "")
        self.updateComponent(which)

    def on_color_command(self, event):
        which = event.target.name.replace("clr", "")
        result = dialog.colorDialog(self, color=util.colorFromString(self.components["fld"+which].text))
        if result.accepted:
            self.components["fld"+which].text = str(result.color)
            self.components["clr"+which].backgroundColor = util.colorFromString(self.components["fld"+which].text)
            self.updateComponent(which)

    def on_changeFont_command(self, event):
        which = event.target.name.replace("fnt", "")
        wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
#multicol        wName, wClass = self.components.wComponentList.getStringSelection()[0].split("  :  ")
        widget = self._comp[wName]
        f = widget.font
        if f is None:
            desc = font.fontDescription(widget.GetFont())
            f = font.Font(desc)
        result = dialog.fontDialog(self, f)
        if result.accepted:
            f = result.font
            self.components["fld"+which].text = "%s" % f
            self.updateComponent(which)

    def on_btnFile_command(self, event):
        which = event.target.name.replace("btn", "")
        path, filename = os.path.split(self.components["fld"+which].text)
        result = dialog.openFileDialog(self, directory=path, filename=filename)
        #rint result.paths[0]
        if result.accepted:
            self.components["fld"+which].text = util.relativePath(self._parent.filename, result.paths[0])
            self.updateComponent(which)


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

    def updateComponentList(self):
        if not self._parent.multipleSelected:
            return
        self.components.alphabetizeComponents.enabled = False
######  multicol
######        lastList = self.components.wComponentList.getStringSelection()
######        if lastList: 
######            for last in lastList:
######                self.components.wComponentList.SetStringSelection(last, 0)
######                #print "un setting", self.components.wComponentList.SetStringSelection(last, 0)
######        self.components.wComponentList.SetStringSelection(wName + "  :  " + wClass)
######        #print "setting", self.components.wComponentList.SetStringSelection(wName + "  :  " + wClass)
        self.components.wComponentList.Clear()
        self.PropertyListClear()
        for c in self.multiCompControls:
            self.components[c].visible = True
        for c,pref in self._parent.multipleComponents:
            self.addWidgetToComponentList(self._comp[c])                


    def selectComponentList(self, wName, wClass):
        if self._parent.multipleSelected:
            for c in self.multiCompControls:
                self.components[c].visible = False
             
        self.components.wComponentList.stringSelection = wName + "  :  " + wClass
######  multicol
######        lastList = self.components.wComponentList.getStringSelection()
######        if lastList: 
######            for last in lastList:
######                self.components.wComponentList.SetStringSelection(last, 0)
######                #print "un setting", self.components.wComponentList.SetStringSelection(last, 0)
######        self.components.wComponentList.SetStringSelection(wName + "  :  " + wClass)
######        #print "setting", self.components.wComponentList.SetStringSelection(wName + "  :  " + wClass)
        self.setValidProps(wClass)
        
        self.components.chkallowNameLabelVariation.checked = not DO_TRICKY_NAME_DERIVATIONS
        self.displayProperties(wName, wClass)
        c = self._parent.components[wName]
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
            if not self._parent.isSizingHandle(wName):
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

    def on_chkallowNameLabelVariation_mouseClick(self, event):
        if not self.components.chkallowNameLabelVariation.checked:
            # no longer allow them to be different
            # should we allow user to choose which one to keep ?
            # resolve if they are currently different
            # or simply leave as is ?
            wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
            if 'label'  in self.propertyList:
                propName = 'label'
                deriveName = self._parent.convertToValidName(self._comp[wName].label)            
            else:
                propName = 'text'
                deriveName = self._parent.convertToValidName(self._comp[wName].text)
            # do they already match ?
            if wName == deriveName:
                self.components.chkallowNameLabelVariation.checked = False
                return
                
            result = dialog.messageDialog(self, 
                                'Do you want '+propName+' to revert to reflect the name: '+wName,
                                'Empty '+propName,
                                wx.ICON_QUESTION | wx.YES_NO | wx.NO_DEFAULT)
            if result.accepted:
                self.components['fld'+propName].text = wName
                # temporarily allow diff name/label to allow update to happen, then revert
                self.components.chkallowNameLabelVariation.checked = True
                self.updateComponent(propName)
                self.components.chkallowNameLabelVariation.checked = False
            else:
                self.components.chkallowNameLabelVariation.checked = True

    def updateComponent(self, which):
        wName, wClass = self.components.wComponentList.stringSelection.split("  :  ")
        propName = which
        
        if propName in self.checkItems:
            value = self.components["chk"+propName].checked
        elif propName in self.popItems:
            value = self.components["pop"+propName].stringSelection
        elif propName in ('items', 'userdata') or (wClass == 'TextArea' and propName == 'text'):
            value = self.components["fld"+propName].text
        else:
            value = self.components["fld"+propName].text

        if propName == "textArea": propName = 'text'
        if propName not in ['name', 'label', 'stringSelection', 'text', 'toolTip', 'userdata']:
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
                dialog.alertDialog(None, "Name must start with a letter and only contain letters and numbers.", 
                                         'Error: Name is invalid')
                self.components["fld"+which].text = wName
                self.components["fld"+which].setFocus()
                self.components["fld"+which].setSelection(-1, -1)
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
        else:
            if (propName in self.cantModify) or \
               (propName == 'items' and wClass == 'RadioGroup') or \
               (propName in ['label', 'text']):
                if (propName == 'layout'):
                    xx,yy = widget.size
                    widget.size = yy, xx
                    
                order = self._comp.order.index(wName)
                desc = multiresourceOutput.widgetAttributes(self._parent, widget)
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
                        self.components["fldname"].text = wName
                        self.components["fldname"].setFocus()
                        self.components["fldname"].setSelection(-1, -1)
                        return
                if propName in ['label', 'text']:
                    if not self.components.chkallowNameLabelVariation.checked: 
                        if value == "":
                            result = dialog.messageDialog(self, 
                                'To set '+propName+' to be empty, you must allow Name and '+propName+' to differ.\n'+
                                'Do you want to allow that ?', 'Empty '+propName,
                                wx.ICON_QUESTION | wx.YES_NO | wx.NO_DEFAULT)
                            if result.accepted:
                                self.components.chkallowNameLabelVariation.checked = True
                                desc[propName] = value
                            else:
                                # don't allow this change
                                #self.components["fldname"].text = wName
                                self.components["fld"+propName].text = desc[propName]      
                                self.components["fld"+propName].setFocus()
                                self.components["fld"+propName].setSelection(-1, -1)   
                                return
                        else:
                            oldval = desc[propName]
                            desc[propName] = value
                            self._parent.deriveNameFromLabel(desc)
                                
                            if desc['name'] in self._comp:
                                # we already have a component with that name
                                dialog.alertDialog(self, 'Another component already exists with the name ' + value,
                                                   'Error: unable to rename component')
                                desc['name'] = wName
                                desc[propName] = oldval
                                self.components["fldname"].text = wName
                                self.components["fld"+propName].text = desc[propName]      
                                self.components["fld"+propName].setFocus()
                                self.components["fld"+propName].setSelection(-1, -1)   
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
                if propName in ['name']:
                    if not self.components.chkallowNameLabelVariation.checked: self._parent.deriveLabelFromName(desc)
                    wName = desc['name']
                elif propName in ['label', 'text']:
                    if not self.components.chkallowNameLabelVariation: self._parent.deriveNameFromLabel(desc)
                    wName = desc['name']

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
        
        # and check if we now have matching name/label, and if so, assume they now maintain derivation
        self.determineNameLabelState(wName)
        
    def determineNameLabelState(self, wName):
        if 'label' in self.propertyList:
            deriveName = self._parent.convertToValidName(self._comp[wName].label)
            #rint wName, (self._comp[wName].label)
        elif 'text' in self.propertyList: 
            deriveName = self._parent.convertToValidName(self._comp[wName].text)
            #rint wName, (self._comp[wName].text)
        else:
            return
        if wName <> deriveName or not DO_TRICKY_NAME_DERIVATIONS:
            self.components["chkallowNameLabelVariation"].checked = True
            

    def setValidProps(self, wClass):
        if wClass == "":
            self.PropertyListClear()
        else:
            # get the property (attribute) list from the spec
            klass = registry.Registry.getInstance().getComponentClass(wClass)
            props = klass._spec.getAttributes().keys()

            # KEA 2002-03-24
            # only show the 'id' attribute for Button
            # and only when displaying dialog properties
            if not (self._parent.editingDialog and wClass == 'Button'):
                props.remove('id')
            props.sort()
            ##print "spec props", specProps
            
            self.PropertyListClear()
            self.PropertyListInsertItems(props)

    def PropertyListClear(self):
        self.propertyList = []
        for name, c in self.components.iteritems():
            prefix = name[:3]
            if prefix in self.standardPrefixes:
                self.components[name].visible = False
                self.components[name].enabled = False

    def PropertyListInsertItems(self, props):
        self.propertyList = props
               

    def updateSingleProperty(self, wName, propName, newValue):
        wClass = wName.__class__.__name__
        if propName in ['label', 'stringSelection', 'text', 'toolTip'] or propName in self.checkItems:
            newValue = newValue #getattr(widget, propName)
        else:
            newValue = str(newValue) #str(getattr(widget, propName))

        if propName in self.checkItems:
            self.components["chk"+propName].checked = newValue
        elif propName in self.popItems:
            self.components["pop"+propName].Clear()
            if propName == 'stringSelection':
                for v in widget.items:
                    self.components["pop"+propName].Append(v)
            else:
                for v in widget._spec.getAttributes()[propName].values:
                    self.components["pop"+propName].Append(v)
            try:
                self.components["pop"+propName].stringSelection = newValue
            except:
                # if value is empty or doesn't already exist
                pass
        elif propName in ('items', 'userdata') or (wClass == 'TextArea' and propName == 'text'):
            self.components["fld"+propName].text = newValue
        else:
            self.components["fld"+propName].text = newValue

        
    def displayProperties(self, wName, wClass):
        maxy = 0
        for theprop in self.standardProps:
            prop = theprop
            if prop == "text" and wClass == "TextArea": prop = "textArea"
            if prop in self.propertyList:
                vis = True
            else:
                vis = False
            for prefix in self.standardPrefixes:
                if prefix+prop in self.components.iterkeys():
                    self.components[prefix+prop].visible = vis
                    self.components[prefix+prop].enabled = vis
                    maxy = max(maxy, self.components[prefix+prop].position[1])
                    #rint self.components[prefix+prop].name, self.components[prefix+prop].position, self.components[prefix+prop].size, self.components[prefix+prop].GetBestSize()
        
        x,y = self.components.Properties.position
        
        # get values from one of the standard fields - use backgroundCcolor
        #  for text, field and button sizes
        
        # get the size as defined in the resource file, adjust for BestSize
        tx, ty = self.components.txtbackgroundColor.position
        tdefx, tdefy = self.components.txtbackgroundColor.size
        tsx, tsy = self.components.txtbackgroundColor.GetBestSize() ## + (20,10)
        tx = tx + tdefx - tsx
        
        fx, fy = self.components.fldbackgroundColor.position
        fdefx, fdefy = self.components.fldbackgroundColor.size
        fsx, fsy = self.components.fldbackgroundColor.GetBestSize() ## + (20,10)
        fx = fx + fdefx - fsx
        #rint fx, fy, fsx, fsy
        
        # Color buttons are odd, so use the font button for button positioning
        bx, by = self.components.fntfont.position
        bdefx, bdefy = self.components.fntfont.size
        bsx, bsy = self.components.fntfont.GetBestSize() ## + (20,10)
        #rint bx, by, bdefx, bdefy, bsx, bsy
        # bx = bx + bdefx - bsx
        bsx = bdefx
        #rint bx, by, bsx, bsy

        y = maxy+fsy 
        
        if DO_TRICKY_NAME_DERIVATIONS and ('label' in self.propertyList or 'text' in self.propertyList):
            self.components["chkallowNameLabelVariation"].visible = True
            self.components["chkallowNameLabelVariation"].enabled = True
            self.determineNameLabelState(wName)
        else:
            self.components["chkallowNameLabelVariation"].visible = False
            self.components["chkallowNameLabelVariation"].enabled = True
            self.determineNameLabelState(wName)
                        
        for propName in self.propertyList:
            widget = self._comp[wName]
            if propName in ['label', 'stringSelection', 'text', 'toolTip'] or propName in self.checkItems:
                value = getattr(widget, propName)
            else:
                value = str(getattr(widget, propName))

            if propName in self.checkItems:
                if not propName in self.standardProps:
                    if not "chk"+propName in self.components.iterkeys():
                        self.add_chk("chk"+propName, (fx, y), (fsx,fsy))
                    else:
                        self.components["chk"+propName].position = (fx, y)
                        self.components["chk"+propName].size = (fsx, fsy)
                    y += fsy + 5
                    self.components["chk"+propName].label = propName
                    self.components["chk"+propName].visible = True
                    self.components["chk"+propName].enabled = True
                    self.components["chk"+propName].checked = value
                else:
                    self.components["chk"+propName].visible = True
                    self.components["chk"+propName].checked = value
            elif propName in self.popItems:
                if not propName in self.standardProps:
                    if not "txt"+propName in self.components.iterkeys():
                        self.add_field("StaticText", "txt"+propName, (tx, y), (tsx,tsy), propName, "right")
                    else:
                        self.components["txt"+propName].position = (tx, y)
                        self.components["txt"+propName].size = (tsx, tsy)
                    if not "pop"+propName in self.components.iterkeys():
                        self.add_pop("pop"+propName, (fx, y), (fsx,fsy))
                    else:
                        self.components["pop"+propName].position = (fx, y)
                        self.components["pop"+propName].size = (fsx, fsy)
                    y += max(tsy, fsy) + 5    
                self.components["txt"+propName].visible = True
                self.components["txt"+propName].enabled = True                    
                self.components["pop"+propName].visible = True
                self.components["pop"+propName].enabled = True
                self.components["pop"+propName].Clear()
                if propName == 'stringSelection':
                    for v in widget.items:
                        self.components["pop"+propName].Append(v)
                else:
                    for v in widget._spec.getAttributes()[propName].values:
                        self.components["pop"+propName].Append(v)
                try:
                    self.components["pop"+propName].stringSelection = value
                except:
                    # if value is empty or doesn't already exist
                    pass
            elif propName in ('items', 'userdata') or (wClass == 'TextArea' and propName == 'text'):
                if not propName in self.standardProps:
                    if not "txt"+propName in self.components.iterkeys():
                        self.add_field("StaticText", "txt"+propName, (tx, y), (tsx,tsy), propName, "right")
                    else:
                        self.components["txt"+propName].position = (tx, y)
                        self.components["txt"+propName].size = (tsx, tsy)    
                    if not "fld"+propName in self.components.iterkeys():
                        self.add_field("TextArea", "fld"+propName, (fx, y), (fsx,fsy*3), value, "left")
                    else:
                        self.components["fld"+propName].position = (fx, y)
                        self.components["fld"+propName].size = (fsx, fsy*3)    
                    y += 3*fsy+5
                if wClass == 'TextArea' and propName == 'text':
                    propName = 'textArea'
                self.components["txt"+propName].visible = True
                self.components["txt"+propName].enabled = True
    
                self.components["fld"+propName].visible = True
                self.components["fld"+propName].enabled = True
                self.components["fld"+propName].text = value
            else:
                if not propName in self.standardProps:
                    if not "txt"+propName in self.components.iterkeys():
                        self.add_field("StaticText", "txt"+propName, (tx, y), (tsx,tsy), propName, "right")
                    else:
                        self.components["txt"+propName].position = (tx, y)
                        self.components["txt"+propName].size = (tsx, tsy)    
                    if not "fld"+propName in self.components.iterkeys():
                        self.add_field("TextField", "fld"+propName, (fx, y), (fsx,fsy), value, "left")
                    else:
                        self.components["fld"+propName].position = (fx, y)
                        self.components["fld"+propName].size = (fsx, fsy)
                        
                    if propName == 'file':
                        if not "btn"+propName in self.components.iterkeys():
                            self.add_btnFile("btn"+propName, (bx, y), (bsx,bsy))
                        else:
                            self.components["btn"+propName].position = (bx, y)
                            self.components["btn"+propName].size = (bsx, bsy)    
                        print "btn"+propName, bx, y, bsx, bsy
                        self.components["btn"+propName].visible = True
                        self.components["btn"+propName].enabled = True
                        # allow extra space for the "file" button
                        y += max(tsy, fsy, bsy) - max(tsy,fsy)

                    y += max(tsy, fsy) + 5
                else:
                    # all colors and fonts are "standard" items
                    if propName == 'foregroundColor' or propName == 'backgroundColor':
                        self.components["clr"+propName].visible = True
                        #rint propName, self.components["fld"+propName].text, value
                        self.components["clr"+propName].backgroundColor = util.colorFromString(value)

                self.components["txt"+propName].visible = True
                self.components["txt"+propName].enabled = True
    
                if propName == "font":
                    self.components["fld"+propName].visible = False 
                else:
                    self.components["fld"+propName].visible = True
                self.components["fld"+propName].enabled = True
                self.components["fld"+propName].text = value
                
##                self.components.wName.text = propName + ":"
                        
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
    
                    self.components["fld"+propName].text = value
            # this should only display if the attribute is settable
            # so name, alignment, and others are read-only

    def on_wComponentList_select(self, event):
        #print 'selectComponentListEvent: %s\n' % event.GetString()
#multicol        print self.components.wComponentList.getStringSelection()
#multicol        print self.components.wComponentList.getStringSelection()[0]
#multicol        wName, wClass = self.components.wComponentList.getStringSelection()[0].split("  :  ")
        wName, wClass = event.GetString().split("  :  ")

        if self._parent.multipleSelected: return   # cannot select from list while in multi-mode

        self.setValidProps(wClass)

        self.components.chkallowNameLabelVariation.checked = not DO_TRICKY_NAME_DERIVATIONS
        self.displayProperties(wName, wClass)
        self._parent.showSizingHandles(wName)
        c = self._parent.components[wName]
        self._parent.startName = wName
        self._parent.setToolTipDrag(wName, c.position, c.size)

    def clearComponentList(self):
        self.components.wComponentList.Clear()
        self.statusBar.text = ''

    def clearPropertyList(self):
        self.PropertyListClear()
        
    def on_alphabetizeComponents_mouseClick(self, event):
        self.displayComponents(self._comp)


    def displayComponents(self, components):
        self.components.wComponentList.Freeze()
        self.components.wComponentList.Clear()
        if self._parent.multipleSelected:
            self.components.alphabetizeComponents.enabled = False
            for c in self.multiCompControls:
                self.components[c].visible = True
            for c,pref in self._parent.multipleComponents:
                    self.addWidgetToComponentList(self._comp[c])
                    
        else:
            self.components.alphabetizeComponents.enabled = True
            for c in self.multiCompControls:
                self.components[c].visible = False
            self._comp = components
            #rint "here ", self.components.alphabetizeComponents.checked
            if self.components.alphabetizeComponents.checked:
                for c in self.compOrderControls:
                    self.components[c].enabled = False
                xxx = []
                for c in components.order:
                    #print "display", c, self._parent.isSizingHandle(c)
                    if c not in self._parent.sizingHandleNames and not self._parent.isSizingHandle(c):
                        xxx.append(components[c])
                xxx.sort()
                for c in xxx:
                    self.addWidgetToComponentList(c)
            else:
                for c in self.compOrderControls:
                    self.components[c].enabled = True
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
            
    def on_align_command(self, event):
        # offset is two x,y pairs
        # first pair is how far (whether) to move this dimension
        # second is how much of width to use
        #   all numbers used to multiply the difference between moving comp and base
        #   so (1,0,0,0) means make left X same as base, leave Y unchanged
        #     (1,0,1,0) means make right X same as base, leave Y unchanged
        #     (0,1,0,0.5) means make centre Y same as base, leave X unchanged
        alignOffsets = {'alignLeft': (1,0,0,0), 'alignRight': (1,0,1, 0), 
                        'alignTop': (0,1,0,0), 'alignBottom': (0,1,0,1),
                        'alignHorizontalCentres': (1,0,0.5,0), 
                        'alignVerticalCentres': (0,1,0,0.5)}
        if not self._parent.multipleComponents:
            return
        if not event.target.name in alignOffsets.keys():
            return
        BX, BY, SX, SY = alignOffsets[event.target.name]
        count = 0
        for c, pre in self._parent.multipleComponents:
            x,y = self._comp[c].position
            sx,sy = self._comp[c].size
            if count == 0:
                finalx = x + SX * sx
                finaly = y + SY * sy
            else:
                newx = x + BX * (finalx - SX*sx - x)
                newy = y + BY * (finaly - SY*sy - y)
                self._comp[c].position = (newx, newy)
            count += 1
        if count > 0:
            self._parent.showMultiSizingHandles()
            
    def on_equal_command(self, event):
        # settings is a single X,Y pair
        # specifies how much of final result comes from base (remainder from original)
        # so (1,0) means make comp's X size (i.e. width) be same as base's
        equalSettings = {'equalWidth': (1,0),
                         'equalHeight': (0,1), 
                         'equalBoth': (1,1)}
        if not self._parent.multipleComponents:
            return
        if not event.target.name in equalSettings.keys():
            return
        # set up Base fraction and Own fraction
        BX, BY = equalSettings[event.target.name]
        OX, OY = (1-BX, 1-BY)
        count = 0
        for c, pre in self._parent.multipleComponents:
            w,h = self._comp[c].size
            if count == 0:
                basew = w
                baseh = h
            else:
                neww,newh = (BX*basew + OX*w, BY*baseh+OY*h)
                self._comp[c].size = (neww, newh)
            count += 1
        if count > 0:
            self._parent.showMultiSizingHandles()

    def on_nudge_command(self, event):
        # Offsets are distance to move in each of X,Y
        # distance = 1 = 1, 2(,3) = gridsize, 4 = gridsize * gridsize
        nudgeOffsets = {'nudgeUp': (0,-1), 'nudgeDown': (0,1),
                        'nudgeLeft': (-1,0), 'nudgeRight': (1,0)}

        # can be applied in single component mode
##        if not self._parent.multipleComponents:
##            return

        if not event.target.name in nudgeOffsets.keys():
            return
        self._parent.nudge( nudgeOffsets[event.target.name], self.components.nudgeDistance.value)
            
    def on_distribute_command(self, event):
        # setting is x,y for which is to change, plus style

        distributeSettings = {'distHorizEdge': (1,0,'E'), 'distHorizFirstLast': (1,0,'F'), 
                              'distVertEdge': (0,1,'E'), 'distVertFirstLast': (0,1,'F')}
        if not self._parent.multipleComponents:
            return
        if not event.target.name in distributeSettings.keys():
            return
        
        BX, BY, style = distributeSettings[event.target.name]
        
        nameList = [ x[0] for x in self._parent.multipleComponents ]
        
        # Calculate First-to-Last.
        N = len(self._parent.multipleComponents) - 1  # number of gaps
        if style == "F":
            if N <= 1: return

            x1,y1 = self._comp[nameList[0]].position
            x2,y2 = self._comp[nameList[N]].position
            
            if BX*(x2-x1) + BY*(y2-y1) < 0:
                nameList.reverse()
                x1,y1 = self._comp[nameList[0]].position
                x2,y2 = self._comp[nameList[N]].position
            
            used = 0
            for c in nameList:
                sx,sy = self._comp[c].size
                used = used + BX*sx + BY*sy

            gapSpace = BX*(x2-x1-used+sx) + BY*(y2-y1-used+sy)
        elif style == 'E':
            gapSpace = 0
        else:
            return
            
        count = 0
        for c in nameList:
            x,y = self._comp[c].position
            sx,sy = self._comp[c].size
            if count == 0:
                basex, basey = (x, y)
                nextx, nexty = (x+sx, y+sy)
            else:
                useup = gapSpace / N
                N = N-1
                gapSpace = gapSpace - useup
                
                newx = BX * (nextx+useup) + (1-BX) * x
                newy = BY * (nexty+useup) + (1-BY) * y
                nextx, nexty = (newx+sx, newy+sy)

                self._comp[c].position = (newx, newy)
            count += 1
        if count > 0:
            self._parent.showMultiSizingHandles()
            
    
