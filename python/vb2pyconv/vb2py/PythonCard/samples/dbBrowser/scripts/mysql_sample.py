#!/usr/bin/python
# Usage: python mysql_sample.py <username> <password>
# 
# If you do not specify a username and a password then you will need
# to have 'open' access to your local MySQL database.
#
# This script kind of assumes you are one Windows. With the Windows binary
# distribution of MySQL you get two databases 'for free', one called MYSQL
# and another called 'test'. We create the tables in 'test' if the user does
# not specify a database name. If there is no database called 'test' on *nix
# then we are in trouble.
# 
import MySQLdb, sys

# Specify some default values
usageString="Usage: python %s <username> <password> <db name>" % sys.argv[0]
dbName='test'

if __name__=="__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h","--help"):
            print usageString
            sys.exit(0)
        if sys.argv[3]:
            # There is a database name on the command line
            dbName=sys.argv[3]
        # We assume arguments 1 and 2 are username and password
        try:
            db=MySQLdb.connect(user=sys.argv[1], passwd=sys.argv[2], db=dbName)
        except MySQLdb.OperationalError: 
            print usageString
            print "Invalid username, password or db name, please try again"
            sys.exit(1)
    else:
        # Free entry for all
        try:
            db=MySQLdb.connect(db=dbName)
        except MySQLdb.OperationalError:
            print usageString
            print "You cannot connect to the 'test' database without a valid username and password"
            sys.exit(1)
    # We have connected to a database now, lets issue some SQL
    # There is no error handling here, if anything goes wrong exceptions
    # will be raised by the MySQLdb package
    cursor=db.cursor()
    stmt="""
         CREATE TABLE currencies
           ( currency_code VARCHAR(3) NOT NULL
            ,currency_desc VARCHAR(255) 
            ,PRIMARY KEY ( currency_code )
           )
         """
    result=cursor.execute(stmt)

    stmt="""
         INSERT INTO currencies
           ( currency_code, currency_desc )
         VALUES
           ( 'USD', 'US Dollars'),
           ( 'AUD', 'Australian Dollars'),
           ( 'UKP', 'Pounds Sterling'),
           ( 'FFR', 'French Francs'),
           ( 'HKD', 'Hong Kong Dollar'),
           ( 'CHF', 'Swiss Franc'),
           ( 'CAD', 'Canadian Dollar'),
           ( 'VND', 'Vietnamese Dong')
         """
    result=cursor.execute(stmt)

    stmt="""
         CREATE TABLE exchange_rates
           ( exchange_date  DATE NOT NULL
            ,currency_from  VARCHAR(3) NOT NULL
            ,currency_to    VARCHAR(3) NOT NULL
            ,exchange_rate  NUMERIC(15,3)
           )
         """
    result=cursor.execute(stmt)

    stmt="""
         INSERT INTO exchange_rates
           ( exchange_date, currency_from, currency_to, exchange_rate )
         VALUES
           ( '2001-08-01', 'USD', 'AUD', 1.869 ),
           ( '2001-08-01', 'USD', 'UKP', 0.750 ),
           ( '2001-08-01', 'UKP', 'HKD', 11.02 )
         """
    result=cursor.execute(stmt)

