"""
__version__ = "$Revision: 1.23 $"
__date__ = "$Date: 2003/07/21 18:45:53 $"
"""

import os, sys
import shutil
import util

"""
Unix
os.environ['HOME']

Windows
os.environ['USERPROFILE']

On Windows 2000: \Documents and Settings\%UserName%
On Windows NT 4.0: \Winnt\Profiles\%UserName%
On Windows 98: \Windows\Profiles\%UserName%
On Windows Me: \Windows\Profiles\%UserName%
On Windows 2000 after upgrading from Windows NT 4.0:
\Winnt\Profiles\%UserName%


fallback
__file__
"""

# KEA 2003-06-04
# the config dir was named .pythoncard in release 0.7
# but this caused problems on Windows and the Mac OS X Finder
PYTHONCARD_CONFIG_DIR = "pythoncard_config"

PYTHONCARD_CONFIG_FILE = 'pythoncard_config.txt'

STC_CONFIG_FILE = 'stc-styles.cfg'

# KEA 2003-06-04
# pythoncard_config.txt
# for standalones
# updated 2004-05-14
DEFAULT_CONFIG = {
   'enableLogging':False,
   'logfile':'pythoncard.log',
   'logToStdout':True,
   'showMessageWatcher':False,
   'messageWatcherPosition':(0, 0),
   'messageWatcherSize':(200, 300),
   'showPropertyEditor':False,
   'propertyEditorPosition':(0, 0),
   'propertyEditorSize':(360, 240),
   'showShell':False,
   'shellPosition':(0, 0),
   'shellSize':(500, 200),
   'showNamespace':False,
   'namespacePosition':(0, 0),
   'namespaceSize':(600, 300),
}


#print "sys.path[0]", sys.path[0]
if util.main_is_frozen():
    # running standalone
    default_homedir = sys.path[0]
    homedir = default_homedir
else:
    default_homedir = os.path.dirname(os.path.abspath(__file__))
    #print "default_homedir", default_homedir
    for evar in ('HOME', 'USERPROFILE', 'TMP'):
        try:
            path = os.environ[evar]
            if os.path.isdir(path):
                homedir = os.path.join(path, PYTHONCARD_CONFIG_DIR)
                try:
                    # create the config directory if it
                    # doesn't already exist
                    if not os.path.isdir(homedir):
                        os.mkdir(homedir)
                    # if we were able to create the dir we're done
                    break
                except:
                    print "unable to create config directory", homedir
        except:
            homedir = os.path.join(default_homedir, PYTHONCARD_CONFIG_DIR)

    #print "homedir", homedir

    # should copying the config files be within the block above?
    try:
        # make copies of the default configs
        # for the user to modify
        for file in (PYTHONCARD_CONFIG_FILE, STC_CONFIG_FILE):
            path = os.path.join(homedir, file)
            if not os.path.exists(path):
                shutil.copy2(os.path.join(default_homedir, file), path)
    except:
        print "unable to copy config files"

try:
    configDict = util.readAndEvalFile(os.path.join(homedir, PYTHONCARD_CONFIG_FILE))
except:
    try:
        configDict = util.readAndEvalFile(os.path.join(default_homedir, PYTHONCARD_CONFIG_FILE))
    except:
        configDict = DEFAULT_CONFIG


def getStyleConfigPath():
    configfile = os.path.join(homedir, STC_CONFIG_FILE)
    if not os.path.exists(configfile):
        configfile = os.path.join(default_homedir, STC_CONFIG_FILE)
    return configfile

