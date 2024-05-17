
"""
__version__ = "$Revision: 1.12 $"
__date__ = "$Date: 2006/01/24 19:59:35 $"
"""

import os
import urllib
import zipfile

# EXAMPLE LIF FILE
"""
#Life 1.05
#D Acorn
#D The most vigorously growing 7-cell
#D "methuselah" pattern.  See also RABBITS.
#N
#P -3 -1
.*
...*
**..***
"""


def patternDimensions(patterns):
    # figure out the dimensions of the entire file
    left = 0
    top = 0
    right = 0
    bottom = 0
    for pattern in patterns:
        l, t = pattern['position']
        width, height = pattern['size']
        r = l + width
        b = t + height
        if l < left:
            left = l
        if t < top:
            top = t
        if r > right:
            right = r
        if b > bottom:
            bottom = b
    return left, top, right, bottom

def readLifeFile(path):
    # this could be changed to a user-defined dir
    # saved in a config
    description = ''
    # each pattern will consist of an x, y
    # offset
    patterns = []
    pattern = {}
    try:
        fp = open(path)
        data = fp.readlines()
        fp.close()
    except IOError:
        return None
    if data[0].strip() != '#Life 1.05':
        return None
    for line in data[1:]:
        s = line.strip()
        if s == '':
            pass
        elif s.startswith('#N') or s.startswith('#R'):
            # assume Conway (Normal) rules for now
            pass
        elif s.startswith('#D'):
            if description == '':
                description = s[3:].strip()
            else:
                description += "\n" + s[3:].strip()
        elif s.startswith('#P'):
            # beginning of a cell block
            if pattern != {}:
                pattern['size'] = (width, height)
                patterns.append(pattern.copy())
            x, y = s[3:].split(' ')
            width = 0
            height = 0
            pattern = {}
            pattern['position'] = (int(x), int(y))
            pattern['rows'] = []
        else:
            pattern['rows'].append(s)
            if len(s) > width:
                width = len(s)
            height += 1
    if pattern != {}:
        pattern['size'] = (width, height)
        patterns.append(pattern.copy())
    left, top, right, bottom = patternDimensions(patterns)
    #print "bounds", left, top, right, bottom
    #print "size", abs(right - left), abs(bottom - top)
    return description, patterns, (left, top), (abs(right - left), abs(bottom - top))

"""
test tube baby
 **....** (p2)
 *.*..*.*
 ..*..*..
 ..*..*..
 ...**...
"""
# be able to copy and paste from the glossary
# process each line
# strip off any leading and trailing spaces
# only lines that begin with a . or * are
# part of the pattern
# blank lines are ignored
# other lines are added to the description
# a split is done on the lines to remove
# things like (p60) from the pattern
# this will not handle patterns larger
# than a block because there is no support
# for (x, y) offsets
def translateClipboardPattern(data):
    descriptionStarted = 0
    description = ''
    patterns = []
    pattern = {}
    for line in data.splitlines():
        s = line.strip()
        if s == '':
            pass
        elif not s[0] in ('.', '*', 'O'):
            # add line to the description
            # by supporting the capital O
            # as a symbol we can get
            # thrown off by a line in
            # the description that starts with O
            # in which case the pattern will
            # get corrupted
            # of course it would be nice to think the clipboard
            # will just contain a pattern with no description
            # or just use . and *
            if description == '':
                description = s
            else:
                description += "\n" + s
        else:
            try:
                s, desc = s.split(' ')
                description += "\n" + desc
            except ValueError:
                # no description
                pass
            # beginning of a cell block
            if pattern == {}:
                width = 0
                height = 0
                # just use 0, 0 for now
                # offset based on size later
                pattern['position'] = (0, 0)
                pattern['rows'] = []
            pattern['rows'].append(s)
            if len(s) > width:
                width = len(s)
            height += 1
    if pattern != {}:
        pattern['size'] = (width, height)
        patterns.append(pattern.copy())

    left, top, right, bottom = patternDimensions(patterns)
    #print "bounds", left, top, right, bottom
    #print "size", abs(right - left), abs(bottom - top)
    return description, patterns, (left, top), (abs(right - left), abs(bottom - top))


def neighborsTuple(col, row):
    # return a tuple of neighbor tuples
    # this no longer wraps in a torus
    prevRow = row - 1
    nextRow = row + 1
    prevCol = col - 1
    nextCol = col + 1
    return ((prevCol, prevRow), (col, prevRow), (nextCol, prevRow),
            (prevCol, row), (nextCol, row),
            (prevCol, nextRow), (col, nextRow), (nextCol, nextRow))

def placePattern(grid, colOffset, rowOffset, pattern):
    row = rowOffset
    # pattern is a list of strings
    for line in pattern:
        col = colOffset
        for c in line:
            if c in ('*', 'O'):
                grid[(col, row)] = 1
                for neighbor in neighborsTuple(col, row):
                    grid.setdefault(neighbor, 0)
            else:
                grid[(col, row)] = 0
            col += 1
        row += 1
    return grid


def savefile(path, data):
    try:
        f = open(path, "w")
        f.write(data)
        f.close()
    except IOError, msg:
        print "failed to save %s: %s", path, str(msg)

# KEA 2004-03-18
# these functions could be changed to use a pythoncard_config/life dir
# and automatically call them when the life.py sample starts up
# making sure to check whether the zip files already exist before
# downloading another copy

def getLexicon(path):    
    filename = 'lexicon.txt'
    zipname = 'lex_asc.zip'
    zippath = os.path.join(path, zipname)
    url = 'http://www.argentum.freeserve.co.uk/' + zipname
    urllib.urlretrieve(url, zippath)
    zz = zipfile.ZipFile(zippath)
    savefile(os.path.join(path, filename), zz.read(filename))

def getPatterns(path):
    zipname = 'lifep.zip'
    zippath = os.path.join(path, zipname)
    url = 'http://www.ibiblio.org/lifepatterns/' + zipname
    urllib.urlretrieve(url, zippath)
    zz = zipfile.ZipFile(zippath)
    for name in zz.namelist():
        savefile(os.path.join(path, 'patterns', name), zz.read(name))
