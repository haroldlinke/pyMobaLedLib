#!/usr/bin/python

"""
A fairly simple implementation of Conway's Game of Life.
"""
__version__ = "$Revision: 1.19 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"

from PythonCard import model, util
import wx

import os

from util import readLifeFile, translateClipboardPattern

"""
:101: (p5)  Found by Achim Flammenkamp in August 1994.  The name was
   suggested by Bill Gosper, noting that the phase shown below displays
   the period in binary.
    ....**......**....
    ...*.*......*.*...
    ...*..........*...
    **.*..........*.**
    **.*.*..**..*.*.**
    ...*.*.*..*.*.*...
    ...*.*.*..*.*.*...
    **.*.*..**..*.*.**
    **.*..........*.**
    ...*..........*...
    ...*.*......*.*...
    ....**......**....

"""

def readLexiconFile(path):
    try:
        fp = open(path)
        data = fp.readlines()
        fp.close()
    except IOError:
        return None
    lexicon = {}
    # first collect the header
    # up to the first row of
    # ------
    # then collect the definitions and patterns
    # and finally the bibliography after
    # the second row of
    # -----
    inIntroduction = 1
    inBibliography = 0
    bibliography = ''
    introduction = ''
    term = ''
    for line in data:
        stripped = line.strip()
        if inIntroduction:
            if line.startswith('-----'):
                inIntroduction = 0
            else:
                introduction += line
        elif inBibliography:
            bibliography += line
        else:
            if line.startswith('-----'):
                inBibliography = 1
            else:
                # collecting an entry
                if stripped == '':
                    continue
                elif stripped.startswith(':'):
                    # start of new term
                    if term != '':
                        lexicon[term] = (description, pattern)
                    offset = stripped.find(':', 1)
                    term = stripped[1:offset]
                    description = stripped[offset + 1:].lstrip()
                    #crud, term, description = stripped.split(':')
                    pattern = ''
                elif stripped.startswith('.') or stripped.startswith('*'):
                    pattern += stripped + '\n'
                else:
                    if line.startswith('    '):
                        description += '\n\n' + stripped
                    else:
                        description += '\n' + stripped
    if term != '':
        lexicon[term] = (description, pattern)
    lexicon['INTRODUCTION'] = (introduction, '')
    lexicon['BIBLIOGRAPHY'] = (bibliography, '')
    #print len(lexicon)
    return lexicon

class Lexicon(model.Background):

    def on_initialize(self, event):
        #self.initSizers()
        self.components.fldDescription.lineNumbersVisible = False
        self.components.fldDescription.setEditorStyle('text')
        self.lexiconPath = self.getParent().lexiconPath
        self.populatePatternsList()

    def populatePatternsList(self):
        self.lexicon = readLexiconFile(self.lexiconPath)
        if self.lexicon is None:
            self.getParent().menuBar.setEnabled('menuAutomataLexicon', False)
            self.visible = False
        else:
            items = self.lexicon.keys()
            items = util.caseinsensitive_sort(items)
            self.components.lstPatterns.items = items
            self.components.lstPatterns.selection = 0
            # now simulate the user doing a selection
            self.on_lstPatterns_select(None)
            self.getParent().menuBar.setEnabled('menuAutomataLexicon', True)
            self.visible = True

    def loadPattern(self, name):
        #filename = name + '.lif'
        #path = os.path.join(self.application.applicationDirectory, 'patterns', filename)
        description, patternString = self.lexicon[name]
        if patternString != '':
            crud, patterns, topLeft, size = translateClipboardPattern(patternString)
            #print "topLeft:", topLeft, "size", size
            self.getParent().initAndPlacePatterns(patterns, topLeft, size)

    def on_lstPatterns_select(self, event):
        name = self.components.lstPatterns.stringSelection
        description, patternString = self.lexicon[name]
        if patternString == '':
            self.components.fldDescription.text = description
            self.components.stcSize.text = ""
        else:
            crud, patterns, topLeft, size = translateClipboardPattern(patternString)
            self.components.fldDescription.text = description + "\n\n" + patternString
            self.components.stcSize.text = "Size: (%d, %d)" % size

    def on_btnLoad_mouseClick(self, event):
        self.loadPattern(self.components.lstPatterns.stringSelection)

    def on_lstPatterns_mouseDoubleClick(self, event):
        self.loadPattern(self.components.lstPatterns.stringSelection)

    def on_close(self, event):
        self.visible = False
