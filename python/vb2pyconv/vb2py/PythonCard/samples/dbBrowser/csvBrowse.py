#!/usr/bin/python

"""
Module Name: csvBrowse
Description: Plug in for PythonCard application dbBrowse to provide simple CSV functionality

Constant/configuration values are currently maintained in the source code. If we are to optimise this application they should be split into seperate configuration files (as per PythonCard/Webware style guidelines)

The structure of this module should be replicated for different RDBMS so that they can be interchanged by dbBrowse - hopefully.
"""
__version__="$Revision $"[11:-2]
__date__="$Date $"
__author__="Andy Todd <andy47@halfcooked.com>"

import csv, os

class browse:
    # Connection should be a dictionary with at least two keys, 
    # 'databasename' and 'directory'
    # This is wildly different to other database modules 
    def __init__(self, connection):
        "Setup the database connection"
        self._system_tables=[]
        try:
            name = os.path.join(connection["directory"], connection["databasename"])
            self.reader = csv.reader(file(name, "rb"))
            self.headers = self.reader.next()
            self._db = "ok"
            self._cursor="ok"
        except IOError:
            self._db = None
            self._cursor = None
        # This one is used in getRow
        self._tableName='TheOnlyTable'

    def getTables(self):
        "Return a list of all of the non-system tables in <database>"
        return [ "TheOnlyTable" ]

    def getColumns(self, tableName):
        "Get the definition of the columns in tableName"
        # format of dbBrowser column definitions is
        #  column name, data type, length (for display), nullable, key, default
        columnDefs = []
        for column in self.headers:
            columnName = column
            dataType, nullable, key, default  = "varchar", "", "", ""
            # Dodgy default, but it works for me
            precision = 255
            columnDefs.append((columnName, dataType, precision, nullable, key, default))
        return columnDefs

    def getQueryString(self, tableName):
        "Return a SQL statement which queries all of the columns in tableName"
        # only used internally, not needed for csv files
        return ""

    def getRow(self, tableName):
        "Get a row from tableName"
        if tableName!=self._tableName:
            self._tableName=tableName
        result = self.reader.next()
        return result

    def getRows(self, tableName):
        "Get all of the rows from tableName"
        if tableName!=self._tableName:
            self._tableName=tableName
        result = []
        for row in self.reader:
            result.append(row)
        return result

if __name__ == '__main__':
    # We are in an interactive session so run our test routines
    # Connect to the database
    connection={ 'databasename':'testfile.csv'
                ,'directory':'.'}
    dbHolder = browse(connection)
    # Return all of our table names into user_tables
    user_tables = dbHolder.getTables()

    # Print out the structure of each table and its first row
    print "--------------------------------------------------"
    for table in user_tables:
        print dbHolder.getQueryString(table)
        print dbHolder.getRow(table)
        print "--------------------------------------------------"
