
"""
__version__ = "$Revision: 1.37 $"
__date__ = "$Date: 2004/05/25 19:47:08 $"

wxStyledTextCtrl documentation
http://wiki.wxpython.org/index.cgi/wxStyledTextCtrl

"""

import wx
from wx import stc
import os
import keyword
from PythonCard import configuration, event, STCStyleEditor, widget

LINE_NUMBER_MARGIN = 1
LINE_NUMBER_MARGIN_WIDTH = 40
CODE_FOLDING_MARGIN = 2
CODE_FOLDING_MARGIN_WIDTH = 12

class CodeEditorSpec(widget.WidgetSpec):
    def __init__(self):        
        events = [event.KeyPressEvent, 
                event.KeyDownEvent, 
                event.KeyUpEvent, 
                #event.TextEnterEvent,
                #event.TextUpdateEvent,
                #event.CloseFieldEvent
        ]
        attributes = {
            'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
            'text' : { 'presence' : 'optional', 'default' : '' },
            'editable' : { 'presence' : 'optional', 'default' : 1 },
            #'border' : { 'presence' : 'optional', 'default' : '3d', 'values' : [ '3d', 'none' ] }
        }
        widget.WidgetSpec.__init__(self, 'CodeEditor', 'Widget', events, attributes )


# POB 2002-05-04
# Borrowed stuff from PyCrust just to get this working.
if wx.Platform == '__WXMSW__':
    faces = { 'times'  : 'Times New Roman',
              'mono'   : 'Courier New',
              'helv'   : 'Lucida Console',
              'lucida' : 'Lucida Console',
              'other'  : 'Comic Sans MS',
              'size'   : 10,
              'lnsize' : 9,
              'backcol': '#FFFFFF',
            }
else:  # GTK
    faces = { 'times'  : 'Times',
              'mono'   : 'Courier',
              'helv'   : 'Helvetica',
              'other'  : 'new century schoolbook',
              'size'   : 12,
              'lnsize' : 10,
              'backcol': '#FFFFFF',
            }

