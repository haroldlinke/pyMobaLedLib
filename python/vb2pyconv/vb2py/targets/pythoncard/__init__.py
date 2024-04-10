from vb2py.PythonCard import registry
vb2py.PythonCardRegistry = registry.Registry.getInstance()

def Register(control):
    """Register a control for vb2py.PythonCard"""
    #
    #import pdb; pdb.set_trace()
    vb2py.PythonCardRegistry.register(control)
