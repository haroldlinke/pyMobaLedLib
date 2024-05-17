#!/usr/bin/python

"""
Module Name: psyopg
Description: Plug in for PythonCard application dbBrowse to provide Psycopg specific functionality

Psycopg version of the mysqlBrowse class
"""
__version__="$Release $"
__date__="Sat Jun  7 13:39:12 BST 2003"
__author__="Jon Dyte <jon@totient.co.uk>"

import psycopg
from psycopg import NUMBER, STRING, INTEGER, FLOAT, DATETIME
from psycopg import BOOLEAN, ROWID, LONGINTEGER

class browse:

    # Connection should be a dictionary with at least three keys, 'username',
    # 'password', 'database' - may need to be normalised for other RDBMS
    def __init__(self, connection):
        "Setup the database connection"
        self._system_tables = []
        # Not providing a db name is guaranteed to ruin our connection
        if not connection['database']:
            raise ValueError
        self._db = psycopg.connect( "user=%s password=%s dbname=%s" % (connection['username'],
                                                                       connection['password'],
                                                                       connection['database']) )
        self._cursor=self._db.cursor()
        # This one is used in getRow
        self._tableName=''

    def getTables(self):
        "Return a list of all of the non-system tables in <database>.\
        CAVEAT: actually gets all the tables not owned by user 'postgres'"
        stmt ="SELECT t.tablename FROM pg_tables t WHERE tableowner <> \'postgres\'"
        self._cursor.execute(stmt)
        # I'm using a list comprehension here instead of a for loop,
        # either will do but I think this is more concise (unlike this comment)
        return [ x[0] for x in self._cursor.fetchall() if x[0] not in self._system_tables ]

    def getColumns(self, tableName):
        "Get the definition of the columns in tableName"
        stmt = 'select * from %s where 1=0 ' % tableName
        try:
            self._cursor.execute(stmt)
        except psycopg.Error:
            return ()
        desc = self._cursor.description
        r = []
        a = r.append
        ## shamelessly borrowed from the ZPsycopgDA for Zope
        for name, type, width, ds, p, scale, null_ok in desc:
            if type == NUMBER:
                if type == INTEGER:
                    type = INTEGER
                elif type == FLOAT:
                    type = FLOAT
                else: type = NUMBER
            elif type == BOOLEAN:
                type = BOOLEAN
            elif type == ROWID:
                type = ROWID
            elif type == DATETIME:
                type = DATETIME
            else:
                type = STRING
            a((name,type.name,0,0,0))
        return r

    def getQueryString(self, tableName):
        "Return a SQL statement which queries all of the columns in tableName"
        tableStructure=self.getColumns(tableName)
        # Construct and return the string
        return 'SELECT %s FROM %s' % (", ".join([column[0] for column in tableStructure]),
                                      tableName)
    
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
    connection={ 'username':'<username>'
                ,'password':'<password>'
                ,'database':'<db name>'}
    dbHolder = browse(connection)
    # Return all of our table names into user_tables
    user_tables = dbHolder.getTables()

    # Print out the structure of each table and its first row
    print "--------------------------------------------------"
    for table in user_tables:
        print table
        print dbHolder.getQueryString(table)
        print dbHolder.getRow(table)
        print "--------------------------------------------------"
