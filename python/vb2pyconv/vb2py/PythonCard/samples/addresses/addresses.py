#!/usr/bin/python

"""
A lot of the record structure and logic mirrors Winkler's approach used in
the textIndexer, but I coded this from scratch to see what kind of differences
would appear. I also didn't bother using a separate class to hold the internal
data structures initially, so this version will get refactored. I realized that
once I started porting the Addresses stack from HyperCard, we could use this
addresses sample to test different approaches to storage formats: ZODB, mySQL,
plain text files using lists and dictionaries, CSV text files, etc.
"""
__version__ = "$Revision: 1.36 $"
__date__ = "$Date: 2005/12/13 11:13:21 $"

from PythonCard import configuration, dialog, model, util
import os, sys
import pprint
import shutil
import outlook

DATA_FILE = 'data.txt'

"""
The Document class below has a reference to the view, so it is responsible for
updating the fields in the view.

There should be an abstract Document class, an abstract RecordsDocument subclass
and finally a DictionaryRecordsDocument or a name that reflects that the actual
records are stored as a list of dictionaries.

If the Document was stored as a DBM or dictionary of dictionaries then an additional
field would be needed to keep track of record order and goPrevRecord, goNextRecord,
goFirstRecord, and goLastRecord would have to be modified to use that ordering.
"""

class Document:
    def __init__(self, view, filename=None):
        self.view = view
        self.current = -1
        self.fieldNames = self.getFieldNames()
        if filename is None:
            self.records = []
        else:
            self.filename = filename
            self.openFile(filename)

    """
    This should probably be a list supplied as part of initialization.
    There might also be a list for field order and fields to search.
    There isn't any meta-data at this point, so there isn't field type
    info either.
    """
    def getFieldNames(self):
        fields = []
        for wName in self.view.components.iterkeys():
            widget = self.view.components[wName]
            wClass = widget.__class__.__name__
            if wClass in ['TextField', 'TextArea'] and widget.visible:
                fields.append(wName)
        if fields.count('Notes') == 0:
            fields.append('Notes')
        return fields

    def clearFields(self):
        for wName in self.fieldNames:
            self.view.components[wName].text = ""
        
    def displayRecord(self, recordNumber):
        self.clearFields()
        self.current = recordNumber
        if self.current != -1:
            record = self.records[recordNumber]
            for fld in record:
                self.view.components[fld].text = record[fld]

    def goPrevRecord(self):
        if len(self.records) > 1:
            prevRec = self.current - 1
            if prevRec == -1:
                prevRec = len(self.records) - 1
            self.saveRecord(self.current)
            self.displayRecord(prevRec)
            
    def goNextRecord(self):
        if len(self.records) > 1:
            nextRec = self.current + 1
            if nextRec == len(self.records):
                nextRec = 0
            self.saveRecord(self.current)
            self.displayRecord(nextRec)

    def goFirstRecord(self):
        if len(self.records) > 1:
            if self.current != 0:
                self.saveRecord(self.current)
                self.displayRecord(0)

    def goLastRecord(self):
        n = len(self.records) - 1
        if n > 0:
            if self.current != n:
                self.saveRecord(self.current)
                self.displayRecord(n)

    def findRecord(self, searchText, caseSensitive):
        # we can't search unless there is at least one record
        if len(self.records) > 1:
            self.saveRecord(self.current)
            current = self.current
            if not caseSensitive:
                searchText = searchText.lower()
            while 1:
                for name in self.fieldNames:
                    if caseSensitive:
                        fieldText = self.records[self.current][name]
                    else:
                        fieldText = self.records[self.current][name].lower()
                    offset = fieldText.find(searchText)
                    if offset != -1:
                        # if the text is found in the Notes field and it isn't visible
                        # then the selection below doesn't work without making the field
                        # visible, but then the Show Notes/Hide Notes button will be out
                        # of sync if we just set visible = 1
                        # so some different logic is really needed here
                        #self.view.components[name].visible = 1
                        # the solution below is a hack
                        if not self.view.components[name].visible:
                            self.view.on_showNotes_command(self.view.components['ShowNotes'], None)
                        self.view.components[name].setSelection(offset, offset + len(searchText))
                        self.view.components[name].setFocus()
                        return
                self.goNextRecord()
                if current == self.current:
                    return

    def newRecord(self):
        self.saveRecord(self.current)
        if self.current == -1:
            self.current = 0
            #self.records.append({})
        else:
            self.current += 1
        self.records.insert(self.current, {})
        self.clearFields()

    def deleteRecord(self):
        # should probably do a dialog here to give the user
        # a chance to cancel
        if self.current != -1:
            del self.records[self.current]
            if len(self.records) == 0:
                self.current = -1
            elif self.current == len(self.records):
                # the last record was deleted,
                # so display the next to last record
                self.current = self.current - 1
        self.displayRecord(self.current)

    def saveRecord(self, recordNumber):
        """
        it would be more efficient to set a 'dirty' flag per field
        or at least per record if any fields change
        but this still works
        """
        n = len(self.records)
        # in HyperCard there is always at least one record
        # which is not always what you want, so if we're going to
        # support 0 records our logic will be different for creating
        # an empty record initially

        # the boundary condition of no records will break the code right now        
        if recordNumber == -1:
            pass

        if n > 0 and recordNumber > -1 and recordNumber < n:
            for wName in self.fieldNames:
                self.records[recordNumber][wName] = self.view.components[wName].text

    def openFile(self, filename):
        self.records = []
        self.filename = filename
        try:
            if os.path.exists(filename):
                addresses = util.readAndEvalFile(filename)
            for c in addresses:
                self.records.append(c)
            if self.current == -1 and len(self.records) > 0:
                self.displayRecord(0)
        except IOError:
            pass

    def saveFile(self):
        # always save the records list
        # for transparent saves
        self.saveRecord(self.current)
        try:
            f = open(self.filename, "w")
            pprint.pprint(self.records, f)
            f.close()
        except IOError:
            pass

