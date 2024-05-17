#!/usr/bin/python

"""
Module Name: pysqlite2Browse
Description: Plug in for PythonCard application dbBrowse to provide pysqlite2 specific functionality

Constant/configuration values are currently maintained in the source code. If we are to optimise this application they should be split into seperate configuration files (as per PythonCard/Webware style guidelines)

The structure of this module should be replicated for different RDBMS so that they can be interchanged by dbBrowse - hopefully.
"""
__version__="$Revision $"[11:-2]
__date__="$Date $"
__author__="Andy Todd <andy47@halfcooked.com>"

# AGT 2005-05-17
# see http://www.pysqlite.org
# see http://www.hwaci.com/sw/sqlite/faq.html

from pysqlite2 import dbapi2 as sqlite
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
        # AGT 2005-05-15 single parameter, no mode on connect
        self._db = sqlite.connect(filename)
        self._cursor=self._db.cursor()
        # This one is used in getRow
        self._tableName=''

    def getTables(self):
        "Return a list of all of the non-system tables in <database>"
        ##stmt = "SELECT table_name FROM __table_names__"
        stmt = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        self._cursor.execute(stmt)
        # I'm using a list comprehension here instead of a for loop,
        # either will do but I think this is more concise (unlike this comment)
        return [ x[0] for x in self._cursor.fetchall() if x[0] not in self._system_tables ]

    def getColumns(self, tableName):
        "Get the definition of the columns in tableName"
        stmt = "select * from " + tableName
        self._cursor.execute(stmt)
        #row = self._cursor.fetchone()
        columnDefs = []
        # AGT 2005-05-15 description is a list of item, not a dict
        for column in self._cursor.description:
            columnName = column[0]
            dataType, nullable, key, default  = "varchar", "", "", ""
            # Dodgy default, but if works for me
            precision = 255
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
            self._cursor.execute(self.getQueryString(tableName))
        result = self._cursor.fetchone()
        return result

    def getRows(self, tableName):
        "Get all of the rows from tableName"
        if tableName!=self._tableName:
            self._tableName=tableName
        self._cursor.execute(self.getQueryString(tableName))
        result=self._cursor.fetchall()
        return result

if __name__ == '__main__':
    # We are in an interactive session so run our test routines
    # Connect to the database
    ##connection={ 'databasename':'andy'
    ##            ,'directory':'E:\Gadfly'}
    print os.getcwd()
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
