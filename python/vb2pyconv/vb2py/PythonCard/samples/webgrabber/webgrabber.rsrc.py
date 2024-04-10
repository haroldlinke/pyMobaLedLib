{'application':{'type':'Application',
          'name':'webgrabber',
    'backgrounds': [
    {'type':'Background',
          'name':'bgGrabber',
          'title':'webgrabber PythonCard Application',
          'size':(540, 172),
          'statusBar':1,

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

{'type':'TextField', 
    'name':'fldURL', 
    'position':(65, 0), 
    'size':(466, -1), 
    },

{'type':'TextField', 
    'name':'fldDirectory', 
    'position':(65, 30), 
    'size':(370, -1), 
    },

{'type':'StaticText', 
    'name':'stcDirectory', 
    'position':(0, 30), 
    'text':'Directory:', 
    },

{'type':'StaticText', 
    'name':'stcURL', 
    'position':(0, 5), 
    'text':'URL:', 
    },

{'type':'Button', 
    'name':'btnDirectory', 
    'position':(455, 30), 
    'label':'Directory...', 
    },

{'type':'Button', 
    'name':'btnGo', 
    'position':(360, 70), 
    'label':'Go', 
    'default':1,
    },

{'type':'Button', 
    'name':'btnCancel', 
    'position':(455, 70), 
    'label':'Cancel', 
    },

] # end components
} # end background
] # end backgrounds
} }