class Addresses(model.Background):

    def on_initialize(self, event):
        if not outlook.WIN32_FOUND:
            self.menuBar.setEnabled('menuFileImportOutlook', 0)
        self.loadConfig()

    def loadConfig(self):
        self.configPath = os.path.join(configuration.homedir, 'addresses')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        basePath = self.application.applicationDirectory
        self.dataPath = os.path.join(self.configPath, DATA_FILE)
        if not os.path.exists(self.dataPath):
            shutil.copy2(os.path.join(basePath, DATA_FILE), self.dataPath)

        self.document = Document(self, self.dataPath)

    def doExit(self):
        self.document.saveFile()

    def on_close(self, event):
        self.doExit()
        event.skip()

    def on_fileImportOutlook_command(self, event):
        addressesToOutlookMap = {'Name':'FullName',
                                 'Company':'CompanyName',
                                 'Street':'MailingAddressStreet',
                                 'City':'MailingAddressCity',
                                 'State':'MailingAddressState',
                                 'Zip':'MailingAddressPostalCode',
                                 'Phone1':'HomeTelephoneNumber',
                                 'Phone2':'BusinessTelephoneNumber',
                                 'Phone3':'MobileTelephoneNumber',
                                 'Phone4':'Email1Address',
                                 'Notes':'Body'
                                 }
        print "attempting to load Outlook"
        oOutlook = outlook.MSOutlook()
        # delayed check for Outlook on win32 box
        if not oOutlook.outlookFound:
            # could also display an error message here
            self.menuBar.setEnabled('menuFileImportOutlook', 0)
            return

        print "loading records..."
        oOutlook.loadRecords()
        print "importing into addresses"
        for r in oOutlook.records:
            aRecord = {}
            for fld in addressesToOutlookMap:
                """
                if fld == 'Name':
                    names = addressesToOutlookMap[fld]
                     fullName = r[names[0]] + " " + r[names[1]]
                     aRecord['Name'] = fullName.strip()
                else:
                """
                aRecord[fld] = r[addressesToOutlookMap[fld]]
            self.document.records.append(aRecord)
        print "done importing"
        self.document.goNextRecord() # show that we imported at least one record

    def on_exit_command(self, event):
        self.close()

    def on_goPrev_command(self, event):
        self.document.goPrevRecord()

    def on_goNext_command(self, event):
        self.document.goNextRecord()

    def on_goFirst_command(self, event):
        self.document.goFirstRecord()

    def on_goLast_command(self, event):
        self.document.goLastRecord()

    def on_findRecord_command(self, event):
        result = dialog.findDialog(self)
        if result.accepted:
            self.document.findRecord(result.searchText, result.caseSensitive)

    def on_editUndo_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canUndo():
            widget.undo()

    def on_editRedo_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canRedo():
            widget.redo()

    def on_editCut_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCut():
            widget.cut()

    def on_editCopy_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCopy():
            widget.copy()

    def on_editPaste_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canPaste():
            widget.paste()

    def on_editClear_command(self, event):
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

    def on_editSelectAll_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            widget.setSelection(0, widget.getLastPosition())

    def on_editNewCard_command(self, event):
        self.document.newRecord()

    def on_editDeleteCard_command(self, event):
        self.document.deleteRecord()

    def on_showNotes_command(self, event):
        target = event.target
        if target.label == 'Show Notes':
            self.components.Notes.visible = 1
            target.label = 'Hide Notes'
        else:
            self.components.Notes.visible = 0
            target.label = 'Show Notes'

if __name__ == '__main__':
    app = model.Application(Addresses)
    app.MainLoop()
