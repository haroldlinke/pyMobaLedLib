"""System web service for meta-information about other available web services"""

# KEA 2002-06-09
# I removed the $ $ below to preserve Mark's info
# when this file gets checked into cvs

__author__ = "Mark Pilgrim (f8dy@diveintomark.org)"
__version__ = "Revision: 1.1.1.1 "
__date__ = "Date: 2002/02/21 19:20:22"
__copyright__ = "Copyright (c) 2002 Mark Pilgrim"
__license__ = "Python"

import inspect, os, sys

#WEBSERVICESDIR = '/home/f8dy/webservices/'
WEBSERVICESDIR = '..' + os.sep + 'webservices' + os.sep

def _getAvailableServices(dirname):
    path = os.path.abspath(os.path.split(dirname)[0])
    files = os.listdir(path)
    isService = lambda f: os.path.splitext(f)[1] == '.py'
    files = filter(isService, files)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    sys.path.insert(0, dirname)
    modules = map(__import__, moduleNames)
    return modules

def _getModuleInfo(module):
    info = {}
    for name, f in inspect.getmembers(module, inspect.isfunction):
        if name[0] != '_':
            info[name] = {"args":apply(inspect.formatargspec, inspect.getargspec(f)),
                          "doc":inspect.getdoc(f)}
    return info

def listMethods():
    rc = {}
    modules = _getAvailableServices(WEBSERVICESDIR)
    for module in modules:
        info = _getModuleInfo(module)
        for functionname, functioninfo in info.items():
            rc[module.__name__ + '.' + functionname + functioninfo['args']] = str(functioninfo['doc'])
    return rc

def _test():
    rc = listMethods()
    for desc, doc in rc.items():
        print desc
        print '  %s' % doc

if __name__ == '__main__':
    _test()
