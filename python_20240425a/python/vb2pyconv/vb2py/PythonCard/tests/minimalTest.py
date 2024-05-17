from PythonCard import model, test
import addresses
import time

if __name__ == '__main__':
    runtime = test.Runtime( '../addresses/addresses.py', addresses.Addresses )
    app = runtime.getApplication()
    user = test.User( app.getWindows()[ 0 ] )
    time.sleep( 1 )
    user.click( 'Next' )
    user.type( 'Name', 'dude' )
    time.sleep( 1 )
    user.click( 'Next' )
    
    #assert( w.getComponent( 'field1' ).GetValue() == 'this is some text' )


