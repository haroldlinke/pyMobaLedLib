"""
    MoinMoin - Python Source Parser

    KEA, modified for PythonCard to use wxSTC styles 2002-06-28
    
__version__ = "$Revision: 1.7 $"
__date__ = "$Date: 2004/04/25 15:23:45 $"

"""

# Imports
import cgi, sys, cStringIO
import keyword, token, tokenize

import os
from PythonCard import configuration, STCStyleEditor


cfg = STCStyleEditor.initFromConfig(configuration.getStyleConfigPath(), 'python')
# cfg is a big tuple
styles = cfg[3]
styleDict = {}

# build style dict based on given styles
for numStyle in styles:
    num, style = STCStyleEditor.parsePropLine(numStyle)
    attributes = style.split(',')
    for a in attributes:
        if a.startswith('fore:'):
            foreColor = a[a.find(':')+1:]
            styleDict[num] = foreColor
        else:
            if num not in styleDict:
                styleDict[num] = "#000000"


#############################################################################
### Python Source Parser (does Hilighting)
#############################################################################

_KEYWORD = token.NT_OFFSET + 1
_TEXT    = token.NT_OFFSET + 2

"""
_colors = {
    token.NUMBER:       '#0080C0',
    token.OP:           '#0000C0',
    token.STRING:       '#004080',
    tokenize.COMMENT:   '#008000',
    token.NAME:         '#000000',
    token.ERRORTOKEN:   '#FF8080',
    _KEYWORD:           '#C00000',
    _TEXT:              '#000000',
}
"""
_colors = {
    token.NUMBER:       styleDict[2],
    token.OP:           styleDict[10],
    token.STRING:       styleDict[3],
    tokenize.COMMENT:   styleDict[1],
    token.NAME:         styleDict[11],
    token.ERRORTOKEN:   '#FF8080',
    _KEYWORD:           styleDict[5],
    _TEXT:              styleDict[0],
}


class Parser:
    """ Send colored python source.
    """

    def __init__(self, raw, out = sys.stdout):
        """ Store the source text.
        """
        self.raw = raw.expandtabs().strip()
        self.out = out

    def format(self, formatter, form):
        """ Parse and send the colored source.
        """
        # store line offsets in self.lines
        self.lines = [0, 0]
        pos = 0
        while 1:
            pos = self.raw.find('\n', pos) + 1
            if not pos: break
            self.lines.append(pos)
        self.lines.append(len(self.raw))

        # parse the source and write it
        self.pos = 0
        text = cStringIO.StringIO(self.raw)
        self.out.write('<pre><font face="Lucida,Courier New">')
        try:
            tokenize.tokenize(text.readline, self)
        except tokenize.TokenError, ex:
            msg = ex[0]
            line = ex[1][0]
            self.out.write("<h3>ERROR: %s</h3>%s\n" % (
                msg, self.raw[self.lines[line]:]))
        self.out.write('</font></pre>')

    def __call__(self, toktype, toktext, (srow,scol), (erow,ecol), line):
        """ Token handler.
        """
        if 0:
            print "type", toktype, token.tok_name[toktype], "text", toktext,
            print "start", srow,scol, "end", erow,ecol, "<br>"

        # calculate new positions
        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext)

        # handle newlines
        if toktype in [token.NEWLINE, tokenize.NL]:
            self.out.write('\n')
            return

        # send the original whitespace, if needed
        if newpos > oldpos:
            self.out.write(self.raw[oldpos:newpos])

        # skip indenting tokens
        if toktype in [token.INDENT, token.DEDENT]:
            self.pos = newpos
            return

        # map token type to a color group
        if token.LPAR <= toktype and toktype <= token.OP:
            toktype = token.OP
        elif toktype == token.NAME and keyword.iskeyword(toktext):
            toktype = _KEYWORD
        color = _colors.get(toktype, _colors[_TEXT])

        style = ''
        if toktype == token.ERRORTOKEN:
            style = ' style="border: solid 1.5pt #FF0000;"'

        # send text
        self.out.write('<font color="%s"%s>' % (color, style))
        self.out.write(cgi.escape(toktext))
        self.out.write('</font>')


if __name__ == "__main__":
    import os, sys
    print "Formatting..."

    # assume first argument is the filename
    filename = sys.argv[1]
    print filename
    url = filename + '.html'
    # open own source
    source = open(filename).read()

    # write colorized version to "python.html"
    Parser(source, open(url, 'wt')).format(None, None)

    print "Opening..."
    import webbrowser
    webbrowser.open(url, 1, 1)

