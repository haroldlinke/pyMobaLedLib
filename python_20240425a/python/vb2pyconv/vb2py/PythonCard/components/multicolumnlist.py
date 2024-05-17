
"""
+__version__ = "$Revision: 1.28 $"
+__date__ = "$Date: 2004/11/07 18:13:13 $"
"""

import wx
from wx.lib.mixins.listctrl import ColumnSorterMixin, ListCtrlAutoWidthMixin
from types import TupleType, ListType, StringTypes, NoneType, IntType
from PythonCard import event, widget

class MultiColumnListEvent(event.Event):
    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        aWxEvent.item = aWxEvent.GetItem()
        return aWxEvent

class MultiColumnListSelectEvent(MultiColumnListEvent, event.CommandTypeEvent):
    name = 'select'
    binding = wx.EVT_LIST_ITEM_SELECTED
    id = wx.wxEVT_COMMAND_LIST_ITEM_SELECTED

class MultiColumnListItemActivatedEvent(MultiColumnListEvent):
    name = 'itemActivated'
    binding = wx.EVT_LIST_ITEM_ACTIVATED
    id = wx.wxEVT_COMMAND_LIST_ITEM_ACTIVATED

class MultiColumnListItemFocusedEvent(MultiColumnListEvent):
    name = 'itemFocused'
    binding = wx.EVT_LIST_ITEM_FOCUSED
    id = wx.wxEVT_COMMAND_LIST_ITEM_FOCUSED

class MultiColumnListMouseContextClickEvent(MultiColumnListEvent):
    name = 'mouseContextClick'
    binding = wx.EVT_LIST_ITEM_RIGHT_CLICK
    id = wx.wxEVT_COMMAND_LIST_ITEM_RIGHT_CLICK

class MultiColumnListKeyDownEvent(MultiColumnListEvent):
    name = 'keyDown'
    binding = wx.EVT_LIST_KEY_DOWN
    id = wx.wxEVT_COMMAND_LIST_KEY_DOWN

    def decorate(self, aWxEvent, source):
        aWxEvent = MultiColumnListEvent.decorate(self, aWxEvent, source)
        
        aWxEvent.keyCode = aWxEvent.GetKeyCode()
        return aWxEvent

class MultiColumnListColumnClickEvent(MultiColumnListEvent):
    name = 'columnClick'
    binding = wx.EVT_LIST_COL_CLICK
    id = wx.wxEVT_COMMAND_LIST_COL_CLICK


MultiColumnListEvents =(MultiColumnListSelectEvent,
                        MultiColumnListItemActivatedEvent,
                        MultiColumnListItemFocusedEvent,
                        MultiColumnListMouseContextClickEvent,
                        MultiColumnListKeyDownEvent,
                        MultiColumnListColumnClickEvent)

class MultiColumnListSpec(widget.WidgetSpec):
    def __init__(self):
##        events =[event.SelectEvent,
##                            event.ItemActivatedEvent,
##                            event.ItemFocusedEvent,
##                            event.MouseContextClickEvent,
##                            event.ListColumnClickEvent,
##                            event.KeyDownEvent]
        events = list(MultiColumnListEvents)
        attributes ={
            'items' : { 'presence' : 'optional', 'default' : [] },
            #'selected' : { 'presence' : 'optional', 'default' : None },
            'maxColumns' : { 'presence' : 'optional', 'default' : 20 },
            'columnHeadings' : { 'presence' : 'optional', 'default' : [] },
            'rules' : { 'presence' : 'optional', 'default' : 1 },
            #'style' : { 'presence' : 'optional', 'default' : [], 'values' : [ 'horizontal', 'vertical' ] },
            'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
        }
        widget.WidgetSpec.__init__( self, 'MultiColumnList', 'Widget', events, attributes )
        

