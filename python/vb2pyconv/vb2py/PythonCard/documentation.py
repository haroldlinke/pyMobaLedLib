
"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2005/12/29 20:48:43 $"
"""

# the start of some functions to help generate documentation for PythonCard

import inspect, os, time, inspect
import wx
from PythonCard import dialog


# KEA 2002-05-07
# some methods to build up component documentation
# using the built-in component specs

def getAttributesList(attributes):
    names = [a for a in attributes]
    names.sort()
    listX = []
    for n in names:
        if attributes[n].hasDefaultValueList():
            listX.append([n, attributes[n].getDefaultValueList()])
        else:
            value = attributes[n].getDefaultValue()
            if value == '':
                value = "''"
            listX.append([n, value])
    return listX

def getEventsList(objspec):
    events = [e.name for e in objspec.getEvents()]
    events.sort()
    return events

def getMethodsList(obj):
    listX = []
    methods = inspect.getmembers(obj, inspect.ismethod)
    for m in methods:
        if m[0][0] in "abcdefghijklmnopqrstuvwxyz":
            listX.append(m[0])
    return listX


def dumpDocs(self):
    result = dialog.directoryDialog(None, 'Create documention in:', '')
    if result.accepted:
        widgetsDir = result.path
        dumpBackgroundDocs(self, widgetsDir)
        # self.dumpComponentDocs(widgetsDir)

def dumpBackgroundDocs(self, widgetsDir):
    w = self
    name = w.__class__.__name__
    objspec = w._spec

    doc = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'
    doc += '<html>\n<head><title>%s</title></head><body>\n' % (name + ': PythonCard Background')
    doc += '<h1>Background: %s</h1>' % name

    doc += '\n<img src="%s"><BR>\n' % ('images/' + name + '.png')

    doc += '\n<h2>Required Attributes</h2>\n'
    doc += '<table border="1">\n'
    doc += '<tr><td><b>Name<b></td><td><b>Default value</b></td></tr>\n'
    for a in getAttributesList(objspec.getRequiredAttributes()):
        doc += "<tr><td>%s</td><td>%s</td></tr>\n" % (a[0], a[1])
    doc += '</table>'

    doc += '\n\n<h2>Optional Attributes</h2>\n'
    doc += '<table border="1">\n'
    doc += '<tr><td><b>Name<b></td><td><b>Default value</b></td></tr>\n'
    for a in getAttributesList(objspec.getOptionalAttributes()):
        doc += "<tr><td>%s</td><td>%s</td></tr>\n" % (a[0], a[1])
    doc += '</table>'

    # KEA 2005-12-29
    # Background spec still using default in spec.py so doesn't have
    # events defined like it should
##        doc += '\n\n<h2>Events:</h2>\n'
##        doc += '<table border="1">\n'
##        for e in getEventsList(objspec):
##            doc += "<tr><td>%s</td></tr>\n" % e
##        doc += '</table>'

    doc += '\n\n<h2>Methods:</h2>\n'
    doc += '<table border="1">\n'
    td = '<td><b>%s</b></td>' * 4
    tr = '<tr>' + td + '</tr>\n'
    doc += tr % ('method', 'args', 'doc string', 'comments')
    for e in getMethodsList(w):
        method = getattr(w, e)
        docstring = inspect.getdoc(method)
        if docstring is None:
            docstring = "&nbsp;"
        comments = inspect.getcomments(method)
        if comments is None:
            comments = "&nbsp;"
        #source = inspect.getcomments(method)
        argspec = inspect.getargspec(method)
        formattedargs = inspect.formatargspec(argspec[0], argspec[1], argspec[2], argspec[3])
        doc += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % \
            (e, formattedargs, docstring, comments)
    doc += '</table>'
    
    # write out the documentation for the component
    doc += '\n<hr><img src="http://sourceforge.net/sflogo.php?group_id=19015&type=1" width="88" height="31" border="0" alt="SourceForge Logo">'
    doc += '\n<p>Last updated: %s</p>' % time.strftime("%B %d, %Y")
    doc += '\n</body>\n</html>'
    filename = name + '.html'
    path = os.path.join(widgetsDir, filename)
    f = open(path, 'w')
    f.write(doc)
    f.close()


def dumpComponentDocs(self, widgetsDir):
    widgetsDir = os.path.join(widgetsDir, 'components')
    if not os.path.exists(widgetsDir):
        os.mkdir(widgetsDir)
    imagesDir = os.path.join(widgetsDir, 'images')
    if not os.path.exists(imagesDir):
        os.mkdir(imagesDir)

    toc = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'
    toc += '<html>\n<head><title>%s</title></head><body>\n' % 'PythonCard Components'
    toc += '<h1>PythonCard Components</h1>\n'
    componentsList = []

    for w in self.components.values():
        if w.__class__.__name__.startswith(w.name[3:]):
            # document each widget
            name = w.__class__.__name__
            objspec = w._spec

            doc = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'
            doc += '<html>\n<head><title>%s</title></head><body>\n' % (name + ': PythonCard component')
            doc += '<h1>Component: %s</h1>' % name

            doc += '\n<img src="%s"><BR>\n' % ('images/' + name + '.png')

            doc += '\n<h2>Required Attributes</h2>\n'
            doc += '<table border="1">\n'
            doc += '<tr><td><b>Name<b></td><td><b>Default value</b></td></tr>\n'
            for a in getAttributesList(objspec.getRequiredAttributes()):
                doc += "<tr><td>%s</td><td>%s</td></tr>\n" % (a[0], a[1])
            doc += '</table>'

            doc += '\n\n<h2>Optional Attributes</h2>\n'
            doc += '<table border="1">\n'
            doc += '<tr><td><b>Name<b></td><td><b>Default value</b></td></tr>\n'
            for a in getAttributesList(objspec.getOptionalAttributes()):
                doc += "<tr><td>%s</td><td>%s</td></tr>\n" % (a[0], a[1])
            doc += '</table>'

            doc += '\n\n<h2>Events:</h2>\n'
            doc += '<table border="1">\n'
            for e in getEventsList(objspec):
                doc += "<tr><td>%s</td></tr>\n" % e
            doc += '</table>'

            doc += '\n\n<h2>Methods:</h2>\n'
            doc += '<table border="1">\n'
            td = '<td><b>%s</b></td>' * 4
            tr = '<tr>' + td + '</tr>\n'
            doc += tr % ('method', 'args', 'doc string', 'comments')
            for e in getMethodsList(w):
                method = getattr(w, e)
                docstring = inspect.getdoc(method)
                if docstring is None:
                    docstring = "&nbsp;"
                comments = inspect.getcomments(method)
                if comments is None:
                    comments = "&nbsp;"
                #source = inspect.getcomments(method)
                argspec = inspect.getargspec(method)
                formattedargs = inspect.formatargspec(argspec[0], argspec[1], argspec[2], argspec[3])
                doc += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % \
                    (e, formattedargs, docstring, comments)
            doc += '</table>'

            # need to decide what we want to dump from the methods
            # we probably don't want to dump everything including
            # wxPython methods, so this is where we need to decide
            # on the case of the first letter of the method
            # whatever is done here should be the same thing used
            # to display methods in the shell
            # arg lists and tooltips (docstrings) will be used here too

            # write out the documentation for the component
            doc += '\n<hr><img src="http://sourceforge.net/sflogo.php?group_id=19015&type=1" width="88" height="31" border="0" alt="SourceForge Logo">'
            doc += '\n<p>Last updated: %s</p>' % time.strftime("%B %d, %Y")
            doc += '\n</body>\n</html>'
            filename = name + '.html'
            path = os.path.join(widgetsDir, filename)
            f = open(path, 'w')
            f.write(doc)
            f.close()

            # create an image using the actual component
            # on screen
            # comment this out once you have created the images
            # you want
            bmp = wx.EmptyBitmap(w.size[0], w.size[1])
            memdc = wx.MemoryDC()
            memdc.SelectObject(bmp)
            dc = wx.WindowDC(w)
            memdc.BlitPointSize((0, 0), w.size, dc, (0, 0))
            imgfilename = os.path.join(imagesDir, name + '.png')
            bmp.SaveFile(imgfilename, wx.BITMAP_TYPE_PNG)
            dc = None
            memdc.SelectObject(wx.NullBitmap)
            memdc = None
            bmp = None

            componentsList.append('<a href="%s">%s</a><br>\n' % (filename, name))

    # now create the table of contents, index.html
    componentsList.sort()
    for c in componentsList:
        toc += c
    toc += '\n<hr><img src="http://sourceforge.net/sflogo.php?group_id=19015&type=1" width="88" height="31" border="0" alt="SourceForge Logo">'
    toc += '\n</body>\n</html>'
    filename = os.path.join(widgetsDir, 'index.html')
    f = open(filename, 'w')
    f.write(toc)
    f.close()
