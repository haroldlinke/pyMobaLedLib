
"""
__version__ = "$Revision: 1.22 $"
__date__ = "$Date: 2004/09/25 03:20:57 $"
"""

import wx
from PythonCard import event, widget
import textfield

class PasswordFieldSpec(textfield.TextFieldSpec):
    def __init__(self):
        textfield.TextFieldSpec.__init__( self )
        self._name = 'PasswordField'
        self._parent = 'TextField'
 
class PasswordField(textfield.TextField):
    """
    A text field that displays '*' characters in place
    of the actual characters typed - suitable for entering
    passwords securely.
    """

    _spec = PasswordFieldSpec()

    def __init__( self, aParent,  aResource ) :
        ##textfield.TextField.__init__( self, aParent, aResource )

        self._border = aResource.border

        # previously _createDelegate would be called by Widget.__init__
        # so put wxTextCtrl.__init__ here
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
            #style = wx.TE_PASSWORD | wx.TE_PROCESS_ENTER | borderStyle | wx.CLIP_SIBLINGS,
            style = wx.TE_PASSWORD | borderStyle | \
                textfield.getAlignment(aResource.alignment) | \
                wx.NO_FULL_REPAINT_ON_RESIZE | wx.CLIP_SIBLINGS,
            name = aResource.name
        )

        widget.Widget.__init__( self, aParent, aResource )

        if not aResource.editable:
            self.SetEditable(False)

        if aResource.border == 'none':
            self.SetBackgroundColour(self.GetParent().GetBackgroundColour())

        #adapter = textfield.TextFieldEventBinding(self)
        #adapter.bindEvents()
##        self._bindEvents(event.WIDGET_EVENTS + textfield.TextFieldEvents)
        # KEA 2004-09-24
        # changing to CallAfter to force the gainFocus
        # event to occur after the initialize event
        wx.CallAfter(self._bindEvents, event.WIDGET_EVENTS + textfield.TextFieldEvents)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].PasswordField)