class Configuration :
    """
    Provides access to PythonCard's runtime configuration options.
    """

    class ConfigurationImpl :

        def __init__( self ) :
            # KEA 2001-11-17
            # change to import on configs
            """
            basePath = os.path.dirname( os.path.abspath( __file__ ) )
            path = os.path.join( basePath, PYTHONCARD_USER_CONFIG_FILE )
            # KEA 2001-08-09
            # first look in the directory of the program we're going to run
            # can't do this yet, given how the loader runs right now
            # then look for a user config file, then finally use the default
            #if os.path.exists(PYTHONCARD_USER_CONFIG_FILE):
            #    self._resource = resource.ResourceFile( PYTHONCARD_USER_CONFIG_FILE ).getResource()
            if os.path.exists(path):
                #print "using", path
                self._resource = resource.ResourceFile( path ).getResource()
                #print self._resource
            else:
                path = os.path.join( basePath, PYTHONCARD_CONFIG_FILE )
                self._resource = resource.ResourceFile( path ).getResource()
            """
            #self._resource = resource.Resource(configDict)
            self._resource = configDict
        
        def setOption( self, name, value ) :
            self._resource[name] = value
            #setattr( self._resource, name, value )
            #eval( 'self._resource.' + name + ' = ' + value )

        def getOption(self, name):
            return self._resource.get(name, None)

        #def getGuiToolkitName( self ) :
        #    return self._resource.gui

        def getLogFileName( self ) :
            # KEA 2001-12-13
            # return the application path for the log file directory
            # unless the user supplied filename contains a directory
            path = os.path.split(self.getOption('logfile'))[0]
            if path == '':
                return os.path.abspath( \
                    os.path.join( \
                    os.path.dirname(sys.argv[0]), \
                    self.getOption('logfile')))
            else:
                return os.path.abspath(self.getOption('logfile'))
            #return self._resource.logfile

        # KEA 2001-09-10
        # there should probably be generic method for turning Resources back into
        # dictionaries
        def saveConfig(self):
            global homedir
            
            #listX = self._resource.__dict__.keys()
            listX = self._resource.keys()
            listX.sort()
            dictStr = "{\n"
            for k in listX:
                if isinstance(self._resource[k], str):
                    dictStr += "'%s':'%s',\n" % (k, self._resource[k])
                else:
                    dictStr += "'%s':%s,\n" % (k, self._resource[k])
                """
                if isinstance(self._resource.__dict__[k], str):
                    dictStr += "'%s':'%s',\n" % (k, self._resource.__dict__[k])
                else:
                    dictStr += "'%s':%s,\n" % (k, self._resource.__dict__[k])
                """
            dictStr += "}\n"

            try:
                path = os.path.join(homedir, PYTHONCARD_CONFIG_FILE)
                f = open(path, 'w')
                f.write(dictStr)
                f.close()
            except:
                pass
                    

    _impl = None

    def __init__( self ) :
        if Configuration._impl is None :
            Configuration._impl = self.ConfigurationImpl()

    def setOption( self, name, value ) :
        Configuration._impl.setOption( name, value )

    def getOption( self, name ) :
        return Configuration._impl.getOption( name )

    #def getGuiToolkitName( self ) :
    #    return Configuration._impl.getGuiToolkitName()

    def getLogFileName( self ) :
        return Configuration._impl.getLogFileName()

    def saveConfig(self):
        Configuration._impl.saveConfig()


config = Configuration()
def getOption(name): return config.getOption(name)
def setOption(name, value): config.setOption(name, value)
def getLogFileName(): return config.getLogFileName()
def saveConfig(): config.saveConfig()

def hasOption( aOption ) :
    for arg in sys.argv :
        if arg == aOption :
            return 1
    return 0

def configOptions():
    # KEA 2001-08-09
    # this needs to be reworked, the old implementation overwrites whatever
    # might be in the .config.py files
    # also this implementation can only turn on an option, not turn it off
    if hasOption('-p'):
        setOption('showPropertyEditor', 1)
    if hasOption('-m'):
        setOption('showMessageWatcher', 1)
    if hasOption('-l'):
        setOption('enableLogging', 1)
    if hasOption('-s'):
        setOption('showShell', 1)
    if hasOption('-n'):
        setOption('showNamespace', 1)
    if hasOption('-d'):
        setOption('showDebugMenu', 1)

def saveUserConfiguration(app):
    """
    Given an application instance, save the current settings of the runtime
    windows.
    """
    if app.mw is not None:
        setOption('messageWatcherPosition', app.mw.GetPositionTuple())
        setOption('messageWatcherSize', app.mw.GetSizeTuple())
        setOption('showMessageWatcher', False)
    if app.namespaceFrame is not None:
        setOption('namespacePosition', app.namespaceFrame.GetPositionTuple())
        setOption('namespaceSize', app.namespaceFrame.GetSizeTuple())
        setOption('showNamespace', False)
    if app.pw is not None:
        setOption('propertyEditorPosition', app.pw.GetPositionTuple())
        setOption('propertyEditorSize', app.pw.GetSizeTuple())
        setOption('showPropertyEditor', False)
    if app.shellFrame is not None:
        setOption('shellPosition', app.shellFrame.GetPositionTuple())
        setOption('shellSize', app.shellFrame.GetSizeTuple())
        setOption('showShell', False)
    setOption('enableLogging', False)
    saveConfig()

        
if __name__ == '__main__' :
    __file__ = 'config.py'
    print 'config.py - Unit Test'
    setOption( 'myOption', 'myValue' )
    print getOption( 'myOption' )
    print 'showMessageWatcher=', getOption( 'showMessageWatcher' )
    setOption( 'showMessageWatcher', 1 )
    print 'showMessageWatcher=', getOption( 'showMessageWatcher' )
