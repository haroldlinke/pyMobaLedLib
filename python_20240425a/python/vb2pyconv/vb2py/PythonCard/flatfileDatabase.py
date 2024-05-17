#!/usr/bin/python

"""
__version__ = "$Revision: 1.26 $"
__date__ = "$Date: 2005/01/24 10:28:20 $"

flatfileDatabase was derived from the addresses sample.

"""

import wx
from PythonCard import dialog, log, model, util
import os, sys
import configparser
import pprint
import pickle
import time

from .templates.dialogs import findDialog

CONFIG_FILE = 'flatfileDatabase.ini'
IGNORE_PREFIX = 'ignore'

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

# KEA 2002-06-24
# adapted from the "A sorted list" topic at:
# http://www.faqts.com/knowledge_base/index.phtml/fid/540

# KEA 2002-07-18
# no longer using SortableList
# but I won't remove it until we're sure it isn't needed

from collections import UserList

class SortableList(UserList):

    def __init__(self, listX=None):
        self.fieldName = None
        self.fieldType = None
        self.data = []
        if listX is not None:
            for item in listX:
                self.append(item)

    def sort(self, *args):
        """ Sort according to *our* rules. """
        self.data.sort(self.cmp)

    # need to decide on what types of sort to support
    # besides a case-insensitive alphabetical sort
    def cmp(self, a, b):
        """ Define your own sorting routine here. """
        if self.fieldName is None:
            return 0
        try:
            if self.fieldType == 'string':
                a = a[self.fieldName].lower()
                b = b[self.fieldName].lower()
            elif self.fieldType == 'numeric':
                a = float(a[self.fieldName])
                b = float(b[self.fieldName])
        except:
            # if for some reason the fields don't exist
            # then use dummy values
            a = None
            b = None
        # print "a:", a, "b:", b
        return cmp(a,b)

