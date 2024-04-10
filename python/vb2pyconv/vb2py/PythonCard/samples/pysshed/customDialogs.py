# customDialogs.py
# This file contains all the custom dialogs (each based on CustomDialog) used by PySSHed
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
from PythonCard import dialog, resource, graphic, model
from PythonCard.model import CustomDialog
import wx
import os, time, socket

class HTMLHelp(CustomDialog):
    """Displays an HTML based about box"""

    def __init__(self, aBg, links=None):
        path = os.path.join(aBg.application.applicationDirectory, 'helpAbout')
        aDialogRsrc = resource.ResourceFile(model.internationalResourceName(path)).getResource()
        CustomDialog.__init__(self, aBg, aDialogRsrc)
        self.parent = aBg

        # links is a 3-element list giving the HTML files to use for the About, Author
        # and License buttons
        if links is None: links = ['about.html', 'author.html', 'license.html']
        self.links = links
        self.components.HtmlWindow.text = self.links[0]
    
    def on_btnOK_mouseClick(self, event):
        event.skip()

    def on_AboutBtn_mouseClick(self, event):
        self.components.HtmlWindow.text = self.links[0]

    def on_AuthorBtn_mouseClick(self, event):
        self.components.HtmlWindow.text = self.links[1]

    def on_LicenseBtn_mouseClick(self, event):
        self.components.HtmlWindow.text = self.links[2]

class prefsDialog(CustomDialog):
    """Displays a preferences dialog box"""

    def __init__(self, aBg, section='Defaults'):
        path = os.path.join(aBg.application.applicationDirectory, 'prefsDialog')
        aDialogRsrc = resource.ResourceFile(model.internationalResourceName(path)).getResource()
        CustomDialog.__init__(self, aBg, aDialogRsrc)
        self.parent = aBg
        self.section = section

        # retrieve the right section from the config file
        self.components.sessionName.text = self.section

        if self.section =='Defaults':
            self.components.portNumber.text = self.parent.cfg.get(self.section, 'port')
            self.components.userName.text = self.parent.cfg.get(self.section, 'user')
            self.components.identityFile.text = self.parent.cfg.get(self.section, 'identityfile')
            self.components.connectCmd.text = self.parent.cfg.get(self.section, 'command')
            self.components.sessionName.editable = 0
            self.components.StaticText4.enabled = 0
            self.components.hostName.enabled = 0
        else:
            if self.section != 'NewSession':
                self.components.hostName.text = self.parent.cfg.get(self.section, 'hostname')
            self.components.portNumber.text = self.parent.cfg.get(self.section, 'port')
            self.components.userName.text = self.parent.cfg.get(self.section, 'user')
            self.components.identityFile.text = self.parent.cfg.get(self.section, 'identityfile')
            self.components.connectCmd.text = self.parent.cfg.get(self.section, 'command')
        
    def on_idFileBtn_mouseClick(self, event):
        # select SSH private key file
        title = 'Select SSH private key file'
        start = os.path.join(os.path.expanduser('~'), '.ssh')
        wildcard = "All Files|*"
        result = dialog.openFileDialog(self, 'Open', start, '', wildcard)
        if result.accepted:
            self.components.identityFile.text = result.paths[0]

    def on_btnOK_mouseClick(self, event):
        if self.components.sessionName.text == 'Defaults':
            self.parent.cfg.set(self.components.sessionName.text, 'port', self.components.portNumber.text)
            self.parent.cfg.set(self.components.sessionName.text, 'user', self.components.userName.text)
            self.parent.cfg.set(self.components.sessionName.text, 'identityfile', self.components.identityFile.text)
            self.parent.cfg.set(self.components.sessionName.text, 'command', self.components.connectCmd.text)
            event.skip()
        elif self.components.sessionName.text == 'NewSession':
            bull = dialog.alertDialog(self, 'Invalid session name', 'Oops!')
        else:
            if self.components.hostName.text == '' and self.components.sessionName.text != 'Defaults':
                bull = dialog.alertDialog(self, 'You must enter a valid host name', 'Oops!')
            else:
                accept = 1
                try:
                    bull = socket.gethostbyname(self.components.hostName.text)
                except socket.gaierror:
                    msgtxt = '"%s" may not be a valid DNS hostname. ' % self.components.hostName.text
                    msgtxt += 'This may be because you do not currently have a connection to the internet, '
                    msgtxt += 'or it may be that the name you have entered really is invalid. Do you '
                    msgtxt += 'want to accept it anyway?'
                    result = dialog.messageDialog(self, wrap_string(msgtxt, 50), 'Warning:',
                        wx.ICON_EXCLAMATION | wx.YES_NO | wx.NO_DEFAULT)
                    accept = result.accepted
                if accept:
                    if not self.parent.cfg.has_section(self.components.sessionName.text):
                        self.parent.cfg.add_section(self.components.sessionName.text)
                    self.parent.cfg.set(self.components.sessionName.text, 'hostname', self.components.hostName.text)
                    self.parent.cfg.set(self.components.sessionName.text, 'port', self.components.portNumber.text)
                    self.parent.cfg.set(self.components.sessionName.text, 'user', self.components.userName.text)
                    self.parent.cfg.set(self.components.sessionName.text, 'identityfile', self.components.identityFile.text)
                    self.parent.cfg.set(self.components.sessionName.text, 'command', self.components.connectCmd.text)
                    event.skip()

    def on_btnCancel_mouseClick(self, event):
        event.skip()

def wrap_string(s, max, para = "\n\n"):
    paras = s.split(para)
    outStr = ""
    
    for paragraph in paras:
        paragraph = paragraph.replace("\n", " ")
        words = paragraph.split()
        outLine = ""
        lineCount = wordCount = 0
        
        for i in range(len(words)):
            if (len(outLine) + len(words[i])) > max:
                if lineCount:
                    outStr += "\n"
                outStr += outLine
                outLine = words[i]
                lineCount += 1
                wordCount = 1
            else:
                if wordCount:
                    outLine += " "
                outLine +=  words[i]
                wordCount += 1

        if lineCount:
            outStr += "\n"
        outStr += outLine
        outStr += para
        
    return outStr
