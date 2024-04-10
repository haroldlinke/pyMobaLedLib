#!/usr/bin/python
"""CGI wrapper for implementing an XML-RPC server

Any .py scripts in the WEBSERVICESDIR directory
(defined below) will be accessible via XML-RPC
by using the URL of this CGI script as the XML-RPC
server.

Example:
- This script is at http://diveintomark.org/cgi-bin/webservices.cgi
- sample.py is in WEBSERVICESDIR and contains this function:

def helloWorld():
  return "Hello World!"

- From the client, you would invoke it like this:

>>> import xmlrpclib
>>> server = xmlrpclib.Server('http://diveintomark.org/cgi-bin/webservices.cgi')
>>> server.sample.helloWorld()
'Hello World!'

The WEBSERVICESDIR can contain as many services as
you like, each in its own .py file.  The .py files
are imported like normal modules, so all the normal
Python tricks apply: you can have module-level globals,
or hide functions by naming them starting with "_".
"""

# KEA 2002-06-09
# I removed the $ $ below to preserve Mark's info
# when this file gets checked into cvs

__author__ = "Mark Pilgrim (f8dy@diveintomark.org)"
__version__ = "Revision: 1.1.1.1 "
__date__ = "Date: 2002/02/21 19:20:22 "
__copyright__ = "Copyright (c) 2002 Mark Pilgrim"
__license__ = "Python"

import os, sys
import xmlrpclib

# directory of web service-enabled scripts
#WEBSERVICESDIR = '../../../webservices/'
WEBSERVICESDIR = '..' + os.sep + 'webservices'

# maximum allowed length of XML-RPC request (in bytes)
MAXREQUESTLENGTH = 10000

def isAvailable(modulename):
    def getFullPath(filename):
        return os.path.join(WEBSERVICESDIR, filename)
    def isModuleOrFolder(filename):
        return os.path.isdir(filename) or os.path.splitext(filename)[1] == '.py'
    def stripName(filename):
        return os.path.splitext(os.path.split(filename)[1])[0]
    all = map(getFullPath, os.listdir(WEBSERVICESDIR))
    some = filter(isModuleOrFolder, all)
    stripped = map(stripName, some)
    return modulename in stripped

def dispatch(method, params):
    modulename, functionname = method.split('.', 1)
    if not isAvailable(modulename):
        raise ImportError, 'Requested service not found'
    sys.path.insert(0, WEBSERVICESDIR)
    m = __import__(modulename)
    result = apply(getattr(m, functionname), params)
    result = (result,)
    return result
    
def main():
    try:
        contentLength = int(os.environ["CONTENT_LENGTH"])
        if contentLength > MAXREQUESTLENGTH:
            raise ValueError, 'Request too large'
        data = sys.stdin.read(contentLength)
        params, method = xmlrpclib.loads(data)
        result = dispatch(method, params)
        response = xmlrpclib.dumps(result, methodresponse=1)
    except Exception, msg: # Should test for a particular Exception
        response = xmlrpclib.dumps(xmlrpclib.Fault(1, "%s: %s" % sys.exc_info()[:2]))
    print 'Content-type: text/xml'
    print 'Content-length: %s' % len(response)
    print
    print response
    
if __name__ == '__main__':
    main()
