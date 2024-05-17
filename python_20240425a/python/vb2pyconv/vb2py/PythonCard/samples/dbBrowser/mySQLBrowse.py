#!/usr/bin/python

"""
Module Name: mySQLBrowse
Description: Plug in for PythonCard application dbBrowse to provide MySQL specific functionality

Constant/configuration values are currently maintained in the source code. If we are to optimise this application they should be split into seperate configuration files (as per PythonCard/Webware style guidelines)

The structure of this module should be replicated for different RDBMS so that they can be interchanged by dbBrowse - hopefully.

The only manipulation to data is to format date values as DD-Mon-YYYY

The class name was changed to 'browse' for version 0.2.1, this allows us to use 
the same class name in each database handler module.

Data returned from getColumns has been changed for version 0.3. This enables dbBrowser.DbBrowser to be a lot more generic and removes a lot of data manipulationin the on_btnBrowse_mouseClick method. Also added 'func' to the list of system tables (it was added after version 3.23.37)
"""
__version__="0.3"
__date__="30th March, 2002"
__author__="Andy Todd <andy47@halfcooked.com>"

import MySQLdb

class browse:

    # Connection should be a dictionary with at least three keys, 'username',
    # 'password', 'database' - may need to be normalised for other RDBMS
    def __init__(self, connection):
        "Setup the database connection"
        self._system_tables=['columns_priv', 'db', 'host', 'tables_priv', 'user', 'func']
        # Not providing a db name is guaranteed to ruin our connection
        if not connection['database']:
            raise ValueError
        self._db = MySQLdb.connect( user=connection['username']
                                   ,passwd=connection['password']
                                   ,db=connection['database'] )
        self._cursor=self._db.cursor()
        # This one is used in getRow
        self._tableName=''

    def getTables(self):
        "Return a list of all of the non-system tables in <database>"
        stmt = 'show tables'
        self._cursor.execute(stmt)
        # I'm using a list comprehension here instead of a for loop,
        # either will do but I think this is more concise (unlike this comment)
        return [ x[0] for x in self._cursor.fetchall() if x[0] not in self._system_tables ]

    def getColumns(self, tableName):
        "Get the definition of the columns in tableName"
        stmt = 'describe ' + tableName
        self._cursor.execute(stmt)
        # format of MySQL definitions is;
        #  column name,type (incl length & precision),null,key,default,extra
        # format of dbBrowser column definitions is
        #  column name, data type, length (for display), nullable, key, default
        columnDefs = []
        for column in self._cursor.fetchall():
            columnName, nullable, key, default = column[0], column[2], column[3], column[4]
            columnDetails = column[1].split("(")
            dataType = columnDetails[0] # the first 'word' in the definition
            if dataType == "date":
                precision = 22
            elif len(columnDetails) > 1:
                precision = columnDetails[1]
                bracketPosition = precision.find(")")
                if bracketPosition != -1:
                    precision = precision[0:bracketPosition]
                commaPosition = precision.find(",")
                if commaPosition != -1:
                    precision = precision[0:commaPosition]
                precision = int(precision)
            else:
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
            if columnList[1]=='date':
                stmt+='date_format('+columnList[0]+", '%d-%b-%Y'), "
            else:
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
        return self._cursor.fetchone()

    def getRows(self, tableName):
        "Get all of the rows from tableName"
        # When we upgrade to 2.2 this will be a great candidate for a
        # generator/iterator. In the meantime we use self._tableName to keep
        # track of what we are doing
        if tableName!=self._tableName:
            self._tableName=tableName
        self._cursor.execute(self.getQueryString(tableName))
        return self._cursor.fetchall()

if __name__ == '__main__':
    # We are in an interactive session so run our test routines
    # Connect to the database
    connection={ 'username':'andy'
                ,'password':'andy'
                ,'database':'mysql'}
    dbHolder = mySQLBrowse(connection)
    # Return all of our table names into user_tables
    user_tables = dbHolder.getTables()

    # Print out the structure of each table and its first row
    print "--------------------------------------------------"
    for table in user_tables:
        print dbHolder.getQueryString(table)
        print dbHolder.getRow(table)
        print "--------------------------------------------------"
