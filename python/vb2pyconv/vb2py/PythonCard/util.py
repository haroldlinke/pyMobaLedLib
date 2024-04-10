"""
__version__ = "$Revision: 1.39 $"
__date__ = "$Date: 2006/05/18 21:11:49 $"
"""

import os
import sys
import imp
import re
import fnmatch
from functools import reduce

# Thomas Heller's function for determining
# if a module is running standalone
def main_is_frozen():
    if sys.platform == 'darwin':
        # this is a temporary hack for bundlebuilder
        return not (sys.executable == '/System/Library/Frameworks/Python.framework/Versions/2.3/Resources/Python.app/Contents/MacOS/Python' or \
                    sys.executable == '/Library/Frameworks/Python.framework/Versions/2.4/Resources/Python.app/Contents/MacOS/Python' or \
                    sys.executable == '/Library/Frameworks/Python.framework/Versions/2.5/Resources/Python.app/Contents/MacOS/Python')
    else:
        return (hasattr(sys, "frozen") or # new py2exe, McMillan
                hasattr(sys, "importers") # old py2exe
                or imp.is_frozen("__main__")) # tools/freeze, cx_freeze

def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(sys.argv[0])

# this is how I expected os.path.dirname to work
# it might be better to name this directoryName instead?!
def dirname(path):
    if os.path.isdir(path):
        return path
    else:
        return os.path.split(path)[0]

def readAndEvalFile(filename):
    f = open(filename)
    # KEA 2004-09-11
    # this should be a cleaner way of changing line endings
    # that works for the Mac (\r) as well as Windows (\r\n) line endings
    # but just in case this breaks something I'll leave the
    # old way commented out
    #txt = f.read().replace('\r\n','\n')
    txt = '\n'.join(f.read().splitlines())
    f.close()
    return eval(txt, globals())

def findString(pattern, text, caseSensitive=0, wholeWordsOnly=0):
    """
    search for pattern in text and return the offset
    of the first match or -1 if the text is not found
    """
    if wholeWordsOnly or not caseSensitive:
        # we could probably just always use
        # a regular expression, but I'm guessing
        # that string find() is quicker
        if wholeWordsOnly:
            pattern = r'\b' + pattern + r'\b'
        if caseSensitive:
            p = re.compile(pattern)
        else:
            p = re.compile(pattern, re.IGNORECASE)
        match = p.search(text)
        if match is None:
            return -1
        else:
            return match.start()
    else:
        return text.find(pattern)

# original function by Steve Purcell 
def findnth(s, substr, n):
    """find the nth occurance of substr in s
    
    return the offset"""
    offset = -1
    for i in range(n):
        offset = s.find(substr, offset+1)
        if offset == -1: break
    return offset

# KEA 2002-01-16
# we may switch to the findnth function below
# I have tested it for large values of n yet
"""
# original by Mark Pilgrim and Alex Martelli
def findnth(theString, searchString, n):
    pieces = theString.split(searchString, n)
    # print 'O',pieces,len(pieces),n+1
    if len(pieces) != n+1: return -1
    # print 'O',len(theString), len(pieces[n]), len(searchString)
    return len(theString)-len(pieces[n])-len(searchString)
"""

def normalizeEOL(text):
    """Return text with line endings replaced by \n."""
    #return text.replace('\r\n', '\n').replace('\r', '\n')
    return '\n'.join(text.splitlines())

# KEA doc handling adapted from python_docs 
# method in IDLE EditorWindow.py

def documentationURL(filename):
    fn = os.path.dirname(__file__)
    if isinstance(filename, str):
        url = "http://pythoncard.sourceforge.net/" + filename
        fn = os.path.join(fn, "docs", "html", filename)
    else:
        url = "http://pythoncard.sourceforge.net/" + "/".join(filename)
        fn = os.path.join(fn, "docs", "html", os.sep.join(filename)) 
    fn = os.path.normpath(fn)
    if os.path.isfile(fn):
        if sys.platform == 'darwin':
            # webbrowser on Mac OS X likes a file: prefix
            fn = 'file:' + fn
        return fn
    else:
        return url

