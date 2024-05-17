#!/usr/bin/python

__version__ = "$Revision: 1.11 $"
__date__ = "$Date: 2004/08/12 19:40:39 $"

"""
flatfileDatabase was derived from the addresses sample.
gadflyDatabase was derived from the flatfileDatabase
"""

from PythonCard import log, model
from PythonCard import flatfileDatabase
import os, sys
import configparser
import time

import gadfly
from gadfly.store import StorageError

CONFIG_FILE = 'gadflyDatabase.ini'
IGNORE_PREFIX = 'ignore'

class Document(flatfileDatabase.Document):
    def __init__(self, view, db=None, tableName=None):
        self.view = view
        self.documentChanged = 0

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

        if db is None:
            self.records = []
        else:
            self.tableName = tableName
            self.openFile(db, tableName)
            self._db = db

    def newRecord(self):
        self.saveRecord(self.current)
        if self.current == -1:
            self.current = 0
        else:
            stmt = "UPDATE %s SET ID=ID+1 WHERE ID > %d" % (self.tableName, self.current)
            cursor = self._db.cursor()
            cursor.execute(stmt)
            self._db.commit()
            self.current += 1
        self.records.insert(self.current, {})
        self.clearViewFields()
        self.displayRecord(self.current) # Needed to sync the model & the view
        self.updateStatusBar()

    def deleteRecord(self):
        if self.current != -1:
            del self.records[self.current]
            stmt = "DELETE FROM %s WHERE id = %d" % (self.tableName, self.current)
            cursor = self._db.cursor()
            cursor.execute(stmt)
            self._db.commit()
            #  Re-sequence the remaining records
            if len(self.records) > 0:
                stmt = "UPDATE %s SET ID=ID-1 WHERE ID > %d" % (self.tableName, self.current)
                cursor = self._db.cursor()
                cursor.execute(stmt)
                self._db.commit()
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
        "Save the record <recordNumber> to the database"
        if recordNumber == -1:
            recordNumber = 0
            self.current = 0
            self.records = []
            self.records.append({})
            n = 1
        else:
            n = len(self.records)

        if n > 0 and recordNumber > -1 and recordNumber < n:
            record = self.records[recordNumber]
            if recordNumber == self.current:
                changed = 0
                for name in self.fieldNames:
                    try:
                        field = self.getViewField(name)
                        if (name not in record) or (field != record[name]):
                            record[name] = field
                            changed = 1
                    except:
                        # missing a field
                        pass
            else:
                # Just use the value in self.records
                changed = 1
            if changed:
                self.documentChanged = changed
                
                for field in record:
                    self.records[recordNumber][field] = record[field]

                cursor = self._db.cursor()
                stmt = "INSERT INTO %s ( ID, " % self.tableName
                values = []
                for field in self.fieldNames:
                    stmt += "%s, " % field
                stmt = stmt[:-2] + ") VALUES ( %d, " % recordNumber
                for field in self.fieldNames:
                    stmt += "?, " 
                    values.append(self.getViewField(field))
                stmt = stmt[:-2] + ")"
                try:
                    cursor.execute(stmt, tuple(values))
                except StorageError:
                    # Update failed, try an insert
                    self._db.rollback()
                    stmt = "UPDATE %s SET " % self.tableName
                    values = []
                    for field in self.fieldNames:
                        stmt += "%s = ?, " % field
                        values.append(self.getViewField(field) )
                    stmt = stmt[:-2] + "WHERE ID = %d" % recordNumber
                    cursor.execute(stmt, tuple(values))
                self._db.commit()
                self.displayRecord(recordNumber)

    def sortRecords(self):
        "Sort the records in memory, and in the database"
        flatfileDatabase.Document.sortRecords(self)
        index = 0
        for record in self.records:
            self.saveRecord(index)
            index += 1

    def openFile(self, db, tableName):
        self.commonOpenFileInit(tableName)
        cursor = db.cursor()
        # Check to see if our table exists, if it doesn't create it
        stmt = "SELECT count(*) FROM __table_names__ WHERE table_name = ?" 
        cursor.execute(stmt, (tableName.upper(), ))
        result = cursor.fetchall()[0][0]
        if result == 0:
            self.createTable(db, tableName)
        else:
            stmt = "SELECT "
            for column in self.fieldNames:
                stmt += "%s, " % column
            stmt = stmt[:-2] + ", ID FROM " + tableName
            stmt += " ORDER BY ID"
            cursor.execute(stmt)
            for data in cursor.fetchall():
                record = {}
                index = 0
                for column in self.fieldNames:
                    record[column]=data[index]
                    index += 1
                self.records.append(record)
        if self.current == -1 and len(self.records) > 0:
            self.displayRecord(0)

    def createTable(self, db, tableName):
        "Create our actual application table"
        cursor = db.cursor()
        stmt = "CREATE TABLE %s ( ID integer, " % tableName
        for column in self.fieldNames:
            stmt += "%s varchar, " % column
        stmt = stmt[:-2] + ")"
        cursor.execute(stmt)
        # And a unique index on the primary key
        stmt = "CREATE UNIQUE INDEX %s ON %s (ID)" % ( tableName+'_pk', tableName)
        cursor.execute(stmt)
        db.commit()

    def saveFile(self):
        # always save the records list
        # for transparent saves
        self.saveRecord(self.current)

class GadflyDatabase(flatfileDatabase.FlatfileDatabase):

    def on_initialize(self, event):
        startTime = time.time()

        # allow a subclass to provide its own configuration so it doesn't need
        # to have a config file. See companies sample
        if not hasattr(self, 'configFilename'):
           self.configFilename = CONFIG_FILE

        db, tableName = self.getDatabase(self.configFilename)
        self.document = Document(self, db, tableName)

        self.lastFind = {'searchText':'', 
                         'replaceText':'', 
                         'wholeWordsOnly':0, 
                         'caseSensitive':0,
                         'field':'',
                         'offset':0,
                         'searchField':None
                        }

        self._initComplete = 1
        log.info("startup took %f seconds" % (time.time() - startTime))

    def on_findRecord_command(self, event):
        "Save the current record and find a new one"
        self.doSave()
        flatfileDatabase.FlatfileDatabase.on_findRecord_command(self, event)

    def getDatabase(self, filename):
        "Return the db and table name from <filename>"
        # assume the ini file is in the same directory as the script
        path = os.path.join(os.path.dirname(sys.argv[0]), filename)
        parser = configparser.ConfigParser()
        parser.read(path)
        dbDir = parser.get('ConfigData', 'dbDir')
        dbName = parser.get('ConfigData', 'dbName')
        tableName = parser.get('ConfigData', 'tableName')
        try:
            db = gadfly.gadfly(dbName, dbDir)
        except IOError:
            db = gadfly.gadfly()
            db.startup(dbName, dbDir)
        return db, tableName

    def doSave(self):
        self.document.saveFile()

if __name__ == '__main__':
    # assume the ini file is in the same directory as the script
    path = os.path.join(os.path.dirname(sys.argv[0]), CONFIG_FILE)
    parser = configparser.ConfigParser()
    parser.read(path)
    # the resourceFile is settable via the ini file
    resourceFile = parser.get('ConfigData', 'resourceFile')
    
    app = model.Application(GadflyDatabase, resourceFile)
    app.MainLoop()
