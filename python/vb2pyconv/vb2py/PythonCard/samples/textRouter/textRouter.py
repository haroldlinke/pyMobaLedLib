#!/usr/local/bin/python

"""
__version__ = "$Revision: 1.85 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
__author__ = "simon@kittle.co.uk"

App:  TextRouter
Desc: TextRouter is a generic weblogging and text "routing"
      application.  It's main use is for posting to Blogger and/or
      Manila maintained weblogs.  It is designed to be the sort of
      app which is kept running the whole time; the idea being that
      if you find a piece of text you'd like to send somewhere, you
      can simply copy and paste it into TextRouter and send it on
      its way.
"""

import pprint            # for config
import webbrowser
import smtplib        

# standard python + pythoncard imports

from time import sleep   # for the text auto scroller reader.

from PythonCard import dialog, model, util

import os
import sys
import re

import wx # sizer stuff

from types import *

from wordwrap import wrap_string

# my own imports

from customDialogs import *
from bloggeraccount import *
from manilaaccount import *
from shortcutsSet import *
from trDragDrop import *

    
## ===================== ##
## Main TextRouter Class ##
## ===================== ##

class TextRouter(model.Background):

    #def __init__(self, aParent, aId, aStackRsrc, aBgRsrc):
    #    PythonCard.model.Background.__init__(self, aParent, aId, aStackRsrc, aBgRsrc)
    def on_initialize(self, event):
        """Startup"""
        
        ## -- window configuration follows

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        controlsSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        comp = self.components

        ## -- handle the drop + drop of text
        # - myTextDropTarget = trTextDropTarget(self)
        # - comp.area1._delegate.SetDropTarget(myTextDropTarget)


        if wx.__version__ == "2.3.2b7" or wx.__version__ == "2.3.2":
            myURLDropTarget = trURLDropTarget(self)
            comp.area1.SetDropTarget(myURLDropTarget)
        
        # buttons, no vert. resize, border of 2 pixels round all edges
        buttonSizer.Add(comp.buttonClearIt, 0, wx.ALL, 2)
        buttonSizer.Add(comp.buttonClipIt, 0,  wx.ALL, 2)
        
        # top sizer.  this does the subject/title: label + text box.
        topSizer.Add(comp.lblSubject, 0, wx.ALL | wx.ALIGN_LEFT, 3)
        topSizer.Add(comp.area2, 1, wx.ALL | wx.ALIGN_LEFT, 0)


        # bottom controls panel, no horiz. resizing, borders round all edges of width 0 for buttons (they've
        # already got border) and 4 for the two radio choices.
        controlsSizer.Add(buttonSizer, 0, wx.ALL | wx.ALIGN_LEFT, 0)
        controlsSizer.Add(comp.nextInputActionMode, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        controlsSizer.Add(comp.nextOutputActionMode, 0, wx.ALL | wx.ALIGN_RIGHT, 4)
        
        # main sizer, the big text area can be resized vertically, others can't.  they can all be sized
        # horizontally (wx.EXPAND), plus statusLine StaticText control has a bit of padding round all edges
        mainSizer.Add(topSizer, 0, wx.EXPAND)
        mainSizer.Add(comp.area1, 1, wx.EXPAND)
        mainSizer.Add(controlsSizer, 0, wx.EXPAND)
        #mainSizer.Add(comp.statusLine._delegate, 0, wx.EXPAND | wx.ALL, 2)

        # we don't want this because it always resizes window to "shrink-wrap" the controls on startup,
        # which means you can't use GNOME or presumably some Windows toys to remember the size + position
        # - mainSizer.Fit(self)

        # put it in to action.
        self.panel.SetSizer(mainSizer)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()
        self.panel.Refresh()
        wx.Yield()

        self.status("Loading...")
        
        ## -- data configuration follows

        # keep track of find parameters
        self.lastFind = {'searchText':'', 'wholeWordsOnly':0, 'caseSensitive':0}

        # the two main accounts
        self.theManilaAccounts = []
        self.theCurrentManilaAccount = -1
        
        self.theBloggerAccounts = []
        self.theCurrentBloggerAccount = -1
        
        # misc setup + settings
        self.configFile   = "textRouter.conf"

        self.undoStack = []
        self.undoStackPos = 0

        self.shortcuts = ShortcutsSet()

        # default preferences lists
        self.generalPrefs = {"defaultDirectory" : '.', "tmpFile" : "temp.txt", "externalEditor" : "notepad",\
                             "alwaysClear" : 'Yes', "autoSaveConfig" : 'Yes', \
                             "undoHistorySize" : 10, "autoLoadTextFile":'No', 'autoSaveTextFile':'No',
                             "mainFont" : "", "paragraphWidth" : 74,
                             "useProxy" : "No", "proxyServer" : "", "proxyPort" : 0}
        
        self.htmlPrefs = { "boldTag" : 'b', "italicTag" : 'i', 'centerTag' : 'div' }
        
        self.manilaPrefs = { "manilaAutoLogin" : 'No', 'manilaAutoGetHomepage' : 'No', \
                             'routeToManilaAction' : 'adds', 'autoRender' : 'Yes' }
        
        self.bloggerPrefs = { "bloggerAutoLogin" : 'No' } 

        self.utilitiesPrefs = { "externalEditor" : "notepad", "textScrollerDelay" : 0.2, \
                                "textScrollerWords" : 4, \
                                "textScrollerFont" : \
                                "{'style':'bold','faceName':'helvetica','family':'sansSerif','size': 24}",
                                "shortcutsFile" : "shortcuts.txt",
                                "autoSaveShortcuts" : "Yes",
                                "expandShortcuts" : "blogger" }

        self.emailPrefs   = {"serverName" : "", "serverPort" : 25, "name" : "", "email" : ""}
        self.emailRcpts   = []

        self.filters   = []
        
        self.stateSettings = {}

        self.loadInStrings()
        self.loadInConfig()
        self.loadInShortcuts()

        # load up the text file if the users pref says so, and if we have a last-load file to load
        if self.generalPrefs["autoLoadTextFile"] == "Yes" and \
               ("defaultFileLoad" in self.stateSettings):
            self.insertFile(self.stateSettings["defaultFileLoad"])

        self.saveState()
        self.components.area1.setFocus()

    def saveState(self):
        """Saves the current text and selection state to the undo history stack."""
        wx.Yield()
        currentText = self.components.area1.text
        currentSel  = self.components.area1.getSelection()
        
        self.undoStack.insert(self.undoStackPos, [ currentText, currentSel ] )

        if self.undoStackPos != 0:
            self.undoStack[0:self.undoStackPos] = []
            self.undoStackPos = 0

        if len(self.undoStack) > (self.generalPrefs["undoHistorySize"]+1):
            self.undoStack[(self.generalPrefs["undoHistorySize"]+1):] = []

        #print "===== SAVE"
        #print "    undoStackPosition %d" % self.undoStackPos
        #print "    stack size %d" % len(self.undoStack)
       
        #print "----- stack:"
        #for state in self.undoStack:
            #print "    Text:" + state[0][0:40]
            #print "    (%d, %d)" % (state[1][0], state[1][1])
            #print ""
            

    def restoreState(self):
        """Restores the last text and selection state from the undo history stack."""
        if self.undoStackPos+1 == len(self.undoStack) or self.undoStackPos == \
               (self.generalPrefs["undoHistorySize"]+1):
            # no more undo info
            val = []
        else:
            self.undoStackPos = self.undoStackPos + 1
            val = self.undoStack[self.undoStackPos]

        #print "===== UNDO"
        #print "    undoStackPosition %d" % self.undoStackPos
        #print "    stack size %d" % len(self.undoStack)
        #print "----- stack:"
        #for state in self.undoStack:
            #print "    Text:" + state[0][0:40]
            #print "    (%d, %d)" % (state[1][0], state[1][1])
            #print "VAL:"
            #print val
            #print ""

        return val
    

    def doRedo(self):
        if self.undoStackPos == 0:
            return []
        else:
            self.undoStackPos = self.undoStackPos - 1
            val = self.undoStack[self.undoStackPos]
            return val


    # ------------------------- #
    #    File  Menu  Handlers   #
    # ------------------------- #

    def on_menuFileLoad_select(self, event):
        if ("defaultFileLoad" in self.stateSettings) and self.stateSettings["defaultFileLoad"] != "":
            self.insertFile(self.stateSettings["defaultFileLoad"])
            self.saveState()
        else:
            self.on_menuFileLoadFrom_select(event)

    def on_menuFileLoadFrom_select(self, event):
        """Load a file from disk and insert/append/overwrite it in to the main text box."""
        #print "on_menuFileLoadFrom_select: entered"

        result = dialog.fileDialog(self, 'Open...', \
                                self.generalPrefs["defaultDirectory"], '', \
                                "*")
        if result.accepted:
            path = result.paths[0]
        else:
            self.status("File insert cancelled.")
            return 0

        self.insertFile(path)
        self.stateSettings["defaultFileLoad"] = path

        self.saveState()


    ## -- MENU: FILE: Save Text --
    def on_menuFileSave_select(self, event):
        """Saves the text to the last used file."""
        if ("defaultFileSave" in self.stateSettings) and self.stateSettings["defaultFileSave"] != "":
            self.saveText(self.stateSettings["defaultFileSave"])
        else:
            self.on_menuFileSaveAs_select(event)

    def on_menuFileSaveAs_select(self, event):
        """Saves the text to a file chosen by dialog box."""
        result = dialog.fileDialog(self, 'Save As...', self.generalPrefs["defaultDirectory"],\
                                "text.txt", "*", wx.SAVE)
        
        if result.accepted:
            path = result.paths[0]

            self.saveText(path)
            self.stateSettings["defaultFileSave"] = path
        else:
            self.status("Save cancelled.")


    ## -- MENU: FILE: Load + Save Config File --
    def on_menuFileLoadConfig_select(self, event):
        """Loads in the config file in to the default location"""

        result = dialog.fileDialog(self, 'Open', self.generalPrefs["defaultDirectory"], \
                                self.configFile, "conf")
        
        if result.accepted:
            path = result.paths[0]
            self.loadInConfig(path)

    def on_menuFileSaveConfig_select(self, event):
        """Saves the config file in to the default location"""
        self.saveConfig()

    def on_menuFileSaveConfigAs_select(self, event):
        """Saves the config file in to a specified (by dialog) file"""
        result = dialog.fileDialog(self, 'Save As...', self.generalPrefs["defaultDirectory"],\
                                self.configFile, "conf", wx.SAVE)
        if result.accepted:
            path = result.paths[0]
            self.saveConfig(path)


    ## -- MENU: FILE: Preferences --
    def on_menuFilePreferences_select(self, event):
        """Let the user specify some general preferences"""

        inputDetails = [["defaultDirectory", self.strs["genPrefs"]["defDirP"],\
                         self.strs["genPrefs"]["defDirH"],\
                         self.generalPrefs["defaultDirectory"], 1],

                        ["tmpFile", self.strs["genPrefs"]["tmpFileP"], \
                         self.strs["genPrefs"]["tmpFileH"],
                         self.generalPrefs["tmpFile"], 1],
                        
                        ["alwaysClear", self.strs["genPrefs"]["aClrP"], \
                         self.strs["genPrefs"]["aClrH"],
                         self.generalPrefs["alwaysClear"], 4],
                        
                        ["autoSaveConfig", self.strs["genPrefs"]["aSaveP"], \
                         self.strs["genPrefs"]["aSaveH"], \
                         self.generalPrefs["autoSaveConfig"], 4],
                        
                        ["autoLoadTextFile", self.strs["genPrefs"]["aLdTxtP"], \
                         self.strs["genPrefs"]["aLdTxtH"], \
                         self.generalPrefs["autoLoadTextFile"], 4 ],
                        
                        ["autoSaveTextFile", self.strs["genPrefs"]["aSvTxtP"], \
                         self.strs["genPrefs"]["aSvTxtH"], \
                         self.generalPrefs["autoSaveTextFile"], 4 ],
                        
                        ["undoHistorySize", self.strs["genPrefs"]["undoP"], \
                         self.strs["genPrefs"]["undoH"], \
                         self.generalPrefs["undoHistorySize"], 2],
                        
                        ["paragraphWidth", self.strs["genPrefs"]["pWdthP"], \
                         self.strs["genPrefs"]["pWdthH"], \
                         self.generalPrefs["paragraphWidth"], 2],
                        
                        ["useProxy", self.strs["genPrefs"]["usePxyP"], \
                         self.strs["genPrefs"]["usePxyH"], \
                         self.generalPrefs["useProxy"], 4],

                        ["proxyServer", self.strs["genPrefs"]["pxyServP"], \
                         self.strs["genPrefs"]["pxyServH"], \
                         self.generalPrefs["proxyServer"], 1],

                        ["proxyPort", self.strs["genPrefs"]["pxyPortP"], \
                         self.strs["genPrefs"]["pxyPortH"], \
                         self.generalPrefs["proxyPort"], 2],

                        ]

        c_useProxy = self.generalPrefs["useProxy"]
        c_proxyServer = self.generalPrefs["proxyServer"]
        c_proxyPort = self.generalPrefs["proxyPort"]
        
        self.showPreferencesScreen(self.generalPrefs, inputDetails, "Main Preferences", "General preferences updated.")

        # re-generate xmlrpclib server objects if any of the proxy settings has changed
        if self.generalPrefs["useProxy"] != c_useProxy or \
           self.generalPrefs["proxyServer"] != c_proxyServer or \
           self.generalPrefs["proxyPort"] != c_proxyPort:
            # here we really need to regenertate all the settings, but that ain't done yet
            print "changed in proxy settings detected, redoing HTTP req objects"
        

    
    def on_close(self, event):
        self.doExit()
        event.skip()
        

    def doExit(self):
        """Exits"""
        if self.generalPrefs["autoSaveConfig"] == 'Yes':
            self.saveConfig()

        if self.generalPrefs["autoSaveTextFile"] == 'Yes':
            if ("defaultFileSave" in self.stateSettings):
                self.saveText(self.stateSettings["defaultFileSave"])

        if self.utilitiesPrefs["autoSaveShortcuts"] == 'Yes':
            self.saveShortcuts()


    # ------------------------- #
    #    Edit  Menu  Handlers   #
    # ------------------------- #

    # following taken from the textEditor example, which in turn was taken from the searchexplorer
    # example.  Here, we always use  'self.components.area1' and don't use findFocus() because the whole
    # point of the app is to be quick, there is no other text area, and if you use findFocus() and the focus
    # isn't in the textbox (it's in the button, or radio-group, etc) then the thing won't happen.

    # UNDO + REDO don't use the builtin things either, this is because I wanted to keep a small
    # history of things.

    # the following was copied and pasted from the searchexplorer sample
    def on_menuEditUndo_select(self, event):
        """Undoes the last action."""
        newState = self.restoreState()
        if newState == []:
            self.status("No more undo information.")
        else:
            self.components.area1.text = newState[0]
            self.components.area1.setSelection(newState[1][0], newState[1][1])

    def on_menuEditRedo_select(self, event):
        """Returns to a saved state."""
        newState = self.doRedo()
        if newState == []:
            self.status("No redo information.")
        else:
            self.components.area1.text = newState[0]
            self.components.area1.setSelection(newState[1][0], newState[1][1])

    def on_menuEditCut_select(self, event):
        """Cuts the current selection."""
        widget = self.components.area1
        if hasattr(widget, 'editable') and widget.canCut():
            widget.cut()
        self.saveState()

    def on_menuEditCopy_select(self, event):
        """Copies current selection."""
        widget = self.components.area1
        if hasattr(widget, 'editable') and widget.canCopy():
            widget.copy()

    def on_menuEditPaste_select(self, event):
        """Pastes in to the textbox, obey's nextInputActionMode."""
        widget = self.components.area1
        if hasattr(widget, 'editable') and widget.canPaste():
            self.updateTextBoxFromClipboard()
        self.saveState()
        

    def findNext(self, searchText, wholeWordsOnly, caseSensitive):
        fieldText = self.components.area1.text
        if not caseSensitive:
            searchText = searchText.lower()
            fieldText = fieldText.lower()
        
        selOffset = self.components.area1.getSelection()[1]
        # need to update the algorithm so we can match whole words only
        # are there any tools built into Python to help with that?
        # do we have to use a regular expression?
        offset = fieldText[selOffset:].find(searchText)
        
        if offset != -1:
            offset += selOffset
            #offset += fieldText.count('\n', 0, offset)
            self.components.area1.setSelection(offset, offset + len(searchText))
            self.components.area1.setFocus()

    def on_doEditFind_command(self, event):
        # keep track of the last find and preload
        # the search text and radio buttons
        lastFind = self.lastFind
        
        result = dialog.findDialog(self, lastFind['searchText'],
                                lastFind['wholeWordsOnly'],
                                lastFind['caseSensitive'])
        if result.accepted:
            lastFind['searchText'] = result.searchText
            lastFind['wholeWordsOnly'] = result.wholeWordsOnly
            lastFind['caseSensitive'] = result.caseSensitive

            self.findNext(lastFind['searchText'],
                          lastFind['wholeWordsOnly'],
                          lastFind['caseSensitive'])

    def on_doEditFindNext_command(self, event):
        self.findNext(self.lastFind['searchText'],
                      self.lastFind['wholeWordsOnly'],
                      self.lastFind['caseSensitive'])


    def on_menuEditRemoveNewlines_select(self, event):
        """Removes the newlines from the selection/all."""
        txt = self.getOutputText().replace("\n", " ")
        self.updateTextBox(txt)
        self.saveState()

    def on_menuEditWrapText_select(self, event):
        """Folds selected/all text in to a paragraph of text.  Line width specified in user prefs."""
        txt = self.getOutputText()
        self.updateTextBox(wrap_string(txt, self.generalPrefs["paragraphWidth"]))
        self.saveState()

    def on_menuEditClear_select(self, event):
        """Clears selection."""
        widget = self.components.area1
        if hasattr(widget, 'editable'):
            if widget.canCut():
                # delete the current selection,
                # if we can't do a Cut we shouldn't be able to delete either
                # which is why i used the test above
                sel = widget.replaceSelection('')
            else:
                ins = widget.getInsertionPoint()
                widget.replace(ins, ins + 1, '')
        self.saveState()

    def on_menuEditSelectAll_select(self, event):
        """Selects all."""
        widget = self.components.area1
        if hasattr(widget, 'editable'):
            widget.setSelection(0, widget.getLastPosition())
        self.saveState()


    # ------------------------- #
    #   HTML   Menu   Handlers  #
    # ------------------------- #

    def tagSelection(self, tagName):
        if tagName + 'Tag' in self.htmlPrefs:
            tag = self.htmlPrefs[tagName + 'Tag']
        else:
            tag = tagName
        widget = self.components.area1
        if hasattr(widget, 'editable') and widget.canCut():
            sel = widget.getSelection()
            selectedText = widget.getStringSelection()
            widget.replaceSelection("<%s>%s</%s>" % (tag, selectedText, tag))
            widget.setSelection( sel[0], (sel[1] + 2 * len(tag) + 5) )
            self.saveState()

    def on_menuHtmlStripHTML_select(self, event):
        """Strips all the HTML tags from the selection."""
        txt = self.getOutputText()
        #print txt
        #print re.sub("<[^>]*>", "", txt)
        self.updateTextBox(re.sub("<[^>]*>", "", txt))
        self.saveState()

    def on_menuHtmlMake_command(self, event):
        # strip menuHtml from the name
        self.tagSelection(event.target.name[8:].lower())

    def on_menuHtmlAddLink_command(self, event):
        widget = self.components.area1
        if hasattr(widget, 'editable') and widget.canCut():
            result = dialog.textEntryDialog(self, 'URL:', 'Add Link', 'http://')
            if result.accepted:
                url = result.text
                sel = widget.getSelection()
                selectedText = widget.getStringSelection()
                widget.replaceSelection('<a href="%s">%s</a>' % (url, selectedText))
                hrefLen = len(url) + len('<a href=""></a>')
                widget.setSelection( sel[0], (sel[1] + hrefLen) )
                self.saveState()
            
    def on_menuHtmlCenter_select(self, event):
        """Puts the prefrence of centering tag's around selected text."""
        # we need this here because the <DIV> option isn't simply <DIV> </DIV>, we have the attribute, etc
        widget = self.components.area1
        if hasattr(widget, 'editable') and widget.canCut():
            sel = widget.getSelection()
            selectedText = widget.getStringSelection()
            if self.htmlPrefs["centerTag"] == "center":
                self.tagSelection("center")
            else:
                widget.replaceSelection('<div align="center">%s</div>' % (selectedText))
                divLen = len('<div align="center"></div>')
                widget.setSelection( sel[0], (sel[1] + divLen) )
            self.saveState()


    def on_menuHtmlPreferences_select(self, event):
        """Let the user specify some general preferences"""

        inputDetails = [
                         ["boldTag", self.strs["htmlPrefs"]["bTagP"],
                          self.strs["htmlPrefs"]["bTagH"],
                          self.htmlPrefs["boldTag"], 1],

                         ["italicTag", self.strs["htmlPrefs"]["iTagP"],
                          self.strs["htmlPrefs"]["iTagH"],
                          self.htmlPrefs["italicTag"], 1],

                         ["centerTag", self.strs["htmlPrefs"]["cTagP"],
                          self.strs["htmlPrefs"]["cTagH"],
                          self.htmlPrefs["centerTag"], 5, ['center', 'div']],
                         ]

        self.showPreferencesScreen(self.htmlPrefs,inputDetails,"HTML Preferences","HTML preferences updated.")

    # ------------------------- #
    # 'Route To' Menu Handlers  #
    # ------------------------- #

    def on_menuRouteToManila_select(self, event):
        """Routes the text to the Manila homepage."""
        if self.manilaPrefs["routeToManilaAction"] == "adds":
            self.on_menuManilaAddToHP_select(event)
        elif self.manilaPrefs["routeToManilaAction"] == "sets":
            self.on_menuManilaSetAsHP_select(event)
        elif self.manilaPrefs["routeToManilaAction"] == "opml":
            self.on_menuManilaSetHPFromOPML_select(event)

    def on_menuRouteToBlogger_select(self, event):
        """Routes the text to the active blog in the current Blogger account."""
        if not self.checkBloggerAccounts(3):
            return

        curBlogAccount = self.theBloggerAccounts[self.theCurrentBloggerAccount]

        if curBlogAccount.currentPostId != -1:
            result = dialog.messageDialog(self, \
                                       "You have previously started editing an existing post.\nDo you really want to blog current text as a new post?", \
                                       "Warning: Editing of previous post detected.",
                                       wx.ICON_EXCLAMATION | wx.YES_NO)
            if not result.accepted:
                self.status("Blogging of text cancelled.")
                return 0

        self.showWaitMsg("Blogging text...")

        outputText = self.getOutputText()
        if self.utilitiesPrefs["expandShortcuts"] == "blogger" or \
           self.utilitiesPrefs["expandShortcuts"] == "all":
            outputText = self.shortcuts.applyTo(outputText)
            
        postid = curBlogAccount.bloggerBlogText(outputText)
        if curBlogAccount.anErrorOccured():
            self.status(curBlogAccount.getErrorMessage())
        else:
            self.status("Text blogged successfully, the ID of the post is: %s" % postid)

            if self.generalPrefs["alwaysClear"] == 'Yes':
                self.components.area1.text = ""


    def on_menuRouteToEmailPredefined_select(self, event):
        if self.emailPrefs["serverName"] == "" or self.emailPrefs["name"] == "" or \
           self.emailPrefs["email"] == "":
            self.status("You must configure your email settings before you can send email.")
            return 0

        if self.getOutputText() == "":
            self.status("You must type something before you can email it.")
            return 0

        if self.emailRcpts == []:
            self.status("There are no predefined email address to route email to.")
            return 0

        options = [ "%s <%s>" % (addy[0], addy[1]) for addy in self.emailRcpts ]

        default = options[0]
        dlg = ChooserDialog(self, 'Choose Email Address', \
                            "Choose which email address to route text to...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Email cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No recipient selected.")
            else:
                self.showWaitMsg("Emailing text...")
            
                self.sendEmailTo(options[i], self.getOutputText(), self.components.area2.text)
                self.status("Email sent to '%s'" % options[i])
                
                if self.generalPrefs["alwaysClear"] == 'Yes':
                    self.components.area1.text = ""
                    
        dlg.destroy()
        

    def on_menuRouteToEmail_select(self, event):
        if self.emailPrefs["serverName"] == "" or self.emailPrefs["name"] == "" or \
           self.emailPrefs["email"] == "":
            self.status("You must configure your email settings before you can send email.")
            return 0
        
        if self.getOutputText() == "":
            self.status("You must type something before you can email it.")
            return 0

        result = dialog.textEntryDialog(self, 
                                     'Please enter the email address:', 
                                     "Please enter the email address",
                                     '')
        if not result.accepted:
            self.status("Email cancelled.")
            return
        self.showWaitMsg("Emailing text...")

        recipient = result.text
        self.sendEmailTo(recipient, self.getOutputText())
        self.status("Email sent to '%s'" % recipient)
        
        if self.generalPrefs["alwaysClear"] == 'Yes':
            self.components.area1.text = ""

    def on_menuRouteToRSS_select(self, event):
        self.status("on_menuRouteToRSS_select: Not implemented yet")
        return

    # ------------------------- #
    #   Manila  Menu Handlers   #
    # ------------------------- #

    def on_menuManilaLogin_select(self, event):
        """Calls method to login to the Manila server.  Shows result in status bar."""
        if not self.checkManilaAccounts(3):
            return

        self.showWaitMsg("Logging in...")
        self.theManilaAccounts[self.theCurrentManilaAccount].manilaLogin()
        if self.theManilaAccounts[self.theCurrentManilaAccount].anErrorOccured():
            self.status(self.theManilaAccounts[self.theCurrentManilaAccount].getErrorMessage())
        else:
            self.status("Logged in to '%s' successfully." %
                        self.theManilaAccounts[self.theCurrentManilaAccount].prefs["siteurl"])


    def on_menuManilaFlipHomepage_select(self, event):
        """Confirms user request to flip homepage, and then attempts to flip it."""
        if not self.checkManilaAccounts(3):
            return

        result = dialog.messageDialog(self, \
                                          "Really flip homepage?", \
                                          "Flip Homepage Confirm")
        if result.accepted:
            self.showWaitMsg("Flipping homepage...")
            self.theManilaAccounts[self.theCurrentManilaAccount].manilaFlipHomepage()
            if self.theManilaAccounts[self.theCurrentManilaAccount].anErrorOccured():
                self.status(self.theManilaAccounts[self.theCurrentManilaAccount].getErrorMessage())
            else:
                self.status("Homepage flipped successfully.")
        else:
            self.status("Homepage not flipped.")

        # now make it so we have to reget the message number before we can set it again. (Flip homepage,
        # changes the message number)
        self.currentHPMsgNum = -1

        
    def on_menuManilaAddToHP_select(self, event):
        """Adds the text to the Manila homepage."""
        if not self.checkManilaAccounts(3):
            return

        self.showWaitMsg("Adding text to homepage...")

        self.theManilaAccounts[self.theCurrentManilaAccount].manilaAddTextToHP(self.getOutputText())
        if self.theManilaAccounts[self.theCurrentManilaAccount].anErrorOccured():
            self.status(self.theManilaAccounts[self.theCurrentManilaAccount].getErrorMessage())
        else:
            self.status("Text added to homepage successfully.")

            if self.generalPrefs["alwaysClear"] == 'Yes':
                self.components.area1.text = ""


    def on_menuManilaGetHP_select(self, event):
        """Get's the current homepage content, and places it in the text box."""
        if not self.checkManilaAccounts(3):
            return

        curManilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]

        self.showWaitMsg("Fetching homepage...")

        curManilaAccount.manilaGetHP()
        if curManilaAccount.anErrorOccured():
            self.status(curManilaAccount.getErrorMessage())
        else:
            self.updateTextBox(curManilaAccount.currentHPContent["body"].replace("\r", "\n"))
            self.status("Homepage content successfully downloaded.")
            self.saveState() # undo stack history.


    def on_menuManilaSetAsHP_select(self, event):
        """Set's the current homepage content, and places it in the text box."""
        if not self.checkManilaAccounts(3):
            return

        self.showWaitMsg("Updating homepage...")

        #print self.manilaPrefs["autoRender"]
        self.theManilaAccounts[self.theCurrentManilaAccount].manilaSetHP(self.getOutputText(), \
                                                                         self.manilaPrefs["autoRender"])
        if self.theManilaAccounts[self.theCurrentManilaAccount].anErrorOccured():
            self.status(self.theManilaAccounts[self.theCurrentManilaAccount].getErrorMessage())
        else:
            self.status("Manila homepage '%s' successfully updated." % \
                        self.theManilaAccounts[self.theCurrentManilaAccount].prefs["siteurl"])


    def on_menuManilaSetHPFromOPML_select(self, event):
        """Set's the current homepage content direct from an OPML file."""
        if not self.checkManilaAccounts(3):
            return

        curManilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]

        if curManilaAccount.prefs["weblogOPML"] == "":
            self.status("You haven't defined an OPML file for this Manila account yet.")
            return

        self.showWaitMsg("Uploading OPML file to homepage...")


        #print self.manilaPrefs["autoRender"]
        curManilaAccount.manilaSetHPFromOutline(curManilaAccount.prefs["weblogOPML"])

        if curManilaAccount.anErrorOccured():
            self.status(curManilaAccount.getErrorMessage())
        else:
            self.status("Manila homepage '%s' successfully updated." % \
                        curManilaAccount.prefs["siteurl"])


    def on_menuManilaGetStoryList_select(self, event):
        """Update the story list."""
        if not self.checkManilaAccounts(3):
            return

        self.showWaitMsg("Getting story list...")

        self.theManilaAccounts[self.theCurrentManilaAccount].manilaGetStoryList()
        if self.theManilaAccounts[self.theCurrentManilaAccount].anErrorOccured():
            self.status(self.theManilaAccounts[self.theCurrentManilaAccount].getErrorMessage())
        else:
            self.status("Story list for '%s' downloaded." %
                        self.theManilaAccounts[self.theCurrentManilaAccount].prefs["siteurl"])


    def on_menuManilaDownloadStory_select(self, event):
        """Download's a story.  Cool."""
        if not self.checkManilaAccounts(3):
            return

        curManilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]

        if not curManilaAccount.checkSetupOK():
            self.status(curManilaAccount.getErrorMessage())
            return

        listX = [ "%s" % curManilaAccount.storiesList[key][0] for key in curManilaAccount.storiesList.keys() ]
        dlg = ChooserDialog(self, "Story Download", \
                            "Choose a story to download...", \
                            listX, listX[0])

        result = dlg.showModal()

        if result.accepted:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No story selected for downloading.")
            else:
                msgNum = int(curManilaAccount.storiesList.keys()[i])
                self.showWaitMsg("Downloading story '%s' (msg num: %d)..." % \
                                 (listX[i],msgNum))
                story = curManilaAccount.manilaDownloadStory(msgNum)
                if curManilaAccount.anErrorOccured():
                    self.status("Story download failed: %s" % curManilaAccount.getErrorMessage())
                else:
                    self.updateTextBox(story["body"].replace("\r", "\n"))
                    self.updateSubject(story["subject"])
                    curManilaAccount.currentStory = i
                    if "opml" in story:
                        result = dialog.messageDialog(self, \
                                                    "Warning: The story you downloaded also contained an OPML version,\nif you save this text version of the story it may overwrite the OPML version.",
                                                    "Warning..", wx.ICON_EXCLAMATION | wx.OK)
                    self.status("Downloaded story '%s' (msg num: %d) successfully." % \
                                (listX[i],msgNum))
        else:
            self.status("Story download cancelled.")

        dlg.destroy()



    def on_menuManilaUploadStory_select(self, event):
        """Upload's a story."""
        if not self.checkManilaAccounts(3):
            return

        curManilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]

        if not curManilaAccount.checkSetupOK():
            self.status(curManilaAccount.getErrorMessage())
            return

        listX = [ "%s" % curManilaAccount.storiesList[key][0] for key in curManilaAccount.storiesList.keys() ]

        defIndex = ((curManilaAccount.currentStory != -1) and [curManilaAccount.currentStory] or [0])[0]

        dlg = ChooserDialog(self, "Story Upload", \
                            "Choose a story to upload the text to...", \
                            listX, listX[defIndex])
        dlg.showModal()

        if dlg.accepted():
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No story selected for uploading text to.")
            else:
                msgNum = int(curManilaAccount.storiesList.keys()[i])
                self.showWaitMsg("Uploading to story '%s' (msg num: %d)..." % \
                                 (listX[i],msgNum))
                curManilaAccount.manilaUploadStory(msgNum, self.getSubjectText(),\
                                                   self.getOutputText(), "text/x-outline-tabbed")
                if curManilaAccount.anErrorOccured():
                    self.status("Story upload failed: %s" % curManilaAccount.getErrorMessage())
                else:
                    self.status("Uploaded to story '%s' (msg num: %d) successfully." % \
                                (listX[i],msgNum))
        else:
            self.status("Story upload cancelled.")

        dlg.destroy()



    def on_menuManilaUploadPicture_select(self, event):
        """Upload's an image to the Manila server."""
        if not self.checkManilaAccounts(3):
            return

        curManilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]

        if not curManilaAccount.checkSetupOK():
            self.status(curManilaAccount.getErrorMessage())
            return

        wildcard = "JPG files (*.jpg;*.jpeg)|*.jpg;*.jpeg|GIF files (*.gif)|*.gif|All Files (*.*)|*.*"

        result = dialog.fileDialog(self, 'Open...', \
                                self.generalPrefs["defaultDirectory"], '', \
                                wildcard)
        if result.accepted:
            path = result.paths[0]
            
            if path.endswith("gif"):
                mimeType = "image/gif"
            elif path.endswith("jpeg") or path.endswith("jpg"):
                mimeType = "image/jpeg"
            else:
                imgTypes = ["image/jpeg", "image/gif"]
                dlgC = ChooserDialog(self, 'Choose Image Type', \
                                     "Choose the type of your image (Manila only supprts GIF + JPEG)...", \
                                     imgTypes, imgTypes[0])
                result = dlgC.showModal()
                if not result.accepted:
                    self.status("Image uploading cancelled.")
                    dlgC.destroy()
                    return
                i = dlgC.components.options.findString(dlgC.components.options.stringSelection)
                if i == -1:
                    self.status("Image uploading cancelled (no mime type selected for image).")
                    dlgC.destroy()
                    return
                dlgC.destroy()
                mimeType = imgTypes[i]

            result = dialog.textEntryDialog(self, 'Picture Name:', 'Picture Name', '')
            if result.accepted:
                imageTitle = result.text

                self.showWaitMsg("Uploadng image...")
                msg = curManilaAccount.manilaCreateMsg(imageTitle,\
                                                       "...", "text/x-outline-tabbed")
                if curManilaAccount.anErrorOccured():
                    self.status("Error uploading image: %s" % curManilaAccount.getErrorMessage())
                else:
                    curManilaAccount.manilaAttachPicture(msg["msgnum"], path, mimeType)
                    if curManilaAccount.anErrorOccured():
                        self.status("Error uploading image: %s" % curManilaAccount.getErrorMessage())
                    else:
                        self.status("Image uploaded successfully.")
            else:
                self.status("Image upload cancelled.")
        else:
            self.status("Image upload cancelled.")


    def on_menuManilaPostNewStory_select(self, event):
        """Posts text as a new story."""
        if not self.checkManilaAccounts(3):
            return

        self.showWaitMsg("Posting text as story...")
        
        curManilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]

        if not curManilaAccount.checkSetupOK():
            self.status(curManilaAccount.getErrorMessage())
            return

        msg = curManilaAccount.manilaCreateMsg(self.getSubjectText(),\
                                               self.getOutputText(), "text/x-outline-tabbed")
        if curManilaAccount.anErrorOccured():
            self.status("Error posting new story: %s" % curManilaAccount.getErrorMessage())
        else:
            #print "message:"
            #print msg
            curManilaAccount.manilaAddToStoriesList(msg)
            if curManilaAccount.anErrorOccured():
                self.status("Error posting new story: %s" % curManilaAccount.getErrorMessage())
            else:
                self.status("New story '%s' posted successfully. (msg num: %d)" % \
                            (self.getSubjectText(), int(msg["msgnum"])))
            

    def on_menuManilaSetStoryAsHP_select(self, event):
        """Set's a chosen story to be the current homepage."""
        if not self.checkManilaAccounts(3):
            return

        curManilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]

        if not curManilaAccount.checkSetupOK():
            self.status(curManilaAccount.getErrorMessage())
            return

        listX = [ "%s" % curManilaAccount.storiesList[key][0] for key in curManilaAccount.storiesList.keys() ]

        defIndex = ((curManilaAccount.currentStory != -1) and [curManilaAccount.currentStory] or [0])[0]

        dlg = ChooserDialog(self, "Set Homepage", \
                            "Choose a story to set the homepage as...", \
                            listX, listX[defIndex])
        dlg.showModal()

        if dlg.accepted():
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No story selected for making the homepage.")
            else:
                msgNum = int(curManilaAccount.storiesList.keys()[i])
                self.showWaitMsg("Setting homepage from story '%s' (msg num: %d)..." % \
                                 (listX[i],msgNum))
                curManilaAccount.manilaSetHomepageFromMSG(msgNum)
                if curManilaAccount.anErrorOccured():
                    self.status("Error setting homepage from story: %s" % curManilaAccount.getErrorMessage())
                else:
                    self.status("Set homepage from story '%s' (num: %d) successfully." % \
                                (listX[i],msgNum))
        else:
            self.status("Story upload cancelled.")

        dlg.destroy()


    def on_menuManilaNewAccount_select(self, event):
        """Defines a new Manila account settings."""

        inputDetails = [ ["siteurl", self.strs["newMnlPrefs"]["siteUrlP"], \
                          self.strs["newMnlPrefs"]["siteUrlH"], \
                          "", 1],

                         ["rpcserver", self.strs["newMnlPrefs"]["rpcP"], \
                          self.strs["newMnlPrefs"]["rpcH"], \
                          "", 1],

                         ["username", self.strs["newMnlPrefs"]["userP"], \
                          self.strs["newMnlPrefs"]["userH"], \
                          "", 1],

                         ["password", self.strs["newMnlPrefs"]["passP"], \
                          self.strs["newMnlPrefs"]["passH"], \
                          "", 3],

                         ["weblogOPML", self.strs["newMnlPrefs"]["opmlP"], \
                          self.strs["newMnlPrefs"]["opmlH"], \
                          "", 1],

                         ["usePostedLine", self.strs["newMnlPrefs"]["usePosP"], \
                          self.strs["newMnlPrefs"]["usePosH"], \
                          "No", 4],

                         ["postedLine", self.strs["newMnlPrefs"]["postedP"], \
                          self.strs["newMnlPrefs"]["postedH"], \
                          "posted at %I:%M %p", 1],

                         ]

        dlg = PreferencesDialog(self, "Manila Account Settings", inputDetails)

        dlg.showModal()
        if dlg.accepted():
            if self.generalPrefs["useProxy"] == "Yes":
                proxy = self.generalPrefs["proxyServer"] + ":" + str(self.generalPrefs["proxyPort"])
            else:
                proxy = ""

            self.theManilaAccounts.append(ManilaAccount(proxy))
            
            self.theManilaAccounts[-1].setPrefs(dlg.components.siteurl.text, \
                                                dlg.components.rpcserver.text, \
                                                dlg.components.username.text, \
                                                dlg.components.password.text,
                                                dlg.components.weblogOPML.text, \
                                                dlg.components.usePostedLine.stringSelection, \
                                                dlg.components.postedLine.text, \
                                                )

            if len(self.theManilaAccounts) == 1:
                self.theCurrentManilaAccount = 0
            self.status("New manila account defined.")
        else:
            self.status("Cancelled.")