class Document:
    def __init__(self, view, filename=None):
        self.view = view
        self.documentChanged = 0

        # KEA 2002-07-02
        # there could be a flag to autosave every time
        # a record changes, so saveRecord would call saveFile
        # that should be more like HyperCard and since data
        # probably doesn't change that often
        # the delay introduced shouldn't be that bad
        # maybe saves could be done in a separate thread?!
        self.saveDocumentOnRecordChange = 1

        self.current = -1
        self.fieldTypes = {'date':['Calendar'],
                           'boolean':['CheckBox'],
                           'integer':['Slider', 'Spinner'],
                           'list':['Choice', 'List', 'RadioGroup'],
                           'string':['CodeEditor',
                                      'PasswordField',
                                      'TextField',
                                      'TextArea']
                           }
        self.allFieldTypes = []
        for value in self.fieldTypes.values():
            self.allFieldTypes += value

        self.fieldNames = self.getFieldNames()
        self.searchableFields = self.getSearchableFields()
        self.sortableFields = self.getSortableFields()

        if filename is None:
            #self.records = SortableList()
            self.records = []
        else:
            self.filename = filename
            self.openFile(filename)


    def getFieldType(self, name):
        fieldType = None
        fieldName = self.view.components[name].__class__.__name__
        for key, value in self.fieldTypes.items():
            if fieldName in value:
                fieldType = key
                break
        return fieldType

    """
    This should probably be a list supplied as part of initialization.
    There might also be a list for field order and fields to search.
    There isn't any meta-data at this point, so there isn't field type
    info either.
    """
    def getFieldNames(self):
        fields = []
        for wName in self.view.components.order:
            if not wName.startswith(IGNORE_PREFIX):
                widget = self.view.components[wName]
                wClass = widget.__class__.__name__
                if wClass in self.allFieldTypes:
                    fields.append(wName)
        return fields

    def getSearchableFields(self):
        fields = []
        for name in self.fieldNames:
            if self.getFieldType(name) == 'string' and self.view.components[name].visible:
                fields.append(name)
        return fields
    
    def getSortableFields(self):
        # this could be different than searchable, but for now
        # just sort on strings until we figure out how to deal with
        # numeric and date fields ...
        sortable = self.searchableFields[:]
        sortable.sort()
        return sortable

    # KEA 2004-04-22
    # clearViewField, getViewField, and setViewField
    # must be updated for selected -> selection, stringSelection
    # change as well as having the right logic for empty lists and choice
    def clearViewField(self, name):
        # based on widget.__class__.__name__
        # set the field correctly
        comp = self.view.components[name]
        fieldType = self.getFieldType(name)
        if fieldType == 'string':
            comp.text = ''
        elif fieldType == 'list':
            comp.selection = 0
        elif fieldType == 'integer':
            comp.value = 0
        elif fieldType == 'date':
            comp.SetNow()
        elif fieldType == 'boolean':
            comp.checked = 0

    def clearViewFields(self):
        for name in self.fieldNames:
            self.clearViewField(name)
        self.updateStatusBar()

    def getViewField(self, name):
        comp = self.view.components[name]
        fieldType = self.getFieldType(name)
        if fieldType == 'string':
            return comp.text
        elif fieldType == 'list':
            return comp.stringSelection
        elif fieldType == 'integer':
            return comp.value
        elif fieldType == 'date':
            return comp.GetDate().Format('%m/%d/%Y %I:%M:%S %p')
        elif fieldType == 'boolean':
            return comp.checked

    def setViewField(self, name, value):
        # based on widget.__class__.__name__
        # set the field correctly
        comp = self.view.components[name]
        fieldType = self.getFieldType(name)
        if fieldType == 'string':
            comp.text = value
        elif fieldType == 'list':
            comp.stringSelection = value
        elif fieldType == 'integer':
            comp.value = value
        elif fieldType == 'date':
            d = wx.DateTime()
            d.ParseFormat(value, '%m/%d/%Y %I:%M:%S %p')
            comp.SetDate(d)
        elif fieldType == 'boolean':
            comp.checked = value
        
    def displayRecord(self, recordNumber):
        #self.clearViewFields()
        self.current = recordNumber
        if self.current != -1:
            record = self.records[recordNumber]
            #for fld in record:
            for name in self.fieldNames:
                #self.view.components[fld].text = record[fld]
                try:
                    self.setViewField(name, record[name])
                except:
                    # what should we do if there is no data?
                    self.clearViewField(name)
        self.updateStatusBar()

    def goRecord(self, recordNumber):
        n = len(self.records) - 1
        if n > 0 and recordNumber >= 0:
            if recordNumber > n:
                recordNumber = n
            if self.current != recordNumber:
                self.saveRecord(self.current)
                self.displayRecord(recordNumber)

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

    def getRecordField(self, num, name):
        return self.records[num][name]

    # KEA 2002-05-28
    # to make the find work like searching one big field, the initial search
    # needs to keep track of the field and selection offset
    # find can probably be refactored to be more efficient, but I want
    # to get it working correctly first and then simplify
    def findTextOnCard(self, searchText, caseSensitive, wholeWordsOnly, field, offset, searchField):
        # we can't search unless there is at least one record
        if len(self.records) > 0:
            current = self.current
            numRecords = len(self.records)
            ##if not caseSensitive:
            ##    searchText = searchText.lower()

            if field in self.searchableFields:
                # only search forward
                searchableFields = self.searchableFields[self.searchableFields.index(field) + 1:]
                if searchField is not None:
                    if not searchField in searchableFields:
                        # the current selection is past the
                        # field we want to search
                        #print "searching field on card not found"
                        return 0
                    else:
                        searchableFields = [searchField]
                    
                #print searchableFields, field, offset
                ##if caseSensitive:
                ##    fieldText = self.records[current][field][offset:]
                ##else:
                ##    fieldText = self.records[current][field][offset:].lower()
                #print fieldText
                ##found = fieldText.find(searchText)
                found = util.findString(searchText, self.getRecordField(current, field)[offset:], 
                    caseSensitive, wholeWordsOnly)
                if found != -1:
                    self.view.components[field].setSelection(offset + found, 
                                                            offset + found + len(searchText))
                    self.view.components[field].setFocus()
                    return 1
                else:
                    #print "not found"
                    # now search the remaining fields on the card
                    for name in searchableFields:
                        try:
                            # if the dictionary is missing a field
                            # name this will avoid throwing an exception
                            ##if caseSensitive:
                            ##    fieldText = self.records[current][name]
                            ##else:
                            ##    fieldText = self.records[current][name].lower()
                            ##found = fieldText.find(searchText)
                            found = util.findString(searchText, self.getRecordField(current, name), 
                                caseSensitive, wholeWordsOnly)
                            if found != -1:
                                # found a match
                                self.displayRecord(current)
                                # KEA 2002-05-28
                                # need to special case for CodeEditor field
                                # this will only work for wxTextCtrl derived fields
                                self.view.components[name].setSelection(found, found + len(searchText))
                                self.view.components[name].setFocus()
                                return 1
                        except:
                            pass
            else:
                #print "what are we searching?"
                #searchableFields = self.searchableFields[:]
                # this should mean that no field has focus
                pass
                
            return 0

    # KEA 2002-05-28
    # changed logic to only search data rather than displaying
    # each record and then searching
    def findRecord(self, searchText, caseSensitive, wholeWordsOnly, field, offset, searchField):
        # we can't search unless there is at least one record
        if len(self.records) > 0:
            found = self.findTextOnCard(searchText, 
                                        caseSensitive,
                                        wholeWordsOnly,
                                        field,
                                        offset,
                                        searchField)
            #print found
            if found:
                return

            self.saveRecord(self.current)
            current = self.current
            numRecords = len(self.records)
            ##if not caseSensitive:
            ##    searchText = searchText.lower()

            # KEA 2002-04-21
            # changed the logic so only visible fields are searched
            if searchField is None:
                searchableFields = self.searchableFields
            else:
                searchableFields = [searchField]

            while 1:
                # we already searched the current card
                # so move onto the next one
                current = current + 1
                if current == numRecords:
                    current = 0
                if current == self.current:
                    # didn't find a match
                    return

                for name in searchableFields:
                    try:
                        # if the dictionary is missing a field
                        # name this will avoid throwing an exception
                        ##if caseSensitive:
                        ##    fieldText = self.records[current][name]
                        ##else:
                        ##    fieldText = self.records[current][name].lower()
                        ##offset = fieldText.find(searchText)
                        offset = util.findString(searchText, self.getRecordField(current, name), 
                            caseSensitive, wholeWordsOnly)
                        if offset != -1:
                            # found a match
                            self.displayRecord(current)
                            # KEA 2002-05-28
                            # need to special case for CodeEditor field
                            # this will only work for wxTextCtrl derived fields
                            self.view.components[name].setSelection(offset, offset + len(searchText))
                            self.view.components[name].setFocus()
                            return
                    except:
                        pass

    def newRecord(self):
        self.saveRecord(self.current)
        if self.current == -1:
            self.current = 0
            #self.records.append({})
        else:
            self.current += 1
        self.records.insert(self.current, {})
        self.clearViewFields()
        self.updateStatusBar()

    def deleteRecord(self):
        # should probably do a dialog here to give the user
        # a chance to cancel
        if self.current != -1:
            del self.records[self.current]
            self.documentChanged = 1
            if len(self.records) == 0:
                self.current = -1
            elif self.current == len(self.records):
                # the last record was deleted,
                # so display the next to last record
                self.current = self.current - 1
        if self.current == -1:
            self.clearViewFields()
            self.updateStatusBar()
        else:
            self.displayRecord(self.current)

    def saveRecord(self, recordNumber):
        """
        it would be more efficient to set a 'dirty' flag per field
        or at least per record if any fields change
        but this still works
        """
        # in HyperCard there is always at least one record
        # which is not always what you want, so if we're going to
        # support 0 records our logic will be different for creating
        # an empty record initially

        # the boundary condition of no records will break the code right now
        # instead we always have at least one record, but it can appear empty
        if recordNumber == -1:
            recordNumber = 0
            self.current = 0
            #self.records = [{}]
            #self.records = SortableList()
            self.records = []
            self.records.append({})
            n = 1
        else:
            n = len(self.records)

        if n > 0 and recordNumber > -1 and recordNumber < n:
            record = self.records[recordNumber]
            changed = 0
            for name in self.fieldNames:
                try:
                    #self.records[recordNumber][wName] = self.view.components[wName].text
                    ##self.records[recordNumber][name] = self.getViewField(name)
                    field = self.getViewField(name)
                    if (name not in record) or (field != record[name]):
                        record[name] = field
                        changed = 1
                        print(recordNumber, record[name])
                except:
                    # missing a field
                    pass
            if changed:
                # should log something here
                #print "changed: ", changed
                self.documentChanged = changed
                #record != self.records[recordNumber]
                
                # KEA 2002-07-09
                # this is destructive, so if a field doesn't exist
                # in the replacement record that information would be lost
                # it might be better to iterate over the fields in record
                # and simply replace the values that we have keys for
                #self.records[recordNumber] = record
                
                for field in record:
                    self.records[recordNumber][field] = record[field]

                if self.saveDocumentOnRecordChange:
                    self.saveFile()

    def commonOpenFileInit(self, filename):
        #self.records = SortableList()
        self.records = []
        self.clearViewFields()
        self.documentChanged = 0
        self.filename = filename
        log.info("filename: %s" % (filename))
        
    def openFile(self, filename):
        self.commonOpenFileInit(filename)
        try:
            if os.path.exists(filename):
                data = util.readAndEvalFile(filename)
                for c in data:
                    self.records.append(c)
                if self.current == -1 and len(self.records) > 0:
                    self.displayRecord(0)
        except:
            pass

    # KEA 2002-07-02
    # to be safe, this should
    # rename the old file with a .bak extension
    # then write a new file
    def saveFile(self):
        # always save the records list
        # for transparent saves
        self.saveRecord(self.current)
        if self.documentChanged:
            print("document changed, saving...")
            try:
                fp = open(self.filename, "w")
                pprint.pprint(self.records, fp)
                fp.close()
                self.documentChanged = 0
            except:
                print("something went wrong")
                pass

    def sortByFieldName(self, name, ascending=1):
        comp = self.view.components[name]
        fieldType = self.getFieldType(name)
        if fieldType == 'string':
            if self.view.statusBar is not None:
                self.view.statusBar.text = 'Sorting...'

            current = self.current
            currentRecord = self.records[self.current]
            #print current, currentRecord[name]
            startTime = time.time()
            try:
                # the 'integer' checks below will never happen since the
                # outer if above prevents sorting on anything but
                # strings, but eventually this will need to be expanded to cover
                # dates and other field types
                if fieldType == 'string':
                    # to see how we got to this function
                    # check out the source and extensive comments in an older version
                    # of the sortByFieldName method, join the url below
                    # http://cvs.sourceforge.net/cgi-bin/viewcvs.cgi/pythoncard/PythonCard
                    # /flatfileDatabase.py?rev=1.5&content-type=text/vnd.viewcvs-markup
                    self.records = util.caseinsensitive_listKeySort(self.records, name)
                elif fieldType == 'integer':
                    # need to figure out how to generalize the code above to work
                    # with different field types, or just put the test for fieldType
                    # in the initial offsets building loop
                    # one of th problems here is that trying to convert a non-existant
                    # field to a float will throw an exception, so instead of '' or None
                    # what value should be used? 0?
                    self.records.sort(lambda a, b: cmp(float(a[name]), float(b[name])))
                if fieldType in ['string', 'integer']:
                    # don't reverse if we didn't sort above
                    if not ascending:
                        self.records.reverse()
            except:
                print("sort failed")
            log.info("sort took %f seconds" % (time.time() - startTime))
            index = self.records.index(currentRecord)
            #print "index", index
            self.current = index
            #print self.current, self.records[self.current][name]
            self.updateStatusBar()

    def sortRecords(self, name=None):
        result = dialog.singleChoiceDialog(self.view, "Sort cards by field:", "Sort", self.sortableFields)
        if result.accepted:
            self.sortByFieldName(result.selection)

    def updateStatusBar(self):
        if self.view.statusBar is not None:
            self.view.statusBar.text = '%d of %d' % (self.current + 1, len(self.records))

