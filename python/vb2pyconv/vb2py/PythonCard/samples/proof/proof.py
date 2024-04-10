#!/usr/bin/python

"""
__version__ = "$Revision: 1.16 $"
__date__ = "$Date: 2004/05/05 03:51:54 $"
"""

import time
from PythonCard import log, model

class Proof(model.Background) :

    def on_bogus_select( self, event ) :
        print 'bogus!'

    def on_button1_mouseClick( self, event ) :
        button = event.target
        #Set the value of 'field1' to the current time
        #when 'button1' is clicked.
        now = time.localtime(time.time())
        field1 = self.components.field1
        print '\n\n\n\n\nfield1=', field1
        field1.text = "it's %s" % time.asctime( now )
        listX = self.components.list
        log.debug( listX.items )
        log.debug( listX.stringSelection )
        listX.stringSelection = "one"

        slider = self.components.aSlider
        log.debug( 'min='+ str( slider.min ) )
        log.debug( 'max=' + str( slider.max ) )
        log.debug( 'value=' + str( slider.value ) )

        # RDS 2001-07-29
        # Test setting StaticText.
        self.components.label.text = self.components.field2.text
        # KEA 2001-07-27
        # test out setting colors
        # three different forms accepted
        # no mapping between names and color yet
        #button.setBackgroundColor('LAVENDER BLUSH')
        button.backgroundColor = 'BLUE'
        #button.setBackgroundColor('#FF0000')
        #rgb = (255, 0, 0)
        button.backgroundColor = (255, 0, 0)
        print button.backgroundColor

    
    def on_imagebtn_mouseClick( self, event ) :
        log.debug( 'imagebutton-mouseClick:' + str( event.target ) )

    def on_list_select ( self, event ) :
        print 'list-select event, selected: ' + str( event.target.stringSelection )
        print self
        
    def on_list_mouseDoubleClick( self, event ) :
        print 'list-mouseDoubleClick, selected: ' + str( event.target.stringSelection )

    def on_field1_textUpdate ( self, event ) :
        log.debug( 'text-update:' + event.target.text )

    #def on_field1_textEnter ( self, field, event ) :
    #    log.debug( 'text-enter:' + field.text )

    def on_field1_keyUp ( self, event ) :
        log.debug( 'key-up:' + str( event ) )

    def on_radiogroup_select( self, event ) :
        log.debug( event.target )

    def on_checkbox_mouseClick( self, event ) :
        log.debug( '\ncheckbox-clicked: ' + str( event.target ) )

    def on_choice_select( self, event ) :
        log.debug( '\nchoice-selected: ' + str( event.target ) )

    def on_mnuExit_select(self, event):
        self.close()


if __name__ == '__main__':
    app = model.Application(Proof)
    app.MainLoop()
