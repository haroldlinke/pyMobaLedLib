
"""
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2004/11/01 01:11:22 $"
"""

import wx
from PythonCard import event, widget

class NotebookEvent(event.Event):
    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        aWxEvent.oldSelection = aWxEvent.GetOldSelection()
        aWxEvent.selection = aWxEvent.GetSelection()
        return aWxEvent

class NotebookPageChangedEvent(NotebookEvent):
    name = 'pageChanged'
    binding = wx.EVT_NOTEBOOK_PAGE_CHANGED
    id = wx.wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGED

class NotebookPageChangingEvent(NotebookEvent):
    name = 'pageChanging'
    binding = wx.EVT_NOTEBOOK_PAGE_CHANGING
    id = wx.wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGING

NotebookEvents = (NotebookPageChangedEvent, 
                  NotebookPageChangingEvent)


class NotebookSpec(widget.WidgetSpec):
    def __init__(self):
        events = list(NotebookEvents)
        attributes = {
            # KEA 2004-09-14
            # we could provide an attribute for the labels
            #'label' : { 'presence' : 'optional', 'default':'Button' },
            #'default':{'presence':'optional', 'default':0}
            }
        widget.WidgetSpec.__init__(self, 'Notebook', 'Widget', events, attributes )


class Notebook(widget.Widget, wx.Notebook):

    _spec = NotebookSpec()

    def __init__(self, aParent,  aResource):
        wx.Notebook.__init__(self,
                    aParent,
                    widget.makeNewId(aResource.id),
                    aResource.position,
                    aResource.size,
                    style = wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
                    name = aResource.name
                   )

        widget.Widget.__init__(self, aParent, aResource)
        
        self._bindEvents(self._spec._events)

    def _getPageNames(self):
        names = []
        for i in range(self.GetPageCount()):
            names.append(self.GetPageText(i))
        return names

    def _getStringSelection(self):
        return self.GetPageText(self.GetSelection())

    def _setStringSelection(self, s):
        names = self._getPageNames()
        try:
            self.SetSelection(names.index(s))
        except:
            # what kind of exception should we throw here for
            # an invalid string selection?
            pass

    # KEA 2004-09-14
    # rather than using all these methods there could
    # be a list wrapper where the __add__, __del__, etc.
    # methods call the right method below
    # but that might be needlessly complicated
    # I didn't add aliases for all methods
    # in particular I'm not sure about image support
    
    addPage = wx.Notebook.AddPage
    deleteAllPages = wx.Notebook.DeleteAllPages
    deletePage = wx.Notebook.DeletePage
    getPage = wx.Notebook.GetPage
    getPageCount = wx.Notebook.GetPageCount
    getPageText = wx.Notebook.GetPageText
    #getSelection = wx.Notebook.GetSelection
    insertPage = wx.Notebook.InsertPage
    removePage = wx.Notebook.RemovePage
    setPageText = wx.Notebook.SetPageText
    #setSelection = wx.Notebook.SetSelection
    
    selection = property(wx.Notebook.GetSelection, wx.Notebook.SetSelection)
    stringSelection = property(_getStringSelection, _setStringSelection)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Notebook)