class PickleDocument(Document):
    def openFile(self, filename):
        self.commonOpenFileInit(filename)
        try:
            if os.path.exists(filename):
                fp = open(filename, 'rb')
                # avoid having SortableList referenced in the pickle
                #self.records.data = cPickle.load(fp)
                self.records = pickle.load(fp)
                fp.close()
                if self.current == -1 and len(self.records) > 0:
                    self.displayRecord(0)
        except:
            pass

    def saveFile(self):
        self.saveRecord(self.current)
        if self.documentChanged:
            print("document changed, saving...")
            try:
                fp = open(self.filename, "wb")
                # dump binary
                # avoid having SortableList referenced in the pickle
                #cPickle.dump(self.records.data, fp, 1)
                pickle.dump(self.records, fp, 1)
                fp.close()
                self.documentChanged = 0
            except:
                print("something went wrong in saving the pickle")
                pass

class XmlDocument(Document):
    def openFile(self, filename):
        self.commonOpenFileInit(filename)
        #try:
        if os.path.exists(filename):
            self.records = util.XmlToListOfDictionaries(filename)
            if self.current == -1 and len(self.records) > 0:
                self.displayRecord(0)
        #except:
        #    print "failed to load XML", filename
        #    pass

    def saveFile(self):
        return
        
        self.saveRecord(self.current)
        if self.documentChanged:
            print("document changed, saving...")
            try:
                fp = open(self.filename, "wb")
                #cPickle.dump(self.records, fp, 1)
                fp.close()
                self.documentChanged = 0
            except:
                print("something went wrong in saving the XML file")
                pass

