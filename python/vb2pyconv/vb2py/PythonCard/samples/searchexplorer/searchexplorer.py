#!/usr/bin/python

"""
App Name: SearchExplorer
Created: 2001-07-21
Description: The first useful application using the PythonCard prototype.

List widget needs to support selections by number rather than just by string
List widget needs to support more methods for inserting, appending, clearing, etc.

Need support for a default button in the resource format...

If you are familiar with OOP design you'll notice that PythonCard does not
implement a Model View Controller. However, unlike HyperCard I'm
not using widgets themselves as data storage or storing data needed across
methods in global variables, both of which were common techniques in
HyperCard. Instead, I'm using instance variables. Where data is stored and
how it is read and saved transparently is one of the issues we have to explore.

I'm playing with naming conventions. When I make a reference to an actual
widget object I'm prefixing the variable name with 'w' followed by the actual widget
unique name. Visual Basic recommended a convention of three letter abbreviations
for each widget type, but these abbreviations were both hard to remember except
for the simplest ones (btn, lbl, fld, chk, mnu) and the convention doesn't scale
well as the list of widgets grows. So, I'm also trying a verbose naming
convention where I prefix the name with the widget class (listSites). This makes
for much more typing, but it has an appeal.

Naming conventions are just that, conventions, not hard rules or something enforced
by Python or the PythonCard framework, but if everyone follows the same conventions
then it will make reading and modifying PythonCard user code much easier.

No attempt has been made to modularize the logic into appropriate classes and
methods. I wanted to try some Rapid Application Development (RAD)
without much planning, just sticking code into the event handlers as I went.

There isn't much in the way of error checking either.

The initial definition of the widgets for the resource file wasn't too bad, but
using a GUI to create, resize, and set the properties of the widgets would have
been much quicker, so creating even a simple GUI layout tool is a high priority
for me once a little bit more of the prototype framework is in place.

Until we have an IDE that manages both the source code and the resource file
and has a way of showing the valid widgets in context, then getting widget names
and method names out of sync will be a source of problems. Consequently, it might
help when coding to keep a copy of the valid widgets for a given card or background
at the top of the source code or class such as the list below. This is particularly
nice if your editor supports split windows.

fldSearch
btnSearch
lblSites
lblPastSearches
listSites
listPastSearches
chkExitAfterSearch
btnRemoveSearch

"""
__version__ = "$Revision: 1.35 $"
__date__ = "$Date: 2005/12/13 11:13:25 $"
__author__ = "Kevin Altis <altis@semi-retired.com>"

import urllib
import webbrowser
import pprint

from PythonCard import configuration, dialog, model, util, log
import os, sys
import shutil

FAVORITES_FILE = 'favorites.py'

