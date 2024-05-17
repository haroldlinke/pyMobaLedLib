
"""
__version__ = "$Revision: 1.13 $"
__date__ = "$Date: 2004/09/09 21:08:46 $"
"""

import wx
from wx import grid
from PythonCard import event, widget



class GridEvent(event.Event):
    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        try:
            aWxEvent.row = aWxEvent.GetRow()
            aWxEvent.column = aWxEvent.GetCol()
            aWxEvent.position = aWxEvent.GetPosition()
        except:
            pass
        return aWxEvent
        
class GridMouseClickEvent(GridEvent):
    name = 'mouseClick'
    binding = wx.grid.EVT_GRID_CELL_LEFT_CLICK
    id = wx.grid.wxEVT_GRID_CELL_LEFT_CLICK

class GridMouseContextClickEvent(GridEvent):
    name = 'mouseContextClick'
    binding = wx.grid.EVT_GRID_CELL_RIGHT_CLICK
    id =  wx.grid.wxEVT_GRID_CELL_RIGHT_CLICK

class GridMouseDoubleClickEvent(GridEvent):
    name = 'mouseDoubleClick'
    binding = wx.grid.EVT_GRID_CELL_LEFT_DCLICK
    id =  wx.grid.wxEVT_GRID_CELL_LEFT_DCLICK

class GridMouseContextDoubleClickEvent(GridEvent):
    name = 'mouseContextDoubleClick'
    binding = wx.grid.EVT_GRID_CELL_RIGHT_DCLICK
    id =  wx.grid.wxEVT_GRID_CELL_RIGHT_DCLICK

class GridLabelClickEvent(GridEvent):
    name = 'labelClick'
    binding = wx.grid.EVT_GRID_LABEL_LEFT_CLICK
    id = wx.grid.wxEVT_GRID_LABEL_LEFT_CLICK

class GridLabelContextClickEvent(GridEvent):
    name = 'labelContextClick'
    binding = wx.grid.EVT_GRID_LABEL_RIGHT_CLICK
    id =  wx.grid.wxEVT_GRID_LABEL_RIGHT_CLICK

class GridLabelDoubleClickEvent(GridEvent):
    name = 'labelDoubleClick'
    binding = wx.grid.EVT_GRID_LABEL_LEFT_DCLICK
    id =  wx.grid.wxEVT_GRID_LABEL_LEFT_DCLICK

class GridLabelContextDoubleClickEvent(GridEvent):
    name = 'labelContextDoubleClick'
    binding = wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK
    id =  wx.grid.wxEVT_GRID_LABEL_RIGHT_DCLICK

class GridRowSizeEvent(GridEvent):
    name = 'rowSize'
    binding = wx.grid.EVT_GRID_ROW_SIZE
    id = wx.grid.wxEVT_GRID_ROW_SIZE

class GridColumnSizeEvent(GridEvent):
    name = 'columnSize'
    binding = wx.grid.EVT_GRID_COL_SIZE
    id = wx.grid.wxEVT_GRID_COL_SIZE

class GridRangeSelectEvent(GridEvent):
    name = 'rangeSelect'
    binding = wx.grid.EVT_GRID_RANGE_SELECT
    id = wx.grid.wxEVT_GRID_RANGE_SELECT

class GridCellChangeEvent(GridEvent):
    name = 'cellChange'
    binding = wx.grid.EVT_GRID_CELL_CHANGE
    id = wx.grid.wxEVT_GRID_CELL_CHANGE

class GridSelectCellEvent(GridEvent):
    name = 'selectCell'
    binding = wx.grid.EVT_GRID_SELECT_CELL
    id = wx.grid.wxEVT_GRID_SELECT_CELL

class GridEditorShownEvent(GridEvent):
    name = 'editorShown'
    binding = wx.grid.EVT_GRID_EDITOR_SHOWN
    id = wx.grid.wxEVT_GRID_EDITOR_SHOWN

class GridEditorHiddenEvent(GridEvent):
    name = 'editorHidden'
    binding = wx.grid.EVT_GRID_EDITOR_HIDDEN
    id = wx.grid.wxEVT_GRID_EDITOR_HIDDEN

class GridEditorCreatedEvent(GridEvent):
    name = 'editorCreated'
    binding = wx.grid.EVT_GRID_EDITOR_CREATED
    id = wx.grid.wxEVT_GRID_EDITOR_CREATED

        
GridEvents = (#GridSelectEvent, 
                GridMouseClickEvent,
                GridMouseContextClickEvent,
                GridMouseDoubleClickEvent,
                GridMouseContextDoubleClickEvent,
                GridLabelClickEvent,
                GridLabelContextClickEvent,
                GridLabelDoubleClickEvent,
                GridLabelContextDoubleClickEvent,
                GridRowSizeEvent,
                GridColumnSizeEvent,
                GridRangeSelectEvent,
                GridCellChangeEvent,
                GridSelectCellEvent,
                GridEditorShownEvent,
                GridEditorHiddenEvent,
                GridEditorCreatedEvent,
             )
        
class GridSpec(widget.WidgetSpec):
    def __init__(self):
        events = list(GridEvents)

        attributes = { 
            'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
            #'items' : { 'presence' : 'optional', 'default' : [] },
            #'style' : { 'presence' : 'optional', 'default' : [], 'values' : [ 'horizontal', 'vertical' ] },
        }
        widget.WidgetSpec.__init__( self, 'Grid', 'Widget', events, attributes )
        # might need to remove these events, not sure yet
        #self._events.remove(event.MouseDoubleClickEvent)
        #self._events.remove(event.MouseContextClickEvent)
        #self._events.remove(event.MouseContextDoubleClickEvent)


class Grid(widget.Widget, grid.Grid):
    """
    A Grid.
    """
    
    _spec = GridSpec()

    def __init__(self, aParent, aResource) :
        grid.Grid.__init__(
            self,
            aParent, 
            widget.makeNewId( aResource.id ), 
            aResource.position, 
            aResource.size, 
            #aResource.items,
            #style = border | wx.LC_REPORT | wx.CLIP_SIBLINGS,
            name = aResource.name
        )

        widget.Widget.__init__(self, aParent, aResource)

##        self._bindEvents(event.WIDGET_EVENTS)
        self._bindEvents(self._spec._events)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Grid)