def dirwalk(dir, patterns=['*'], recurse=1):
    """walk a directory tree, using a generator
    matching filenames with the patterns list
    based on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/105873"""
    for f in os.listdir(dir):
        fullpath = os.path.join(dir,f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            if recurse:
                for x in dirwalk(fullpath, patterns, recurse):  # recurse into subdir
                    yield x
        else:
            for pattern in patterns:
                if fnmatch.fnmatch(f, pattern):
                    yield fullpath
                    break

def wordwrap(text, width):
    """word-wrap function that preserves line breaks and spaces
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061"""
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line[line.rfind('\n')+1:])
                         + len(word.split('\n')[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

def caseinsensitive_sort(strList):
    """case-insensitive string comparison sort
    doesn't do locale-specific compare
    though that would be a nice addition
    usage: strList = caseinsensitive_sort(strList)"""

    tuplesList = [(x.lower(), x) for x in strList]
    tuplesList.sort()
    return [x[1] for x in tuplesList]

# this is similar to the function above
# but is used for sorting a list of dictionaries
# by a particular key
# it is used by the flatfileDatabase.py module
# records missing the name field will end up
# ahead of records that do
def caseinsensitive_listKeySort(recs, name):
    tupleList = [(recs[i].get(name, '').lower(), i) for i in range(len(recs))]
    tupleList.sort()
    return [recs[i] for dummy, i in tupleList]


# adapted from John Bair's Xml2Obj cookbook recipe
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/149368

from xml.parsers import expat

class Element:
    'A parsed XML element'
    def __init__(self,name,attributes):
        'Element constructor'
        # The element's tag name
        self.name = name
        # The element's attribute dictionary
        self.attributes = attributes
        # The element's cdata
        self.cdata = ''
        # The element's child element list (sequence)
        self.children = []
        
    def AddChild(self,element):
        'Add a reference to a child element'
        self.children.append(element)
        
    def getAttribute(self,key):
        'Get an attribute value'
        return self.attributes.get(key)
        #return unicode.encode(self.attributes.get(key))
    
    def getData(self):
        'Get the cdata'
        return self.cdata
        
    def getElements(self,name=''):
        'Get a list of child elements'
        #If no tag name is specified, return the all children
        if not name:
            return self.children
        else:
            # else return only those children with a matching tag name
            elements = []
            for element in self.children:
                if element.name == name:
                    elements.append(element)
            return elements

class Xml2Obj:
    'XML to Object'
    def __init__(self):
        self.root = None
        self.nodeStack = []
        
    def StartElement(self,name,attributes):
        'SAX start element even handler'
        # Instantiate an Element object
        element = Element(name.encode(),attributes)
        
        # Push element onto the stack and make it a child of parent
        if len(self.nodeStack) > 0:
            parent = self.nodeStack[-1]
            parent.AddChild(element)
        else:
            self.root = element
        self.nodeStack.append(element)
        
    def EndElement(self,name):
        'SAX end element event handler'
        self.nodeStack = self.nodeStack[:-1]

    def CharacterData(self,data):
        'SAX character data event handler'
        if data.strip():
            data = data.encode()
            element = self.nodeStack[-1]
            element.cdata += data
            return

    def Parse(self,filename):
        # Create a SAX parser
        Parser = expat.ParserCreate()

        # SAX event handlers
        Parser.StartElementHandler = self.StartElement
        Parser.EndElementHandler = self.EndElement
        Parser.CharacterDataHandler = self.CharacterData

        # Parse the XML File
        fp = open(filename)
        data = fp.read()
        fp.close()
        ParserStatus = Parser.Parse(data, 1)
        
        return self.root

def XmlToListOfDictionaries(filename):
    parser = Xml2Obj()
    element = parser.Parse(filename)
    return [rec.attributes for rec in element.getElements()]


# KEA 2003-07-02
# this will become the generalized script launching function after
# release 0.7.1
# currently it is only used by the slideshow sample

def getCommandLineArgs(cmdLineArgs):
    args = []
    if cmdLineArgs['otherargs'] != '':
        args.append(cmdLineArgs['otherargs'])
    if cmdLineArgs['debugmenu']:
        args.append('-d')
    if cmdLineArgs['logging']:
        args.append('-l')
    if cmdLineArgs['messagewatcher']:
        args.append('-m')
    if cmdLineArgs['namespaceviewer']:
        args.append('-n')
    if cmdLineArgs['propertyeditor']:
        args.append('-p')
    if cmdLineArgs['shell']:
        args.append('-s')
    return args

def runScript(filename, args=' ', requireConsole=False, useInterpreter=False):
    if filename is None:
        # KEA 2002-03-25
        # should probably present an error dialog here
        return

    filename = '"' + filename + '"'

    if useInterpreter:
        interp = ' -i '
    else:
        interp = ' '
        
    if sys.platform.startswith('win'):
        python = sys.executable
        if ' ' in python:
            pythonQuoted = '"' + python + '"'
        else:
            pythonQuoted = python
        if useInterpreter and os.name != 'nt':
            os.spawnv(os.P_NOWAIT, python, [pythonQuoted, interp, filename, args])
        else:
            os.spawnv(os.P_NOWAIT, python, [pythonQuoted, interp, filename, args])
    else:
        if ' ' in sys.executable:
            python = '"' + sys.executable + '"'
        else:
            python = sys.executable
        os.system(python + interp + filename + ' ' + args + ' &')

# KEA 2004-04-25
# let's finally figure out all the quoting rules for 0.8
# whether we need to run as a background process, whatever
# and establish a generalized launch routine
# args should probably be passed in as a list
# from samples.py
# on_launch_command
# 
# also see codeEditor, findfiles, and resourceEditor script launching
# slideshow for example usage of runScript above
# runScript should handle any required quoting rather than the calling script
#
# this is the perfect kind of thing to have a unit test for to try various
# pathnames with spaces, characters that need to be quoted a specific way,
# whether args need to be quoted, etc.
"""
        # KEA 2002-04-28
        # os.spawnv probably works on all platforms
        # and regardless of the quoting needs for paths with
        # and without spaces, but each platform is separate
        # below until that is confirmed
        if ' ' in filename:
            filename = '"' + filename + '"'
        python = sys.executable
        if ' ' in python:
            pythonQuoted = '"' + python + '"'
        else:
            pythonQuoted = python
        os.spawnv(os.P_NOWAIT, python, [pythonQuoted, filename] + args)
"""


def colorFromString(s):
    s = s.strip()
    if s == '':
        color = None
    elif (s.startswith('(') and s.endswith(')')) or (s.startswith('[') and s.endswith(']')):
        # assume a color tuple
        try:
            r, g, b = s[1:-1].split(',')
            color = (int(r), int(g), int(b))
        except:
            color = None
    else:
        # assume color string such as blue or #0000FF
        # we could do further verification here
        # to avoid an exception being thrown when color is set
        color = s
    return color

# compute relative path
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/208993

def pathsplit(p, rest=[]):
    (h,t) = os.path.split(p)
    if len(h) < 1: return [t]+rest
    if len(t) < 1: return [h]+rest
    return pathsplit(h,[t]+rest)

def commonpath(l1, l2, common=[]):
    if len(l1) < 1: return (common, l1, l2)
    if len(l2) < 1: return (common, l1, l2)
    if l1[0] != l2[0]: return (common, l1, l2)
    return commonpath(l1[1:], l2[1:], common+[l1[0]])

# KEA 2004-08-24
# I made a few changes below to get rid of redundant leading ..
def relativePath(p1, p2):
    # AGT 2005-05-10
    # Protect against the case where one of the parameters is 'None'
    #  e.g. in the resourceEditor before the resource file has been saved
    if not p1: p1 = ''
    if not p2: p2 = ''
    (common,l1,l2) = commonpath(pathsplit(p1), pathsplit(p2))
    p = []
    if len(l1) > 0:
        p = ['../' * len(l1)]
    p = p + l2
    path = os.path.join(*p)
    # KEA 2004-08-24
    # this isn't really the right place to get rid of Windows-specific
    # path stuff, but I don't want to have to stick this code everywhere
    # I call relativePath, so let's see if this causes a problem
    # we want all paths to be Unix-like with forward slashes
    path = path.replace('\\\\', '/').replace('\\', '/')
    if path.startswith('../'):
        path = path[3:]
    return path

# platform independent way of getting highest
# resolution for doing timing
if sys.platform[:3] == 'win':
    # time.clock has better resolution on Windows
    from time import clock
    time = clock
else:
    # but time.time is better on *nix
    from time import time
