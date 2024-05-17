{'application':{'type':'Application',
          'name':'TestEvents',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'Test Events PythonCard Application',
          'size':(300, 250),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'Button', 
    'name':'childBtn', 
    'position':(149, 65), 
    'command':'openChildWindow', 
    'label':'childBtn', 
    },

{'type':'TextField', 
    'name':'fld', 
    'position':(0, 0), 
    'text':'Hello PythonCard', 
    },

{'type':'TextArea', 
    'name':'fldArea', 
    'position':(0, 30), 
    'size':(-1, 100), 
    'text':'The quick brown fox jumped over the lazy dog.', 
    },

{'type':'Button', 
    'name':'btn', 
    'position':(150, 0), 
    'label':'btn', 
    },

{'type':'Button', 
    'name':'cmdBtn', 
    'position':(150, 30), 
    'command':'openChildWindow', 
    'label':'cmdBtn', 
    },

] # end components
} # end background
] # end backgrounds
} }
