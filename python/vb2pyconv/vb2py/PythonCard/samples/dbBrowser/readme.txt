Module  : dbBrowser
Date    : 2nd July, 2003
Author  : Andy Todd <andy47@halfcooked.com> 
Minor additions: May 17, 2005  Alex Tweedly <alex@tweedly.net>

dbBrowser is a client for viewing data from relational databases. Once you connect to a database, select a table and the rows of data from it are available for you to view.

The current version of dbBrowser works with MySQL, Gadfly, SQLite, Metakit, PySQLite, PySQLite2, PostgreSQL and Oracle. The code is stable but this is still an alpha release so if you are not already using any of these databases it is probably best to give this a miss until it is more stable.

The current distribution includes an alternative version of dbBrowser (called dbBrowser2) which uses a wxGrid to display the results of your queries rather than the row at a time of dbBrowser. 

To access MySQL databases you will need MySQL installed, get it from:
  http://www.mysql.com/

You will also need the MySQLdb package, which can be found at (rpm, tar.gz, source):
  http://sourceforge.net/projects/mysql-python/

If you have MySQL but don't have any database tables or data a sample schema is included with this sample. From the scripts directory run "python mysql_sample.py"

To access Oracle databases you will need the Oracle client installed, get it from:
  http://www.oracle.com

You will also need access to an Oracle database with the appropriate user name, password and connection string. Ensure you can connect to your database through SQL*Plus before attempting to use this application.

You will also need the either the cx_Oracle package which can be found at:
   http://www.computronix.com/utilities
Or DCOracle2, available at;
   http://www.zope.org/Members/matt/dco2
If you have either of these modules installed dbBrowser will use them automatically. 

You will need the Gadfly pure Python module from:
  http://gadfly.sourceforge.net/

This has only been tested with release candidate 1 of this module. 

To access PySQLite databases you will need pysqlite installed, either version 1 or 2, get them from:
  http://www.pysqlite.org/

If you have pysqlite2 installed but don't have any database tables or data, a utility is included with this sample, to create a db from any CSV file. From the scripts directory run "python pysqlite2_from_csv.py".

Future versions will use different databases. I'm planning to include support for ODBC. If you would like to add support for another RDBMS please send me an e-mail or post a notice to the mailing list (pythoncard-users@lists.sourceforge.net).

Observations
------------

You will need to know the name of the database you want to connect to. By default MySQL creates databases called 'test' and 'mysql' when you install it. If you are stuck try the on line documentation at:
  http://www.mysql.com/doc/
After that you are definitely on your own - unless you send me a really nice e-mail.

By default there are no tables in a fresh installation of MySQL. The application 'ignores' the system tables (columns_priv, db, host, tables_priv, user). For the application to work you will need to have created and populated your own tables. Otherwise it will simply connect to the database and then not provide you with any tables to browse.

If you are connecting to oracle you will need to connect as a schema owner. If the user you connect to the database with does not own any tables you will not be able to browse any data. This is because the handler module uses the 'USER' data dictionary views. Future versions may use the 'ALL' data dictionary views but the best way to support these would be to write the code yourself, submissions are always welcome.

If you select a database type of Gadfly, SQLite or Metakit the connection details will change. You need to provide a database name and location.

Change Notices
--------------
16.08.2005 - Clean up and re-factoring
17.05.2005 - Added PySQLite2 support, including script to create a test database from a csv file.
??.09.2004 - Added CSV support, including a testfile.csv test sample.
02.07.2003 - Added PostgreSQL support thanks to Jon Dyte
04.05.2003 - Added dbBrowser2
11.06.2002 - Added support for the 'new' gadfly module
11.06.2002 - On startup place the cursor in the username field and make the 'connect'
             button the default when the user presses 'enter'.
04.04.2002 - Changed the format of the column definitions passed around by the
             different modules. This should cope with different datatypes in the
             database modules much more elegantly.
20.11.2001 - Moved icon setting code to framework
10.11.2001 - Added support for Oracle as well as MySQL. Changed the version numbering to date values
0.3 - Moved the login process to a modal dialog. This will pop up on startup.
      It can also be displayed when you select File|Open from the menu allowing
      you to change the database (or schema) the application is connected to.
0.2 - Added dynamic event handling for the navigation buttons/menu items.
      Changed the layout of data widgets to one label and data item per line.
      The focus changes to the table widget after connecting to a database.
      Changed format of date columns to DD-MON-YYYY for MySQL.
      Added some error handling to check for a valid MySQL database connection.
