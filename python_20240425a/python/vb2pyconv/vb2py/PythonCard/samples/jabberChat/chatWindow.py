#!/usr/bin/python

"""
__version__ = "$Revision: 1.22 $"
__date__ = "$Date: 2004/05/05 16:53:26 $"
"""

import PythonCard
from PythonCard import dialog, log, model
import wx

import os
import time

class ChatWindow(model.Background):

    def on_initialize(self, event):
        if not hasattr(self, 'parent'):
            self.parent = self.GetParent()
        self.initSizers()
        self.components.fldInput.setFocus()

    # this isn't quite right, the wxFlexGridSizer
    # containing the headers should expand horizontally as the window
    # expands
    def initSizers(self):
        comp = self.components
        
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
        stcSizerAttrs = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL         
        fldSizerAttrs = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND
        vertFlags = wx.LEFT | wx.TOP | wx.ALIGN_LEFT
        chkSizerAttrs = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL

        sizer2.Add(comp.fldInput, 1, fldSizerAttrs, 20)
        sizer2.Add((5, 5), 0)  # spacer
        sizer2.Add(comp.btnSend, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 20)

        sizer1.Add(comp.fldTranscript, 1, wx.EXPAND)
        sizer1.Add((5, 5), 0)  # spacer
        sizer1.Add(sizer2, 0, wx.EXPAND)

        self.sizer1 = sizer1

        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def setFonts(self, font=None):
        if font:
            self.components.fldInput.font = font
            self.components.fldTranscript.font = font

    def setToJID(self, jid, toName):
        self.toJID = jid
        self.toName = toName
        if jid == toName:
            self.title = jid
        else:
            self.title = "%s (%s)" % (toName, jid)

    def appendMessage(self, jid, txt):
        oldFocus = self.findFocus()

        jid = str(jid)
        # appendMessage could be called before
        # openBackground event is processed
        if not hasattr(self, 'parent'):
            self.parent = self.GetParent()

        now = time.localtime(time.time())
        timeStr = time.strftime("[%H:%M:%S] ", now)
        
        #self.components.fldTranscript.appendText("<" + str(jid) + "> " + str(txt) + '\n')
        f = self.components.fldTranscript.font.description()
        f['style'] = 'bold'
        color = 'black'
        if self.parent.jabberConnection.JID != jid:
            color = 'blue'
        self.components.fldTranscript.SetDefaultStyle(wx.TextAttr(color, 
            font=PythonCard.font.fontFromDescription(f)))

        # this might be changed to get a nickname or full name
        # based on the jid
        # strip off resource for matching purposes
        shortJID = jid.split('/')[0]
        if shortJID in self.parent.displayNames:
            # use just the first name
            # this is potentially buggy
            # but I don't really want to display the full name
            # so I probably need both a full name and nickname field
            nickname = self.parent.displayNames[shortJID].split(" ")[0]
        else:
            nickname = shortJID.split('@')[0]
        if len(self.components.fldTranscript.text) == 0:
            self.components.fldTranscript.appendText(timeStr + nickname + ":")
        else:
            self.components.fldTranscript.appendText("\n" + timeStr + nickname + ":")
            # workaround for scroll bug
            # http://sourceforge.net/tracker/?func=detail&aid=665381&group_id=9863&atid=109863
            self.components.fldTranscript.ScrollLines(-1)
                    
        f['style'] = 'regular'
        self.components.fldTranscript.SetDefaultStyle(wx.TextAttr('black', 
            font=PythonCard.font.fontFromDescription(f)))
        
        ##oldFocus = self.findFocus()
        # making it editable, should force auto-scroll
        # but it doesn't seem to work, setting the focus
        # appears to be the key
        #self.components.fldTranscript.editable = 1
        self.components.fldTranscript.appendText(" " + str(txt))
        ##self.components.fldTranscript.SetInsertionPointEnd()
        #self.components.fldTranscript.editable = 0
        ##self.components.fldTranscript.setFocus()
        ##if (oldFocus == self.components.fldInput) or (oldFocus == self.components.btnSend):
        ##    self.components.fldInput.setFocus()
        ##elif oldFocus is not None:
        ##    oldFocus.setFocus()
        if self.GetParent().menuBar.getChecked('menuOptionsShowWindow'):
            # this will bring a window in front
            # of another in the app and steal the focus
            # which might not be what the user wants
            # so show and raise are separate options
            if self.IsIconized():
                self.Iconize(0)
            self.visible = True
        # make sure the chat window is in front
        if self.GetParent().menuBar.getChecked('menuOptionsRaiseWindow'):
            wx.CallAfter(self.Raise)

    def on_fldInput_keyPress(self, event):
        keyCode = event.keyCode
        if keyCode == 13:
            if self.menuBar.getChecked('menuOptionsSendOnReturn'):
                self.on_doSend_command(None)
            else:
                event.skip()
        else:
            event.skip()

    def on_doSend_command(self, event):
        txt = self.components.fldInput.text.rstrip()
        if txt:
            self.parent.jabberConnection.sendChatMessage(self.toJID, txt)
            self.appendMessage(self.parent.jabberConnection.JID, txt)
            self.components.fldInput.text = ""

    def on_menuFileClose_select(self, event):
        self.close()

    def on_close(self, event):
        # just hide the window until the app is actually closed
        # this simplifies keeping the transcript up-to-date
        # and means we don't have to worry about a missing window
        # or multiple windows for each id we are sending/receiving
        self.visible = False
