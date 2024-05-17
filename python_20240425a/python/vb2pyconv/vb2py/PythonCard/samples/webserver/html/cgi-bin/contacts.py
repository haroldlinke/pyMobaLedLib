#!/usr/bin/python

import os, sys
import cgi
from PythonCard import util

DATA_FILE = ["..", "..", "addresses", "data.txt"]
FIELD_ORDER = ['Name', 'Company', 'Street', 'State', 'Zip', 
               'Phone1', 'Phone2', 'Phone3', 'Phone4', 'Notes']

class Document:
    def __init__(self, filename):
        self.current = -1
        #self.fieldNames = self.getFieldNames()
        if filename is None:
            self.records = []
        else:
            self.filename = filename
            self.openFile(filename)

    def openFile(self, filename):
        self.records = []
        self.filename = filename
        try:
            if os.path.exists(filename):
                addresses = util.readAndEvalFile(filename)
            for c in addresses:
                self.records.append(c)
            if self.current == -1 and len(self.records) > 0:
                #self.displayRecord(0)
                pass
        except Exception, msg:
            pass

    def findRecords(self, fields, value):
        results = []
        for record in self.records:
            for field in fields:
                if record[field].lower().find(value) != -1:
                    results.append(record)
                    continue
        return results


# probably want to stick this in a table
def printRecord(record):
    #keys = record.keys()
    #keys.sort()
    #for k in keys:
    for k in FIELD_ORDER:
        # on the off chance the field doesn't exist in the record
        # use try/except
        try:
            s = record[k]
            if s == '':
                # skip empty fields
                continue
            s = s.replace('\n\n', '<P>')
            s = s.replace('\n', '<BR>')
            print "<b>%s:</b> %s<br>" % (k, s)
        except Exception, msg:
            pass
    print "<hr>"

path = os.sep.join(DATA_FILE)
document = Document(path)

form = cgi.FieldStorage()
name = form['name'].value.lower()

results = document.findRecords(['Name', 'Company'], name)

print "Content-type: text/html\r\n\r\n",
print '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
print "<html><body>"

# change this so the CGI is also the form
print "Search for %s<hr>" % name
#print "Path: %s<br>" % os.path.abspath(path)
#print "exists: %s<br>" % str(os.path.exists(path))
for record in results:
    printRecord(record)

#print "</pre>"
print "</body></html>"
