
"""
__version__ = "$Revision: 1.16 $"
__date__ = "$Date: 2004/08/22 19:11:35 $"
"""

from PythonCard import log, model, resource
import os
import wx


MENULIST_PADDING = '....'


def menuItemAttributes(menuItem):
    desc =  "                  {'type':'MenuItem',\n"
    desc += "                   'name':'%s',\n" % menuItem['name']
    # KEA 2002-05-16
    # work on string repr to get strings with mixed ' and " to work correctly
    if menuItem['shortcut'] == '':
        desc += """                   'label':%s,\n""" % repr(menuItem['label'])
    else:
        desc += """                   'label':%s,\n""" % repr(menuItem['label'] + '\t' + menuItem['shortcut'])
    try:
        if menuItem['command'] is not None:
            desc += "                   'command':'%s',\n" % menuItem['command']
    except:
        pass
    try:
        if not menuItem['enabled']:
            desc += "                   'enabled':0,\n"
    except:
        pass
    try:
        if menuItem['checkable']:
            desc += "                   'checkable':1,\n"
        if menuItem['checked']:
            desc += "                   'checked':1,\n"
    except:
        pass
    desc += "                  },\n"
    return desc

def menuAttributes(menu):
    desc =  "            {'type':'Menu',\n"
    desc += "              'name':'%s',\n" % menu['name']
    desc += """              'label':%s,\n""" % repr(menu['label'])
    desc += "              'items': [\n"
    
    return desc

def menuResourceFromList(menuList):
    #desc =  "    'menubar': {'type':'MenuBar',\n"
    desc =  "{'type':'MenuBar',\n"
    desc += "         'menus': [\n"

    inMenu = 0
    for m in menuList:
        if m['type'] == 'Menu':
            if inMenu:
                # close Menu
                desc += "               ]\n"
                desc += "             },\n"
            desc += menuAttributes(m)
            inMenu = 1
        else:
            desc += menuItemAttributes(m)
            

    # close Menu
    desc += "               ]\n"
    desc += "             },\n"
    # close MenuBar
    desc += "         ]\n"
    desc += "}\n"
    d = eval(desc)
    return resource.Resource(d)