class MetakitDocument(Document):
    def openFile(self, filename):
        import metakit
        self.commonOpenFileInit(filename)

        #print filename
        if os.path.exists(filename):
            # need to keep a reference to the storage
            # or it will be garbage collected
            self._db = metakit.storage(filename, 0)
            # there should only be one view, but this
            # needs to be made more robust, perhaps only
            # grabbing the first view?
            viewName = self._db.description().split('[')[0]
            # *** the view is hard-code below but shouldn't be
            # I just want the default view
            # self.records = self._db.view('companies')
            self.records = self._db.view(viewName)
            #print "len(self.records)", len(self.records)
            if self.current == -1 and len(self.records) > 0:
                self.displayRecord(0)

    def displayRecord(self, recordNumber):
        #self.clearViewFields()
        self.current = recordNumber
        if self.current != -1:
            record = self.records[recordNumber]
            #print recordNumber, record
            for name in self.fieldNames:
                try:
                    self.setViewField(name, getattr(record, name))
                except:
                    # what should we do if there is no data?
                    self.clearViewField(name)
        self.updateStatusBar()

    def getRecordField(self, num, name):
        return getattr(self.records[num], name)

    def saveRecord(self, recordNumber):
        return
        # not implemented yet

    def saveFile(self):
        return
        # not implemented yet
        
    def sortByFieldName(self, name, ascending=1):
        comp = self.view.components[name]
        fieldType = self.getFieldType(name)
        if fieldType == 'string':
            if self.view.statusBar is not None:
                self.view.statusBar.text = 'Sorting...'

            current = self.current
            currentRecord = {}
            for field in self.fieldNames:
                value = getattr(self.records[current], field)
                if value:
                    currentRecord[field] = value
            #print currentRecord
            #print current, currentRecord[name]
            startTime = time.time()
            if fieldType == 'string':
                ##self.records = util.caseinsensitive_listKeySort(self.records, name)
                ##self.records.sort(self.records.Company)
                self.records = self.records.sort(getattr(self.records, name))
                if fieldType in ['string', 'integer']:
                    pass
                    # don't reverse if we didn't sort above
                    ##if not ascending:
                    ##    self.records.reverse()
                    ## this needs to use the metakit reverse sort operation
            log.info("sort took %f seconds" % (time.time() - startTime))
            index = self.records.find(currentRecord)
            ##index = self.records.index(currentRecord)
            #print "index", index
            self.current = index
            #print self.current, self.records[self.current][name]
            self.updateStatusBar()