class CodeEditor(widget.Widget, stc.StyledTextCtrl):
    """
    A Python source code editor.
    """

    _spec = CodeEditorSpec()

    def __init__( self, aParent,  aResource ) :
        stc.StyledTextCtrl.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            #aResource.text, 
            aResource.position, 
            aResource.size, 
            #style = wxTE_PROCESS_ENTER | borderStyle | wxCLIP_SIBLINGS,
            #style = borderStyle | wx.CLIP_SIBLINGS,
            style = wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name )

        widget.Widget.__init__( self, aParent, aResource )

        # POB 2002-05-04
        # Borrowed stuff from PyCrust just to get this working.
        self.SetMarginType(LINE_NUMBER_MARGIN, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(LINE_NUMBER_MARGIN, LINE_NUMBER_MARGIN_WIDTH)
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, ' '.join(keyword.kwlist))
        self._setStyles(faces)
        self.SetViewWhiteSpace(0)
        self.SetTabWidth(4)
        self.SetUseTabs(0)
        self.CallTipSetBackground(wx.Colour(255, 255, 232))
        self.SetBackSpaceUnIndents(1)

        stc.EVT_STC_UPDATEUI(self, self.GetId(), self.OnUpdateUI)


        # KEA 2002-12-16
        # code folding code taken from
        # wxStyledTextCtrl_2.py
        self.SetProperty("fold", "1")
        # Setup a margin to hold fold markers
        self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetMarginType(CODE_FOLDING_MARGIN, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(CODE_FOLDING_MARGIN, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(CODE_FOLDING_MARGIN, 1)
        self.SetMarginWidth(CODE_FOLDING_MARGIN, CODE_FOLDING_MARGIN_WIDTH)
        # initially code folding should be off
        self.SetMarginWidth(CODE_FOLDING_MARGIN, 0)
        
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,  "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,  "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,    "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,  "white", "black")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS, "white", "black")

        # KEA 2004-05-20
        # get rid of the annoying text drag and drop
        #stc.EVT_STC_START_DRAG(self, self.GetId(), self.OnStartDrag)
        
        stc.EVT_STC_MARGINCLICK(self, self.GetId(), self.OnMarginClick)

        if not aResource.editable:
            self._setEditable(False)
        
        #adapter = CodeEditorEventBinding(self)
        #adapter.bindEvents()
        self._bindEvents(event.WIDGET_EVENTS + (event.KeyPressEvent, event.KeyDownEvent, event.KeyUpEvent))
        
    # POB 2002-05-04
    # Borrowed stuff from PyCrust just to get this working.
    def _setStyles(self, faces):
        """Configure font size, typeface and color for lexer."""
        
        # Default style
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)

        self.StyleClearAll()

        # Built in styles
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(mono)s,size:%(lnsize)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(mono)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#0000FF,back:#FFFF88")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#FF0000,back:#FFFF88")

        # Python styles
        self.StyleSetSpec(stc.STC_P_DEFAULT, "face:%(mono)s" % faces)
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(mono)s" % faces)
        self.StyleSetSpec(stc.STC_P_NUMBER, "")
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(mono)s" % faces)
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(mono)s" % faces)
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold")
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000")
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#000033,back:#FFFFE8")
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold")
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold")
        self.StyleSetSpec(stc.STC_P_OPERATOR, "")
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "")
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F")
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eolfilled" % faces)

        configfile = configuration.getStyleConfigPath()
        if os.path.exists(configfile):
            STCStyleEditor.initSTC(self, configfile, 'python')

    def _getLineNumbersVisible(self):
        return self.GetMarginWidth(LINE_NUMBER_MARGIN) / LINE_NUMBER_MARGIN_WIDTH

    def _setLineNumbersVisible(self, aBoolean):
        self.SetMarginWidth(LINE_NUMBER_MARGIN, LINE_NUMBER_MARGIN_WIDTH * int(aBoolean))

    def _getCodeFoldingVisible(self):
        return self.GetMarginWidth(CODE_FOLDING_MARGIN) / CODE_FOLDING_MARGIN_WIDTH

    def _setCodeFoldingVisible(self, aBoolean):
        if not aBoolean:
            self.FoldAll(toggle=0)
        self.SetMarginWidth(CODE_FOLDING_MARGIN, CODE_FOLDING_MARGIN_WIDTH * int(aBoolean))

    # KEA 2002-05-03
    # GetReadOnly and SetReadOnly are the opposite of
    # IsEditable and SetEditable in wxTextCtrl
    # so the methods are wrapped below

    def _getEditable(self):
        return not self.GetReadOnly()

    def _setEditable(self, aBoolean):
        self.SetReadOnly(not aBoolean)

    def _getText(self):
        return self.GetText()

    def _setText(self, text):
        if self.GetReadOnly():
            self.SetReadOnly(0)
            self.SetText(text)
            self.SetReadOnly(1)
        else:
            self.SetText(text)

    # KEA 2002-05-20
    # methods added to mimic wxTextCtrl

    def CanCopy(self):
        return 1

    def CanCut(self):
        return 1

    # KEA 2002-05-06
    # taken from wxPython\lib\pyshell.py
    def OnUpdateUI(self, evt):
        #document = self.components.document
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            # KEA 2002-05-29
            # see message from Jean-Michel Fauth 
            # http://aspn.activestate.com/ASPN/Mail/Message/wxPython-users/1218004
            #******
            if charBefore < 0:
                charBefore = 32 #mimic a space
            #******
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            # KEA 2002-05-29
            # see message from Jean-Michel Fauth 
            # http://aspn.activestate.com/ASPN/Mail/Message/wxPython-users/1218004
            #******
            if charAfter < 0:
                charAfter = 32 #mimic a space
            #******
            styleAfter = self.GetStyleAt(caretPos)
            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

    # KEA 2002-12-16
    # code folding code taken from
    # wxStyledTextCtrl_2.py
    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, 1)
                        self.Expand(lineClicked, 1, 1, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, 0)
                            self.Expand(lineClicked, 0, 1, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, 1)
                            self.Expand(lineClicked, 1, 1, 100)
                    else:
                        self.ToggleFold(lineClicked)


    def FoldAll(self, toggle=1):
        lineCount = self.GetLineCount()
        expanding = 1

        if toggle:
            # find out if we are folding or unfolding
            for lineNum in range(lineCount):
                if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                    expanding = not self.GetFoldExpanded(lineNum)
                    break;

        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, 1)
                    lineNum = self.Expand(lineNum, 1)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, 0)
                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1



    def Expand(self, line, doExpand, force=0, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, 1)
                    else:
                        self.SetFoldExpanded(line, 0)
                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, 1, force, visLevels-1)
                    else:
                        line = self.Expand(line, 0, force, visLevels-1)
            else:
                line = line + 1;

        return line

    def setEditorStyle(self, ext=None):
        config = configuration.getStyleConfigPath()
        if config is not None:
            if ext is not None:
                ext = ext.lower().split('.')[-1]
            if ext in ['py', 'pyw']:
                style = 'python'
            elif ext in ['ini', 'text', 'txt']:
                style = 'text'
            elif ext in ['htm', 'html']:
                # 'html' style appears broken, just use xml for now
                style = 'xml'
            elif ext in ['rdf', 'xml']:
                style = 'xml'
            else:
                style = 'text'
            STCStyleEditor.initSTC(self, config, style)

    def OnStartDrag(self, evt):
        evt.SetDragText("")
        pos = self.GetCurrentPos()
        self.SetSelection(pos, pos)
        evt.Skip()

    ClearSelection = stc.StyledTextCtrl.Clear

    codeFoldingVisible = property(_getCodeFoldingVisible, _setCodeFoldingVisible)
    editable = property(_getEditable, _setEditable)
    lineNumbersVisible = property(_getLineNumbersVisible, _setLineNumbersVisible)
    text = property(_getText, _setText)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].CodeEditor)