class MenuDialog(model.CustomDialog):
    def __init__(self, aBg, rsrc):
        model.CustomDialog.__init__(self, aBg)
        
        self.parent = aBg
        
        # if some special setup is necessary, do it here
        if rsrc is not None:
            #aBg.printMenubar(rsrc)
            self.menuList = self.parseMenus(rsrc)
        else:
            self.menuList = []
        for m in self.menuList:
            if m['type'] == 'Menu':
                self.components.listMenus.append(m['label'])
            else:
                self.components.listMenus.append(MENULIST_PADDING + m['label'])
        #self.components.listMenus.items = self.parseMenus(rsrc)

        # Esc doesn't seem to work, it ends up closing the dialog
        # so need to work on that
        self.keyCodes = {wx.WXK_ESCAPE:'ESC',
                         wx.WXK_SPACE:'Space',
                         wx.WXK_DELETE:'Del',
                         wx.WXK_F1:'F1',
                         wx.WXK_F2:'F2',
                         wx.WXK_F3:'F3',
                         wx.WXK_F4:'F4',
                         wx.WXK_F5:'F5',
                         wx.WXK_F6:'F6',
                         wx.WXK_F7:'F7',
                         wx.WXK_F8:'F8',
                         wx.WXK_F9:'F9',
                         wx.WXK_F10:'F10',
                         wx.WXK_F11:'F11',
                         wx.WXK_F12:'F12',
                         }
        #self.components.fldName.text = rsrc.application.name
        #self.components.fldTitle.text = rsrc.application.title
        #self.components.fldPosition.text = str(rsrc.application.position)
        #self.components.fldSize.text = str(rsrc.application.size)
        #self.components.chkStatusBar.checked = rsrc.application.statusBar

    def buildMenu(self, name, label):
        m = {}
        m['type'] = 'Menu'
        m['name'] = name
        m['label'] = label
        return m

    def buildMenuItem(self, name, label, shortcut, command, enabled, checkable, checked):
        m = {}
        m['type'] = 'MenuItem'
        m['name'] = name
        m['label'] = label
        m['shortcut'] = shortcut
        m['command'] = command
        m['enabled'] = enabled
        m['checkable'] = checkable
        m['checked'] = checked
        return m

    def parseMenus(self, menubar):
        menuList = []
        for menu in menubar.menus:
            #menuList.append(menu.label)
            #print menu.type, menu.name, menu.label
            menuList.append(self.buildMenu(menu.name, menu.label))
            for menuItem in menu.items:
                itemParts = menuItem.label.split("\t")
                label = itemParts[0]
                try:
                    shortcut = itemParts[1]
                except:
                    shortcut = ''
                #menuList.append("....%s" % itemParts[0])
                #print menuItem.type, menuItem.name, itemParts, menuItem.command, menuItem.enabled, menuItem.checkable, menuItem.checked
                menuList.append(self.buildMenuItem(menuItem.name, label, shortcut, menuItem.command, menuItem.enabled, menuItem.checkable, menuItem.checked))
        return menuList

    def on_fldShortcut_keyDown(self, event):
        # this should handle the special key codes
        keyCode = event.keyCode
        if keyCode > 32 and keyCode < 127:
            keyStr = chr(keyCode).upper()
        elif keyCode in self.keyCodes:
            keyStr = self.keyCodes[keyCode]
        else:
            event.target.text = ''
            return

        if event.shiftDown:
            keyStr = 'Shift+' + keyStr
        if event.altDown:
            keyStr = 'Alt+' + keyStr
        if event.controlDown:
            keyStr = 'Ctrl+' + keyStr
        if len(keyStr) > 1:
            # don't allow just a number or letter
            # without a modifier
            # might also need a leading Ctrl or Alt
            event.target.text = keyStr

    def on_fldShortcut_keyPress(self, event):
        pass

    def on_fldName_loseFocus(self, event):
        sel = self.components.listMenus.selection
        try:
            self.menuList[sel]['name'] = event.target.text
            log.info(self.menuList[sel])
        except:
            pass

    def on_fldLabel_loseFocus(self, event):
        def normalize(label):
            name = label.replace("&", "").replace(".", "").replace(" ", "")
            return name

        sel = self.components.listMenus.selection
        try:
            label = event.target.text
            if self.menuList[sel]['type'] == 'Menu' and self.menuList[sel]['label'] == 'New Menu':
                oldname = self.menuList[sel]['name']
                if oldname == 'menuNewMenu':
                    name = 'menu'+normalize(label)
                    self.menuList[sel]['name'] = name
                    self.components.fldName.text = name
            elif self.menuList[sel]['type'] == 'MenuItem' and self.menuList[sel]['label'] == 'New Item':
                oldname = self.menuList[sel]['name']
                menuname = 'menuMenu'
                for i in range(sel+1):
                    if self.menuList[sel-i]['type'] == 'Menu':
                        menuname = self.menuList[sel-i]['name'] 
                        break
                if oldname == menuname+'NewItem':
                    name = menuname+normalize(label)
                    self.menuList[sel]['name'] = name
                    self.components.fldName.text = name
            self.menuList[sel]['label'] = label
            if self.menuList[sel]['type'] == 'MenuItem':
                label = MENULIST_PADDING + label
            self.components.listMenus.setString(sel, label)
            log.info(self.menuList[sel])
        except:
            pass

    def on_fldShortcut_loseFocus(self, event):
        sel = self.components.listMenus.selection
        try:
            if self.menuList[sel]['type'] == 'MenuItem':
                self.menuList[sel]['shortcut'] = event.target.text
            log.info(self.menuList[sel])
        except:
            pass

    def on_fldCommand_loseFocus(self, event):
        sel = self.components.listMenus.selection
        try:
            if self.menuList[sel]['type'] == 'MenuItem':
                if event.target.text == '':
                    self.menuList[sel]['command'] = None
                else:
                    self.menuList[sel]['command'] = event.target.text
            log.info(self.menuList[sel])
        except:
            pass

    def on_chkEnabled_mouseClick(self, event):
        sel = self.components.listMenus.selection
        try:
            if self.menuList[sel]['type'] == 'MenuItem':
                self.menuList[sel]['enabled'] = event.target.checked
            log.info(self.menuList[sel])
        except:
            pass

    def on_chkCheckable_mouseClick(self, event):
        sel = self.components.listMenus.selection
        try:
            if self.menuList[sel]['type'] == 'MenuItem':
                self.menuList[sel]['checkable'] = event.target.checked
            log.info(self.menuList[sel])
        except:
            pass

    def on_chkChecked_mouseClick(self, event):
        sel = self.components.listMenus.selection
        try:
            if self.menuList[sel]['type'] == 'MenuItem':
                self.menuList[sel]['checked'] = event.target.checked
            log.info(self.menuList[sel])
        except:
            pass

    def displayItemAttributes(self, sel):
        m = self.menuList[sel]
        self.components.fldListIndex.text = str(sel)
        self.components.fldName.text = m['name']
        self.components.fldLabel.text = m['label']
        if m['type'] == 'MenuItem':
            self.components.fldShortcut.text = m['shortcut']
            if m['command'] is None:
                self.components.fldCommand.text = ''
            else:
                self.components.fldCommand.text = m['command']
            self.components.chkEnabled.checked = m['enabled']
            self.components.chkCheckable.checked = m['checkable']
            self.components.chkChecked.checked = m['checked']
            
            self.components.stcShortcut.visible = 1
            self.components.stcCommand.visible = 1
            self.components.fldShortcut.visible = 1
            self.components.fldCommand.visible = 1
            self.components.chkEnabled.visible = 1
            self.components.chkCheckable.visible = 1
            self.components.chkChecked.visible = 1
        else:
            self.components.stcShortcut.visible = 0
            self.components.stcCommand.visible = 0
            self.components.fldShortcut.visible = 0
            self.components.fldCommand.visible = 0
            self.components.chkEnabled.visible = 0
            self.components.chkCheckable.visible = 0
            self.components.chkChecked.visible = 0

    def on_listMenus_select(self, event):
        self.displayItemAttributes(event.target.selection)

    def rebuildListMenus(self, sel=-1):
        self.components.listMenus.clear()
        for m in self.menuList:
            if m['type'] == 'Menu':
                self.components.listMenus.append(m['label'])
            else:
                self.components.listMenus.append(MENULIST_PADDING + m['label'])
        if sel != -1:
            self.components.listMenus.selection = sel
            
    def on_btnUp_mouseClick(self, event):
        sel = self.components.listMenus.selection
        # a selection of -1 means no selection
        # a selection of 0 is the first item in the list
        if sel > 0:
            temp = self.menuList[sel]
            self.menuList[sel] = self.menuList[sel - 1]
            self.menuList[sel - 1] = temp
            self.rebuildListMenus(sel - 1)

    def on_btnDown_mouseClick(self, event):
        sel = self.components.listMenus.selection
        if sel != -1 and sel < len(self.menuList) - 1:
            temp = self.menuList[sel]
            self.menuList[sel] = self.menuList[sel + 1]
            self.menuList[sel + 1] = temp
            self.rebuildListMenus(sel + 1)

    def on_btnDelete_mouseClick(self, event):
        sel = self.components.listMenus.selection
        if sel != -1:
            del self.menuList[sel]
            self.components.listMenus.delete(sel)
            if len(self.menuList) > 0:
                if sel > 0:
                    sel = sel - 1
                self.components.listMenus.selection = sel
                self.displayItemAttributes(sel)

    def on_btnNewMenu_mouseClick(self, event):
        sel = self.components.listMenus.selection
        self.menuList.append(" ") # extend list
        if sel == -1:
            sel = len(self.menuList) - 1
        else:
            self.menuList[sel+1:] = self.menuList[sel:-1]
            sel = sel+1
        self.menuList[sel] = self.buildMenu('menuNewMenu', 'New Menu')
        self.rebuildListMenus(sel)
        self.displayItemAttributes(sel)

    def on_btnNewMenuItem_mouseClick(self, event):
        sel = self.components.listMenus.selection
        self.menuList.append(" ") # extend list
        if sel == -1:
            sel = len(self.menuList) - 1
        else:
            self.menuList[sel+1:] = self.menuList[sel:-1]
            sel = sel+1
        name = 'menuMenu'
        for i in range(1, sel+1):
            if self.menuList[sel-i]['type'] == 'Menu':
                name = self.menuList[sel-i]['name'] 
                break
        self.menuList[sel] = self.buildMenuItem(name+'NewItem', 'New Item', '', None, 1, 0, 0)
        self.rebuildListMenus(sel)
        self.displayItemAttributes(sel)


def menuDialog(parent, rsrc):
    dlg = MenuDialog(parent, rsrc)
    result = dlg.showModal()
    if result.accepted:
        if len(dlg.menuList) == 0:
            result.menubar = None
        else:
            result.menubar = menuResourceFromList(dlg.menuList)
    dlg.destroy()
    return result
