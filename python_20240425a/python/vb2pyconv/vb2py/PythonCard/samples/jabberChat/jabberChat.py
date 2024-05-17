#!/usr/bin/python

"""
__version__ = "$Revision: 1.34 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"
"""

from PythonCard import configuration, model, sound, timer
import threading 
import Queue
import ConfigParser
import wx

import os
import jabber
import time
import shutil

from chatWindow import ChatWindow
from groupChatWindow import GroupChatWindow
from connection import JabberConnection
import conferenceDialog

CONFIG_FILE = 'jabberChat.ini'    

class Chat(model.Background):

    def on_initialize(self, event):
        self.initSizers()
        self.loadConfig()
        self.displayOfflineUsers = 0
        self.roster = {}
        self.chatWindows = {}
        
        self.msgQueue = Queue.Queue()
        self.rosterQueue = Queue.Queue()

        self.jabberConnection = JabberConnection(self, self.account)
        self.thread = threading.Thread(target = self.jabberConnection.spinMyWheels)
        self.thread.setDaemon(1)
        self.thread.start()

        self.idleTimer = timer.Timer(self.components.listRoster, -1)
        self.idleTimer.start(1000)  # 1 second

        self.doResetIdle()

        # the Available and Do Not Disturb strings
        # should probably be settable as resource strings
        # the connection module references them as menu item labels
        # when the user starts the program, just default to Available
        self.statusBar.text = "Available"

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.components.listRoster, 1, wx.EXPAND)
        
        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def setChatWindowFont(self):
        for win in self.chatWindows.itervalues():
            win.setFonts(self.config['font'])

    def on_doSetFont_command(self, event):
        result = dialog.fontDialog(self, self.components.fldDocument.font)
        if result.accepted:
            self.config['font'] = result.font
            self.setChatWindowFont()

    def loadConfig(self):
        self.configPath = os.path.join(configuration.homedir, 'jabberchat')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        basePath = self.application.applicationDirectory
        configPath = os.path.join(self.configPath, CONFIG_FILE)
        if not os.path.exists(configPath):
            shutil.copy2(os.path.join(basePath, CONFIG_FILE), configPath)
        namesPath = os.path.join(self.configPath, 'names.txt')
        if not os.path.exists(namesPath):
            shutil.copy2(os.path.join(basePath, 'names.txt'), namesPath)
        parser = ConfigParser.ConfigParser()
        parser.read(configPath)
        self.account = {}
        self.account['server'] = parser.get('Account', 'server')
        self.account['username'] = parser.get('Account', 'username')
        self.account['password'] = parser.get('Account', 'password')
        self.account['resource'] = parser.get('Account', 'resource')

        self.config = {}
        # this needs to be made safe instead of using eval
        try:
            self.config['font'] = eval(parser.get('ChatWindow', 'font', None))
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.config['font'] = None
        try:
            self.config['playsound'] = eval(parser.get('Options', 'playsound'))
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.config['playsound'] = 0
        try:
            self.config['idletime'] = eval(parser.get('Options', 'idletime')) * 60
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.config['idletime'] = 0

        self.displayNames = {}
        try:
            f = open(namesPath)
            data = f.readlines()
            f.close()
            for line in data:
                jid, name = line.rstrip().split(',')
                self.displayNames[jid] = name
        except IOError:
            pass

    # when user selects "Available"
    # we need to reset
    def doResetIdle(self):
        self.checkForIdle = 1
        self.userIsIdle = 0
        self.startIdle = time.time()
        self.lastPosition = wx.GetMousePosition()
        
    def on_idle(self, event):
        # handle incoming Jabber messages
        if not self.msgQueue.empty():
            msg = self.msgQueue.get()
            self.doDisplayMsgReceived(msg)
            event.RequestMore()
        # handle roster changes
        if not self.rosterQueue.empty():
            jid, roster = self.rosterQueue.get()
            if jid is None:
                self.updateRosterDisplay(roster)
            else:
                self.updateGroupChatRosterDisplay(jid, roster) 
            event.RequestMore()

    # KEA 2002-11-17
    # updates to how the roster displays
    # I would like to move this into a MultiColumnList
    # with icons for online/offline...
    # 2002-11-30
    # moved from JabberConnection class
    # I'm still not sure that thread conflicts won't occur
    # but this at least seems safer
    # one thing that probably still needs to be added is a way
    # of always using the same display order
    def updateRosterDisplay(self, roster):
        items = []
        # use this instead of displayed list since the
        # display may have a name or jid and the roster
        # itself is a dictionary that doesn't match one to one
        # with self._parent.components.listRoster.items
        self.displayedRosterList = []
        # KEA 2003-06-04
        # roster dictionary might change in size
        # due to other thread, so make a list of keys
        rosterList = roster.keys()
        for key in rosterList:
            status = roster[key][0]
            show = roster[key][1]
            if show:
                show = " (%s)" % roster[key][1]
            else:
                show = ''
            name = self.displayNames.get(key, key)
            if status == 'online':
                items.append('* ' + name + show)
                self.displayedRosterList.append(key)
            elif self.displayOfflineUsers:
                items.append('  ' + name)
                self.displayedRosterList.append(key)
        self.components.listRoster.items = items
        self.roster = roster

    def updateGroupChatRosterDisplay(self, jid, roster):
        listRoster = self.chatWindows[jid].components.listRoster
        items = []
        for key in roster:
            status = roster[key][0]
            if status:
                items.append("%s (%s)" % (key, str(status)))
            else:
                items.append(key)
        items.sort()
        listRoster.items = items
        
    def on_listRoster_timer(self, event):
        # check for user idle if user is currently Available
        # but don't bother if Do Not Disturb... are set instead
        if self.checkForIdle and (self.config['idletime'] != 0):
            position = wx.GetMousePosition()
            if position == self.lastPosition:
                if self.userIsIdle == 0:
                    # check whether we've been idle too long
                    if (time.time() - self.startIdle) > self.config['idletime']:
                        self.userIsIdle = 1
                        self.jabberConnection.sendPresence("Idle")
                        self.statusBar.text = "Idle"
                        #print "***user is idle***"
            else:
                if self.userIsIdle:
                    #print "***user is no longer idle"
                    #print "there was no activity for", round((time.time() - self.startIdle) / 60), "minutes"
                    self.userIsIdle = 0
                    self.jabberConnection.sendPresence("Available")
                    self.statusBar.text = "Available"
                self.startIdle = time.time()
                self.lastPosition = position

    def createChatWindow(self, jid):
        # the jid should be in the form of username@domain
        win = model.childWindow(self, ChatWindow)
        win.setFonts(self.config['font'])
        # override resource position
        #win.SetPosition((425, -1))
        # just in case, convert to string, will this clear up Unicode issues?
        jid = str(jid)
        toName = self.displayNames.get(jid, jid)
        win.setToJID(jid, toName)
        win.visible = True
        self.chatWindows[jid] = win

    def createGroupChatWindow(self, jid, nickname=None):
        # the jid should be in the form of username@domain
        win = model.childWindow(self, GroupChatWindow)
        win.setFonts(self.config['font'])
        # override resource position
        #win.SetPosition((425, -1))
        # just in case, convert to string, will this clear up Unicode issues?
        jid = str(jid)
        toName = self.displayNames.get(jid, jid)

        if nickname is None:
            nickname = self.jabberConnection.username
        win.nickname = nickname

        win.setToJID(jid, toName)
        win.visible = True
        self.chatWindows[jid] = win
        self.jabberConnection.joinGroupChat(jid, nickname)

    def playIncomingSound(self):
        if self.config['playsound']:
            try:
                filename = os.path.join(self.application.applicationDirectory, 'incoming.wav')
                snd = sound.Sound(filename)
                snd.play(1, 0)
            except IOError:
                pass
        
    def doDisplayMsgReceived(self, data):
        if data is not None:
            jid, txt = data
            jid = str(jid)
            try:
                jid, resource = jid.split('/')
            except ValueError:
                resource = "default"
            if jid not in self.chatWindows:
                self.createChatWindow(jid)
            self.playIncomingSound()
            #self.components.fldTranscript.appendText(data + '\n')
            self.chatWindows[jid].appendMessage(jid + "/" + resource, txt)
        else:
            pass

    # this code is dependent on the format
    # of the text in the list
    # so a change to the updateRosterDisplay
    # method in the connection module must be
    # reflected here until the jids are stored
    # outside the list
    def on_listRoster_mouseDoubleClick(self, event):
        jid = self.displayedRosterList[event.target.selection]
        if jid not in self.chatWindows:
            self.createChatWindow(jid)
        else:
            self.chatWindows[jid].visible = True
        # make sure the chat window is in front
        # and isn't minimized (iconized)
        if self.chatWindows[jid].IsIconized():
            self.chatWindows[jid].Iconize(0)
        wx.CallAfter(self.chatWindows[jid].Raise)

    def on_close(self, event):
        self.jabberConnection.keepRunning = 0
        self.jabberConnection.disconnect()
        self.idleTimer.stop()
        event.skip()
        
    def on_changeStatus_command(self, event):
        self.jabberConnection.sendPresence(event.target.label)
        self.statusBar.text = event.target.label
        if event.target.label == "Available":
            self.doResetIdle()
        else:
            self.checkForIdle = 0

    def on_menuOptionsDisplayOfflineUsers_select(self, event):
        self.displayOfflineUsers = event.IsChecked()
        self.updateRosterDisplay(self.roster)

    def on_menuFileJoinConference_select(self, event):
        room = ''
        server = None
        nickname = self.jabberConnection.username
        result = conferenceDialog.conferenceDialog(self, '', server, nickname)
        if result.accepted:
            room = result.room
            server = result.server
            nickname = result.nickname
            jid = room + '@' + server
            self.createGroupChatWindow(jid, nickname)


if __name__ == '__main__':
    app = model.Application(Chat)
    app.MainLoop()
