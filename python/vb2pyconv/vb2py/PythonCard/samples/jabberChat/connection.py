
"""
__version__ = "$Revision: 1.10 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"
"""

import wx
import os, sys
import jabber

DEBUG_LEVEL = 1

class JabberConnection:
    def __init__(self, parent, account):
        self.keepRunning = 1
        self._parent = parent
        self.con = None
        self.server = account['server']
        self.username = account['username']
        self.password = account['password']
        self.resource = account['resource']
        self.createNewConnection()

    def createNewConnection(self):
        # should make debug level settable in configuration
        con = jabber.Client(host=self.server, debug=DEBUG_LEVEL, log=sys.stderr)
        self.con = con
        con.setMessageHandler(self.messageCB)
        con.setPresenceHandler(self.presenceCB)
        con.setIqHandler(self.iqCB)
        con.setDisconnectHandler(self.disconnectedCB)
        try:
            con.connect()
        except IOError, e:
            print "Couldn't connect: %s" % e
            ##sys.exit(0)
            return
        else:
            print "Connected"
        if con.auth(self.username, self.password, self.resource):
            print "Logged in as %s to server %s" % (self.username, self.server)
        else:
            print "eek -> ", con.lastErr, con.lastErrCode

        print "Requesting Roster Info"
        con.requestRoster()
        con.sendInitPresence()

        JID = self.username + '@' + self.server + '/' + self.resource
        print "JID", JID
        self.JID = JID
        self.shortJID = str(self.JID.split('/')[0])

        self.updateRoster()
        self.updateRosterDisplay()

        # track which groupchat rooms we've joined
        # for special presence handling
        self.groupchatJIDS = {}

    def updateRoster(self):
        _roster = self.con.getRoster()
        print "\n"
        self.roster = {}
        for jid in _roster.getJIDs():
            # 2002-11-30
            # don't show gateways in the roster
            # what is the proper handling of gateways?!
            if '@' not in str(jid):
                continue
            print "%s :: %s (%s/%s)" % \
                (jid, _roster.getOnline(jid), _roster.getStatus(jid), _roster.getShow(jid))
            self.roster[str(jid)] = [_roster.getOnline(jid), _roster.getStatus(jid), _roster.getShow(jid)]
        print "\n"

    def updateRosterDisplay(self):
        roster = self.roster
        items = {}
        for key in roster:
            jid = str(key)
            status = roster[key][0].lower()
            show = roster[key][1]
            if show is None:
                show = ""
            else:
                # I noticed that some clients might let in a CR/LF on the end
                # so might as well get rid of leading and trailing whitespace
                show = show.strip()
            items[jid] = (status, show)
            self._parent.rosterQueue.put((None, items))
            wx.WakeUpIdle()

        """
        Exception in thread Thread-1:
        Traceback (most recent call last):
          File "C:\Python22\lib\threading.py", line 408, in __bootstrap
            self.run()
          File "C:\Python22\lib\threading.py", line 396, in run
            apply(self.__target, self.__args, self.__kwargs)
          File "C:\python\jabberChat\connection.py", line 92, in spinMyWheels
            self.con.process(1)
          File "C:\python\xmlstream.py", line 450, in process
            if not len(self.read()): # length of 0 means disconnect
          File "C:\python\xmlstream.py", line 379, in read
            data_in = data_in + \
          File "<string>", line 1, in recv
        error: (10054, 'Connection reset by peer')
        """

    def spinMyWheels(self):
        while self.keepRunning and self.con is not None:
            #print "spinning..."
            try:
                self.con.process(1)
            except:
                # sometimes I get the connection error above
                # so this is an attempt to workaround losing
                # the connection by creating a new one
                self.createNewConnection()
                print "***** CONNECTION PROBLEM *****"

    def sendMessage(self, to, txt, messageType='chat'):
        print "\n"
        msg = jabber.Message(to, txt.strip())
        msg.setType(messageType)
        print "<%s> %s" % (self.JID, msg.getBody())
        self.con.send(msg)
        print "\n"

    def sendChatMessage(self, to, txt):
        self.sendMessage(to, txt, 'chat')

    def sendGroupChatMessage(self, to, txt):
        self.sendMessage(to, txt, 'groupchat')

    def joinGroupChat(self, to, nickname=None):
        if to not in self.groupchatJIDS:
            self.groupchatJIDS[to] = {}
            if nickname is None:
                nickname = self.username
            print "****** JOINING ROOM ******", to, "as", nickname
            self.sendPresence(to=to + '/' + nickname)
            # we could get an error joining, but I'm not sure 
            # where to process that yet
            
    def messageCB(self, con, msg):
        """Called when a message is recieved"""
        if msg.getBody(): ## Dont show blank messages ##
            print '<' + str(msg.getFrom()) + '>' + ' ' + msg.getBody()
            txt = msg.getBody()
            self._parent.msgQueue.put((msg.getFrom(), txt))
            wx.WakeUpIdle()
    
    def presenceCB(self, con, prs):
        """Called when a presence is recieved"""
        who = str(prs.getFrom())
        type = prs.getType()
        if type is None:
            type = 'available'
        txt = None
    
        # subscription request: 
        # - accept their subscription
        # - send request for subscription to their presence
        if type == 'subscribe':
            print "subscribe request from %s" % (who)
            con.send(jabber.Presence(to=who, type='subscribed'))
            con.send(jabber.Presence(to=who, type='subscribe'))
            txt = "subscribe request from %s" % (who)
    
        # unsubscription request: 
        # - accept their unsubscription
        # - send request for unsubscription to their presence
        elif type == 'unsubscribe':
            print "unsubscribe request from %s" % (who)
            con.send(jabber.Presence(to=who, type='unsubscribed'))
            con.send(jabber.Presence(to=who, type='unsubscribe'))
            txt = "unsubscribe request from %s" % (who)
        elif type == 'subscribed':
            print "we are now subscribed to %s" % (who)
            txt = "we are now subscribed to %s" % (who)
        elif type == 'unsubscribed':
            print "we are now unsubscribed to %s"  % (who)
            txt = "we are now unsubscribed to %s"  % (who)
        elif type == 'available':
            print "%s is available (%s / %s)" % (who, prs.getShow(), prs.getStatus())
            txt = "%s is available (%s / %s)" % (who, prs.getShow(), prs.getStatus())
            # who is of the form 'username@domain/resource'
            jid = str(who.split('/')[0])
            # KEA 2002-11-30
            # should presences for the same jid such as altis@jabber.org/Exodus
            # and altis@jabber.org/default be treated separately?
            # for now, skip duplicate jids for both
            # available and unavailable
            #
            # I'm not showing gateways either
            # and still need to figure out the proper handling
            # of them
            if '@' in jid and jid != self.shortJID:
                if jid in self.groupchatJIDS:
                    nickname = str(who.split('/')[1])
                    print "*******GROUPCHAT", jid, who, prs.getStatus(), prs.getShow()
                    self.groupchatJIDS[jid][nickname] = (prs.getStatus(), prs.getShow())
                    self._parent.rosterQueue.put((jid, self.groupchatJIDS[jid]))
                    wx.WakeUpIdle()
                else:
                    self.roster[jid] = ['online', prs.getStatus(), prs.getShow()]
                    self.updateRosterDisplay()
        elif type == 'unavailable':
            print "%s is unavailable (%s / %s)" % (who, prs.getShow(), prs.getStatus())
            txt = "%s is unavailable (%s / %s)" % (who, prs.getShow(), prs.getStatus())
            # who is of the form 'username@domain/resource'
            jid = str(who.split('/')[0])
            if '@' in jid and jid != self.shortJID:
                if jid in self.groupchatJIDS:
                    nickname = str(who.split('/')[1])
                    print "*******GROUPCHAT", jid, who, prs.getStatus(), prs.getShow()
                    try:
                        del self.groupchatJIDS[jid][nickname]
                        self._parent.rosterQueue.put((jid, self.groupchatJIDS[jid]))
                        wx.WakeUpIdle()
                    except:
                        pass
                else:
                    self.roster[jid] = ['offline', prs.getStatus(), prs.getShow()]
                    self.updateRosterDisplay()

        if txt is not None:
            # need to decide whether we want a separate queue for
            # status messages, for now just let the messages be
            # printed to the console
            #self._parent.msgQueue.put(txt)
            #wx.WakeUpIdle()
            pass
    
    def iqCB(self, con,iq):
        """Called when an iq is recieved, we just let the library handle it at the moment"""
        pass

    # see p. 145 of the Programming Jabber
    # and
    # http://www.jabber.org/protocol/coredata.html#presence
    def sendPresence(self, status="Available", to=None):
        #presence = jabber.Presence(type='available')
        presence = jabber.Presence(to)
        presence.setStatus(status)
        if status == "Available":
            # apparently "normal" is the default
            #presence.setShow("normal")
            pass
        elif status == "Do Not Disturb":
            presence.setShow("dnd")
        else:
            presence.setShow("away")
        self.con.send(presence)

    def disconnectedCB(self, con):
        print "Ouch, network error"
        #sys.exit(1)

    def disconnect(self):
        self.con.disconnect()
        print "Bye!"