class SearchExplorer(model.Background):

    def on_initialize(self, event):
        self.changed = 0
        wFldSearch = self.components.fldSearch
        # copy the clipboard to fldSearch when the app starts
        if wFldSearch.canPaste():
            wFldSearch.paste()
        else:
            wFldSearch.text = ''
        #wFldSearch.setSelection(0, len(wFldSearch.text))
        # below is a simpler way of selecting all of the text in a field
        wFldSearch.setSelection(-1, -1)

        self.configPath = os.path.join(configuration.homedir, 'searchexplorer')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        basePath = self.application.applicationDirectory
        self.sfFilename = os.path.join(self.configPath, FAVORITES_FILE)
        log.debug('Favourites are in %s' % self.sfFilename)
        if not os.path.exists(self.sfFilename):
            try:
                shutil.copy2(os.path.join(basePath, FAVORITES_FILE), self.sfFilename)
            except IOError:
                dialog.messageDialog(self, 'Unable to load ' + self.sfFilename, 'SearchExplorer exiting')
                sys.exit()
            self.sitesDict = util.readAndEvalFile(self.sfFilename)

        defaultSite = 'Google'
        sites = self.sitesDict.keys()
        # need to implement a case-insensitive sort and use that everywhere
        sites.sort()
        pastSearches = self.sitesDict[defaultSite]['pastSearches']
        pastSearches.sort()

        wListSites = self.components.listSites
        wListSites.items = sites
        wListSites.stringSelection = defaultSite

        self.components.listPastSearches.items = pastSearches

    # *** these methods won't be called if the window close button is used ***
    # *** so any searches made will be lost until that event is hooked up  ***
    # *** in the framework, unless the Exit on search checkbox is checked***
    # *** and the Search button is pressed to do a search/launch a browser ***
    # this "event" is a native wxPython event, not our Event class
    def on_close(self, event):
        self.doExit()
        event.skip()

    def OnExit(self):
        print "OnExit"
        self.doExit()

    def doExit(self):
        # always save the current dictionary of search favorites
        # to simulate transparent saves
        if self.changed:
            f = open(self.sfFilename, "w")
            #s = repr(self.sitesDict)
            #f.write(s)
            pprint.pprint(self.sitesDict, f)
            f.close()

    def doLaunch(self):
        wFldSearch = self.components.fldSearch
        s = wFldSearch.text
        if s != "":
            # update the past searches
            # site = self.find('listSites').getSelection()
            # KEA old version above, getSelection now returns a position
            site = self.components.listSites.stringSelection
            pastSearches = self.sitesDict[site]['pastSearches']
            if s not in pastSearches:
                self.changed = 1
                pastSearches.append(s)
                pastSearches.sort()
                self.components.listPastSearches.items = pastSearches

            encodedText = urllib.quote_plus(s)
            url = self.sitesDict[site]['preURL'] + encodedText + self.sitesDict[site]['postURL']
            
            # launch a new browser window and autoraise it
            # there appears to be a bug in webbrowser.py because
            # if a window already exists, a new one isn't being created ?!
            webbrowser.open(url, 1, 1)

            if self.components.chkExitAfterSearch.checked:
                self.close()

    # pressing return when the search button has focus or double-clicking
    # a past search will launch a browser window
    # just pressing return will work once default buttons are supported
    def on_btnSearch_mouseClick(self, event):
        self.doLaunch()

    #def on_fldSearch_textEnter(self, event):
    #    self.doLaunch()

    def on_listPastSearches_mouseDoubleClick(self, event):
        self.doLaunch()

    def on_listSites_select(self, event):
        pastSearches = self.sitesDict[event.target.stringSelection]['pastSearches']
        wListPastSearches = self.components.listPastSearches
        if len(pastSearches) > 1:
            pastSearches.sort()
        wListPastSearches.items = pastSearches

    def on_listPastSearches_select(self, event):
        self.components.fldSearch.text = event.target.stringSelection

    def on_btnRemoveSearch_mouseClick(self, event):
        wListPastSearches = self.components.listPastSearches
        doomed = wListPastSearches.stringSelection
        if doomed != "":
            site = self.components.listSites.stringSelection
            pastSearches = self.sitesDict[site]['pastSearches']
            pastSearches.remove(doomed) # update self.sitesDict[site]['pastSearches']
            self.changed = 1
            wListPastSearches.items = pastSearches


    def on_menuEditUndo_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canUndo():
            widget.undo()

    def on_menuEditRedo_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canRedo():
            widget.redo()

    def on_menuEditCut_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCut():
            widget.cut()

    def on_menuEditCopy_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCopy():
            widget.copy()

    def on_menuEditPaste_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canPaste():
            widget.paste()
        
    def on_menuEditClear_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            if widget.canCut():
                # delete the current selection,
                # if we can't do a Cut we shouldn't be able to delete either
                # which is why i used the test above
                sel = widget.replaceSelection('')
            else:
                ins = widget.getInsertionPoint()
                widget.replace(ins, ins + 1, '')

    def on_menuEditSelectAll_select(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            widget.setSelection(0, widget.getLastPosition())


if __name__ == '__main__':
    app = model.Application(SearchExplorer)
    app.MainLoop()
