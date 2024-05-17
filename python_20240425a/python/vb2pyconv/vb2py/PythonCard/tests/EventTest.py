from PythonCard import event, log
import unittest

class Dummy :

    def visitIdleEvent( self, aParam ) :
        log.debug( 'visitIdleEvent(): ', aParam )


class TestEvents( unittest.TestCase ) :
    
    def setUp( self ) :
        pass

    def testEvent( self ) :
         #self.assert_(element in self.seq)
        dummy = Dummy()
        evt = event.IdleEvent( dummy )
        print evt
        evt.accept( dummy, 'this is a parameter' )


if __name__ == '__main__':
    unittest.main()

