"""
__version__ = "$Revision: 1.8 $"
__date__ = "$Date: 2004/05/12 22:01:59 $"
"""

from PythonCard import singleton
import PythonCard.components
import copy, glob, os

class Registry( singleton.Singleton ) :
    """
    Maintains a regstry of the PythonCard Components that have
    been loaded into the system.
    """

    def __init__( self ) :
        self.components = {}
        #self._moduleNames = self.findBuiltInComponents()
        
    def findBuiltInComponents(self):
        """
        Return a list of the built-in module names that is suitable
        for subsequent calls to resource.loadComponentModule.
        """

        path = PythonCard.components.__path__[0]
        paths = glob.glob(os.path.join(path, '*.py'))
        names = []
        for path in paths:
            filename = os.path.split(path)[1]
            # don't return package file
            if filename != '__init__.py':
                names.append(os.path.splitext(filename)[0])
        #for name in names :
        #    print 'found component: ', name
        return names
            
    def register( self, componentClass ) :
        """
        Register a Component.
        """
        spec = componentClass._spec
        self.components[ spec.getName() ] = componentClass

    def hasComponent( self, name ) :
        """
        Return true if a Component matching 'name' exists
        in the registry.
        """
        return name in self.components

    def getComponents( self ) :
        """
        Get a dictionary that contains all of the 
        registered Components.
        """
        return copy.copy( self.components )

    def getComponentClass( self, name ) :
        """
        Get the class object for a named Component.
        """
        if name not in self.components :
            self.importClass( name )            
        return self.components[ name ]

    def getComponentSpec( self, name ) :
        """
        Get the Spec object for a named Component.
        """
        return self.getComponentClass( name )._spec

    def importClass( self, fqn ) :
        print('fqn=', fqn)
        """
        The path is of the form [Package.[sub-Package].]Module.Class
        """
        name = fqn
        modules = name.split('.')
        className = modules.pop() # remove last item.
        moduleName = '.'.join(modules)
        module = __import__( moduleName , globals(), locals(), []  )        
        for name in modules[ 1:] :
            module = vars( module )[ name ]            
        klass = vars( module )[ className ]
        self.components[ fqn ] = klass
        return klass

