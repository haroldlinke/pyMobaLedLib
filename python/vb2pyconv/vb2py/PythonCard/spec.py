# __version__ = "$Revision: 1.24 $"
# __date__ = "$Date: 2004/05/10 05:01:58 $"

# The format of an entry is:
#
#    '<entry-name>' : {
#        'parent' : < <class-name> | None > ,
#        'events' : < [ '<event-name>', ... ] >,
#        'attributes' : < { '<attribute-name>' : { 
#                         'presence' : < 'mandatory' | 'optional' >,
#                         'default' : <valid-python-value> 
#                       > }
#   }

# How do we distinguish between resource/runtime

# Will 'mouseClick' work if specified in Widget's event list?

# Note that events and attributes are inherited.  The res.Spec class
# depends on the following entries being in order from top to bottom
# based on inheritance.  Component must appear before Widget, Widget
# must appear before TextField, Textfield must appear before PasswordField,
# ad nauseum ;)

specList = [

   { 'name':'Component', 'info':{
        'parent' : None,
        'events' : [],
        'attributes' : {
            'name' : { 'presence' : 'mandatory' },
            'command' : { 'presence' : 'optional', 'default' : None }
        }
    }},

   { 'name':'Application', 'info': {
        'parent' : None,
        'events' : [],
        'attributes' : {
            'name' : { 'presence' : 'mandatory' },
        }
    }},

   { 'name':'MenuBar', 'info': {
        'parent' : None,
        'events' : [],
        'attributes' : {
            'menus' : { 'presence' : 'optional', 'default': [] }
        }
    }},

   { 'name':'Menu' , 'info': {
        'parent' : None,
        'events' : [],
        'attributes' : {
            'name' : { 'presence' : 'mandatory' },
            'label' : { 'presence' : 'mandatory' },
            'enabled' : { 'presence' : 'optional', 'default' : 1 },
            'items' : { 'presence' : 'optional', 'default': [] }
        }
    }},

   { 'name':'MenuItem', 'info': {
        'parent' : 'Component',
        'events' : [],
        'attributes' : {
            'label' : { 'presence' : 'mandatory' },
            'checkable' : { 'presence' : 'optional', 'default': 0 },
            'checked' : { 'presence' : 'optional', 'default': 0 },
            'enabled' : { 'presence' : 'optional', 'default' : 1 }
            }
    }},

   { 'name':'Background', 'info': {
        'parent' : None,
        'events' : ['openBackground'],
        'attributes' : {
            'name' : { 'presence' : 'mandatory' },
            'title' : { 'presence' : 'mandatory' },
            'position' : { 'presence' : 'optional', 'default' : [ -1, -1 ] },
            'size' : { 'presence' : 'optional', 'default' : [ -1, -1 ] },
            'menubar' : { 'presence' : 'optional', 'default' : None },
            'statusBar' : { 'presence' : 'optional', 'default' : 0 },
            'icon' : { 'presence' : 'optional', 'default' : None },
            'foregroundColor' : { 'presence' : 'optional', 'default' : None },
            'backgroundColor' : { 'presence' : 'optional', 'default' : None },
            'image' : { 'presence' : 'optional', 'default' : None } ,
            'tiled' : { 'presence' : 'optional', 'default' : 0 },
            'visible' : { 'presence' : 'optional', 'default' : 1 },
            'style' : { 'presence' : 'optional', 'default' : [] },
            'strings': { 'presence' : 'optional', 'default' : {} },

        }
    }},

   { 'name':'CustomDialog', 'info': {
        'parent' : None,
        #'events' : ['openBackground'],
        'events' : [],
        'attributes' : {
            'name' : { 'presence' : 'mandatory' },
            'title' : { 'presence' : 'mandatory' },
            'position' : { 'presence' : 'optional', 'default' : [ -1, -1 ] },
            'size' : { 'presence' : 'optional', 'default' : [ -1, -1 ] },
            #'file' : { 'presence' : 'mandatory' } ,
            #'foregroundColor' : { 'presence' : 'optional', 'default' : None },
            #'backgroundColor' : { 'presence' : 'optional', 'default' : None },
            'strings': { 'presence' : 'optional', 'default' : {} },
        }
    }},


]
