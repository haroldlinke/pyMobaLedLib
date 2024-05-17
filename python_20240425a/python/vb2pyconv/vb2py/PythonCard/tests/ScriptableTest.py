from PythonCard import event, log, component
import unittest


class TestHandler( component.Scriptable ) :

    def __init__( self, name, parent ) :
        component.Scriptable.__init__( self, parent )
        self._name = name
        
    def on_doIt( self, event ) :
        global handledIn
        handledIn = self._name

    def getName( self ) :
        return self._name
        
        
class HandlerWithMissingMethod( component.Scriptable ) :

    def __init__( self, name, parent ) :
        component.Scriptable.__init__( self, parent )
        self._name = name
        
    def getName( self ) :
        return self._name
        

class TestScriptable( unittest.TestCase, event.EventListener ) :
    
    def __init__( self, name ) :
        unittest.TestCase.__init__( self, name )
        event.EventLog.getInstance().addEventListener( self )
        
    def eventOccurred( self, event ) :
        print 'event=', event
        
    def setUp( self ) :
        pass

    def testScriptable( self ) :
        global handledIn
        parent = TestHandler( 'parent', None )
        parent.execute( 'on_doIt', ( 'howdy parent' ) )
        self.assertEqual( handledIn, 'parent' )
        child = TestHandler( 'child', parent )
        child.execute( 'on_doIt', ( 'howdy child' ) )
        self.assertEqual( handledIn, 'child' )
        missing = HandlerWithMissingMethod( 'missing', parent )
        missing.execute( 'on_doIt', ( 'howdy missing(parent)' ) )
        self.assertEqual( handledIn, 'parent' )
        missing.execute( 'on_wtf', ( 'no dice' ) )

if __name__ == '__main__':
    unittest.main()

