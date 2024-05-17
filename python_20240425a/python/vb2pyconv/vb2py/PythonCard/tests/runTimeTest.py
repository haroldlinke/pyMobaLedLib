"""
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/05/25 19:47:08 $"
"""

import sys
from PythonCard import model
import threading
import wx

class Runtime( threading.Thread ) :
    
    def __init__( self, path, clazz ) :
        threading.Thread.__init__( self )
        sys.argv = [ path ]
        self._clazz = clazz
        self._running = False 
        self.start()
        
    def run( self ) :
       self._app = model.Application( self._clazz )
       self._running = True
       self._app.MainLoop()
       
    def getApplication( self ) :
        while not self._running :
            pass
        return self._app

class User( object ) :

    def __init__( self, window ) :
        """
        Create a test proxy to a PythonCard window.
        """
        self._window = window 
        
    def click( self, path ) :
        """
        Generate a mouse down event for the button
        identified by 'path'.          
        Path example: myPanel.myButton
        """
        button = self._window.getComponent( path )
        event = wx.CommandEvent( wx.wxEVT_COMMAND_BUTTON_CLICKED, button.GetId() )
        wx.PostEvent( button, event )
        
    def type( self, path, text ) :
        """
        Type the 'text', character by character, into
        the TextField or TextArea identified by 'path'
        Path example: myPanel.myField
        """
        field = self._window.getComponent( path )
        field.SetValue( text )
        #event = wx.CommandEvent( wx.wxEVT_COMMAND_TEXT_ENTER, field.GetId() )
        #wx.PostEvent( field, event )
        
    def select( self, path, value ) :
        """
        Set the selected value of the component
        identified by path to 'value'.  This method
        can be used for popop menus, and single selection lists.
        Path example: myPanel.myMenu
        """
        pass
        