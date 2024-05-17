#!/usr/bin/python

"""
__version__ = "$Revision: 1.8 $"
__date__ = "$Date: 2004/05/05 16:53:26 $"
"""

from PythonCard import model
import wx

# events
# itemActivated, itemFocused, 
# select, mouseContextClick, columnClick
# keyDown

class Minimal(model.Background):
    
    def on_initialize(self,event):
        self.initializeList()

    # so how much to wrap and how much to leave raw wxPython?
    def initializeList(self):
        list = self.components.list
        
        list.InsertColumn(0, "Artist")
        list.InsertColumn(1, "Title", wx.LIST_FORMAT_RIGHT)
        list.InsertColumn(2, "Genre")  

        musicdata = {
            14: ("GBV", "14 Cheerleader Coldfront", "Rock"),
            28: ("The Mountain Goats", "Going to Marakesh", "Rock"),
            29: ("The Mountain Goats", "Going to Georgia", "Rock"),
            30: ("The Mountain Goats", "Quetzalcoatal Eats Plums", "Rock"),
            31: ("Howlin Wolf", "Hip Shakin' Woman", "Blues"),
            32: ("Neutral Milk Hotel", "Oh Comely", "Infinite Bliss"),
            33: ("Miles Davis", "Blue in Green", "Jazz"),
            15: ("Taylor Dayne", "you must be KIDDING me", "?")}

        items = musicdata.items()

        for x in range(len(items)):
            key, data = items[x]
            list.InsertStringItem(x, data[0])
            list.SetStringItem(x, 0, data[0])
            list.SetStringItem(x, 1, data[1])
            list.SetStringItem(x, 2, data[2])
            list.SetItemData(x, key)

        list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        list.SetColumnWidth(2, 100)

        list.SetItemDataMap(musicdata)

        # show how to select an item
        list.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        self.currentItem = 0

        # these aren't needed because the events are now part of the
        # MultiColumnList
        #wx.EVT_LIST_ITEM_SELECTED(self.panel, -1, self.on_list_itemSelected)
        #wx.EVT_LEFT_DCLICK(list, self.on_list_mouseDoubleClick)

        # these are still needed if you want the events
        #wx.EVT_LIST_ITEM_ACTIVATED(self.panel, -1, self.on_list_itemActivated)
        #wx.EVT_LIST_COL_CLICK(self.panel, -1, self.on_list_columnClick)

    def getColumnText(self, index, col):
        item = self.components.list.GetItem(index, col)
        return item.GetText()

    def on_list_select(self, event):
        self.currentItem = event.m_itemIndex
        print "on_list_select: %s, %s, %s, %s\n" % (self.currentItem,
                            self.components.list.GetItemText(self.currentItem),
                            self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2))

    def on_list_mouseDoubleClick(self, event):
        # event.target
        # is equivelant to
        # self.components.list
        print "on_list_mouseDoubleClick item %s\n" % self.components.list.GetItemText(self.currentItem)
        event.skip()

    def on_list_itemActivated(self, event):
        self.currentItem = event.m_itemIndex
        print "on_list_itemActivated: %s\n" % self.components.list.GetItemText(self.currentItem)
        item = self.components.list.GetItem(self.currentItem)
        print item.m_text, item.m_itemId, self.components.list.GetItemData(self.currentItem)

    def on_list_columnClick(self, event):
        print "on_list_columnClick: %d\n" % event.GetColumn()

    # KEA 2003-08-31
    # on Windows, there is a system beep for
    # each key press, is that a bug and if so, is it in PythonCard
    # or wxWindows?
    def on_list_keyDown(self, event):
        print "on_list_keyDown: %d\n" % event.keyCode
        event.skip()


if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()




