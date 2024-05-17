"""
__version__ = "$Revision: 1.8 $"
__date__ = "$Date: 2003/01/10 07:19:39 $"
"""

import event, registry, log
import inspect


class IScriptable(object):
    """
    RDS - 2004-05-02
    The public interface for all scriptable objects.
    """
    def execute(self, name, event):
        raise NotImplementedError
    
    
class NullScriptable(IScriptable):
    """
    RDS - 2004-05-02
    Installed as the parent of any Scriptable
    object that is instantiated with a 
    parent=None.  This implementation calls the 
    EventLog when an event is executed and logs 
    it as *not* used.
    """
    def execute(self, name, event):
        event.EventLog.getInstance().log(event, '(not handled)', False)
    
    
class Scriptable(IScriptable):
    """
    RDS - 2004-05-02    
    A new Scriptable that will Component will inherit from.
    In this design, the Scriptable is responsible for
    execution of it's handlers.
    
    All classes that may contain PythonCard EventHandler definitions
    must implement Scriptable.

    A Scriptable object may be specified as the parent of
    this object.  The parent will be searched for EventHandlers
    if a EventHandler can't be found in this object.
    """
    def __init__(self, parent=None):
        if parent is None:
            parent = NullScriptable()
        self._parent = parent
        self._handlers = {}
        self._parseHandlers()

    def _parseHandlers(self):
        """
        Find all of the methods in this object that are
        PythonCard handlers, and register them.
        """
        found = []
        methods = inspect.getmembers(self, inspect.ismethod)
        for m in methods:
            if m[ 0 ].split('_')[ 0 ] == 'on':
                found.append(m[ 1 ])
        map(self._addHandler, found)

    def _isPythonCardHandler(self, aObject):
        """
        Return true if the object is a PythonCard handler.
        """
        return isinstance(aObject, types.FunctionType) and aObject.__name__.split('_')[0] == 'on'
    
    def _addHandler(self, method):
        # Add the EventHandlers to our EventHandler list.
        if method.__name__ not in self._handlers:
            log.debug("_addHandler: " + method.__name__)
            self._handlers[ method.__name__ ] = event.EventHandler(method)  
    
    def _findHandler(self, name):
        """
        Look for a EventHandlers that matches 'name' in our 
        list of EventHandlers.
        """
        handler = self._handlers.get(name, None)
        
        if handler is None:      
            # Change the handler name to target this Scriptable object
            # and look in our list of EventHandlers.
    
            words = name.split('_')
            s = words[ 0 ] + '_' + self.getName() + '_' + words[ len(words) - 1 ]
            h = self._handlers.get(s, None)
            if h is not None:
                return (h)
            else:
                # search for Background and Stack handlers like
                # on_mouseClick, on_initialize
                s = words[ 0 ] + '_' + words[ len(words) - 1 ]
                return self._handlers.get(s, None)
        
        return handler
        
    def execute(self, name, event):
        """
        RDS - 2004-05-02
        
        Find the handler that matches handlerName and
        execute it.
        
        Should we throw an exception if the handler name
        is not found?  
        
        The caller would be responsible for reporting 
        a missing handler as an error.
        """
        handler = self._findHandler(name)
        
        if handler is not None:
            handler.execute(event)
            event.EventLog.getInstance().log(event, handler.getSourceName(), True)
        else:
            self._parent.execute(name, event)
        
        
class AttributeSpec:

    def __init__(self, name, properties):
        self.name = name
        self.presence = properties['presence']
        self.default = None
        if self.presence is 'optional':
            self.default = properties['default']
        if 'values' in properties:
            self.values = properties['values']
        else:
            self.values = None

    # PUBLIC METHODS

    def getName(self):
        return self.name

    def isRequired(self):
        return self.presence is 'mandatory'

    def isOptional(self):
        return self.presence is 'optional'

    def getDefaultValue(self):
        return self.default      

    def hasDefaultValueList(self):
        return self.values is not None

    def getDefaultValueList(self):
        return self.values

