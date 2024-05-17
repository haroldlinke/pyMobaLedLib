import wx

class trURLDropTarget(wx.PyDropTarget):
    def __init__(self, trWindow):
        wx.PyDropTarget.__init__(self)
        self.trWin = trWindow

        self.data = wx.URLDataObject();
        self.SetDataObject(self.data)

    def OnDragOver(self, x, y, d):
        return wx.DragLink

    def OnData(self, x, y, d):
        if not self.GetData():
            return wx.DragNone

        text  = self.data.GetURL()
        
        if text.count("\n") == 0 and text.find("://") != -1:
            text = "<a href=\"" + text + "\"></a>"
        
        self.trWin.updateTextBox(text, "insert")

        return d


class trTextDropTarget(wx.PyDropTarget):
    def __init__(self, trWindow):
        wx.PyDropTarget.__init__(self)
        self.do = wx.TextDataObject()
        self.SetDataObject(self.do)
        self.trWin = trWindow

    def OnEnter(self, x, y, d):
        #print "OnEnter: %d, %d, %d" % (x, y, d)
        return wx.DragCopy

    #def OnLeave(self):
        #print "OnLeave"

    def OnDrop(self, x, y):
        #print "OnDrop: %d %d" % (x, y)
        return true

    def OnData(self, x, y, d):
        #print "OnData: %d, %d, %d" % (x, y, d)
        self.GetData()
        #print "%s" % self.do.GetText()
        self.trWin.updateTextBox(self.do.GetText())
        return d
