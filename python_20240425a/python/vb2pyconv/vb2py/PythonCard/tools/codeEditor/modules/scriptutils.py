
"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2002/12/27 17:26:40 $"

modified version of Pythonwin scriptutils.py
"""

import os, sys
import traceback

# KEA 2002-05-08
# should probably refactor this so we're not passing around the background

def CheckFile(background, pathName):
    what = "check"
    background.statusBar.text = what.capitalize()+'ing module...'
    try:
        f = open(pathName)
    except IOError, details:
        background.statusBar.text = "Cant open file '%s' - %s" % (pathName, details)
        return
    try:
        code = f.read() + "\n"
    finally:
        f.close()
    try:
        codeObj = compile(code, pathName,'exec')
        if RunTabNanny(background, pathName):
            #win32ui.SetStatusText("Python and the TabNanny successfully checked the file '"+os.path.basename(pathName)+"'")
            background.statusBar.text = "Python and the TabNanny successfully checked the file '"+os.path.basename(pathName)+"'"
    except SyntaxError:
        #background.statusBar.text = 'SyntaxError'
        _HandlePythonFailure(background, what, pathName)

def RunTabNanny(background, filename):
    import cStringIO
    import tabnanny
        
    # Capture the tab-nanny output
    newout = cStringIO.StringIO()
    old_out = sys.stderr, sys.stdout
    sys.stderr = sys.stdout = newout
    try:
        tabnanny.check(filename)
    finally:
        # Restore output
        sys.stderr, sys.stdout = old_out
    data = newout.getvalue()
    if data:
        try:
            lineno = data.split()[1]
            lineno = int(lineno)
            _JumpToPosition(background, filename, lineno)
            try: # Try and display whitespace
                #GetActiveEditControl().SCISetViewWS(1)
                pass
            except:
                pass
            #win32ui.SetStatusText("The TabNanny found trouble at line %d" % lineno)
            background.statusBar.text = "The TabNanny found trouble at line %d" % lineno
        except (IndexError, TypeError, ValueError):
            background.statusBar.text = "The tab nanny complained, but I cant see where!"
            print data
        return 0
    return 1

def _JumpToPosition(background, fileName, lineno, col = 1):
    #JumpToDocument(fileName, lineno, col)
    #print fileName, lineno, col
    doc = background.components.document
    doc.GotoLine(lineno - 1)
    if col == 1:
        pos = doc.PositionFromLine(lineno - 1)
        doc.SetSelection(pos, doc.GetLineEndPosition(lineno - 1))
        doc.SetCurrentPos(pos)
    else:
        pos = doc.PositionFromLine(lineno - 1) + col - 1
        doc.SetSelection(pos, pos)
        doc.SetCurrentPos(pos)
    

def _HandlePythonFailure(background, what, syntaxErrorPathName = None):
    typ, details, tb = sys.exc_info()
    if typ == SyntaxError:
        try:
            msg, (fileName, line, col, text) = details
            if (not fileName or fileName =="<string>") and syntaxErrorPathName:
                fileName = syntaxErrorPathName
            _JumpToPosition(background, fileName, line, col)
        except (TypeError, ValueError):
            msg = str(details)
        #win32ui.SetStatusText('Failed to ' + what + ' - syntax error - %s' % msg)
        background.statusBar.text = 'Failed to ' + what + ' - syntax error - %s' % msg
    else:   
        traceback.print_exc()
        #win32ui.SetStatusText('Failed to ' + what + ' - ' + str(details) )
        # KEA 2002-06-03
        # this needs to be more robust, but it is better than nothing for
        # simple indentation errors
        #try:
        # see if we have something of the form
        # (line 10)
        # for an error message that indicates the line number
        # the proper solution is to probably get the line number from the
        # traceback stack frame but I don't know how to do that
        #print traceback.tb_lineno(tb)
        try:
            msg, (fileName, line, col, text) = details
            _JumpToPosition(background, fileName, line, col)
        except:
            pass
        background.statusBar.text = 'Failed to ' + what + ' - ' + str(details)
    tb = None # Clean up a cycle.

