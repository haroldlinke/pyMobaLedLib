#!/usr/bin/python

"""
__version__ = "$Revision: 1.10 $"
__date__ = "$Date: 2005/12/13 11:13:22 $"
"""

# adapted from
# http://docs.python.org/lib/dom-example.html

import os
from xml.dom import minidom
import pprint
import cPickle
import time
import urllib
from xml.sax.saxutils import escape

from PythonCard import configuration
configPath = os.path.join(configuration.homedir, 'companies')
if not os.path.exists(configPath):
    os.mkdir(configPath)

XMLFILENAME = os.path.join(configPath, 'companies.xml')
COMPANIES_URL = 'http://pythoncard.sourceforge.net/companies.xml'
SAVEBINARY = 1


def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    # convert from Unicode to ASCII and hope we aren't
    # tossing some information
    return rc.encode('ascii', 'ignore')

def doParseAsList(xml):
    companies = []
    dom = minidom.parseString(xml)

    entries = dom.getElementsByTagName("entry")
    print "Number of entries: %d" % len(entries)
    for entry in entries:
        nodes = entry.getElementsByTagName("text")[0]
        text = getText(nodes.childNodes)
        companies.append(text)
    return companies

# try and figure out the various parts
# in the text, this is the dumb version
"""
<text>Agilent Technologies Inc. (NYSE:A)
395 Page Mill Road
Palo Alto, CA 94306
(650) 752-5000
http://www.agilent.com

Employees: 41,000
Profile: http://biz.yahoo.com/p/a/a.html
</text>
"""
"""
Company
Symbol
Exchange
Address
Phone
Web
NumberOfEmployees
Profile
"""
#  Address could be split further, but can be tricky
# more screwy formats
# B.V.R. Technologies Ltd. (NasdaqSC:BVRT)http://www.bvrtech.com

# Make Patrick cringe ;-)
# even messier because I'm not using regular expressions
def textToDictionary(text):
    # need to extra the company name to use as
    # a key
    company = {}
    text = text.replace('<small>', '').replace('</small>', '').replace('<nobr>', '')
    text = escape(text)
    lines = text.splitlines()
    i = lines[0].rfind(' (')
    #name, stock = lines[0].split(' (')
    company['Company'] = lines[0][:i]
    stock = lines[0][i + 2:]

    # blank line tells us where the address, phone split is
    try:
        offset = lines.index('')
    except ValueError:
        offset = -1

    if stock.find(')http://') != -1:
        # screwy
        stock, web = stock.split('http://')
        company['Web'] = 'http://' + web
        if stock.find(':') != -1:
            #exchange, symbol = stock[:-1].split(':')
            exchange, symbol = stock[:-1].split(':')
            company['Symbol'] = symbol
            company['Exchange'] = exchange
        else:
            company['Symbol'] = stock[:-1]
    else:
        if stock.find(':') != -1:
            #exchange, symbol = stock[:-1].split(':')
            exchange, symbol = stock[:-1].split(':')
            # *** KEA TO DO
            # need to filter out <strong> </strong>
            # and &lt; &gt; ...
            company['Symbol'] = symbol
            company['Exchange'] = exchange
        else:
            company['Symbol'] = stock[:-1]
            
        if offset != -1:
            company['Address'] = "\n".join(lines[1:offset - 2])
            company['Web'] = lines[offset - 1]
            company['Phone'] = lines[offset - 2]


    employees = lines[-2]
    if employees.startswith('Employees:'):
        company['NumberOfEmployees'] = employees.split(': ')[-1]
    company['Profile'] = lines[-1].split(': ')[-1]
    #print company, "\n"
    return company

def doParseAsDictionary(xml):
    companies = []
    #companies = SortableList()
    dom = minidom.parseString(xml)

    entries = dom.getElementsByTagName("entry")
    print "Number of entries: %d" % len(entries)
    for entry in entries:
        nodes = entry.getElementsByTagName("text")[0]
        company = textToDictionary(getText(nodes.childNodes))
        #print company['Company']
        companies.append(company)
        #print company['Company']
    return companies

# expects a list of dictionaries
# the dictionaries can contain strings and ints
# this version just treats everything as a string
# I'm not sure whether the quoting is robust for
# fields that contain some combination of ' and/or "
def listToXML(records):
    text = '<?xml version="1.0" encoding="UTF-8"?>\n'
    #text = '<?xml version="1.0" encoding="iso-8859-1" ?>\n'
    text += '<records>\n'
    # it is faster to do a big join of lists
    # than to constantly create new huge strings
    recList = []
    for record in records:
        s = ''
        for key, value in record.items():
            value = value.replace('<nobr>', '')
            value = value.replace('</nobr>', '')
            value = value.replace('<small>', '')
            value = value.replace('</small>', '')
            value = escape(value)
            """
            value = value.replace('&', '&amp;')
            value = value.replace('<', '&lt;')
            value = value.replace('>', '&gt;')
            """
            s += """%s=%s """ % (key, repr(value))
        recList.append('    <rec ' + s + '></rec>')
    text += "\n".join(recList)
    text += '\n</records>\n'
    return text

def xmlToList(filename):
    print 'Loading XML...'
    fp = open(filename, 'rb')
    xml = fp.read()
    fp.close()

    print 'Parsing XML...'
    startTime = time.time()
    #companies = doParseAsList(xml)
    companies = doParseAsDictionary(xml)
    endTime = time.time()
    print "Parsing time: %d seconds" % round(endTime - startTime)

    baseDir = os.path.dirname(filename)
    base = os.path.basename(filename)
    base = os.path.splitext(base)[0]

    print 'Saving list...'
    fp = open(os.path.join(baseDir, base + '.txt'), 'wb')
    pprint.pprint(companies, fp)
    fp.close()

    print 'Saving pickle...'
    # do you actually need to open 'wb' or is 'w'
    # correct with pickles either ascii or binary?
    fp = open(os.path.join(baseDir, base + '.pickle'), 'wb')
    # this ends up leaving a reference to SortableList
    # if companies = SortableList[]
    # is used above
    #cPickle.dump(companies, fp, SAVEBINARY)
    ##records = []
    ##for r in companies:
    ##    records.append(r)
    ##cPickle.dump(records, fp, SAVEBINARY)
    #cPickle.dump(companies.data, fp, SAVEBINARY)
    cPickle.dump(companies, fp, SAVEBINARY)
    fp.close()

    print 'Saving recs XML...'
    text = listToXML(companies)
    fp = open(os.path.join(baseDir, base + '-recs.xml'), 'w')
    fp.write(text)
    fp.close()

def downloadCompaniesXML():
    url = COMPANIES_URL
    print 'Downloading XML...'
    fp = urllib.urlopen(url)
    xml = fp.read()
    fp.close()

    print 'Saving XML...'
    fp = open(XMLFILENAME, 'wb')
    fp.write(xml)
    fp.close()

def buildTextAndPickleFiles():
    if not os.path.exists(XMLFILENAME):
        downloadCompaniesXML()
    
    startTime = time.time()
    xmlToList(XMLFILENAME)
    endTime = time.time()
    print "Total Processing time: %d seconds" % round(endTime - startTime)

if __name__ == '__main__':
    buildTextAndPickleFiles()
