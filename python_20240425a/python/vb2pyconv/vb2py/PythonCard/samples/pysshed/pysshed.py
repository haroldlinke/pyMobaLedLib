#!/usr/bin/python
# simple SSH session manager for Linux
# vim: ai et sw=4 ts=4
#
# Copyright 2002 Phil Edwards, phil@linux2000.com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the
#       distribution.
#
# THIS SOFTWARE IS PROVIDED BY PHIL EDWARDS ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR ANY CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# IF THE DISTRIBUTION YOU HAVE RECEIVED IS IN BINARY-ONLY FORMAT, THE SOURCE
# CODE FOR THE MOST RECENTLY-RELEASED VERSION OF THIS SOFTWARE MAY BE
# OBTAINED WITHOUT REQUIRING ANY PAYMENT TO THE AUTHOR AT THE FOLLOWING URL:
#    http://www.linux2000.com/pysshed.html
#

import os, sys
import wx
from PythonCard import dialog, model
import ConfigParser
import customDialogs

# pwd only exists on *NIX
if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.pysshedrc')
    import pwd
else:
    CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]), 'pysshed.ini')

class pysshed(model.Background):

    def on_initialize(self, event):
        self.cfg = ConfigParser.ConfigParser()

        # first job is to see we have any config info
        if not os.path.exists(CONFIG_FILE):
            title = 'Initial setup'
            
            txt = 'Since this is the first time you have run PySSHed, you need to configure '
            txt += 'your default SSH preferences. Most users should find that the '
            txt += 'default settings are satisfactory. On this system, settings will be stored '
            txt += 'in "%s". Click OK to begin configuring PySSHed.' % CONFIG_FILE
            
            bull = dialog.alertDialog(self, customDialogs.wrap_string(txt, 70), title)
            
            self.cfg.add_section('Defaults')

            # set some (hopefully!) reasonable defaults
            self.cfg.set('Defaults', 'port', '22')
            if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
                self.cfg.set('Defaults', 'user', pwd.getpwuid(os.getuid())[0])
                self.cfg.set('Defaults', 'identityfile', os.path.join(os.path.join(os.path.expanduser('~'), '.ssh'), 'identity'))
                self.cfg.set('Defaults', 'command', '/usr/X11R6/bin/xterm -e ssh')
            else: 
                self.cfg.set('Defaults', 'user', '')
                self.cfg.set('Defaults', 'identityfile', os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'identity'))
                self.cfg.set('Defaults', 'command', '"C:\\Program files\\putty\\putty.exe"')

            dlg = customDialogs.prefsDialog(self, 'Defaults')
            if dlg.ShowModal() == wx.ID_OK:
                fd = open(CONFIG_FILE, 'w')
                self.cfg.write(fd)
                fd.close()
            dlg.destroy()
            
        self.cfg.read(CONFIG_FILE)
        self.updateSessionList()
        if len(self.components.sessionList.items) > 0:
            self.components.sessionList.stringSelection = self.components.sessionList.items[0]
        
    def on_connectBtn_command(self, event):
        section = self.components.sessionList.stringSelection
        if section != '':
            cmd = self.cfg.get(section, 'command')
            if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
                cmd += ' -p %s' % self.cfg.get(section, 'port')
                cmd += ' -l %s' % self.cfg.get(section, 'user')
                if self.cfg.get(section, 'identityfile') != '': cmd += ' -i %s' % self.cfg.get(section, 'identityfile')
                cmd += ' %s' % self.cfg.get(section, 'hostname')
                cmd += ' &'
                os.system(cmd)
            else:
                args = []
                args.append(os.path.basename(cmd))
                args.append('-ssh')
                args.append('-P')
                args.append('%s' % self.cfg.get(section, 'port'))
                args.append('-l')
                args.append('%s' % self.cfg.get(section, 'user'))
                if self.cfg.get(section, 'identityfile') != '':
                    args.append('-i')
                    args.append('%s' % self.cfg.get(section, 'identityfile'))
                args.append('%s' % self.cfg.get(section, 'hostname'))
                retval = os.spawnv(os.P_NOWAIT, cmd, args)
            self.components.sessionList.stringSelection = section
            
    def on_addBtn_command(self, event):
        oldlist = self.components.sessionList.items[:]
        self.cfg.add_section('NewSession')
        self.cfg.set('NewSession', 'port', self.cfg.get('Defaults', 'port'))
        self.cfg.set('NewSession', 'user', self.cfg.get('Defaults', 'user'))
        self.cfg.set('NewSession', 'identityfile', self.cfg.get('Defaults', 'identityfile'))
        self.cfg.set('NewSession', 'command', self.cfg.get('Defaults', 'command'))
        dlg = customDialogs.prefsDialog(self, 'NewSession')
        if dlg.ShowModal() == wx.ID_OK:
            bull = self.cfg.remove_section('NewSession')
            fd = open(CONFIG_FILE, 'w')
            self.cfg.write(fd)
            fd.close()
        else:
            bull = self.cfg.remove_section('NewSession')
        dlg.destroy()
        self.updateSessionList()
        newlist = self.components.sessionList.items[:]
        if newlist != oldlist:
            for item in newlist:
                if not item in oldlist:
                    self.components.sessionList.stringSelection = item
                    break
        
    def on_modifyBtn_command(self, event):
        section = self.components.sessionList.stringSelection
        if section != '':
            dlg = customDialogs.prefsDialog(self, self.components.sessionList.stringSelection)
            if dlg.ShowModal() == wx.ID_OK:
                fd = open(CONFIG_FILE, 'w')
                self.cfg.write(fd)
                fd.close()
            dlg.destroy()
            self.updateSessionList()
            self.components.sessionList.stringSelection = section
        
    def on_delBtn_command(self, event):
        msgtxt = 'Are you sure you want to delete "%s"?' % self.components.sessionList.stringSelection
        result = dialog.messageDialog(self, msgtxt, 'Caution!',
            wx.ICON_EXCLAMATION | wx.YES_NO | wx.NO_DEFAULT)
        if result.accepted:
            bull = self.cfg.remove_section(self.components.sessionList.stringSelection)
            fd = open(CONFIG_FILE, 'w')
            self.cfg.write(fd)
            fd.close()
            self.updateSessionList()
            self.components.sessionList.stringSelection = self.components.sessionList.items[0]

    def on_helpAbout_command(self, event):
        dlg = customDialogs.HTMLHelp(self)
        dlg.showModal()
        dlg.destroy()

    def updateSessionList(self):
        configlist = []
        for config in self.cfg.sections():
            if config != 'Defaults':
                configlist.append(config)
        configlist.sort()
        self.components.sessionList.items = configlist

if __name__ == '__main__':
    app = model.Application(pysshed)
    app.MainLoop()
