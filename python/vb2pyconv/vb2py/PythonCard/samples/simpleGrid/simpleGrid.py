#!/usr/bin/python

"""
__version__ = "$Revision: 1.12 $"
__date__ = "$Date: 2004/09/09 21:08:46 $"
"""

from PythonCard import dialog, model
import wx
from wx import grid
import sys

class Minimal(model.Background):

    def on_initialize(self, event):
        self.log = sys.stdout
        self.moveTo = None

##        wx.EVT_IDLE(self, self.OnIdle)
        
        mygrid = self.components.mygrid

        mygrid.CreateGrid(25, 25) #, wxGrid.wxGridSelectRows)
        ##mygrid.EnableEditing(False)

        # simple cell formatting
        mygrid.SetColSize(3, 200)
        mygrid.SetRowSize(4, 45)
        mygrid.SetCellValue(0, 0, "First cell")
        mygrid.SetCellValue(1, 1, "Another cell")
        mygrid.SetCellValue(2, 2, "Yet another cell")
        mygrid.SetCellValue(3, 3, "This cell is read-only")
        mygrid.SetCellFont(0, 0, wx.Font(12, wx.ROMAN, wx.ITALIC, wx.NORMAL))
        mygrid.SetCellTextColour(1, 1, wx.RED)
        mygrid.SetCellBackgroundColour(2, 2, wx.CYAN)
        mygrid.SetReadOnly(3, 3, True)

        mygrid.SetCellEditor(5, 0, grid.GridCellNumberEditor(1,1000))
        mygrid.SetCellValue(5, 0, "123")
        mygrid.SetCellEditor(6, 0, grid.GridCellFloatEditor())
        mygrid.SetCellValue(6, 0, "123.34")
        mygrid.SetCellEditor(7, 0, grid.GridCellNumberEditor())

        mygrid.SetCellValue(6, 3, "You can veto editing this cell")


        # attribute objects let you keep a set of formatting values
        # in one spot, and reuse them if needed
        attr = grid.GridCellAttr()
        attr.SetTextColour(wx.BLACK)
        attr.SetBackgroundColour(wx.RED)
        attr.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        # you can set cell attributes for the whole row (or column)
        mygrid.SetRowAttr(5, attr)

        mygrid.SetColLabelValue(0, "Custom")
        mygrid.SetColLabelValue(1, "column")
        mygrid.SetColLabelValue(2, "labels")

        mygrid.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)

        #mygrid.SetDefaultCellOverflow(False)
        #r = wx.GridCellAutoWrapStringRenderer()
        #mygrid.SetCellRenderer(9, 1, r)

        # overflow cells
        mygrid.SetCellValue( 9, 1, "This default cell will overflow into neighboring cells, but not if you turn overflow off.");
        mygrid.SetCellSize(11, 1, 3, 3);
        mygrid.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
        mygrid.SetCellValue(11, 1, "This cell is set to span 3 rows and 3 columns");

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.components.mygrid, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

##    def OnCellLeftClick(self, event):
    def on_mygrid_mouseClick(self, event):
        self.log.write("mouseClick: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()

    def on_mygrid_mouseContextClick(self, event):
        self.log.write("mouseContextClick: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()

    def on_mygrid_mouseDoubleClick(self, event):
        self.log.write("mouseDoubleClick: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()

    def on_mygrid_mouseContextDoubleClick(self, event):
        self.log.write("mouseContextDoubleClick: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()

    def on_mygrid_labelClick(self, event):
        self.log.write("labelClick: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()

    def on_mygrid_labelContextClick(self, event):
        self.log.write("labelContextClick: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()

    def on_mygrid_labelDoubleClick(self, event):
        self.log.write("labelDoubleClick: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()

    def on_mygrid_labelContextDoubleClick(self, event):
        self.log.write("labelContextDoubleClick: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()


    def on_mygrid_rowSize(self, event):
        self.log.write("rowSize: row %d, %s\n" %
                       (event.GetRowOrCol(), event.position))
        event.skip()

    def on_mygrid_columnSize(self, event):
        self.log.write("columnSize: col %d, %s\n" %
                       (event.GetRowOrCol(), event.position))
        event.skip()

    def on_mygrid_rangeSelect(self, event):
        if event.Selecting():
            self.log.write("rangeSelect: top-left %s, bottom-right %s\n" %
                           (event.GetTopLeftCoords(), event.GetBottomRightCoords()))
        event.skip()


    def on_mygrid_cellChange(self, event):
        self.log.write("cellChange: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))

        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinants to move to in
        # idle time.
        value = self.components.mygrid.GetCellValue(event.row, event.column)
        if value == 'no good':
            self.moveTo = event.row, event.column


    def on_idle(self, event):
        if self.moveTo != None:
            self.components.mygrid.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None
        event.skip()


    def on_mygrid_selectCell(self, event):
        self.log.write("selectCell: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))

        # Another way to stay in a cell that has a bad value...
        mygrid = self.components.mygrid
        row = mygrid.GetGridCursorRow()
        col = mygrid.GetGridCursorCol()
        if mygrid.IsCellEditControlEnabled():
            mygrid.HideCellEditControl()
            mygrid.DisableCellEditControl()
        value = mygrid.GetCellValue(row, col)
        if value == 'no good 2':
            return  # cancels the cell selection
        event.skip()


    def on_mygrid_editorShown(self, event):
        if event.row == 6 and event.column == 3:
            result = dialog.messageDialog(self, "Are you sure you wish to edit this cell?",
                        "Checking", wx.YES_NO)
            if not result.accepted:
                event.Veto()
                return

        self.log.write("editorShown: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()


    def on_mygrid_editorHidden(self, event):
        if event.row == 6 and event.column == 3:
            result = dialog.messageDialog(self, "Are you sure you wish to finish editing this cell?",
                        "Checking", wx.YES_NO)
            if not result.accepted:
                event.Veto()
                return

        self.log.write("on_mygrid_editorHidden: (%d,%d) %s\n" %
                       (event.row, event.column, event.position))
        event.skip()


    def on_mygrid_editorCreated(self, event):
        self.log.write("on_mygrid_editorCreated: (%d, %d) %s\n" %
                       (event.row, event.column, event.GetControl()))


if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
