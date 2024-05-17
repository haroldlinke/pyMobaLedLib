#!/usr/bin/python
# Usage: python pysqlite2_sample.py <databaseName> <databaseDirectory>
# 
# Create a SQLite2 database from a CSV file with headers.
__author__ = "Alex Tweedly <alex@tweedly.net>"

import sys, csv
from pysqlite2 import dbapi2 as sqlite

# Specify some default values
usageString="Usage: python %s <csvfileName> <databaseName> " % sys.argv[0]

if __name__=="__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h","--help") or len(sys.argv) != 3:
            print usageString
            sys.exit(0)
        # There is a database name on the command line
        csvName=sys.argv[1]
        dbName=sys.argv[2]

        db=sqlite.connect(dbName)
        
        # We have connected to a database now, lets issue some SQL
        # There is no error handling here, if anything goes wrong exceptions
        # will be raised by the MySQLdb package
        csvReader = csv.reader(file(csvName))
        
        headers = csvReader.next()
        # clean up headers to ensure they are valid column names
        #  - could do more error checking here -
        header2 = [ x.replace(' ', '').replace('/', '') for x in headers ]
        # add a type to each
        header3 = [ x + " VARCHAR" for x in header2]
        # and build a single string
        header4 = ",".join(header3)
        
        cursor=db.cursor()
        
        stmt="CREATE TABLE sample ( %s ) " % header4
        
        result=cursor.execute(stmt)
        db.commit()
        stmt="""CREATE UNIQUE INDEX sample_id ON sample(%s)""" % header2[0]
        result=cursor.execute(stmt)
        db.commit()
    
        for row in csvReader:
            stmt="""
                INSERT INTO sample
                   ( %s )
                VALUES
                   ( %s )""" % (",".join(header2), ",".join(["'" + r + "'" for r in row]))
            cursor.execute(stmt)
        db.commit()
    
    else:
        print usageString
        #sys.exit(0)

    