#        for site in self.theManilaAccounts:
#            dumpDataStruct(site.prefs)

        dlg.destroy()

    
    def on_menuManilaEditAccount_select(self, event):
        """Edits an existing Manila account settings."""
        if not self.checkManilaAccounts(3):
            return

        curManilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]

        weblogDef = ("weblogOPML" in curManilaAccount.prefs and \
                     [ curManilaAccount.prefs["weblogOPML"] ] or \
                     [ "" ])[0]
        usePostedL = ("usePostedLine" in curManilaAccount.prefs and \
                     [ curManilaAccount.prefs["usePostedLine"] ] or \
                     [ "No" ])[0]
        postedLine = ("postedLine" in curManilaAccount.prefs and \
                     [ curManilaAccount.prefs["postedLine"] ] or \
                     [ "posted at %I:%M %p" ])[0]
            
        inputDetails = [ ["siteurl", self.strs["newMnlPrefs"]["siteUrlP"], \
                          self.strs["newMnlPrefs"]["siteUrlH"], \
                          curManilaAccount.prefs["siteurl"], 1],

                         ["rpcserver", self.strs["newMnlPrefs"]["rpcP"], \
                          self.strs["newMnlPrefs"]["rpcH"], \
                          curManilaAccount.prefs["rpcserver"], 1],

                         ["username", self.strs["newMnlPrefs"]["userP"], \
                          self.strs["newMnlPrefs"]["userH"], \
                          curManilaAccount.prefs["username"], 1],

                         ["password", self.strs["newMnlPrefs"]["passP"], \
                          self.strs["newMnlPrefs"]["passH"], \
                          curManilaAccount.prefs["password"], 3],

                         ["weblogOPML", self.strs["newMnlPrefs"]["opmlP"], \
                          self.strs["newMnlPrefs"]["opmlH"], \
                          weblogDef, 1],

                         ["usePostedLine", self.strs["newMnlPrefs"]["usePosP"], \
                          self.strs["newMnlPrefs"]["usePosH"], \
                          usePostedL, 4],

                         ["postedLine", self.strs["newMnlPrefs"]["postedP"], \
                          self.strs["newMnlPrefs"]["postedH"], \
                          postedLine, 1],
                         ]

        dlg = PreferencesDialog(self, "Manila Account Settings", inputDetails)

        dlg.showModal()
        if dlg.accepted():
            curManilaAccount.setPrefs(dlg.components.siteurl.text, \
                                      dlg.components.rpcserver.text, \
                                      dlg.components.username.text, \
                                      dlg.components.password.text,\
                                      dlg.components.weblogOPML.text, \
                                      dlg.components.usePostedLine.stringSelection, \
                                      dlg.components.postedLine.text, \
                                      )

            self.status("Settings for Manila account '%s' updated." %
                        curManilaAccount.prefs["siteurl"])
        else:
            self.status("Cancelled.")

        dlg.destroy()


    def on_menuManilaChooseActiveAccount_select(self, event):
        """Gives the user a list of defined manila accounts so they can select the active one."""
        if not self.checkManilaAccounts(1):
            return

        options = []
        for manilaSite in self.theManilaAccounts:
            options.append(manilaSite.prefs["siteurl"])

        defIndex = self.theCurrentManilaAccount
        if defIndex == -1:
            defIndex = 0
        default = options[ defIndex ]
        dlg = ChooserDialog(self, 'Choose Active Manila Account', \
                            "Choose which Manila account to set as active...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Manila account selection cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No account selected for activation.")
            else:
                self.theCurrentManilaAccount = i
                self.status("Manila site number %d (%s) set as active." % (i + 1, options[i]))

        dlg.destroy()

    def on_menuManilaRemoveAccount_select(self, event):
        """Gives the user a list of defined manila accounts so they can select on to be removed."""
        if not self.checkManilaAccounts(1):
            return

        options = []
        for manilaSite in self.theManilaAccounts:
            options.append(manilaSite.prefs["siteurl"])

        default = options[0]
        dlg = ChooserDialog(self, 'Remove Manila Account', \
                            "Choose which Manila account to remove...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Removing of manila account cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No account selected for deletion.")
            else:
                self.theManilaAccounts[i:i+1] = []
                if len(self.theManilaAccounts) == 0:
                    self.theCurrentManilaAccount = -1
                else:
                    if self.theCurrentManilaAccount == i:
                        self.theCurrentManilaAccount = 0
                self.status("Manila site number %d (%s) has been removed." % (i + 1, options[i]))

        dlg.destroy()

    def on_menuManilaJumpTo_select(self, event):
        """Displays a quick 'Jump To' choice box."""
        if not self.checkManilaAccounts(1):
            return

        prettyLocations = []
        urls = []
        manilaAccount = self.theManilaAccounts[self.theCurrentManilaAccount]
        if manilaAccount.prefs["siteurl"][-1] == "/":
            url = manilaAccount.prefs["siteurl"][0:-1]
        else:
            url = manilaAccount.prefs["siteurl"]

        prettyLocations.append("Main Page")
        prettyLocations.append("Discussion Chronological View")
        prettyLocations.append("Discussion Topics View")
        prettyLocations.append("Most-Read Messages")
        prettyLocations.append("Hourly Hits")
        prettyLocations.append("Referers")
        prettyLocations.append("Preferences")
        prettyLocations.append("Shortcuts")
        urls.append(url)
        urls.append(url + "/discuss")
        urls.append(url + "/discuss/?mode=topic")
        urls.append(url + "/stats/mostReadMessages")
        urls.append(url + "/stats/hourlyHits")
        urls.append(url + "/stats/referers")
        urls.append(url + "/admin/sitePrefs/default$welcome")
        urls.append(url + "/admin/viewShortcuts")

        storyURL = url + "/stories/storyReader$"
        for key in manilaAccount.storiesList.keys():
            prettyLocations.append(manilaAccount.storiesList[key][0])
            urls.append(storyURL + str(int(key)))

        prompt = "Please choose the URL to jump to on %s" % url
        dlg = ChooserDialog(self, "Choose URL", prompt, \
                                        prettyLocations, prettyLocations[0])
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Jump-To-URL cancelled.")
            dlg.destroy()
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No webpage selected for loading.")
            else:
                dlg.destroy()
                webbrowser.open(urls[i], 1, 1)

    def on_menuManilaPreferences_select(self, event):
        """Let the user specify some Manila specific preferences"""
        inputDetails = [
                         ["manilaAutoLogin", self.strs["mnlPrefs"]["aLogP"],
                          self.strs["mnlPrefs"]["aLogH"],
                          self.manilaPrefs["manilaAutoLogin"], 4],

                         ["manilaAutoGetHomepage", self.strs["mnlPrefs"]["aGetP"],
                          self.strs["mnlPrefs"]["aGetH"],
                          self.manilaPrefs["manilaAutoGetHomepage"], 4],

                         ["routeToManilaAction", self.strs["mnlPrefs"]["rToMP"],
                          self.strs["mnlPrefs"]["rToMH"],
                          self.manilaPrefs["routeToManilaAction"], 5, ['adds', 'sets', 'opml']],

#                         ["autoRender", self.strs["mnlPrefs"]["aRndrP"],
#                          self.strs["mnlPrefs"]["aRndrH"],
#                          self.manilaPrefs["autoRender"], 4 ], 

                         ]

        self.showPreferencesScreen(self.manilaPrefs,inputDetails,"Manila Preferences","Manila preferences updated.")


    # ------------------------- #
    #   Blogger Menu Handlers   #
    # ------------------------- #
        
    def on_menuBloggerLogin_select(self, event):
        """Calls method to login to the Manila server.  Shows result in status bar."""
        if not self.checkBloggerAccounts(3):
            return

        self.showWaitMsg("Logging in...")

        self.theBloggerAccounts[self.theCurrentBloggerAccount].bloggerLogin()
        if self.theBloggerAccounts[self.theCurrentBloggerAccount].anErrorOccured():
            self.status(self.theBloggerAccounts[self.theCurrentBloggerAccount].getErrorMessage())
        else:
            
            self.status("Logged in to Blogger account '%s' successfully." % \
                        self.theBloggerAccounts[self.theCurrentBloggerAccount].prefs["username"] )

    def on_menuBloggerChooseBlog_select(self, event):
        """Chooses a blog from the users' list of weblogs"""
        if not self.checkBloggerAccounts(3):
            return

        if (not self.theBloggerAccounts[self.theCurrentBloggerAccount].checkSetupOK(3)):
            self.status(self.theBloggerAccounts[self.theCurrentBloggerAccount].getErrorMessage())
            return

        options = [ weblog["blogName"] for weblog in self.theBloggerAccounts[self.theCurrentBloggerAccount].blogs ]

        defIndex = self.theBloggerAccounts[self.theCurrentBloggerAccount].prefs["activeBlog"] - 1
        if defIndex == -2:
            defIndex = 0

        default = options[ defIndex ]
        dlg = ChooserDialog(self, 'Choose Active Blog', \
                            "Choose the blog number to make active...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Active blog selection cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No blog selected for activation.")
            else:
                self.status("Blog '%s' set as active." % (self.theBloggerAccounts[self.theCurrentBloggerAccount].blogs[i]["blogName"]))
                self.theBloggerAccounts[self.theCurrentBloggerAccount].setActiveBlog(i+1)
        dlg.destroy()


    def on_menuBloggerFetchPosts_select(self, event):
        """Fetches the previous 10 posts from the Blogger server."""
        if not self.checkBloggerAccounts(3):
            return

        self.showWaitMsg("Fetching posts...")

        postid = self.theBloggerAccounts[self.theCurrentBloggerAccount].bloggerFetchPreviousPosts()
        if self.theBloggerAccounts[self.theCurrentBloggerAccount].anErrorOccured():
            self.status(self.theBloggerAccounts[self.theCurrentBloggerAccount].getErrorMessage())
            #print self.theBloggerAccount.getErrorMessage()
        else:
            self.status("Posts downloaded successfully, now use 'Blogger->Insert Previous Post' to start editing old posts.")


    def on_menuBloggerInsertPrevPost_select(self, event):
        """Gets an existing post for editting."""
        if not self.checkBloggerAccounts(3):
            return

        curBlogAccount = self.theBloggerAccounts[self.theCurrentBloggerAccount]
        
        # check logged in
        if (not curBlogAccount.checkSetupOK(0)):
            self.status(curBlogAccount.getErrorMessage())
            return 0
        
        if ("previousPosts" not in curBlogAccount.blogs[curBlogAccount.prefs["activeBlog"]-1]) or \
               curBlogAccount.blogs[curBlogAccount.prefs["activeBlog"]-1]["previousPosts"] == []:
            self.showWaitMsg("Fetching previous posts...")

            postid = curBlogAccount.bloggerFetchPreviousPosts()
            if curBlogAccount.anErrorOccured():
                self.status(curBlogAccount.getErrorMessage())
                return
            else:
                self.status("Previous posts fetched, now choose one to edit...")

        #if (not curBlogAccount.checkSetupOK(8)):
            #self.status(curBlogAccount.getErrorMessage())
            #return
        
        activeBlogIndex = curBlogAccount.prefs["activeBlog"]-1
        prevPosts = curBlogAccount.blogs[activeBlogIndex]["previousPosts"]


        options = []
        for index in range(len(curBlogAccount.blogs[activeBlogIndex]["previousPosts"])):
            text = prevPosts[index]["content"].replace("\n"," ")
            options.append( "%d: %s%s" % (index+1, text[0:50], (len(text) > 50) and "..." or "") )

        default = options[0]
        dlg = ChooserDialog(self, 'Choose Post To Edit', \
                            "Choose the post to edit...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Post editing cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No previous post selected.")
            else:
                curBlogAccount.currentPostId = prevPosts[i]["postid"]
                self.updateTextBox(prevPosts[i]["content"])

            self.status("Editing previous post, use 'Blogger->Update Post' to save you edits when done.")

            self.saveState()

        dlg.destroy()


    def on_menuBloggerGetPost_select(self, event):
        """Gets an existing post for editting."""
        if not self.checkBloggerAccounts(3):
            return

        curBlogAccount = self.theBloggerAccounts[self.theCurrentBloggerAccount]
        
        # check logged in
        if (not curBlogAccount.checkSetupOK(0)):
            self.status(curBlogAccount.getErrorMessage())
            return 0
        
        result = dialog.textEntryDialog(self, 'Fetch Post:', 'Post ID', '')
        
        if not result.accepted:
            self.status("Post editing cancelled.")
        else:
            try:
                num = result.text
                self.showWaitMsg("Fetching post number '%s'..." % num)
                post = curBlogAccount.bloggerGetPost(num)
                if curBlogAccount.anErrorOccured():
                    self.status(curBlogAccount.getErrorMessage())
                    return
                curBlogAccount.currentPostId = post["postid"]
                self.updateTextBox(post["content"])
                self.status("Editing previous post, use 'Blogger->Update Post' to save you edits when done.")
                self.saveState()
            except ValueError, e:
                self.status("Error: Post ID must be a number.")


    def on_menuBloggerDeletePost_select(self, event):
        """Deletes a post."""
        if not self.checkBloggerAccounts(3):
            return

        curBlogAccount = self.theBloggerAccounts[self.theCurrentBloggerAccount]

        # check logged in
        if (not curBlogAccount.checkSetupOK(15)):
            self.status(curBlogAccount.getErrorMessage())
            return 0


        if "previousPosts" not in curBlogAccount.blogs[curBlogAccount.prefs["activeBlog"]-1] or \
               curBlogAccount.blogs[curBlogAccount.prefs["activeBlog"]-1]["previousPosts"] == []:
            self.showWaitMsg("Fetching previous posts...")

            postid = curBlogAccount.bloggerFetchPreviousPosts()
            if curBlogAccount.anErrorOccured():
                self.status(curBlogAccount.getErrorMessage())
                return
            else:
                self.status("Previous posts fetched, now choose one to delete...")

        #if (not curBlogAccount.checkSetupOK(8)):
            #self.status(curBlogAccount.getErrorMessage())
            #return
        
        
        activeBlogIndex = curBlogAccount.prefs["activeBlog"]-1
        prevPosts = curBlogAccount.blogs[activeBlogIndex]["previousPosts"]

        options = []
        for index in range(len(prevPosts)):
            text = prevPosts[index]["content"].replace("\n"," ")
            options.append( "%d: %s%s" % (index+1, text[0:50], (len(text) > 50) and "..." or "") )

        default = options[0]
        dlg = ChooserDialog(self, 'Choose Post To Delete', \
                            "Choose the post to delete...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Post deletion cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No previous post selected for deletion.")
            else:
                self.showWaitMsg("Deleting...")

                postid = prevPosts[i]["postid"]
                curBlogAccount.bloggerDeletePost(i)
                
                if curBlogAccount.anErrorOccured():
                    self.status(curBlogAccount.getErrorMessage())
                else:
                    self.status("Post deleted successfully.")
                    if curBlogAccount.currentPostId == postid:
                        curBlogAccount.currentPostId = -1
                    
        dlg.destroy()


    def on_menuBloggerUpdatePost_select(self, event):
        """Updates an existing post.  A Previous post much be fetched first."""
        if not self.checkBloggerAccounts(3):
            return

        curBlogAccount = self.theBloggerAccounts[self.theCurrentBloggerAccount]

        if (not curBlogAccount.checkSetupOK(0)):
            self.status(curBlogAccount.getErrorMessage())
            return

        if curBlogAccount.currentPostId == -1:
            self.status("You must start editing a previous post before update it.")
            return

        self.showWaitMsg("Updating...")

        outputText = self.components.area1.text
        if self.utilitiesPrefs["expandShortcuts"] == "blogger" or \
           self.utilitiesPrefs["expandShortcuts"] == "all":
            outputText = self.shortcuts.applyTo(outputText)

        curBlogAccount.bloggerUpdatePost(outputText)
        if curBlogAccount.anErrorOccured():
            self.status(curBlogAccount.getErrorMessage())
            #print self.theBloggerAccount.getErrorMessage()
        else:
            self.status("Post updated successfully.")
        
            if self.generalPrefs["alwaysClear"] == 'Yes':
                self.components.area1.text = ""

                curBlogAccount.currentPostId = -1

                curBlogAccount.blogs[curBlogAccount.prefs["activeBlog"]-1]["previousPosts"] = []

                

    def on_menuBloggerGetTemplate_select(self, event):
        """Gets the users template from Blogger."""
        if not self.checkBloggerAccounts(3):
            return

        if not self.theBloggerAccounts[self.theCurrentBloggerAccount].checkSetupOK():
            self.status(self.theBloggerAccounts[self.theCurrentBloggerAccount].getErrorMessage())
            return

        tmplNames = ["main", "archiveIndex"]
        prettyNames = [ "Main", "Archive" ]
        
        dlg = ChooserDialog(self, 'Choose Template To Get', \
                            "Choose the template to get...", \
                            prettyNames, prettyNames[0])
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Tempalte downloading cancelled.")
            dlg.destroy()
            return
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No temlpate type selected.")
                dlg.destroy()
                return

        dlg.destroy()

        self.showWaitMsg("Downloading template...")

        tmpl = self.theBloggerAccounts[self.theCurrentBloggerAccount].bloggerGetTemplate(tmplNames[i])
        if self.theBloggerAccounts[self.theCurrentBloggerAccount].anErrorOccured():
            self.status(self.theBloggerAccounts[self.theCurrentBloggerAccount].getErrorMessage())
            return
        
        self.updateTextBox(tmpl)
        self.status("%s template for blog '%s' downloaded." %
                    (prettyNames[i], self.theBloggerAccounts[self.theCurrentBloggerAccount].prefs["username"])
                    )


    def on_menuBloggerSetTemplate_select(self, event):
        """Sets the users template from Blogger."""
        if not self.checkBloggerAccounts(3):
            return

        curBlogAccount = self.theBloggerAccounts[self.theCurrentBloggerAccount]
        
        if not curBlogAccount.checkSetupOK():
            self.status(curBlogAccount.getErrorMessage())
            return

        tmplNames = ["main", "archiveIndex"]
        
        dlg = ChooserDialog(self, 'Set Template', \
                            "Choose the template to set...", \
                            ["Main", "Archive"], "Main")
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Template saving cancelled.")
            dlg.destroy()
            return
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No template type selected.")
                dlg.destroy()
                return

        dlg.destroy()

        self.showWaitMsg("Saving template...")

        tmpl = curBlogAccount.bloggerSetTemplate(tmplNames[i],
                                                 self.getOutputText())

        if curBlogAccount.anErrorOccured():
            self.status(curBlogAccount.getErrorMessage())
            return

        self.status("Template saved.")


    def on_menuBloggerJumpTo_select(self, event):
        """Displays a quick 'Jump To' choice box."""
        if not self.checkBloggerAccounts(1):
            return
        self.theBloggerAccounts[self.theCurrentBloggerAccount].checkSetupOK(3)
        if self.theBloggerAccounts[self.theCurrentBloggerAccount].anErrorOccured():
            self.status(self.theBloggerAccounts[self.theCurrentBloggerAccount].getErrorMessage())
            return
        
        prettyLocations = []
        urls = []
        
        for bloggerAccount in self.theBloggerAccounts:
            for blog in bloggerAccount.blogs:
                name = blog["blogName"]
                url = blog["url"]

                prettyLocations.append(name)
                urls.append(url)

        if len(prettyLocations) == 0:
            self.status("There are no blogs to jump to.")

        dlg = ChooserDialog(self, "Choose URL", "Please choose the URL to jump to:", \
                                        prettyLocations, prettyLocations[0])
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Jump-To-URL cancelled.")
            dlg.destroy()
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No webpage selected for loading.")
            else:
                dlg.destroy()
                webbrowser.open(urls[i], 1, 1)



    def on_menuBloggerNewAccount_select(self, event):
        """Defines a new Blogger account settings."""
        inputDetails = [
                         ["rpcserver", self.strs["newBlgPrefs"]["rpcP"], \
                          self.strs["newBlgPrefs"]["rpcH"], \
                          "http://plant.blogger.com/api/RPC2", 1],

                         ["username", self.strs["newBlgPrefs"]["userP"], \
                          self.strs["newBlgPrefs"]["userH"], \
                          "", 1],

                         ["password", self.strs["newBlgPrefs"]["passP"], \
                          self.strs["newBlgPrefs"]["passH"], 
                          "", 3],

                         ["weblogsPing", self.strs["newBlgPrefs"]["bWelogsP"],
                          self.strs["newBlgPrefs"]["bWelogsH"],
                          "Yes" , 4],

                         ]

        dlg = PreferencesDialog(self, "Blogger Account Settings", inputDetails)

        dlg.showModal()
        if dlg.accepted():
            #if self.generalPrefs["useProxy"] == 'Yes':
            #    self.theBloggerAccounts.append(BloggerAccount("yes"))
            #else:
            if self.generalPrefs["useProxy"] == "Yes":
                proxy = self.generalPrefs["proxyServer"] + ":" + str(self.generalPrefs["proxyPort"])
            else:
                proxy = ""

            self.theBloggerAccounts.append(BloggerAccount(proxy))
                
            self.theBloggerAccounts[-1].setPrefs(dlg.components.rpcserver.text, \
                                                 dlg.components.username.text, \
                                                 dlg.components.password.text, \
                                                 dlg.components.weblogsPing.stringSelection)

            if len(self.theBloggerAccounts) == 1:
                self.theCurrentBloggerAccount = 0
            self.status("New Blogger account defined.")
        else:
            self.status("Cancelled.")

        dlg.destroy()


    def on_menuBloggerEditAccount_select(self, event):
        """Edits settings for an existing Blogger account."""
        if not self.checkBloggerAccounts(3):
            return

        curBlogAccount = self.theBloggerAccounts[self.theCurrentBloggerAccount]
        
        if "weblogsPing" in curBlogAccount.prefs:
            defWeblogsPing = curBlogAccount.prefs["weblogsPing"]
        else:
            defWeblogsPing = "Yes"

        inputDetails = [
                         ["rpcserver", self.strs["newBlgPrefs"]["rpcP"], \
                          self.strs["newBlgPrefs"]["rpcH"], \
                          curBlogAccount.prefs["rpcserver"], 1],

                         ["username", self.strs["newBlgPrefs"]["userP"], \
                          self.strs["newBlgPrefs"]["userH"], \
                          curBlogAccount.prefs["username"], 1],

                         ["password", self.strs["newBlgPrefs"]["passP"], \
                          self.strs["newBlgPrefs"]["passH"], 
                          curBlogAccount.prefs["password"], 3],

                         ["weblogsPing", self.strs["newBlgPrefs"]["bWelogsP"],
                          self.strs["newBlgPrefs"]["bWelogsH"],
                          defWeblogsPing , 4],

                         ]

        dlg = PreferencesDialog(self, "Blogger Account Settings", inputDetails)

        dlg.showModal()
        if dlg.accepted():
            curBlogAccount.setPrefs(dlg.components.rpcserver.text, \
                                    dlg.components.username.text, \
                                    dlg.components.password.text, \
                                    dlg.components.weblogsPing.stringSelection)

            self.status("Settings for Blogger account '%s' updated." %
                        curBlogAccount.prefs["username"])
        else:
            self.status("Cancelled.")

        dlg.destroy()


    def on_menuBloggerChooseActiveAccount_select(self, event):
        """Gives the user a list of defined blogger accounts so they can select the active one."""
        if not self.checkBloggerAccounts(1):
            return

        options = []
        for bloggerSite in self.theBloggerAccounts:
            options.append(bloggerSite.prefs["username"])

        defIndex = self.theCurrentBloggerAccount
        if defIndex == -1:
            defIndex = 0
        default = options[ defIndex ]

        dlg = ChooserDialog(self, 'Choose Active Blogger Account', \
                            "Choose which Blogger account to set as active...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Blogger account selection cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No Blogger account selected for activation.")
            else:
                self.theCurrentBloggerAccount = i
                self.status("Blogger site number %d (%s) set as active." % (i + 1, options[i]))

        dlg.destroy()

    def on_menuBloggerRemoveAccount_select(self, event):
        """Gives the user a list of defined Blogger accounts so they can select on to be removed."""
        if not self.checkBloggerAccounts(1):
            return

        options = []
        for bloggerSite in self.theBloggerAccounts:
            options.append(bloggerSite.prefs["username"])

        default = options[0]
        dlg = ChooserDialog(self, 'Remove Blogger Account', \
                            "Choose which Blogger account to remove...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Removing of Blogger account cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            self.theBloggerAccounts[i:i+1] = []
            if len(self.theBloggerAccounts) == 0:
                self.theCurrentBloggerAccount = -1
            else:
                if self.theCurrentBloggerAccount == i:
                    self.theCurrentBloggerAccount = 0
            self.status("Blogger site number %d (%s) has been removed." % (i + 1, options[i]))
                    
        dlg.destroy()


    def on_menuBloggerPreferences_select(self, event):
        """Let the user specify some blogger specific preferences"""

        inputDetails = [
                         ["bloggerAutoLogin", self.strs["blgPrefs"]["aLogP"],
                          self.strs["blgPrefs"]["aLogH"],
                          self.bloggerPrefs["bloggerAutoLogin"], 4],

                         ]

        self.showPreferencesScreen(self.bloggerPrefs, inputDetails, "Blogger Preferences", \
                                   "Blogger preferences updated.")


    # ------------------------- #
    #   Email  Menu  Handlers   #
    # ------------------------- #
    
    def on_menuEmailNewEmailRcpt_select(self, event):
        """Allows the user to define a new email address."""

        inputDetails = [ ["name", self.strs["newEmlPrefs"]["nameP"], \
                          self.strs["newEmlPrefs"]["nameH"],
                          "", 1],
                         ["email", self.strs["newEmlPrefs"]["addrP"], \
                          self.strs["newEmlPrefs"]["addrH"], \
                          "", 1],
                         ]

        dlg = PreferencesDialog(self, "New Predefined Email Address", inputDetails)

        dlg.showModal()
        if dlg.accepted():
            self.emailRcpts.append( [ dlg.components.name.text, dlg.components.email.text ] )
            self.status("Predefined email address added: '%s <%s>'" % (self.emailRcpts[-1][0], self.emailRcpts[-1][1]))
        else:
            self.status("New email address cancelled.")
        dlg.destroy()

    def on_menuEmailRemoveEmailRcpt_select(self, event):
        """Lists the predefined email address so the user can choose one to delete."""
        if self.emailRcpts == []:
            self.status("There are no predefined email address to remove.")
            return 0

        options = [ "%s <%s>" % (addy[0], addy[1]) for addy in self.emailRcpts ]

        default = options[0]
        dlg = ChooserDialog(self, 'Choose Email Address', \
                            "Choose which email address to remove...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Address deletion cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No address selected for deleting.")
            else:
                self.status("Removed predefined address: '%s'." % options[i])
                self.emailRcpts[i:i+1] = []
        dlg.destroy()


    def on_menuEmailPreferences_select(self, event):
        """Handles the inputting of email settings"""

        inputDetails = [ ["serverName", self.strs["emlPrefs"]["srvNamP"], 
                          self.strs["emlPrefs"]["srvNamH"],
                          self.emailPrefs["serverName"], 1],

                         ["serverPort", self.strs["emlPrefs"]["srvPtP"],
                          self.strs["emlPrefs"]["srvPtH"],
                          self.emailPrefs["serverPort"], 2],

                         ["name", self.strs["emlPrefs"]["nameP"],
                          self.strs["emlPrefs"]["nameH"],
                          self.emailPrefs["name"], 1],

                         ["email", self.strs["emlPrefs"]["addrP"],
                          self.strs["emlPrefs"]["addrH"],
                          self.emailPrefs["email"], 1],

                         ]

        dlg = PreferencesDialog(self, "Email Preferences", inputDetails)

        dlg.showModal()
        if dlg.accepted():
            self.emailPrefs["serverName"] = dlg.components.serverName.text
            self.emailPrefs["serverPort"] = int(dlg.components.serverPort.text)
            self.emailPrefs["name"] = dlg.components.name.text
            self.emailPrefs["email"] = dlg.components.email.text
            self.status("Email settings updated.")
        else:
            self.status("Cancelled.")
        dlg.destroy()



    def on_menuSettingsRSS_select(self, event):
        self.status("on_menuSettingsRSS_select: Not implemented yet")
        return

    # ------------------------- #
    #  Utilities Menu  Handlers #
    # ------------------------- #

    def on_menuUtilitiesExternalEditor_select(self, event):
        """Loads the text up in an external editor for editing, then reads it back in when done."""
        if not self.saveText(self.generalPrefs["tmpFile"]):
            return
        
        os.system(self.utilitiesPrefs["externalEditor"] + " " + self.generalPrefs["tmpFile"] + ' &')
        if wx.Platform == "__WXMSW__":
            self.insertFile(self.generalPrefs["tmpFile"])


    def on_menuUtilitiesTextScroller_select(self, event):
        dlg=AutoTextScrollerDialog(self,"TextRouter - Auto Scroller",self.utilitiesPrefs,self.getOutputText())
        dlg.showModal()
        if dlg.accepted():
            self.status("Done.")
        dlg.destroy()


    def on_menuUtilitiesNewFilter_select(self, event):
        """Allows the user to define a new filter."""

        inputDetails = [ ["name", self.strs["newFltPrefs"]["nameP"],
                          self.strs["newFltPrefs"]["nameH"],
                          "", 1],
                         ["command", self.strs["newFltPrefs"]["cmdP"],
                          self.strs["newFltPrefs"]["cmdH"],
                          "", 1],
                         ]

        dlg = PreferencesDialog(self, "New Filter", inputDetails)

        dlg.showModal()
        if dlg.accepted():
            self.filters.append( [ dlg.components.name.text, dlg.components.command.text ] )
            self.status("Filter (%s) added." % (self.filters[-1][0]))
        else:
            self.status("New filter definition cancelled.")
        dlg.destroy()

    def on_menuUtilitiesRemoveFilter_select(self, event):
        """Lists the defined filters so the user can choose one to delete."""
        if self.filters == []:
            self.status("There are currently no filters defined.")
            return 0

        options = [ "%s" % filter[0] for filter in self.filters ]

        default = options[0]
        dlg = ChooserDialog(self, 'Choose Filter', \
                            "Choose which filter to remove...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Filter deletion cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            if i == -1:
                self.status("No filter selected for deleting.")
            else:
                self.status("Removed filter: '%s'." % options[i])
                self.filters[i:i+1] = []
        dlg.destroy()


    def on_menuUtilitiesNewShortcut_select(self, event):
        """Allows the user to define a new shortcut."""

        inputDetails = [ ["name", self.strs["newShortcut"]["nameP"],
                          self.strs["newShortcut"]["nameH"],
                          "", 1],
                         ["shortcut", self.strs["newShortcut"]["scP"],
                          self.strs["newShortcut"]["scH"],
                          "", 1],
                         ]

        dlg = PreferencesDialog(self, "New Shortcut", inputDetails)

        dlg.showModal()
        if dlg.accepted():
            self.shortcuts.addShortcut( dlg.components.name.text, dlg.components.shortcut.text )
            self.status("Shortcut '%s' added, type \"%s\" (with the quotes) to use this shortcut." %
                        (dlg.components.name.text,dlg.components.name.text) )
        else:
            self.status("New shortcut definition cancelled.")
        dlg.destroy()


    def on_menuUtilitiesRemoveShortcut_select(self, event):
        """Lists shortcuts so the user can choose one to delete."""
        if len(self.shortcuts.shortcuts) == 0:
            self.status("There are currently no shortcuts defined.")
            return 0

        options = self.shortcuts.shortcuts.keys()

        default = options[0]
        dlg = ChooserDialog(self, 'Choose Shortcut', \
                            "Choose which shortcut to remove...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Shortcut deletion cancelled.")
        else:
            if dlg.components.options.stringSelection == "":
                self.status("No shortcut selected for deleting.")
            else:
                self.status("Removed shortcut '%s'." % dlg.components.options.stringSelection)
                self.shortcuts.delShortcut(dlg.components.options.stringSelection)
        dlg.destroy()

        #self.shortcuts.printShortcuts()

    def on_menuUtilitiesPreferences_select(self, event):
        """Let the user specify some preferences which pertain to the utility functions."""

        inputDetails = [
                         ["externalEditor", self.strs["utilPrefs"]["extEdP"], \
                          self.strs["utilPrefs"]["extEdH"], \
                          self.utilitiesPrefs["externalEditor"], 1],

                         ["textScrollerDelay", self.strs["utilPrefs"]["tsDelP"], \
                          self.strs["utilPrefs"]["tsDelH"], \
                          self.utilitiesPrefs["textScrollerDelay"], 6],

                         ["textScrollerWords", self.strs["utilPrefs"]["tsWrdsP"], \
                          self.strs["utilPrefs"]["tsWrdsH"], \
                          self.utilitiesPrefs["textScrollerWords"], 2],

                         ["textScrollerFont", self.strs["utilPrefs"]["tsFntP"], \
                          self.strs["utilPrefs"]["tsFntH"], \
                          self.utilitiesPrefs["textScrollerFont"], 7],

                         ["shortcutsFile", self.strs["utilPrefs"]["shctFP"], \
                          self.strs["utilPrefs"]["shctFH"], \
                          self.utilitiesPrefs["shortcutsFile"], 1],

                         ["autoSaveShortcuts", self.strs["utilPrefs"]["asShctP"], \
                          self.strs["utilPrefs"]["asShctH"], \
                          self.utilitiesPrefs["autoSaveShortcuts"], 4],

                         ["expandShortcuts", self.strs["utilPrefs"]["apShctP"], \
                          self.strs["utilPrefs"]["apShctH"], \
                          self.utilitiesPrefs["expandShortcuts"], 5, ['blogger', 'all', 'none'] ],

                         ]

        self.showPreferencesScreen(self.utilitiesPrefs, inputDetails, "Utility Preferences", "Utility preferences updated.")

    def on_menuUtilitiesApplyFilter_select(self, event):
        """Lets the user choose a filter which is then applied to the text."""
        if self.filters == []:
            self.status("There are currently no filters defined.")
            return 0

        options = [ "%s" % filter[0] for filter in self.filters ]

        default = options[0]
        dlg = ChooserDialog(self, 'Choose Filter', \
                            "Choose which filter to apply...", \
                            options, default)
        dlg.showModal()
        
        if not dlg.accepted():
            self.status("Filter application cancelled.")
        else:
            i = dlg.components.options.findString(dlg.components.options.stringSelection)
            fhandles = os.popen2(self.filters[i][1])
            fhandles[0].write(self.getOutputText())
            fhandles[0].close()
            self.updateTextBox(fhandles[1].read())
        dlg.destroy()



    # ------------------------- #
    #   Help  Menu   Handlers   #
    # ------------------------- #
    def on_menuHelpHelp_select(self, event):
        """Displays the TextRouter help in a ScrolledMessage dialog window."""
        webbrowser.open("docs/textRouter_help.html", 1, 1)

    def on_menuHelpReadme_select(self, event):
        """Displays the README in a ScrolledMessage dialog window."""
        webbrowser.open("docs/readme.html", 1, 1)

    def on_menuHelpAbout_select(self, event):
        """Displays a small About dialog box."""
        dlg = AboutDialog(self, "TextRouter 0.60", \
                          """\
TextRouter is a generic weblogging and text "routing"
application.  It's main use is for posting to Blogger
and/or Manila maintained weblogs.  It is designed to be
the sort of app which is kept running the whole time;
the idea being that if you find a piece of text you'd
like to send somewhere, you can simply copy and paste
it into TextRouter and send it on its way.\
""",\
                          [ ["TextRouter Homepage:", "http://simon.kittle.info/textrouter/"],
                            ["PythonCard Homepage:", "http://pythoncard.sourceforge.net/"]
                            ] )
        dlg.showModal()
        dlg.destroy()
    

    # ------------------------- #
    #   Button       Handlers   #
    # ------------------------- #

    def on_buttonClearIt_mouseClick(self, event):
        """Clears the text input box"""
        # this was debugging other stuff.
        #print "stuff:"
        #print self.components.area1.getInsertionPoint()
        #print self.components.area1.getSelection()
        #self.components.area1.replaceSelection("boo", 0)
        self.components.area1.text = ""
        self.components.area2.text = ""
        self.saveState()
                

    def on_buttonClipIt_mouseClick(self, event):
        """Puts the clip-board text in to the input text box"""
        self.updateTextBoxFromClipboard()
        self.saveState()

    def on_area1_keyPress(self, event):
        #print "keyPress", event.GetKeyCode()
        if event.keyCode == 9:
            event.target.replaceSelection("\t")
        else:
            event.skip()

    # ------------------------- #
    #        Misc  Stuff        #
    # ------------------------- #

    def showPreferencesScreen(self, prefsList, inputDetails, title, updatedMsg):
        dlg = PreferencesDialog(self, title, inputDetails)

        dlg.showModal()
        if dlg.accepted():
            for pref in inputDetails:
                if pref[4] == 1 or pref[4] == 3:
                    # text entry (text + passwords)
                    prefsList[pref[0]] = getattr(dlg.components, pref[0]).text
                elif pref[4] == 2:
                    # numbers
                    try:
                        prefsList[pref[0]] = int(getattr(dlg.components, pref[0]).text)
                    except ValueError, e:
                        pass
                elif pref[4] == 4 or pref[4] == 5:
                    # Yes/No + Custom choices
                    prefsList[pref[0]] = getattr(dlg.components, pref[0]).stringSelection

                elif pref[4] == 6:
                    # floats
                    try:
                        prefsList[pref[0]] = float(getattr(dlg.components, pref[0]).text)
                    except ValueError, e:
                        pass
                elif pref[4] == 7:
                    # fonts
                    if pref[0] in dlg.values:
                        prefsList[pref[0]] = dlg.values[pref[0]]
                        #print type(prefsList[pref[0]])
                
            self.status(updatedMsg)
        else:
            self.status("Cancelled.")
        dlg.destroy()
        

    def sendEmailTo(self, emailRcpt, body, subject):
        """Sends the text specified to the address specified."""
        # build up the email.
        msg = "From: %s <%s>\r\n" % (self.emailPrefs["name"], self.emailPrefs["email"])
        msg = msg + "To: %s\r\n" % emailRcpt
        msg = msg + "Subject: %s\r\n" % subject
        msg = msg + "User-Agent: TextRouter/0.40\r\n\r\n"
        msg = msg + body.replace("\n", "\r\n")
        msg = msg + "\r\n"
        
        # send the email
        smtpServer = smtplib.SMTP(self.emailPrefs["serverName"], self.emailPrefs["serverPort"])
        smtpServer.sendmail(self.emailPrefs["email"], emailRcpt, msg)
        smtpServer.quit()

    def checkManilaAccounts(self, toCheck = 0):
        """This checks that at least one Manila account is defined and that there is an active account."""
        code = 1
        if toCheck & 2 and self.theCurrentManilaAccount == -1:
            self.status("Warning: You must set a Manila account as active.")
            code = 0

        if toCheck & 1 and self.theManilaAccounts == []:
            self.status("Warning: No Manila accounts have been defined.")
            code = 0
        return code

    def checkBloggerAccounts(self, toCheck = 0):
        """This checks that at least one Blogger account is defined and that there is an active account."""
        code = 1
        if toCheck & 2 and self.theCurrentBloggerAccount == -1:
            self.status("Warning: You must set a Blogger account as active.")
            code = 0

        if toCheck & 1 and self.theBloggerAccounts == []:
            self.status("Warning: No Blogger accounts have been defined.")
            code = 0
        return code


    def getInputActionMode(self):
        """Returns the type of action the next text input should do."""
        if self.components.nextInputActionMode.stringSelection == "inserts":
            return "insert"
        elif self.components.nextInputActionMode.stringSelection == "appends":
            return "append"
        elif self.components.nextInputActionMode.stringSelection == "replaces":
            return "replace"
        
    def getOutputActionMode(self):
        """Returns what part of the text the next output action should work on."""
        return self.components.nextOutputActionMode.stringSelection

    def insertFile(self, path):
        """Given a filename this method opens it, and add's it to the main text box."""
        try:
            file = open(path, "r")
        except IOError, e:
            self.status("Can't open file (%s) for inserting: " % e)
            return 0
        
        data = file.read()
        file.close()
        
        actionStr = self.updateTextBox(data)
        self.status("File '%s' %s." % (path, actionStr))
        return 1


    def getOutputText(self):
        """Returns the current output text according to the current output mode."""
        mode = self.getOutputActionMode()
        if mode == "all":
            return self.components.area1.text
        elif mode == "selection":
#            cursel = self.components.area1.getSelection()
            return self.components.area1.getStringSelection() #text[cursel[0]:cursel[1]]


    def getSubjectText(self):
        """Returns the subject text."""
        return self.components.area2.text

    def updateSubject(self, subject):
        """Updates the subject box."""
        self.components.area2.text = subject

    def updateTextBox(self, newText, mode = ""):
        """Takes a new piece of text, and adds it to the text box according to the current action mode."""
        if mode == "":
            mode = self.getInputActionMode()

        ## open new, overwriting existing text in main textbox.
        if mode == "replace":
            self.components.area1.text = newText
            actionStr = "loaded"

        ## apend
        elif mode == "append":
            self.components.area1.text = self.components.area1.text + newText
            actionStr = "appended"

        ## insert
        elif mode == "insert":
            sel = self.components.area1.getSelection()
            pos = self.components.area1.getInsertionPoint()
            #if wx.Platform == "__WXMSW__":
                #str = self.components.area1.text[0:pos]
                #pos = pos - str.count('\n')
            if sel[0] != sel[1]:
                # this make's it act like "normal".  like when you paste in a selection.
                self.components.area1.replaceSelection("")
            self.components.area1.text = self.components.area1.text[0:pos] + \
                                         newText + \
                                         self.components.area1.text[pos:]
            
            actionStr = "inserted"
        return(actionStr)

    def updateTextBoxFromClipboard(self):
        """Updates the text box from clipboard, taking in to account the current input mode.

        Needed because for the clipboard so we can use .paste() and not mess with wxTheClipboard."""
        mode = self.getInputActionMode()
        if mode == "replace":
            self.components.area1.text = ""
            self.components.area1.paste()
        elif mode == "append":
            curpos = self.components.area1.getInsertionPoint()
            cursel = self.components.area1.getSelection()

            self.components.area1.setInsertionPoint(self.components.area1.getLastPosition())
            self.components.area1.setSelection(self.components.area1.getLastPosition(), \
                                               self.components.area1.getLastPosition())
            
            self.components.area1.paste()
            wx.Yield() # needed because the above statement seems to happen after the two below sometimes
            self.components.area1.setInsertionPoint(curpos)
            self.components.area1.setSelection(cursel[0], cursel[1])
        elif mode == "insert":
            self.components.area1.paste()
        


    def status(self, txt):
        """Sets the status bar text to given argument"""
        self.statusBar.text = txt
        wx.Yield()
        #self.components.statusLine.text = txt

    def showWaitMsg(self, txt):
        """Sets the status bar text to given argument"""
        #self.components.statusLine.text = txt
        #wx.Yield()
        self.status(txt)

    def loadInStrings(self, stringsFile = "strings.txt"):
        """Loads in the strings (prompts, help messages) from the strings file."""
        try:
            self.strs = util.readAndEvalFile(stringsFile)
        except IOError, e:
            result = dialog.messageDialog(self, \
                                       "Error:  The strings file containing the user prompts and messages could not be found.\nThis file is needed to run the program.  Please find the file and restart",
                                       "Strings File Error", wx.ICON_ERROR | wx.OK)
            sys.exit(1)


    def loadInConfig(self, configFile = "textRouter.conf"):
        """Loads in a config file, and sets the Manila site account settings accordingly"""
        msg = "Loading: Config file loaded."
        self.status(msg)
        try:
            configuration = util.readAndEvalFile(configFile)
        except IOError, e:
            self.status("Error loading config file: %s" % e)
            return
        
        # load's up the general preferences
        self.loadInPrefsSet(configuration, "generalPrefs", "generalPreferences")

        # load's up the html preferences
        self.loadInPrefsSet(configuration, "htmlPrefs", "htmlPreferences")

        # load's up the email preferences
        self.loadInPrefsSet(configuration, "emailPrefs", "emailPreferences")

        # load's up the manila preferences
        self.loadInPrefsSet(configuration, "manilaPrefs", "manilaPreferences")

        # load's up the blogger preferences
        self.loadInPrefsSet(configuration, "bloggerPrefs", "bloggerPreferences")

        # load's up the blogger preferences
        self.loadInPrefsSet(configuration, "utilitiesPrefs", "utilitiesPreferences")


        # load's up the state settings (last input/output action, last load/save filenames)
        if "stateSettings" in configuration:
            for aKey in configuration["stateSettings"].keys():
                self.stateSettings[aKey] = configuration["stateSettings"][aKey]
            self.loadInStateSettings()


        # load's up the predefined email recipients
        if "emailRecipients" in configuration:
            self.emailRcpts = configuration["emailRecipients"]

        # load's up the filters
        if "filters" in configuration:
            self.filters = configuration["filters"]

        # sets the manila settings via the setter method
        if "manilaAccounts" in configuration:
            for manilaAccountPrefs in configuration["manilaAccounts"]:

                # these are specifically checked for, because they were later additions, and so by doing
                # this we didn't break the config file for people who were already using it.
                weblogFile = ("weblogOPML" in manilaAccountPrefs and \
                              [ manilaAccountPrefs["weblogOPML"] ] or \
                              [ "" ])[0]

                usePostedL = ("usePostedLine" in manilaAccountPrefs and \
                              [ manilaAccountPrefs["usePostedLine"] ] or \
                              [ "No" ])[0]

                postedLine = ("postedLine" in manilaAccountPrefs and \
                              [ manilaAccountPrefs["postedLine"] ] or \
                              [ "posted at %I:%M %p" ])[0]


                if self.generalPrefs["useProxy"] == "Yes":
                    proxy = self.generalPrefs["proxyServer"] + ":" + str(self.generalPrefs["proxyPort"])
                else:
                    proxy = ""

                self.theManilaAccounts.append(ManilaAccount(proxy))
                
                self.theManilaAccounts[-1].setPrefs(manilaAccountPrefs["siteurl"], \
                                                    manilaAccountPrefs["rpcserver"], \
                                                    manilaAccountPrefs["username"], \
                                                    manilaAccountPrefs["password"], \
                                                    weblogFile, \
                                                    usePostedL, \
                                                    postedLine )
                
        # sets the blogger settings via the setter method, and then setups the active blog.
        if "bloggerAccounts" in configuration:
            for bloggerAccountPrefs in configuration["bloggerAccounts"]:
                if "weblogsPing" in bloggerAccountPrefs:
                    weblogsPing = bloggerAccountPrefs["weblogsPing"]
                else:
                    weblogsPing = "Yes"

                #if self.generalPrefs["useProxy"] == 'Yes':
                #    print "using proxy"
                #    self.theBloggerAccounts.append(BloggerAccount("yes"))
                #else:
                #    print "not using proxy"
                if self.generalPrefs["useProxy"] == "Yes":
                    proxy = self.generalPrefs["proxyServer"] + ":" + str(self.generalPrefs["proxyPort"])
                else:
                    proxy = ""

                self.theBloggerAccounts.append(BloggerAccount(proxy))

                self.theBloggerAccounts[-1].setPrefs(bloggerAccountPrefs["rpcserver"], \
                                                     bloggerAccountPrefs["username"], \
                                                     bloggerAccountPrefs["password"], \
                                                     weblogsPing)

                # can't use setActiveBlog because we haven't logged in yet.  arg.
                self.theBloggerAccounts[-1].prefs["activeBlog"] = int(bloggerAccountPrefs["activeBlog"])
        
        ## -- now do the actual auto login for Blogger
        if self.bloggerPrefs["bloggerAutoLogin"] == 'Yes':
            if "theCurrentBloggerAccount" not in self.stateSettings or \
               self.stateSettings["theCurrentBloggerAccount"] == -1:
                msg += "  Can't login to Blogger because you have no accounts defined."
            else:
                self.status(msg + "  Logging in to Blogger...")
                self.theBloggerAccounts[self.theCurrentBloggerAccount].bloggerLogin()
                if self.theBloggerAccounts[self.theCurrentBloggerAccount].anErrorOccured():
                    msg += "  Error logging in to Blogger."
                else:
                    msg += "  Blogger login OK."
            
        self.status(msg)

        ## -- now do the actual auto login for Manila
        if self.manilaPrefs["manilaAutoLogin"] == 'Yes':
            if self.theCurrentManilaAccount != -1:
                self.theManilaAccounts[self.theCurrentManilaAccount].manilaLogin()
                if self.theManilaAccounts[self.theCurrentManilaAccount].anErrorOccured():
                    msg += "  Error logging in to Manila."
                else:
                    msg += "  Manila login OK."

                    self.status(msg)

                    # now get homepage, if we thats also in the prefs
                    if self.manilaPrefs["manilaAutoGetHomepage"] == 'Yes':
                        self.theManilaAccounts[self.theCurrentManilaAccount].manilaGetHP()
                        if self.theManilaAccounts[self.theCurrentManilaAccount].anErrorOccured():
                            msg += "  Error getting homepage."
                        else:
                            self.updateTextBox(self.theManilaAccounts[self.theCurrentManilaAccount].currentHPContent["body"])
                            msg += "  Homepage downloaded successfully."                    
        self.status(msg)

    def loadInPrefsSet(self, configuration, nameSet, nameSetConfig):
        # load's up the blogger preferences
        if nameSetConfig in configuration:
            for aKey in configuration[nameSetConfig].keys():
                getattr(self, nameSet)[aKey] = configuration[nameSetConfig][aKey]


    def loadInShortcuts(self):
        """Load's in the shortcuts."""

        try:
            self.shortcuts.loadShortcutsFile(self.utilitiesPrefs["shortcutsFile"])
        except IOError, e:
            self.status("Error loading shortcuts: %s" % e)

        #self.shortcuts.printShortcuts()
            
    def saveShortcuts(self):
        """Save's the shortcuts."""

        try:
            self.shortcuts.saveShortcutsFile(self.utilitiesPrefs["shortcutsFile"])
        except IOError, e:
            self.status("Error saving shortcuts: %s" % e)


    def saveText(self, path):
        """ """
        try:
            textFile = open(path, "w")
        except IOError, e:
            self.status("Can't open file (%s) for writing: " % e)
            return 0
        
        textFile.write(self.getOutputText())
        
        if len(self.components.area1.text) > 0 and self.components.area1.text[-1] != "\n":
            textFile.write("\n")
        textFile.close()
        self.status("Text saved to file '%s'." % path)
        return 1
            
    def saveConfig(self, configFile = "textRouter.conf"):
        """Saves a config file."""
        try:
            cfile = open(configFile, "w")
        except IOError, e:
            self.status("Can't open file: %s" % e)
            return
        
        cfile.write("{\n")

        self.writePrefsSet(cfile, "generalPreferences", self.generalPrefs)

        self.writePrefsSet(cfile, "htmlPreferences", self.htmlPrefs)

        self.collectStateSettings()
        self.writePrefsSet(cfile, "stateSettings", self.stateSettings)

        self.writePrefsSet(cfile, "emailPreferences", self.emailPrefs)

        self.writePrefsSet(cfile, "emailRecipients", self.emailRcpts, 2)

        self.writePrefsSet(cfile, "filters", self.filters, 2)

        self.writePrefsSet(cfile, "manilaPreferences", self.manilaPrefs)

        self.writePrefsSet(cfile, "bloggerPreferences", self.bloggerPrefs)

        self.writePrefsSet(cfile, "utilitiesPreferences", self.utilitiesPrefs)

        theManilaAccountPrefs = [ site.prefs for site in self.theManilaAccounts ]
        self.writePrefsSet(cfile, "manilaAccounts", theManilaAccountPrefs, 2)

        theBloggerAccountPrefs = [ site.prefs for site in self.theBloggerAccounts ]
        self.writePrefsSet(cfile, "bloggerAccounts", theBloggerAccountPrefs)
        
        cfile.write("}\n")
        cfile.close()
        
        self.status("Config file saved.")

    def writePrefsSet(self, configFile, setName, prefs, type = 1):
        pp = pprint.PrettyPrinter(indent=4)

        configFile.write("  '%s' : \n" % (setName))
        configFile.write(pp.pformat(prefs))
        configFile.write(",\n")

    def loadInStateSettings(self):
        """Loads the state settings from the dictionary read in from the config file"""
        if "inputActionMode" in self.stateSettings:
            self.components.nextInputActionMode.stringSelection = self.stateSettings["inputActionMode"]
        if "outputActionMode" in self.stateSettings:
            self.components.nextOutputActionMode.stringSelection = self.stateSettings["outputActionMode"]
        if "theCurrentManilaAccount" in self.stateSettings:
            self.theCurrentManilaAccount = self.stateSettings["theCurrentManilaAccount"]
        if "theCurrentBloggerAccount" in self.stateSettings:
            self.theCurrentBloggerAccount = self.stateSettings["theCurrentBloggerAccount"]
        
    def collectStateSettings(self):
        """Collects all the state settings in to 'self.stateSettings' ready for saving to the config file."""
        # some things, like the default load/save files don't need to be collected or loadedIn because
        # they are stored directly in the stateSettings dictionary, thats why they are not here.
        self.stateSettings["inputActionMode"] = self.components.nextInputActionMode.stringSelection
        self.stateSettings["outputActionMode"] = self.components.nextOutputActionMode.stringSelection
        self.stateSettings["theCurrentManilaAccount"] = self.theCurrentManilaAccount
        self.stateSettings["theCurrentBloggerAccount"] = self.theCurrentBloggerAccount


# startup
if __name__ == '__main__':
    app = model.Application(TextRouter)
    app.MainLoop()
