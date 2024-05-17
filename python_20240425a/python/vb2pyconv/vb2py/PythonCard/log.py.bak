"""
__version__ = "$Revision: 1.11 $"
__date__ = "$Date: 2004/05/14 18:57:18 $"
"""

import time
import configuration
import sys
        
class Log :
    """
    A simple file logging class.  In the future we should
    use this class to wrap up log4p.

    The name of the log file is specified in PythonCard's 
    configuration file, 'pythoncard.rsrc.py'

    The log file will be created in the current working directory.

    Each time PythonCard runs, it deletes the old log contents.

    Log has four levels: DEBUG, ERROR, INFO and WARNING.

    Using Log:

        Call Log.getInstance() to get a reference to
        the single Log instance:
    
            log = Log.getInstance()
    
        Logging is initially disabled.  To turn logging on:
    
            log.enable()
    
        To turn logging off:
    
            log.disable()
    
        To selectively enable one or more logging levels:
    
            log.enableLevels( [ Log.ERROR, Log.WARNING ] )

        To selectively disable one or more logging levels:
    
            log.disableLevels( [ Log.DEBUG, Log.INFO ] )

        To write to the Log:

            log.debug( 'a debug message' )
            log.error( 'an error message' )
            log.info( 'an info message' )
            log.warning( 'a warning message' )

            NOTE: The debug(), error(), info(), and warning() methods
                  can be called with any number of parameters, and
                  the parameters can be of any type.  For example, if you
                  want to print a debug message that is a string,
                  and a list of items you can call:

                      items = [ 'one', 'two', 3 ]

                      log.debug( 'the items are: ', items )
    """

    # PUBLIC CLASS VARIABLES

    DEBUG = 'debug'

    ERROR = 'error'

    INFO = 'info'

    WARNING = 'warning'

    # PRIVATE CLASS VARIABLES

    instance = None

    legalLevels = { DEBUG:DEBUG, ERROR:ERROR, INFO:INFO, WARNING:WARNING }

    # PRIVATE INNER CLASSES

    class LogSingletonHelper :
        """
        A helper class used to implement the Singleton Desing Pattern.
        """
        def __call__( self, *args, **kw ) :

            # If an instance of Log does not exist,
            # create one and assign it to Log.instance.

            if Log.instance is None :
                Log.instance = Log()
            
            # Return TestSingleton.instance, which should contain
            # a reference to the only instance of Log in the system.

            return Log.instance
    
    # Create a class level method that must be called to
    # get the single instance of TestSingleton.

    # PUBLIC CLASS METHODS

    getInstance = LogSingletonHelper()

    # PUBLIC METHODS

    def __init__( self ) :
        """
        Initialize a Log instance.
        """
        if Log.instance is not None:
            raise RuntimeError, 'Only one instance of Log is allowed! use Log.getInstance() to get a reference to a Log'
    
        # The Log is initially disabled.

        self.enabled = 0

        self.created = 0

        #self.fileName = configuration.Configuration().getLogFileName()
        self.fileName = configuration.getLogFileName()
        self.logToStdout = configuration.getOption('logToStdout')

        # Enable all logging levels.

        self.errorEnabled = 1
        self.warningEnabled = 1
        self.debugEnabled = 1
        self.infoEnabled = 1
          
    def isEnabled( self ) :
        """
        Return true if logging is enabled.
        """
        return self.enabled

    def enable( self ) :
        """
        Enable all logging - levels remain at their current settings.
        """
        self.enabled = 1

        # If this is the first time logging has been enabled,
        # create a new, empty log file.

        if not self.created:
            if not self.logToStdout:
                file = open(self.fileName, 'w') 
                file.close()
            self.created = 1

    def disable( self ) :
        """
        Disable all logging - levels remain at their current settings.
        """
        self.enabled = 0

    def enableLevels( self, levels ) :
        """
        Enable each logging level listed in 'levels'.
        """
        for level in levels :
            if self.levelIsLegal( level ) :
                exec( 'self.' + level + 'Enabled = 1' )
   
    def disableLevels( self, levels ) :
        """
        Disable each logging level listed in 'levels'.
        """
        for level in levels :
            if self.levelIsLegal( level ) :
                exec( 'self.' + level + 'Enabled = 0' )

    def error( self, *args ) :
        """
        Write an error message to the log.
        """
        if self.errorEnabled :
            self.write( 'ERROR: ', args )

    def warning( self, *args ) :
        """
        Write a warning message to the log.
        """
        if self.warningEnabled :
            self.write( 'WARNING: ', args )

    def debug( self, *args ) :
        """
        Write a debug message to the log.
        """
        if self.debugEnabled :
            self.write( 'DEBUG: ', args )

    def info( self, *args ) :
        """
        Write an info message to the log.
        """
        if self.infoEnabled :
            self.write( 'INFO: ', args )

    # PRIVATE METHODS

    def levelIsLegal( self, level ) :
        if level not in Log.legalLevels:
            print '"', level, '" is not a legal logging level!'
            return 0
        else :
            return 1

    def write( self, prefix, argList ) :
        """
        This method should wait for the file to come available
        in the event that multiple threads are accessing the log file.
        """
        if self.enabled :
            now = time.localtime( time.time() )
            try:
                if self.logToStdout:
                    f = sys.stdout
                else:
                    f = open( self.fileName, 'a' )
                f.write( prefix + ': ' + "%s" % time.asctime( now ) + ': ' )
                for arg in argList :
                    f.write( str( arg ) )
                f.write( '\n' )
                if self.logToStdout:
                    f = None
                else:
                    f.close()
            except:
                pass

log = Log()
def isEnabled(): return log.isEnabled()
def enable(): log.enable()
def disable(): log.disable()
def enablelevels(levels): log.enablelevels(levels)
def disablelevels(levels): log.disablelevels(levels)
def error(*args): log.error(*args)
def warning(*args): log.warning(*args)
def debug(*args): log.debug(*args)
def info(*args): log.info(*args)

# Unit Test

if __name__ == '__main__' :

    #log = Log.getInstance()
    
    log.info( 'All logging enabled' )
    log.enable()
    log.debug( 's1', [ 'a', 'list' ] )
    log.error( 's2', { 'a':'dictionary' } )
    log.info( 's3', 1, 2, 3, 4 )
    log.warning( 's4', ' this ', 'is', ' a ', 'string ' )

    log.info( 'Disabling error and warning levels' )
    log.disableLevels( [ Log.ERROR, Log.WARNING ] )
    log.debug( 's1' )
    log.error( 's2' )
    log.info( 's3' )
    log.warning( 's4' )

    log.info( 'Enabling error and warning levels' )
    log.enableLevels( [ Log.ERROR, Log.WARNING ] )
    log.debug( 's1' )
    log.error( 's2' )
    log.info( 's3' )
    log.warning( 's4' )

    log.info( 'All logging disabled' )
    log.disable()
    log.debug( 's1' )
    log.error( 's2' )
    log.info( 's3' )
    log.warning( 's4' )

    log.enable()
    log.info( 'Attempt to enable an unknown level' )
    log.enableLevels( [ 'bogus-level' ] )


