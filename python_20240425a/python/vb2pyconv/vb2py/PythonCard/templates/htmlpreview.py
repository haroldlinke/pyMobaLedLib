#!/usr/bin/python

"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/07/26 15:54:31 $"
"""

from PythonCard import model
import wx
import sys

class HtmlPreview(model.Background):

    def on_initialize(self, event):
        if sys.platform.startswith('win'):
            size = self.components.html.size
            del self.components['html']
            self.components['html'] = {'type':'IEHtmlWindow', 'name':'html', 
                'position':(0, 0), 'size':size, 'visible':True}
        else:
            self.components.html.SetRelatedFrame(self, "HTML Preview: %s")
            self.components.html.SetRelatedStatusBar(0)

        self.singleItemExpandingSizerLayout()

    def on_close(self, event):
        self.visible = False
