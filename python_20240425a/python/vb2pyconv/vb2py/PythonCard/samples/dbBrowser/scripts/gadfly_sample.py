#!/usr/bin/python
# Usage: python gadfly_sample.py <databaseName> <databaseDirectory>
# 
# Based on the mysql_sample.py script shipped with the PythonCard dbBrowser sample
__author__ = "Andy Todd <andy47@halfcooked.com>"

import gadfly, sys

# Specify some default values
usageString="Usage: python %s <databaseName> <databaseDirectory>" % sys.argv[0]

if __name__=="__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h","--help") or len(sys.argv) != 3:
            print usageString
            sys.exit(0)
        # There is a database name on the command line
        dbName=sys.argv[1]
        dbDir=sys.argv[2]
        # If the database doesn't already exist we need to create it
        try:
            db=gadfly.gadfly(dbName, dbDir)
        except IOError: 
            print "Database %s doesn't exist, creating it ..." % dbName
            db=gadfly.gadfly()
            db.startup(dbName, dbDir)

    # We have connected to a database now, lets issue some SQL
    # There is no error handling here, if anything goes wrong exceptions
    # will be raised by the MySQLdb package
    cursor=db.cursor()
    stmt="""
         CREATE TABLE currencies
           ( currency_code VARCHAR(3)
            ,currency_desc VARCHAR(255) 
           )
         """
    result=cursor.execute(stmt)
    db.commit()
    stmt="""CREATE UNIQUE INDEX currency_pk ON currencies(currency_code)"""
    result=cursor.execute(stmt)
    db.commit()

    stmt="""
         INSERT INTO currencies
           ( currency_code, currency_desc )
         VALUES
           ( ?, ? )"""
    cursor.execute(stmt, ( 'USD', 'US Dollars'))
    cursor.execute(stmt, ( 'AUD', 'Australian Dollars'))
    cursor.execute(stmt, ( 'UKP', 'Pounds Sterling'))
    cursor.execute(stmt, ( 'FFR', 'French Francs'))
    cursor.execute(stmt, ( 'HKD', 'Hong Kong Dollar'))
    cursor.execute(stmt, ( 'CHF', 'Swiss Franc'))
    cursor.execute(stmt, ( 'CAD', 'Canadian Dollar'))
    cursor.execute(stmt, ( 'VND', 'Vietnamese Dong'))
    db.commit()

    stmt="""
         CREATE TABLE exchange_rates
           ( exchange_date  VARCHAR
            ,currency_from  VARCHAR(3)
            ,currency_to    VARCHAR(3)
            ,exchange_rate  FLOAT
           )
         """
    result=cursor.execute(stmt)
    db.commit()

    stmt="""
         INSERT INTO exchange_rates
           ( exchange_date, currency_from, currency_to, exchange_rate )
         VALUES
           ( ?, ?, ?, ? )
         """
    cursor.execute(stmt, ( '2001-08-01', 'USD', 'AUD', 1.869 ))
    cursor.execute(stmt, ( '2001-08-01', 'USD', 'UKP', 0.750 ))
    cursor.execute(stmt, ( '2001-08-01', 'UKP', 'HKD', 11.02 ))
    db.commit()

