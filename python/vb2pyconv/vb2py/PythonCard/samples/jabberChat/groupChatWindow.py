#!/usr/bin/python

"""
__version__ = "$Revision: 1.7 $"
__date__ = "$Date: 2004/04/25 23:12:46 $"
"""

import PythonCard
from PythonCard import dialog, log, model
import wx

import os
import time

import chatWindow

class GroupChatWindow(chatWindow.ChatWindow):

    # this isn't quite right, the wxFlexGridSizer
    # containing the headers should expand horizontally as the window
    # expands
    def initSizers(self):
        comp = self.components
        
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        
        stcSizerAttrs = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL         
        fldSizerAttrs = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND
        vertFlags = wx.LEFT | wx.TOP | wx.ALIGN_LEFT
        chkSizerAttrs = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL

        sizer2.Add(comp.fldTranscript, 1, wx.EXPAND)
        #sizer2.Add(comp.fldInput, 1, fldSizerAttrs, 20)
        #sizer2.Add((5, 5), 0)  # spacer
        sizer2.Add(comp.listRoster, 0, wx.EXPAND, 20)

        sizer3.Add(comp.fldInput, 1, fldSizerAttrs, 20)
        sizer3.Add((5, 5), 0)  # spacer
        sizer3.Add(comp.btnSend, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 20)

        sizer1.Add(sizer2, 1, wx.EXPAND)
        sizer1.Add((5, 5), 0)  # spacer
        sizer1.Add(sizer3, 0, wx.EXPAND)

        self.sizer1 = sizer1

        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()


    def setToJID(self, jid, toName):
        self.toJID = jid
        self.toName = toName
        if jid == toName:
            self.title = jid
        else:
            self.title = "%s (%s)" % (toName, jid)

    def appendMessage(self, jid, txt):
##        oldFocus = self.findFocus()

        jid = str(jid)
        # appendMessage could be called before
        # openBackground event is processed
        if not hasattr(self, 'parent'):
            self.parent = self.GetParent()
        # make sure the chat window is in front

        now = time.localtime(time.time())
        timeStr = time.strftime("[%H:%M:%S] ", now)
        
        # in groupchat, the resource is the nickname
        # jabber@conference.jabber.org/altis
        try:
            nickname = jid.split('/')[1]
            if nickname == 'default':
                # this is probably some status message like a user joining
                nickname = jid
        except:
            # this is probably some status message like a user joining
            nickname = jid

        f = self.components.fldTranscript.font.description()
        f['style'] = 'bold'
        color = 'black'
        if nickname == jid:
            color = 'green'
        elif nickname != self.nickname:
            color = 'blue'
        self.components.fldTranscript.SetDefaultStyle(wx.TextAttr(color, 
            font=PythonCard.font.fontFromDescription(f)))

        if len(self.components.fldTranscript.text) == 0:
            self.components.fldTranscript.appendText(timeStr + nickname + ":")
        else:
            self.components.fldTranscript.appendText("\n" + timeStr + nickname + ":")
        
        f['style'] = 'regular'
        if nickname == jid:
            color = 'green'
        else:
            color = 'black'
        self.components.fldTranscript.SetDefaultStyle(wx.TextAttr(color, 
            font=PythonCard.font.fontFromDescription(f)))

        # making it editable, should force auto-scroll
        # but it doesn't seem to work, setting the focus
        # appears to be the key
        #self.components.fldTranscript.editable = 1
        self.components.fldTranscript.appendText(" " + str(txt))
        ##self.components.fldTranscript.SetInsertionPointEnd()
        #self.components.fldTranscript.editable = 0
##        self.components.fldTranscript.setFocus()
##        if (oldFocus == self.components.fldInput) or (oldFocus == self.components.btnSend):
##            self.components.fldInput.setFocus()
##        elif oldFocus is not None:
##            oldFocus.setFocus()
##        if oldFocus:
##            oldFocus.setFocus()
##        else:
##            self.components.fldInput.setFocus()

        if self.GetParent().menuBar.getChecked('menuOptionsShowWindow'):
            if self.IsIconized():
                self.Iconize(0)
            self.visible = True
        if self.GetParent().menuBar.getChecked('menuOptionsRaiseWindow'):
            wx.CallAfter(self.Raise)

    def on_doSend_command(self, event):
        txt = self.components.fldInput.text.rstrip()
        if txt:
            self.parent.jabberConnection.sendGroupChatMessage(self.toJID, txt)
            #self.appendMessage(self.parent.jabberConnection.JID, txt)
            self.components.fldInput.text = ""

