#!/usr/bin/python

"""
__version__ = "$Revision: 1.14 $"
__date__ = "$Date: 2004/08/12 19:19:01 $"
"""

from PythonCard import dialog, model
import wx

class SimpleBrowser(model.Background):

    def on_initialize(self, event):
        filename = self.application.applicationDirectory + '/index.html'
        self.components.htmlDisplay.text = filename

        btnFlags = wx.LEFT | wx.ALIGN_CENTER_VERTICAL

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.components.btnBack, 0, btnFlags, 5)
        sizer2.Add(self.components.btnForward, 0, btnFlags, 5)
        sizer2.Add(self.components.btnReload, 0, btnFlags, 5)
        sizer2.Add(self.components.fldURL, 1, btnFlags, 5)
        sizer2.Add(self.components.btnGo, 0, btnFlags, 5)
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(sizer2, 0, wx.EXPAND)
        sizer1.Add((5, 5), 0) # spacer
        sizer1.Add(self.components.htmlDisplay, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def on_htmlDisplay_titleChange(self, event):
        self.title = "SimpleIEBrowser: %s" % event.Text

    def on_htmlDisplay_statusTextChange(self, event):
        self.statusBar.text = event.Text

    def on_htmlDisplay_documentComplete(self, evt):
        self.current = evt.URL
        self.components.fldURL.text = self.current

    def on_goReload_command(self, event):
        """
        enum wxIEHtmlRefreshLevel {
             wxIEHTML_REFRESH_NORMAL = 0,
             wxIEHTML_REFRESH_IFEXPIRED = 1,
             wxIEHTML_REFRESH_CONTINUE = 2,
             wxIEHTML_REFRESH_COMPLETELY = 3
        };
        """
        # 3 is the same as wxIEHTML_REFRESH_COMPLETELY
        self.components.htmlDisplay.Refresh(3)

    def on_goBack_command(self, event):
        self.components.htmlDisplay.GoBack()

    def on_goForward_command(self, event):
        self.components.htmlDisplay.GoForward()

    def addTextToItems(self):
        target = self.components.fldURL
        text = target.text
        items = target.items
        if not items.count(text):
            items.insert(0, text)
            target.items = items
            target.text = text
            target.SetInsertionPointEnd()
            target.SetMark(-1, -1)

    def on_goURL_command(self, event):
        # KEA 2004-04-06
        # clean up the URL
        # by getting rid of leading and trailing whitespace
        # and adding http:// if it is missing from the front
        # of the url
        target = self.components.fldURL
        text = target.text.strip()
        if not text.startswith('http://'):
            text = 'http://' + text
        if target.text != text:
            target.text = text
        self.addTextToItems()
        self.components.htmlDisplay.text = self.components.fldURL.text

    def openFile(self, path):
        self.components.htmlDisplay.text = path

    def on_menuFileOpen_select(self, event):        
        wildcard = "HTML files (*.htm;*.html)|*.htm;*.html|All files (*.*)|*.*"
        result = dialog.openFileDialog(None, "Open file", '', '', wildcard)
        if result.accepted:
            path = result.paths[0]
            self.openFile(path)

    def on_fldURL_keyPress(self, event):
        keyCode = event.keyCode
        target = event.target
        if keyCode == 13:
            self.on_goURL_command(None)
        else:
            event.skip()


if __name__ == '__main__':
    app = model.Application(SimpleBrowser)
    app.MainLoop()