class MultiColumnList(widget.Widget, wx.ListCtrl, ColumnSorterMixin, ListCtrlAutoWidthMixin):
    """
    A multi-column list.
    """

    _spec = MultiColumnListSpec()

    def __init__( self, aParent, aResource ) :
        if aResource.rules:
            rules = wx.LC_HRULES | wx.LC_VRULES
        else:
            rules = 0

        self._rules = aResource.rules
        self._maxColumns = aResource.maxColumns
        self._autoresize = 1

        wx.ListCtrl.__init__(
            self,
            aParent,
            widget.makeNewId(aResource.id),
            aResource.position,
            aResource.size,
            #aResource.items,
            style = rules | wx.LC_REPORT | \
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )

        widget.Widget.__init__( self, aParent, aResource )

        self.itemDataMap = {}
        # Now that the list exists we can init the other base class,
        # see wxPython/lib/mixins/listctrl.py
        ColumnSorterMixin.__init__(self, self._maxColumns)

        # Perform init for AutoWidth (resizes the last column to take up
        # the remaining display width)
        ListCtrlAutoWidthMixin.__init__(self)

        #if aResource.selected != "" and aResource.selected :
        #    self._setSelection( aResource.selected )

        # After creation we can set the headings
        self._setColumnHeadings(aResource.columnHeadings)

        # And load the list
        self._setItems(aResource.items)
        
        self._bindEvents(event.WIDGET_EVENTS + MultiColumnListEvents)

    # Emulate some listBox methods
    def Clear(self):
        self.DeleteAllItems()
        self.itemDataMap = {}

    # Emulate some listBox methods
    def GetCount(self):
        return self.GetItemCount()

    # Used by the wxColumnSorterMixin, see wxPython/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self

    """
    # KEA 2003-09-04
    # workaround typo bug in wxPython 2.4.1.2 controls2.py
    def GetColumn(self, *_args, **_kwargs):
        val = controls2c.ListCtrl_GetColumn(self, *_args, **_kwargs)
        if val is not None: val.thisown = 1
        return val
    """

    def _getColumnHeadings(self):
        return self._columnHeadings

    def GetColumnHeadingInfo(self):
        numcols = self.GetColumnCount()
        result = [None] * numcols
        if self._autoresize:
            for i in xrange(numcols):
                listItem = self.GetColumn(i)
                result[i] = [listItem.GetText(), wx.LIST_AUTOSIZE, listItem.GetAlign()]
        else:
            for i in xrange(numcols):
                listItem = self.GetColumn(i)
                result[i] = [listItem.GetText(), listItem.GetWidth(), listItem.GetAlign()]
        return result

    def GetSelectedItems(self):
        numcols = self.GetColumnCount()
        numitems = self.GetSelectedItemCount()
        items = [None] * numitems
        GetNextItem = self.GetNextItem
        if numcols == 1:
            GetItemText = self.GetItemText
            itemidx = -1
            for i in xrange( numitems ):
                itemidx = GetNextItem(itemidx, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
                if itemidx == -1:
                    #Odd, selection changed?
                    break
                items[i] = GetItemText(itemidx)
        else:
            GetItem = self.GetItem
            cols = range(numcols)
            itemidx = -1
            for i in xrange(numitems) :
                itemidx = GetNextItem(itemidx, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
                if itemidx == -1:
                    #Odd, selection changed?
                    break
                items[i] = map(lambda x: GetItem(itemidx, x).GetText(), cols)
        return items

    # Emulate some listBox methods
    def getStringSelection(self):
        return self.GetSelectedItems()

    # Emulate some listBox methods
    def Append(self, aList):
        self.InsertItems(aList, self.GetItemCount())

    # Emulate some listBox methods
    def InsertItems(self, aList, position):
        if not isinstance(aList, ListType) and not isinstance(aList, TupleType):
            raise AttributeError, "unsupported type, list expected"
            
        if len(aList) == 0:
            return

        numcols = self.GetColumnCount()
        numitems = self.GetItemCount()

        # If the list is empty or uninitialized fake an assignment and return
        if numitems == 0 or numcols == 0:
            self._setItems(aList)
            return 

        # Convert our input into a list of list entries of the appropriate
        # number of columns.
        if isinstance(aList[0], ListType) or isinstance(aList[0], TupleType):
            if isinstance(aList[0], TupleType):
                aList = list(aList)
            if numcols == len(aList[0]):
                pass
            elif numcols > len(aList[0]):
                blanks = [''] * (numcols - len(aList[0]))
                aList = map(lambda x:x + blanks, aList)
            else:
                aList = map(lambda x:x[:numcols], aList)
        elif isinstance(aList[0], StringTypes):
            blanks = [''] * (numcols - 1)
            aList = map(lambda x:[x] + blanks, aList)
        else:
            raise AttributeError, "unsupported type, list or string expected"

        # Allow negative indexing to mean from the end of the list
        if position < 0:
            position = numitems + position
        # But only allow from the start of the list on
        if position < 0:
            postiion = 0

        # If inserting within the current span of the list, we have
        # to copy the portion below the insertion point
        if position < numitems:
            currentitems = self._getItems()[position:]
            if isinstance(currentitems[0], StringTypes):
                currentitems = map(lambda x:[x], currentitems)
            aList = aList + currentitems

        datamap = self.itemDataMap
        max = [0] * numcols
        for i in xrange(len(aList)):
            offset = position + i
            l = len(aList[i][0])
            if l > max[0]:
                max[0] = l
            if offset >= numitems:
                self.InsertStringItem(offset, aList[i][0])
            else:
                self.SetStringItem(offset, 0, aList[i][0])
            for j in range(1,numcols):
                l = len(aList[i][j])
                if l > max[j]:
                    max[j] = l
                self.SetStringItem(offset, j, aList[i][j])
            self.SetItemData(offset, offset)
            datamap[offset] = aList[i]
        if self._autoresize:
            charwidth = self.GetCharWidth()
            maxwidth = self.GetBestVirtualSize()[0]*2
            for i in range(numcols):
                hdrwidth = (len(self._columnHeadings[i])+1) * charwidth
                colwidth = (max[i]+2) * charwidth
                curcolwidth = self.GetColumnWidth(i)
                if colwidth < curcolwidth:
                    colwidth = curcolwidth
                if colwidth < hdrwidth:
                    colwidth = hdrwidth
                if colwidth < 20:
                    colwidth = 20
                elif colwidth > maxwidth:
                    colwidth = maxwidth
                self.SetColumnWidth(i, colwidth)
            self.resizeLastColumn(self.GetColumnWidth(numcols-1))

    def _setColumnHeadings(self, aList):
        if isinstance(aList, ListType) or isinstance(aList, TupleType) or isinstance(aList, StringTypes):
            pass
        else:
            raise 'invalid MultiColumnList.SetHeading value: ', aList

        self.ClearAll()
        self.itemDataMap = {}
        self._autoresize = 1

        if isinstance(aList, StringTypes):
            self.InsertColumn(0,aList,width=self.GetBestVirtualSize()[0])
            self._columnHeadings = [aList]
            return
        elif isinstance(aList, TupleType):
            aList = list(aList)

        self._columnHeadings = aList

        numcols = len(aList)
        if numcols == 0:
            return
        elif numcols > self._maxColumns:
            numcols = self._maxColumns
            self._columnHeadings = aList[:numcols]

        if isinstance(aList[0], StringTypes):
            for i in xrange(numcols):
                self.InsertColumn(i, aList[i], width=wx.LIST_AUTOSIZE)
        elif isinstance(aList[0], ListType) or isinstance(aList[0], TupleType):
            w = len(aList[0])
            if w == 2 and isinstance(aList[0][0], StringTypes) and isinstance(aList[0][1], IntType):
                flag = 0
                for i in xrange(numcols):
                    if aList[i][1] != wx.LIST_AUTOSIZE:
                        flag = 1
                    self.InsertColumn(i, aList[i][0], width=aList[i][1])
                if flag:
                    self._autoresize = 0
            elif w == 3 and \
                   isinstance(aList[0][0], StringTypes) and \
                   isinstance(aList[0][1], IntType) and \
                   isinstance(aList[0][2], IntType):
                flag = 0
                for i in xrange(numcols):
                    if aList[i][1] != wx.LIST_AUTOSIZE:
                        flag = 1
                    self.InsertColumn(i, aList[i][0], format=aList[i][2], width=aList[i][1])
                if flag:
                    self._autoresize = 0
            elif w == 1 and isinstance(aList[0][0], StringTypes):
                for i in xrange(numcols):
                    self.InsertColumn(i, aList[i][0], width=wx.LIST_AUTOSIZE)
                self._autoresize = 1
            else:
                raise 'invalid MultiColumnList.SetHeading value: ', aList
        else:
            raise 'invalid MultiColumnList.SetHeading value: ', aList

        if numcols == 1:
            self.SetColumnWidth(0, self.GetBestVirtualSize()[0])
 
    def GetItemDataMap(self, aDict):
        return self.itemDataMap

    def SetItemDataMap(self, aDict):
        self.itemDataMap = aDict

    def SetSelection(self, itemidx, select=1):
        numitems = self.GetItemCount()
        if numitems == 0:
            return
        if itemidx < 0:
            itemidx = numitems + itemidx
        if itemidx < 0:
            itemidx = 0
        elif itemidx >= numitems:
            itemidx = numitems - 1

        if select:
            self.SetItemState(itemidx, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        else:
            self.SetItemState(itemidx, 0, wx.LIST_STATE_SELECTED)

    def SetStringSelection(self, item, select=1):
        numitems = self.GetItemCount()
        if numitems == 0:
            return -1
        #TODO:  Expand search to all columns, for now it adds no functionality
        itemidx = self.FindItem(-1, item, 1)
        if itemidx < 0:
            return itemidx

        if select:
            self.SetItemState(itemidx, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        else:
            self.SetItemState(itemidx, 0, wx.LIST_STATE_SELECTED)
        return itemidx

    def _getRules(self):
        return self._rules

    def _setRules(self, aString):
        raise AttributeError, "rules attribute is read-only"

    def _getMaxColumns(self):
        return self._maxColumns

    def _setMaxColumns(self, aString):
        # Could perhaps call the mixin __init__ method again, doesn't look
        # like it would cause harm.  For now however leave this a restriction.
        raise AttributeError, "maxColumns attribute is read-only"

    def _getItems( self ) :
        numitems = self.GetItemCount()
        numcols = self.GetColumnCount()
        items = [None] * numitems
        if numcols == 1:
            GetItemText = self.GetItemText
            for i in xrange(numitems ) :
                items[i] = GetItemText(i)
        else:
            GetItem = self.GetItem
            cols = range(numcols)
            for i in xrange(numitems) :
                items[i] = map(lambda x: GetItem(i, x).GetText(), cols)
        return items

    def _setItems( self, aList ) :
        if isinstance(aList, NoneType):
            aList = []
        elif not isinstance(aList, ListType) and not isinstance(aList, TupleType):
            raise AttributeError, "unsupported type, list expected"

        numitems = len(aList)
        if numitems == 0:
            self.DeleteAllItems()
            self.itemDataMap = {}
            return

        # If just simple list of strings convert it to a single column list
        if isinstance(aList[0], StringTypes):
            aList = map(lambda x:[x], aList)
        elif isinstance(aList[0], ListType) or isinstance(aList[0], TupleType):
            pass
        else:
            raise AttributeError, "unsupported element type"
        # Here we have a list of a list of values.
        # If the number of values is greater than the maximum number
        # of columns allowed, truncate it.  Similarly remove or add
        # columns as necessary to accomodate the data up to the maximum
        # allowed.  It could be thought to just throw an exception
        # since the programmer flubbed it however I chose the
        # 'do what you can' approach. Note that we depend on the
        # first item in the list setting the number of columns for
        # all remaining items in the list.
        numcols = len(aList[0])
        if numcols > self._maxColumns:
            numcols = self._maxColumns
        if numcols != self.GetColumnCount():
            if numcols == 1:
                self.ClearAll()
                self.InsertColumn(0,'List')
                self._columnHeadings = ['List']
            else:
                c = self.GetColumnCount()
                if c > numcols:
                    for i in range(c-1,numcols-1,-1):
                        self.DeleteColumn(i)
                        self._columnHeadings = self._columnHeadings[:-1]
                else:
                    for i in range(c,numcols):
                        colname = 'Col %d' % (i+1,)
                        self.InsertColumn(i,colname)
                        self._columnHeadings.append(colname)
        self.DeleteAllItems()
        datamap = {}
        max = [0] * numcols
        blanks = [''] * numcols
        columnlist = range(1,numcols)
        for i in xrange(numitems):
            aItem = aList[i]
            if len(aItem) < numcols:
                # Not the same number of columns in entry.
                # truncation is automatic, padding with
                # blanks is done here.
                aItem = aItem + blanks
            l = len(aItem[0])
            if l > max[0]:
                max[0] = l
            self.InsertStringItem(i, aItem[0])
            for j in columnlist:
                l = len(aItem[j])
                if l > max[j]:
                    max[j] = l
                self.SetStringItem(i, j, aItem[j])
            self.SetItemData(i, i)
            datamap[i] = aItem
        if self._autoresize:
            charwidth = self.GetCharWidth()
            maxwidth = self.GetBestVirtualSize()[0]*2
            for i in range(numcols):
                hdrwidth = (len(self._columnHeadings[i])+1) * charwidth
                colwidth = int((max[i]+1) * charwidth)
                if colwidth < hdrwidth:
                    colwidth = hdrwidth
                if colwidth < 20:
                    colwidth = 20
                elif colwidth > maxwidth:
                    colwidth = maxwidth
                self.SetColumnWidth(i, colwidth)
            self.resizeLastColumn(self.GetColumnWidth(numcols-1))
        self.itemDataMap = datamap

    # KEA 2004-04-16
    # theoretically this is fixed, need to check then delete this commented block
    """
    def _getFont(self):
        if self._font is None:
            # workaround for GetFont() bug with ListCtrl with
            # wxPython 2.4.1.2 and earlier on wxMSW
            f = self.GetFont()
            if f.Ok():
                desc = font.fontDescription(f)
            else:
                desc = font.fontDescription(self._parent.GetFont())
            self._font = font.Font(desc)
        return self._font
    """

    items = property(_getItems, _setItems)
    columnHeadings = property(_getColumnHeadings, _setColumnHeadings)
    maxColumns = property(_getMaxColumns, _setMaxColumns)
    rules = property(_getRules, _setRules)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].MultiColumnList)

