#!/usr/bin/env python
"""
__version__ = "$Revision: 1.7 $"
__date__ = "$Date: 2004/08/27 02:03:25 $"

"""

import os
from PythonCard import dialog, model
from codeEditor import CodeEditor
from wx import stc
import webbrowser

# reST
from PythonCard.templates.htmlpreview import HtmlPreview
from snippet import restify


class RestEditor(CodeEditor):

    def on_initialize(self, event):
        super(RestEditor, self).on_initialize(event)
        self.renderOnReturn = self.menuBar.getChecked('menuFormatRenderOnReturn')
        self.previewWindow = model.childWindow(self, HtmlPreview)
        #self.previewWindow.position = (425, -1)
        self.previewWindow.visible = True
        self.html = ''

    # reST
    def on_previewPost_command(self, event):
        self.previewWindow.Show()
        txt = self.components.document.text
        if self.menuBar.getChecked('menuViewSourceIsHtml'):
            firstLine = txt[:10].lower()
            if firstLine.startswith('<!doctype') or firstLine.startswith('<html'):
                # assume full HTML document
                html = txt
            else:
                html = '<html>\n<head>\n</head>\n<body>\n' + txt + '\n</body>\n</html>\n'
        else:
            # KEA 2004-08-15
            # snippet.restify is returning None when there is a reST error
            # what's a better way to provide feedback to the user without barfing
            # all over the output?
            rest = restify(txt)
            if rest:
                html = '<html>\n<head>\n</head>\n<body>\n' + rest + '\n</body>\n</html>\n'
            else:
                html = self.previewWindow.components.html.text
        # do make sure stylesheets and relative image references can be found
        # might need to chdir here
        # won't work until there is a document path
        curdir = os.getcwd()
        self.previewWindow.components.html.text = html
        self.html = html
        os.chdir(curdir)

    def on_document_keyDown(self, event):
        if event.keyCode == 13 and self.renderOnReturn:
            # since we won't be calling skip, insert a newline manually
            self.components.document.CmdKeyExecute(stc.STC_CMD_NEWLINE)
            self.on_previewPost_command(None)
        else:
            event.skip()

    def saveHtmlFile(self, path):
        try:
            f = open(path, 'wb')
            try:
                f.write(self.html)
            finally:
                f.close()
        except:
            pass

    def on_saveHtml_command(self, event):
        wildcard = "HTML files (*.html)|*.html|All files (*.*)|*.*"
        #wildcard = self.resource.strings.saveAsWildcard
        if self.documentPath is None:
            dir = ''
            filename = '*.html'
        else:
            dir = os.path.dirname(self.documentPath)
            filename = os.path.splitext(os.path.basename(self.documentPath))[0] + '.html'
        result = dialog.saveFileDialog(None, self.resource.strings.saveAs, dir, filename, wildcard)
        if result.accepted:
            path = result.paths[0]
            self.saveHtmlFile(path)
        
    def on_menuFormatRenderOnReturn_select(self, event):
        self.renderOnReturn = self.menuBar.getChecked('menuFormatRenderOnReturn')

    def on_doHelpRest_command(self, event):
        webbrowser.open('http://docutils.sourceforge.net/rst.html')

    def on_doHelpRestQuickReference_command(self, event):
        webbrowser.open('http://docutils.sourceforge.net/docs/user/rst/quickref.html')

if __name__ == '__main__':
    app = model.Application(RestEditor)
    app.MainLoop()