class BaseSpec:

    def __init__(self, aDictionary):
        self._name = aDictionary[ 'name' ]
        self._parent = None
        self._events = aDictionary[ 'info' ][ 'events' ]
        self._attributes = self._parseAttributes(aDictionary[ 'info' ][ 'attributes' ])
        self._requiredAttributes = self._parseRequiredAttributes()
        self._optionalAttributes = self._parseOptionalAttributes()

    def getName(self):
        return self._name

    def getParent(self):
        return self._parent

    def getEvents(self):
        return self._events

    # KEA 2002-07-01
    def getEventNames(self):
        eventNames = [ e.name for e in self._events ]
        eventNames.sort()
        return eventNames

    def getAttributes(self):
        return self._attributes

    def getRequiredAttributes(self):
        return self._requiredAttributes

    def getOptionalAttributes(self):
        return self._optionalAttributes

    def _parseAttributes(self, aDictionary):
        attributes = {}
        for key in aDictionary:
            value = aDictionary[key]
            attribute = AttributeSpec(key, value)
            attributes[attribute.getName()] = attribute
        return attributes

    def _parseRequiredAttributes(self):
        required = {}
        for key in self._attributes:
            attribute = self._attributes[key]
            if attribute.isRequired():
                required[key] = attribute
        return required

    def _parseOptionalAttributes(self):
        optional = {}
        for key in self._attributes:
            attribute = self._attributes[key]
            if attribute.isOptional():
                optional[key] = attribute
        return optional

    def __repr__(self):
        return str(self.__dict__)


class ComponentSpec(BaseSpec):
    
    def __init__(self, name, parent, events, subclassAttributes):
        # RDS - we should be calling BaseSpec.__init__().
        # this is pretty messy.
        self._name = name
        self._parent = parent
        self._events = events
        attributes = {
            'name': { 'presence': 'mandatory' },
            'command': { 'presence': 'optional', 'default': None },
            'actionBindings' : {'presence':'optional', 'default':None}
        }
        attributes.update(subclassAttributes)
        self._attributes = self._parseAttributes(attributes)
        self._requiredAttributes = self._parseRequiredAttributes()
        self._optionalAttributes = self._parseOptionalAttributes()

    def getMinimalResourceDict(self, name):
        """
        Class method that returns the minimal resource dictionary needed to create a component.
        The spec will provide the optional attributes when the Resource is created.
        """
        return {'type':self.getName(), 'name':name}

        
class Component(event.EventSource):
    """
    The superclass of all PythonCard components.
    Components can be visual (extend Widget) or
    non-visual (extend Component).
    """
    _spec = ComponentSpec
    
    def getEvents(self):
        """
        A convenience method to get the event classes for this component.
        """
        return ComponentClassInspector(self.__class__).getEvents() 

    def __init__(self, aResource):
        event.EventSource.__init__(self)
        self._name = aResource.name
        self._setCommand(aResource.command)
        if getattr(aResource, 'actionBindings', None):
            self._setActionBindings(dict(aResource.actionBindings.__dict__))
        else:
            self._setActionBindings(dict())

    def Lower(self):
        pass

    def _getName(self):
        return self._name

    def _setName(self, aString):
        raise AttributeError, "name attribute is read-only"

    def _setCommand( self, aString ) :
        self._command = aString

    def _getCommand( self ) :
        return self._command

    def _getActionBindings(self):
        return self._actionBindings

    def _setActionBindings(self, actionDict):
        self._actionBindings = actionDict

    name = property(_getName, _setName)
    command = property(_getCommand, _setCommand)
    actionBindings = property(_getActionBindings, _setActionBindings)


def registerAsComponent(pythonClass, attributes={}):
    pythonClass._spec = ComponentSpec(pythonClass.__name__, 'Component', list(), attributes)
    import sys
    from PythonCard import registry
    registry.Registry.getInstance().register(pythonClass)


class ComponentInspector:
    """
    Provides an api for introspection on
    Component instances.
    """
    def __init__(self, component):
        self.componentClass = component.__class__ 

    def getAttributes(self):
        return self.componentClass._spec.getAttributes()

    def getEvents(self):
        return self.componentClass._spec.getEvents()


class ComponentClassInspector:
    """
    Provides an api for introspection on
    Component classes.
    """
    def __init__(self, componentClass):
        self.componentClass = componentClass 

    def getAttributes(self):
        return self.componentClass._spec.getAttributes()

    def getEvents(self):
        return self.componentClass._spec.getEvents()

class ComponentFactory:
    """
    An abstract factory for creating Widgets from a Resource description.
    """
        
    def createComponent(self, aScriptable, aParent, aResource):
        """
        Find the class object based on a component's Resource definition.
        """
            
        # KEA 2001-08-05 is there a better way of coming up with 
        # the module name for model as the package name changes?
        
        reggie = registry.Registry.getInstance()
        clazz = reggie.getComponentClass(aResource.__dict__['type'])
                
        # Construct a new Component.
    
        component = clazz(aParent, aResource)

        # KEA 2004-04-20
        # this is for Widget to do
        #component.initialize()
        
        # Bind the Component to an EventDispatch that will translate
        # events generated by Component into calls to handlers that
        # are defined in a Scriptable object.
    
##        event.EventDispatch(component, aScriptable)
    
        # Return the newly created Component

        return component

