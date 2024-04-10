
"""
__version__ = "$Revision: 1.15 $"
__date__ = "$Date: 2004/05/13 02:40:25 $"
"""

import wx
from PythonCard import event, widget


class TreeEvent(event.Event):
    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        aWxEvent.item = aWxEvent.GetItem()
        return aWxEvent

class TreeItemActivatedEvent(TreeEvent):
    name = 'itemActivated'
    binding = wx.EVT_TREE_ITEM_ACTIVATED
    id = wx.wxEVT_COMMAND_TREE_ITEM_ACTIVATED

class TreeItemCollapsedEvent(TreeEvent):
    name = 'itemCollapsed'
    binding = wx.EVT_TREE_ITEM_COLLAPSED
    id = wx.wxEVT_COMMAND_TREE_ITEM_COLLAPSED

class TreeItemCollapsingEvent(TreeEvent):
    name = 'itemCollapsing'
    binding = wx.EVT_TREE_ITEM_COLLAPSING
    id = wx.wxEVT_COMMAND_TREE_ITEM_COLLAPSING

class TreeItemExpandedEvent(TreeEvent):
    name = 'itemExpanded'
    binding = wx.EVT_TREE_ITEM_EXPANDED
    id = wx.wxEVT_COMMAND_TREE_ITEM_EXPANDED

class TreeItemExpandingEvent(TreeEvent):
    name = 'itemExpanding'
    binding = wx.EVT_TREE_ITEM_EXPANDING
    id = wx.wxEVT_COMMAND_TREE_ITEM_EXPANDING

class TreeSelectionChangedEvent(TreeEvent):
    name = 'selectionChanged'
    binding = wx.EVT_TREE_SEL_CHANGED
    id = wx.wxEVT_COMMAND_TREE_SEL_CHANGED

    def decorate(self, aWxEvent, source):
        aWxEvent = TreeEvent.decorate(self, aWxEvent, source)
        aWxEvent.oldItem = aWxEvent.GetOldItem()
        return aWxEvent

class TreeSelectionChangingEvent(TreeEvent):
    name = 'selectionChanging'
    binding = wx.EVT_TREE_SEL_CHANGING
    id = wx.wxEVT_COMMAND_TREE_SEL_CHANGING

    def decorate(self, aWxEvent, source):
        aWxEvent = TreeEvent.decorate(self, aWxEvent, source)
        aWxEvent.oldItem = aWxEvent.GetOldItem()
        return aWxEvent
    
class TreeKeyDownEvent(TreeEvent):
    name = 'keyDown'
    binding = wx.EVT_TREE_KEY_DOWN
    id = wx.wxEVT_COMMAND_TREE_KEY_DOWN

    def decorate(self, aWxEvent, source):
        aWxEvent = TreeEvent.decorate(self, aWxEvent, source)
        
        aWxEvent.keyCode = aWxEvent.GetKeyCode()
        keyEvent = aWxEvent.GetKeyEvent()
        aWxEvent.position = tuple(keyEvent.GetPosition())
        aWxEvent.x = keyEvent.GetX()
        aWxEvent.y = keyEvent.GetY()
        aWxEvent.altDown = keyEvent.AltDown()
        aWxEvent.controlDown = keyEvent.ControlDown()
        aWxEvent.shiftDown = keyEvent.ShiftDown()
        keyEvent = None        
        return aWxEvent


TreeEvents = (#TreeSelectEvent, 
                TreeItemActivatedEvent,
                TreeItemCollapsedEvent,
                TreeItemCollapsingEvent,
                TreeItemExpandedEvent,
                TreeItemExpandingEvent,
                TreeSelectionChangedEvent,
                TreeSelectionChangingEvent,
                TreeKeyDownEvent
             )


class TreeSpec(widget.WidgetSpec):
    def __init__(self) :
##        events = [event.SelectEvent, 
##                            event.ItemActivatedEvent,
##                            event.ItemExpandedEvent,
##                            event.ItemExpandingEvent,
##                            event.SelectionChangedEvent,
##                            event.SelectionChangingEvent,
##                            event.KeyDownEvent
##                           ]
        events = list(TreeEvents)
        attributes = {
            #'items' : { 'presence' : 'optional', 'default' : [] },
            #'style' : { 'presence' : 'optional', 'default' : [], 'values' : [ 'horizontal', 'vertical' ] },
            'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
        }
        widget.WidgetSpec.__init__( self, 'Tree', 'Widget', events, attributes )


class Tree(widget.Widget, wx.TreeCtrl):
    """
    A tree.
    """
    
    _spec = TreeSpec()

    def __init__(self, aParent, aResource) :
        wx.TreeCtrl.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.position, 
            aResource.size, 
            #aResource.items,
            #style = border | wx.LC_REPORT | wx.CLIP_SIBLINGS,
            name = aResource.name
        )

        widget.Widget.__init__(self, aParent, aResource)

        self._bindEvents(event.WIDGET_EVENTS + TreeEvents)

    # mixedCase aliases
    # probably need to do all the wxTreeCtrl methods
    # this just covers the ones in the minimalTree sample
    addRoot = wx.TreeCtrl.AddRoot
    appendItem = wx.TreeCtrl.AppendItem
    getChildrenCount = wx.TreeCtrl.GetChildrenCount
    getItemText = wx.TreeCtrl.GetItemText
    isExpanded = wx.TreeCtrl.IsExpanded
    selectItem = wx.TreeCtrl.SelectItem
    setItemHasChildren = wx.TreeCtrl.SetItemHasChildren
    
# if it looks like there is a memory leak with Tree components
# then Tree should have its own _dispatch method
# and set aWxEvent.oldItem = None, and aWxEvent.item = None
# after calling widget.Widget._dispatch


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Tree)

