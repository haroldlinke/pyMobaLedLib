#!/usr/bin/python

"""
Module Name: metakitBrowse
Description: Plug in for PythonCard application dbBrowse to provide MetaKit specific functionality

Constant/configuration values are currently maintained in the source code. If we are to optimise this application they should be split into seperate configuration files (as per PythonCard/Webware style guidelines)

The structure of this module should be replicated for different RDBMS so that they can be interchanged by dbBrowse - hopefully.

To Do;
  Because metakit isn't a relational database we probably don't need to support the getQueryString method in this class. Its only really an internal utility method for the other, public, classes anyway.
"""
#jm - marked changes 030218
__version__="$Revision $"[11:-2]
__date__="$Date $"
__author__="Andy Todd <andy47@halfcooked.com>"

import metakit
import os

class browse:

    # Connection should be a dictionary with at least two keys, 
    # 'databasename' and 'directory'
    # This is wildly different to other database modules 
    def __init__(self, connection):
        "Setup the database connection"
        self._system_tables=[]
        # Not providing a db name is guaranteed to ruin our connection
        if not connection['databasename']:
            raise ValueError
        filename = os.path.join(connection['directory'], connection['databasename'])
        # not sure about the mode to use, I assume we just want read-only
        self._db = metakit.storage(filename, 0)
        self._cursor='placeholder'
        # This one is used in getRow
        self._tableName=''

    def getTables(self):
        "Return a list of all of the non-system tables in <database>"
        return [p.name for p in self._db.contents().structure() if p.type == 'V']    #jm

    def getColumns(self, tableName):
        "Get the definition of the columns in tableName"
        columnDefs = []
        for column in self._db.view(tableName).structure():      #jm - this block
            columnName, dataType = column.name,column.type
            if dataType in  ['S','V']:
                dataType == 'varchar'
            elif dataType == 'I':
                dataType == 'int'
            elif dataType in ["F","D"]:
                dataType == 'float'
            nullable, key, default  = "", "", ""
            # Dodgy default, but if works for me
            precision = 25
            columnDefs.append((columnName, dataType, precision, nullable, key, default))
        return columnDefs

    def getQueryString(self, tableName):
        "Return a SQL statement which queries all of the columns in tableName"
        tableStructure=self.getColumns(tableName)
        # Construct and return the string
        stmt='SELECT '
        for columnList in tableStructure:
            stmt+=columnList[0]+', '
        stmt=stmt[:-2]+' FROM '+tableName
        return stmt

    def getRow(self, tableName):
        "Get a row from tableName"
        # When we upgrade to 2.2 this will be a great candidate for a
        # generator/iterator. In the meantime we use self._tableName to keep
        # track of what we are doing
        if tableName!=self._tableName:
            self._tableName=tableName
            self._cursor = self._db.view(tableName)
            self._currentPos = -1

        self._currentPos += 1
        if self._currentPos == len(self._cursor):
            self._currentPos -= 1
            return None

        # could cache these
        # apparently we don't need all the junk info
        # from getColumns nor do we need to use getQueryString
        columnNames = [i.name for i in self._cursor.structure()]    #jm
        row = self._cursor[self._currentPos]
        result = []
        for c in columnNames:
            try:
                result.append(getattr(row, c))
            except AttributeError:
                result.append('')
        #print result
        return result

    def getRows(self, tableName):
        "Get all of the rows from tableName"
        # columnNames = [i[0] for i in self.getColumns(tableName)]
        self._cursor=self._db.view(tableName)
        columnNames = [i.name for i in self._cursor.structure()]    #jm
        rows=[]
        for row in range(0, len(self._cursor)):
            currentRow=[]
            for column in columnNames:
                currentRow.append(getattr(self._cursor[row], column))
            rows.append(currentRow)
        return rows

if __name__ == '__main__':
    # We are in an interactive session so run our test routines
    # Connect to the database
    ##connection={ 'databasename':'andy'
    ##            ,'directory':'E:\Gadfly'}
    connection={'databasename':'calflora.db', 'directory':'.'}
    dbHolder = browse(connection)
    # Return all of our table names into user_tables
    user_tables = dbHolder.getTables()

    # Print out the structure of each table and its first row
    print "--------------------------------------------------"
    for table in user_tables:
        print "table:", table
        print dbHolder.getQueryString(table)
        print dbHolder.getRow(table)
        print "--------------------------------------------------"
