"""
__version__ = "$Revision: 1.40 $"
__date__ = "$Date: 2004/12/31 20:44:09 $"
"""

import wx
from . import event
from . import component

"""
KEA 2003-08-02

Need to test adding, renaming, deleting, a menuitem or menu
once the application is running. In particular, I'm curious about
doing dynamic menus for adding Scriptlets or allowing the user
to override accelerator key bindings.

Also, probably need to refactor so that we just use wxPython methods
when possible and get rid of the extra lists and duplicate method
calls.

The exception are any name related utility routines that make it
simpler to modify menu items and menus based on name rather than
a fixed id.

Also need to make sure a wxMenu can be created for use as a popup menu
and then have it be destroyed correctly. See fpop sample.

Can debug.py have its menu handled via the new menu classes? That is
can we add the Debug menu dynamically. Maybe not because of the event
binding.
"""

class MenuSelectEvent(event.SelectEvent):
    binding = wx.EVT_MENU
    id = wx.wxEVT_COMMAND_MENU_SELECTED

    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        aWxEvent.checked = aWxEvent.IsChecked()
        return aWxEvent


class MenuItem(wx.MenuItem, component.Component):
    """
    A MenuItem represents one selectable item in a Menu.

    A MenuItem with the name '-' is interpreted as
    a  separator.
    """

    def __init__(self, aScriptable, aParent, aResource):
        self.label = aResource.label
        self.command = aResource.command
        self.checkable = aResource.checkable
        self.enabled = aResource.enabled
        self.checked = aResource.checked

        id =  wx.NewId()

        if aResource.label == '-':
            wx.MenuItem.__init__(self, aParent, wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        elif aResource.checkable:
            #print aResource.label, aResource.checked, aResource.checked==True
            wx.MenuItem.__init__(self, aParent, id, aResource.label, "", kind=wx.ITEM_CHECK)
            # must use wxCallAfter to avoid init problems
            # if this ends up causing another conflict with openBackground...
            # then I guess we could drop the wxMenuItem sub-class and
            # just use wxMenu.Append like we used to
            if aResource.checked:
                wx.CallAfter(self.Check, aResource.checked)
            if not aResource.enabled:
                wx.CallAfter(self.Enable, aResource.enabled)
        else:
            #print aResource.label
            wx.MenuItem.__init__(self, aParent, id, aResource.label, "")
            if not aResource.enabled:
                wx.CallAfter(self.Enable, aResource.enabled)


        component.Component.__init__(self, aResource)

        self._bindEvents((MenuSelectEvent,), aScriptable, id)

        # KEA 2004-05-06
        # since the only use of id2itemMap
        # is enableCommand and disableCommand
        # it might make more sense to just store
        # a mapping of command names to ids
        aParent.parent.id2itemMap[id] = self

    def _bindEvents(self, eventList, aScriptable, menuId):        
##        background = wx.GetTopLevelParent(self)
        background = aScriptable

        if wx.GetApp()._showDebugMenu:
            bindUnusedEvents = True
        else:
            bindUnusedEvents = False
        
        # helper variable to simplify test for whether to bind InsteadOfTypeEvents
        # there is a good chance we will need to know
        # which events are bound, if we want to dynamically add or remove
        # events later, so go ahead and keep a reference to the list
        self.boundEvents = {}
        
        self.eventIdToHandler = {}
        self.wxEventIdMap = {}

        if 0:
            print("\nBINDING...", self.name)

        for eventClass in eventList:
            self.wxEventIdMap[eventClass.id] = eventClass
            if issubclass(eventClass, event.CommandTypeEvent) and self.command:
                handler = background.findHandler('on_' + self.command + '_command')
                if not handler:
                    handler = background.findHandler('on_' + self.name + '_' + eventClass.name)
            else:
                handler = background.findHandler('on_' + self.name + '_' + eventClass.name)
            if not handler:
                handler = background.findHandler('on_' + eventClass.name)
            if handler or bindUnusedEvents:
                if not self.boundEvents.get(eventClass.binding, None):
##                    self.Bind(eventClass.binding, self._dispatch)
                    # KEA 2004-05-04
                    # not sure yet if there is a different way to handle the bind
                    # apparently we have to bind the event to the parent frame
                    # and I think we also need the id, need to check with Robin
                    background.Bind(eventClass.binding, self._dispatch, id=menuId)
                    self.boundEvents[eventClass.binding] = eventClass.name
                if handler:
                    if 0:
                        print("  binding", self.name, eventClass.name, handler.__name__, eventClass.id)
                    #self.eventIdToHandler[eventClass.id] = handler.getFunction()
                    self.eventIdToHandler[eventClass.id] = handler

        if 0:
            print("\n  boundEvents:")
            for name in list(self.boundEvents.values()):
                print("   ", name)
            print("\n\n")
            print("\n  self.eventIdToHandler:")
            for id in self.eventIdToHandler:
                # KEA 2004-05-02
                # change to just using the method directly, Handler class not needed
                #print "   ", id, self.eventIdToHandler[id]._function
                print("   ", id, self.eventIdToHandler[id])
            print("\n\n")

    def _dispatch(self, aWxEvent):
        eventType = aWxEvent.GetEventType()
        # KEA 2004-05-04
        # for a menu item this event will always be the same
        # so this is redundant unless there is some binding other than
        # EVT_MENU that we're going to support?!
        eventClass = self.wxEventIdMap[eventType]
        
        eventClassInstance = eventClass()
        # decorate will add the relevant event attributes
        aWxEvent = eventClassInstance.decorate(aWxEvent, self)

        if self.command and isinstance(eventClassInstance, event.CommandTypeEvent):
            # need to report the name for the handler if it exists
            eventName = 'command ' + self.command
        else:
            if isinstance(eventClassInstance, event.InsteadOfTypeEvent):
                # changes eventType if needed
                # e.g. mouseDrag instead of mouseMove
                eventType = eventClassInstance.translateEventType(aWxEvent)
            eventName = self.wxEventIdMap[eventType].name
            
        # cleanup
        eventClass = None
        eventClassInstance = None

        handler = self.eventIdToHandler.get(eventType, None)
        if handler:
            event.EventLog.getInstance().log(eventName, self.name, True)
            if 0:
                print("dispatching", handler.__name__)
            # make a lowercase alias
            aWxEvent.skip = aWxEvent.Skip

            # KEA 2004-05-04
            # the menu events are always bound to the parent frame
            # so the target of the event will be the "background"
            # KEA 2004-05-05
            # it looks like WXMAC might be broken since GetEventObject
            # is returning the menu item, not the frame the event was
            # bound to
            if wx.Platform in ('__WXGTK__', '__WXMAC__'):
                background = aWxEvent.GetEventObject().parent.parent
            else:
                # KEA 2004-05-05
                # it looks like Windows is actually the busted platform
                # this time
                # if we end up caching the handlers as bound methods
                # then I guess this kind of problem would go away because
                # we won't have to supply the first arg "self" 
                background = aWxEvent.GetEventObject()
##            background = wx.GetTopLevelParent(self)

            handler(background, aWxEvent)
            
            # do we have to clean up this alias?
            aWxEvent.skip = None
            # how about this local reference to handler?
            handler = None
            background = None
        else:
            event.EventLog.getInstance().log(eventName, self.name, False)
            # hopefully this is all we need to do for "unused events"
            aWxEvent.Skip()

        # cleanup
        aWxEvent.target = aWxEvent.eventObject = None


    def _getName( self ) :
        return self.name

    def getLabel( self ) :
        return self.label

    def getCommand( self ) :
        return self.command

    def getCheckable( self ) :
        return self.checkable

    def getEnabled( self ) :
        return self.enabled

    def getChecked( self ) :
        return self.checked

    def setName( self, aString ) :
        self.name = aString
             
    def setLabel( self, aString ) :
        self.label = aString

    def setCommand( self, aString ) :
        self.command = aString

    def __repr__( self ) :
        return 'MenuItem=' + str( self.__dict__ )


class Menu(wx.Menu):
    """
    A Menu contains 0..n MenuItem objects.
    """

    def __init__(self, aParent, aResource):
        wx.Menu.__init__(self)

        self.parent = aParent
        self.name = aResource.name
        self.label = aResource.label
        self.enabled = aResource.enabled
        self.items = []

        for itemRsrc in aResource.items:
            menuItem = MenuItem(aParent.parent, self, itemRsrc)
            self.appendMenuItem(menuItem)


    def _getName( self ) :
        return self.name

    def getLabel( self ) :
        return self.label

    def getEnabled( self ) :
        return self.enabled

    def appendMenuItem(self, aMenuItem):
        # self.items is for backwards compatability
        self.items.append(aMenuItem)
        self.AppendItem(aMenuItem)

    def insertMenuItem( self, aMenuItem, aIndex ) :
        pass

    def deleteMenuItem( self, aName ) :
        pass

    def getMenuItem( self, aName ) :
        pass

    def getMenuItemByIndex( self, aIndex ) :
        pass

    def enable( self ) :
        pass

    def disable( self ) :
        pass

    def getMenuItems( self ) :
        return self.items

    def __repr__( self ) :
        return 'Menu=' + str( self.__dict__ )


class MenuBar(wx.MenuBar):

    def __init__(self, aParent, aMenuBarRsrc):
        wx.MenuBar.__init__(self)
        
        self.parent = aParent
        self.menus = []
        #self.parseMenus(aParent, aMenuBarRsrc.menus)

        self.id2itemMap = {}
        enabledMenus = []
        #menus = self.getMenus()

        # KEA 2003-08-02
        # menus probably needs to be a UserList subclass
        # so that menus can be treated as a Python list, but
        # automatically do wxMenuBar.Append... as needed
        # alternatively, the helper methods
        # would just get ids and such dynamically from the menubar
        # using wxPython methods
        for menuRsrc in aMenuBarRsrc.menus:
            menu = Menu(self, menuRsrc)
            self.menus.append(menu)
            self.Append(menu, menu.getLabel())
            enabledMenus.append(menu.getEnabled())

        aParent.SetMenuBar(self)
        # this is a complete hack because we don't have the id of the Menu
        for i in range(0, len(enabledMenus)):
            if not enabledMenus[i]:
                self.EnableTop(i, 0)

    def __repr__(self):
        return 'MenuBar=' + str(self.__dict__)

    def appendMenu( self, aMenu ) :
        pass

    def insertMenu( self, aMenu, aIndex ) :
        pass

    def deleteMenu( self, aName ) :
        pass

    def getMenu( self, aName ) :
        pass

    def getMenuByIndex( self, aIndex ) :
        pass

    def getMenuId(self, aString):
        id = -1
        for m in self.menus:
            menuLabel = m.label.replace('&', '')
            if m.name == aString:
                id = self.FindMenu(menuLabel)
                break
            for mi in m.items:
                if mi.name == aString:
                    menuItemLabel = mi.label.split('\t')[0].replace('&', '')
                    if menuItemLabel == 'Exit' and wx.Platform == '__WXMAC__':
                        # KEA 2004-09-14
                        # I think this is the only label WXMAC changes
                        # but I wonder if this won't work for other languages?!
                        # maybe the Quit menu item would always have the same id?
                        menuItemLabel = 'Quit'
                    id = self.FindMenuItem(menuLabel, menuItemLabel)
                    break
        return id

    # KEA 2004-04-07
    # Rowland suggests that the methods below be separated for release 0.8
    # so that separate methods are used for menus and menu items
    
    def getChecked( self, aString):
        id = self.getMenuId(aString)
        if id == -1:
            # KEA 2004-04-07
            # should we throw an exception here to indicate the menu/menu item wasn't found?
            return -1
        else:
            return self.IsChecked(id)

    def getEnabled( self, aString):
        id = self.getMenuId(aString)
        if id == -1:
            # KEA 2004-04-07
            # should we throw an exception here to indicate the menu/menu item wasn't found?
            return -1
        else:
            return self.IsEnabled(id)

    def setChecked( self, aString, aBoolean=True):
        # KEA 2004-04-07
        # if aString is a menu name instead of a menuItem name
        # and there is a match then an exception will be thrown below
        # when Check is called
        id = self.getMenuId(aString)
        if id == -1:
            # KEA 2004-04-07
            # should we throw an exception here to indicate the 
            # menu/menu item wasn't found instead of failing silently?
            pass
        else:
            self.Check(id, aBoolean)

    def setEnabled( self, aString, aBoolean=1) :
        i = 0
        for m in self.menus:
            menuLabel = m.label.strip('&')
            if m.name == aString:
                self.EnableTop(i, aBoolean)
                break
            for mi in m.items:
                if mi.name == aString:
                    menuItemLabel = mi.label.split('\t')[0].strip('&')
                    id = self.FindMenuItem(menuLabel, menuItemLabel)
                    self.Enable(id, aBoolean)
                    break
            i += 1

    def getMenus( self ) :
        return self.menus

    def enableCommand(self, aString, aBoolean=True):
        for item in self.id2itemMap.values():
            if item.command == aString :
                self.Enable(item.GetId(), aBoolean)

    def disableCommand(self, aString):
        self.enableCommand(aString, False)


# Unit Test

if __name__ == '__main__' :
    import sys
    from . import resource

    r = resource.ResourceFile(sys.argv[1]).getResource()
