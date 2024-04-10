#!/usr/bin/python
print "Content-type: text/html\r\n\r\n",
print '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
print "<html><body>"
print "<pre>"
import os, sys
from cgi import escape
print "<strong>Python %s</strong>" % sys.version
keys = os.environ.keys()
keys.sort()
for k in keys:
    print "%s\t%s" % (escape(k), escape(os.environ[k]))
print "</pre>"
print "</body></html>"
