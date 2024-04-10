#!/usr/bin/python

"""
Module Name: oracleBrowse
Description: Plug in for PythonCard application dbBrowse to provide Oracle specific functionality

Constant/configuration values are currently maintained in the source code. If we are to optimise this application they should be split into seperate configuration files (as per PythonCard/Webware style guidelines)

The structure of this module should be replicated for different RDBMS so that they can be interchanged by dbBrowse - hopefully.

The only manipulation to data is to format date values as DD-Mon-YYYY

This module currently relies on cx_Oracle to access Oracle. It should be expanded to use other DB-API compatible access modules.

Changes;
04-Apr-2002 Changed the format of columnDefs that is passed from the db handler modules back to dbBrowser in the getColumns method. This actually makes the code in this module simpler, which must be a good thing
"""
__version__='$Revision: 1.9 $'[11:-2]
__date__='9th November 2001'
__author__='Andy Todd <andy47@halfcooked.com>'

try:
    import cx_Oracle
    oracle = cx_Oracle
except ImportError:
    import DCOracle2
    oracle = DCOracle2

class browse:
    # Connection should be a dictionary with at least three keys, 'username',
    # 'password', 'database' - may need to be normalised for other RDBMS
    def __init__(self, connection):
        "Setup the database connection"
        # self._system_tables=['columns_priv', 'db', 'host', 'tables_priv', 'user']
        # Not providing some values is guaranteed to ruin our connection
        if ('username' not in connection) and ('password' not in connection):
            raise ValueError
        connectString = connection['username']+'/'+connection['password']
        if 'database' in connection:
            if connection['database']:
                connectString += '@' + connection['database']
        self._db = oracle.connect( connectString )
        self._cursor=self._db.cursor()
        # This one is used in getRow
        self._tableName=''

    def getTables(self):
        "Return a list of all of the non-system tables in schema <username>"
        stmt = 'SELECT table_name FROM user_tables'
        self._cursor.execute(stmt)
        return [ tableName[0] for tableName in self._cursor.fetchall() ]

    def getColumns(self, tableName):
        "Get the definition of the columns in tableName"
        # Have to make the data types lower case to keep in line with MySQL
        # format of dbBrowser column definitions is
        #   column name, data type, length (for display), nullable, key, default
        stmt = """SELECT column_name,
                         lower(data_type) data_type,
                         decode(data_type, 'DATE', 11,
                                           'NUMBER', nvl(data_precision, 38),
                                           data_length) precision,
                         decode(nullable, 'Y', 'YES') nullable,
                         ' ' key,
                         ' ' default_value,
                         ' ' extra
                  FROM  user_tab_columns
                  WHERE table_name = '%s'""" % tableName
        self._cursor.execute(stmt)
        return self._cursor.fetchall()

    def getQueryString(self, tableName):
        "Return a SQL statement which queries all of the columns in tableName"
        tableStructure=self.getColumns(tableName)
        # Construct and return the string
        stmt='SELECT '
        for columnList in tableStructure:
            # if columnList[1]=='DATE':
            #    stmt+='date_format('+columnList[0]+", '%d-%b-%Y'), "
            # else:
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
        if tableName!=self._tableName:
            self._tableName=tableName
        self._cursor.execute(self.getQueryString(tableName))
        return self._cursor.fetchall()

if __name__ == '__main__':
    # We are in an interactive session so run our test routines
    # Connect to the database
    connection={ 'username':'andy'
                ,'password':'andy'
                ,'database':'' }
    dbHolder = browse(connection)
    # Return all of our table names into user_tables
    user_tables = dbHolder.getTables()

    # Print out the structure of each table and its first row
    print "--------------------------------------------------"
    for table in user_tables:
        print dbHolder.getQueryString(table)
        # print dbHolder.getRow(table)
        print "--------------------------------------------------"
