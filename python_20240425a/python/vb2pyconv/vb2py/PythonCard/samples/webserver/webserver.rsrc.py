{'application':{'type':'Application',
          'name':'WebServer',
    'backgrounds': [
    {'type':'Background',
          'name':'bgWeb',
          'title':'WebServer PythonCard Application',
          'size':(800, 482),
          'style':['resizeable'],

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
             {'type':'Menu',
             'name':'menuOptions',
             'label':'&Options',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuOptionsAllowAny',
                   'label':'&Allow any machine to connect',
                   'checkable':1,
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'CodeEditor', 
    'name':'fldLog', 
    'position':(0, 0), 
    'size':(800, 327), 
    'editable':0, 
    },

] # end components
} # end background
] # end backgrounds
} }