class FlatfileDatabase(model.Background):

    def on_initialize(self, event):
        startTime = time.time()

        # allow a subclass to change provide
        # its own dataFile item so it doesn't need
        # to have a config file
        # see companies sample
        if not hasattr(self, 'dataFile'):
            # KEA 2002-07-04
            # allow a subclass to change the config file
            if not hasattr(self, 'configFilename'):
                self.configFilename = CONFIG_FILE
            self.dataFile = self.getDataFile(self.configFilename)

        if self.dataFile.endswith('.pickle'):
            self.document = PickleDocument(self, self.dataFile)
        elif self.dataFile.endswith('.xml'):
            self.document = XmlDocument(self, self.dataFile)
        elif self.dataFile.endswith('.mk'):
            self.document = MetakitDocument(self, self.dataFile)
        else:
            self.document = Document(self, self.dataFile)

        self.document.filename = self.dataFile
        
        self.lastFind = {'searchText':'', 
                         'replaceText':'', 
                         'wholeWordsOnly':0, 
                         'caseSensitive':0,
                         'field':'',
                         'offset':0,
                         'searchField':None
                        }

        # KEA 2002-06-24
        # workaround for loseFocus event occuring before openBackground
        # probably need to rework how openBackground gets posted to make
        # sure it comes before a window can be deactivated...
        self._initComplete = 1

        log.info("startup took %f seconds" % (time.time() - startTime))

    def getDataFile(self, filename):
        # KEA 2004-08-03
        # this should probably be made more flexible by passing in a full path
        # so that we can switch to using the config directory...
        # assume the ini file is in the same directory as the script
        path = os.path.join(self.application.applicationDirectory, filename)
        parser = configparser.ConfigParser()
        parser.read(path)
        return parser.get('ConfigData', 'dataFile')

    def doSave(self):
        self.document.saveFile()

    def on_close(self, event):
        self.doSave()
        event.Skip()

    def on_save_command(self, event):
        self.doSave()

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

    def on_goToRecord_command(self, event):
        result = dialog.textEntryDialog(self, 'Go to card number:', 'Go to Card', '')
        # this version doesn't alert the user if the line number is out-of-range
        # it just fails quietly
        if result.accepted:
            try:
                i = int(result.text)
                if i > 0:
                    self.document.goRecord(i - 1)
            except:
                pass

    def on_goRecordNumber_command(self, event):
        self.document.goLastRecord()

    # this probably needs to be more sophisticated to
    # allow for the sort to be remembered
    def on_sort_command(self, event):
        startTime = time.time()
        self.document.sortRecords()
        log.info("sort_command took %f seconds" % (time.time() - startTime))

    def saveFocus(self, widget=None):
        if widget is None:
            widget = self.findFocus()
        if hasattr(widget, 'editable'):
            self.lastFind['field'] = widget.name
            self.lastFind['offset'] = widget.getSelection()[1]

    # clicking on the Find button wipes out
    # the focus in the text fields, so save it here
    def on_loseFocus(self, event):
        # KEA 2002-06-24
        # workaround for openBackground when debug runtime
        # windows are used, see openBackground
        if not hasattr(self, '_initComplete'):
            return

        self.saveFocus(event.target)
        event.skip()

    def on_findRecord_command(self, event):
        self.saveFocus()

        searchableFields = self.document.searchableFields[:]
        searchableFields.sort()
        result = findDialog.findDialog(self, self.lastFind['searchText'],
                                self.lastFind['wholeWordsOnly'],
                                self.lastFind['caseSensitive'],
                                self.lastFind['searchField'],
                                searchableFields
                                )
        if result.accepted:
            startTime = time.time()

            self.lastFind['searchText'] = result.searchText
            self.lastFind['wholeWordsOnly'] = result.wholeWordsOnly
            self.lastFind['caseSensitive'] = result.caseSensitive
            self.lastFind['searchField'] = result.searchField
            self.document.findRecord(self.lastFind['searchText'],
                                     self.lastFind['caseSensitive'],
                                     self.lastFind['wholeWordsOnly'],
                                     self.lastFind['field'],
                                     self.lastFind['offset'],
                                     self.lastFind['searchField'])
            log.info("findRecord_command took %f seconds" % (time.time() - startTime))

    def on_findNextRecord_command(self, event):
        startTime = time.time()
            
        self.saveFocus()
        self.document.findRecord(self.lastFind['searchText'], 
                                 self.lastFind['caseSensitive'],
                                 self.lastFind['wholeWordsOnly'],
                                 self.lastFind['field'],
                                 self.lastFind['offset'],
                                 self.lastFind['searchField'])
        log.info("findNextRecord took %f seconds" % (time.time() - startTime))

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
                try:
                    widget.replace(ins, ins + 1, '')
                except:
                    pass

    def on_editSelectAll_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            widget.setSelection(0, widget.getLastPosition())

    def on_editNewCard_command(self, event):
        self.document.newRecord()

    def on_editDeleteCard_command(self, event):
        self.document.deleteRecord()


if __name__ == '__main__':
    # assume the ini file is in the same directory as the script
    path = os.path.join(os.path.dirname(sys.argv[0]), CONFIG_FILE)
    parser = configparser.ConfigParser()
    parser.read(path)
    # the resourceFile is settable via the ini file
    resourceFile = parser.get('ConfigData', 'resourceFile')
    
    app = model.Application(FlatfileDatabase, resourceFile)
    app.MainLoop()
