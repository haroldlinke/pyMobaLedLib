
"""
__version__ = "$Revision: 1.29 $"
__date__ = "$Date: 2004/09/30 23:04:52 $"
"""

import wx
from PythonCard import event, widget
import textfield


# KEA 2004-05-12
# due to the way Spec inits are called, I had to duplicate the TextField spec
# just so I could add a 'size' attribute, at least I think I needed to.

class TextAreaSpec(textfield.TextFieldSpec):
    def __init__(self):
        events = list(textfield.TextFieldEvents)       
        attributes = {
            'text' : {'presence' : 'optional', 'default' : ''},
            'editable' : {'presence' : 'optional', 'default' : 1},
            'alignment' : {'presence' : 'optional', 'default' : 'left', 'values' :['left', 'right', 'center']},
            'border' : {'presence' : 'optional', 'default' : '3d', 'values' : ['3d', 'none']},
            'horizontalScrollbar' : {'presence' : 'optional', 'default' : False},
            'size' : { 'presence' : 'optional', 'default' : [ -1, 50 ] },
        }                
        widget.WidgetSpec.__init__( self, 'TextArea', 'TextField' , events, attributes )

class TextArea(textfield.TextField):
    """
    A text area that can have multi-line text, scrollbars, etc..
    """

    _spec = TextAreaSpec()

    def __init__( self, aParent,  aResource ) :
        self._horizontalScrollbar = aResource.horizontalScrollbar
        if aResource.horizontalScrollbar:
            hScroll = wx.HSCROLL
        else:
            hScroll = 0
            
        self._border = aResource.border
        if aResource.border == 'none':
            borderStyle = wx.NO_BORDER
        else:
            borderStyle = 0

        self._alignment = aResource.alignment

        wx.TextCtrl.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id), 
            aResource.text, 
            aResource.position, 
            aResource.size,
            # KEA 2004-07-19
            # don't use wx.TE_PROCESS_TAB with 2.5.2 and later
##            style =  wx.TE_RICH2 | wx.TE_PROCESS_TAB | wx.TE_MULTILINE | borderStyle | \
            style =  wx.TE_RICH2 | wx.TE_MULTILINE | borderStyle | \
                textfield.getAlignment(aResource.alignment) | hScroll |\
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name )

        widget.Widget.__init__(self, aParent, aResource)

        if not aResource.editable:
            self.SetEditable(False)

        if aResource.border == 'none':
            self.SetBackgroundColour(self.GetParent().GetBackgroundColour())

##        self._bindEvents(event.WIDGET_EVENTS + textfield.TextFieldEvents)
        # KEA 2004-09-24
        # changing to CallAfter to force the gainFocus
        # event to occur after the initialize event
        wx.CallAfter(self._bindEvents, event.WIDGET_EVENTS + textfield.TextFieldEvents)

    # KEA 2004-04-20
    # wxPython 2.5.1.5 workaround
    if wx.Platform == '__WXMSW__':
        
        def appendText(self, aString):
            """Appends the text to the end of the text widget.
            After the text is appended, the insertion point will be at the end
            of the text widget. If this behavior is not desired, the programmer
            should use getInsertionPoint and setInsertionPoint."""
            self.AppendText(aString)
            # workaround for scroll bug
            # http://sourceforge.net/tracker/?func=detail&aid=665381&group_id=9863&atid=109863
            self.ScrollLines(-1)

        # KEA 2004-04-19
        # workaround Windows bug where control is shown
        # and the display left corrupted
        def _setText(self, text):
            if self.IsShown():
                self.SetValue(text)
            else:
                parent = self.GetParent()
                parent.Freeze()
                self.SetValue(text)
                # have to toggle here because the control thinks
                # it is hidden
                self.Show()
                self.Hide()
                parent.Refresh()
                parent.Thaw()

        text = property(wx.TextCtrl.GetValue, _setText)
    elif wx.Platform == '__WXMAC__':
        # KEA 2004-04-23
        # workaround for wxPython 2.4.x and 2.5.x
        # returning text with \r instead of \n
        def _getText(self):
            return "\n".join(self.GetValue().splitlines())
        text = property(_getText, wx.TextCtrl.SetValue)

    def _getHorizontalScrollbar( self ) :
        return self._horizontalScrollbar
    
    def _setHorizontalScrollbar ( self, aBool ) :
        raise AttributeError, "horizontalScrollbar attribute is read-only"

    horizontalScrollbar = property(_getHorizontalScrollbar, _setHorizontalScrollbar)

import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].TextArea)
