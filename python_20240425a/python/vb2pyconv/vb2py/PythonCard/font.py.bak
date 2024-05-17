
"""
__version__ = "$Revision: 1.20 $"
__date__ = "$Date: 2004/04/15 22:06:32 $"
"""

import inspect
import wx
import resource

# Construct a Python list from a CSS style font-family list which
# is comma delimited and uses quotes for multi-word items.
# Unquoted multi-word items have starting and ending whitespace stripped
# and all whitespace reduced to single space characters.
def FixWhiteSpace(s):
    s = s.strip()
    s = s.replace('\t', ' ')
    s = s.replace('\n', ' ')
    s = s.replace('\r', ' ')
    while s.find('  ') >= 0:
        s = s.replace('  ', ' ')
    return s

def ListFromCSSFonts(s):
    l = []
    # The starting position of the current item
    start = 0
    # The character that started the current item, empty if outside item
    startChar = ""    
    for i in range(len(s)):
        if startChar:
            if startChar in "\'\"":
                if s[i] == startChar:
                    l.append(s[start+1:i])
                    startChar = ""
            elif s[i] in ",":
                l.append(FixWhiteSpace(s[start:i]))
                startChar = ""
        elif s[i] not in " \t,":
                start = i
                startChar = s[i]
    if startChar:
        l.append(FixWhiteSpace(s[start:]))
    return l

def fontDescription(font):
    desc = {}
    family = font.GetFamily()
    faceName = font.GetFaceName()
    size = font.GetPointSize()
    style = font.GetStyle()
    weight = font.GetWeight()
    #print "wx.DEFAULT, wx.MODERN", wx.DEFAULT, wx.MODERN
    #print family, faceName, size, style, weight
    #print font.GetNativeFontInfo()
    if family >= wx.DEFAULT and family <= wx.MODERN:
        # ['wxDEFAULT', 'wxDECORATIVE', 'wxROMAN', 'wxSCRIPT', 'wxSWISS', 'wxMODERN']
        names = ['default', 'decorative', 'serif', 'script', 'sansSerif', 'monospace']
        desc['family'] = names[family - wx.DEFAULT]
    if faceName != '':
        desc['faceName'] = faceName
    if size != 0:
        desc['size'] = size
    if style == wx.ITALIC and weight == wx.BOLD:
        desc['style'] = 'boldItalic'
    elif style == wx.ITALIC:
        desc['style'] = 'italic'
    elif weight == wx.BOLD:
        desc['style'] = 'bold'
    else:
        desc['style'] = 'regular'
    return desc

def familyId(name):
    if name == 'serif':
        return wx.ROMAN
    elif name == 'sansSerif':
        return wx.SWISS
    elif name == 'monospace':
        return wx.MODERN
    else:
        return wx.DEFAULT

def styleId(name):
    if name.endswith('italic'):
        return wx.ITALIC
    else:
        return wx.NORMAL

def weightId(name):
    if name.startswith('bold'):
        return wx.BOLD
    else:
        return wx.NORMAL

def fontFromDescription(fontDescription):
    return wx.Font(fontDescription.get('size', wx.NORMAL_FONT.GetPointSize()),
                  familyId(fontDescription.get('family', '')),
                  styleId(fontDescription.get('style', 'regular')),
                  weightId(fontDescription.get('style', 'regular')),
                  0,
                  fontDescription.get('faceName', ''))

# KEA 2004-04-15
# have to subclass Python object base class so that property() works below
class Font(object):

    def __init__( self, fontDescription, aParent=None ) :
        self._parent = aParent
        self._family = ''
        self._faceName = ''
        self._size = wx.NORMAL_FONT.GetPointSize()
        self._style = 'regular'
        self._underline = 0
        if fontDescription is not None:
            if isinstance(fontDescription, dict):
                fontDescription = resource.Resource(fontDescription)
            try:
                self._family = fontDescription.family
            except:
                pass
            try:
                self._faceName = fontDescription.faceName
            except:
                pass
            try:
                self._size = fontDescription.size
            except:
                pass
            try:
                self._style = fontDescription.style
            except:
                pass


    def _familyId(self, name):
        if name == 'serif':
            return wx.ROMAN
        elif name == 'sansSerif':
            return wx.SWISS
        elif name == 'monospace':
            return wx.MODERN
        else:
            return wx.DEFAULT

    def _styleId(self, name):
        if name.endswith('italic'):
            return wx.ITALIC
        else:
            return wx.NORMAL

    def _weightId(self, name):
        if name.startswith('bold'):
            return wx.BOLD
        else:
            return wx.NORMAL

    def _getFont(self):
        return wx.Font(self._size,
                      self._familyId(self._family),
                      self._styleId(self._style),
                      self._weightId(self._style),
                      self._underline,
                      self._faceName)

    def _setFont(self, aFont):
        raise AttributeError, "font attribute is read-only"

    def _getSize(self):
        return self._size

    def _setSize(self, size):
        #self._font = self._newFont()
        #self._font.SetPointSize(size)
        self._size = size

    def _getStyle(self):
        return self._style

    def _setStyle(self, style):
        self._style = style

    def _getFaceName(self):
        return self._faceName

    def _setFaceName(self, faceName):
        self._faceName = faceName

    def _getFamily(self):
        return self._family

    def _setFamily(self, family):
        self._family = family

    def description(self):
        desc = {}
        if self._family != '':
            desc['family'] = self._family
        if self._faceName != '':
            desc['faceName'] = self._faceName
        desc['size'] = self._size
        if self._style != 'regular':
            desc['style'] = self._style
        return desc

    def __repr__(self):
        return str(self.description())

    faceName = property(_getFaceName, _setFaceName)
    family = property(_getFamily, _setFamily)
    font = property(_getFont, _setFont)
    size = property(_getSize, _setSize)
    style = property(_getStyle, _setStyle)
