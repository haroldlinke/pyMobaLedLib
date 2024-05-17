"""
__version__ = "$Revision: 1.20 $"
__date__ = "$Date: 2004/04/14 02:38:47 $"
"""

from . import util
from . import error
from . import spec
from . import component
from . import log
from . import registry
from . import singleton

APP_COMPONENTS_PACKAGE = 'appcomponents'
COMPONENTS_PACKAGE = 'components'
        
# the components sub-package and an appcomponents package
# are used rather than a components path
def loadComponentModule(moduleName):
    try:
        #exec("from appcomponents import " + moduleName)
        __import__(APP_COMPONENTS_PACKAGE + '.' + moduleName, globals(), globals(), [APP_COMPONENTS_PACKAGE])
    except ImportError as e:
        try:
            #exec("from components import " + moduleName)
            __import__(COMPONENTS_PACKAGE + '.' + moduleName, globals(), globals(), [COMPONENTS_PACKAGE])
        except ImportError as e:
            log.error(e)
            message = 'cannot import module \'' + moduleName
            raise ImportError(message)
        else:
            log.debug("imported component " + moduleName)
    else:
        log.debug("imported appcomponent " + moduleName)

class ResourceFile :
    """
    Reads a Resource file into a dictionary.
    """

    def __init__( self, rsrcFileName ) :
        #self.dictionary = eval( open( rsrcFileName ).read() )
        # KEA 2001-09-07
        # change to support using Windows-style line endings under Unix
        self.dictionary = util.readAndEvalFile(rsrcFileName)

    def getResource( self ) :
        return Resource( self.dictionary )

class Resource :

    _spec = None
    """
    A generic tree of dictionary, array and primitive objects
    that is accessible using dot(.) notation.
    """
    def __init__ ( self, aDictionary ) :
           
        if Resource._spec is None :
            # KEA 2001-11-17
            # changed spec.py so that it can be imported rather than
            # having to use readAndEvalFile
            
            #thisDir = os.path.dirname( os.path.abspath( __file__ ) )
            #specPath = os.path.join( thisDir, 'spec.py' )
            # KEA 2001-09-07
            # change to support using Windows-style line endings under Unix
            #specDict = util.readAndEvalFile(specPath)
            #Resource._spec = Spec(specDict)
            Resource._spec = Spec(spec.specList)
            # KEA 2001-12-10
            # test sticking the ButtonSpec into the existing spec list
            #from components.button import ButtonSpec
            #Resource._spec.entries.append(ButtonSpec())
            
            # KEA 2001-12-10
            # components is a sub-package
            # rather than importing the entire sub-package
            # the import for each component should occur on demand as a Resource is needed
            # or some other mechanism could be used to force the loading of each module
            #import components

        for key in aDictionary:
            value = aDictionary[key]
            if isinstance(value, dict):
                aDictionary[key] = Resource(value)
            if isinstance(value, list):
                i = 0
                for item in value:
                    if isinstance(item, dict) :
                        value[i] = Resource(item)
                    i = i + 1

        self.__dict__.update(aDictionary)

        self.enforceSpec(aDictionary)


    def enforceSpec( self, aDictionary ) : 
        """
        If Resource._spec is not None, then we look at the Spec definition
        and enforce mandatory/optionl/default constraints on this
        Resource.

        Although I think the Resource  and Spec file formats are
        reasonable, this code is a hack job of the highest degree,
        and I don't mind admitting it - RDS ;)

        Maybe we'll have time to redesign ( or just design ) on the
        next pass ;)
        """            
        attributes = None
        typeStr = None

        if 'type' in aDictionary:
            typeStr = aDictionary['type']
            # Get the appropriate spec.
            if Resource._spec is not None :
                # KEA 2001-12-11
                # attempt to get the spec from the default Spec
                # which contains the non-modular components
                # and if that fails then load a widget (component) module
                # dynamically and get the spec from the imported class
                try:
                    _spec = Resource._spec.getEntry(typeStr)
                except:
                    # dynamic import
                    reggie = registry.Registry.getInstance()
                    
                    # rds: we can lose the following, and allow
                    # te call to getComponentSpec to do all the work.
                    
                    if not reggie.hasComponent(typeStr):
                        # RDS - Prepend the path to the package containing
                        # the built-in PythonCard components.
                        #if typeStr.find( '.' ) == -1 :
                        #    typeStr = 'PythonCard.components.' + typeStr
                        #clazz = Loader.getInstance().importClass( typeStr )
                        loadComponentModule( typeStr.lower() )
                    #print "using", typeStr + "._spec"
                    
                    _spec = reggie.getComponentSpec( typeStr )
                attributes = _spec.getAttributes()

        if attributes is not None :
            for key in attributes:
                attribute = attributes[key]
                if attribute.isRequired():
                    if not self.hasAttribute(key):
                        msg = 'error! ' + typeStr + '.' + key + ' is mandatory'
                        raise error.ResourceException(msg)
                elif attribute.isOptional():
                    if not self.hasAttribute(key):
                        self.__dict__[key] = attribute.getDefaultValue()


    def hasAttribute(self, aString):
        return aString in self.__dict__

    def __repr__( self ) :
        return 'Resource: ' + str( self.__dict__ )
    



class Spec :
    """
    A Spec is a dictionary that contains meta type information that
    is used to validate a Resource file.

    TODO: Raise a warning when unspecified attributes are found in
          a resource.  It may be interesting to process them and
          set them as member with get/set on instances of the 
          class where they are found? - RDS
    """
    def __init__ ( self, specArray ) :

        self.entries = []

        for item in specArray :
            self.mergeChildren( item, specArray )
            self.entries.append( component.BaseSpec( item ) ) 

    # PUBLIC METHODS

    def getEntries( self ) :
        return self.entries

    def getEntry( self, aString ) :
        """
        Find a BaseSpec by name.
        """
        for entry in self.entries :
            if entry.getName() is aString :
                return entry
        raise error.ResourceException('error! cannot find ', aString)

    # PRIVATE METHODS

    def mergeChildren( self, item, specArray ) :
        for child in specArray :
            if child[ 'info' ][ 'parent' ] is item[ 'name' ] :
                self.mergeContents( child, item )

    def mergeContents( self, child, parent ) :
        childEvents = child[ 'info' ][ 'events' ]
        parentEvents = parent[ 'info' ][ 'events' ]
        events = []
        for e in childEvents :
           events.append( e )
        for e in parentEvents :
           events.append( e )
        child[ 'info' ][ 'events' ] = events
        childAttributes = child[ 'info' ][ 'attributes' ]
        parentAttributes = parent[ 'info' ][ 'attributes' ]
        childAttributes.update( parentAttributes )
