{'application':{'type':'Application',
          'name':'TreeTest',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'treetest PythonCard Application',
          'size':(400, 300),

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

{'type':'Tree', 
    'name':'tree', 
    'position':(0, 0), 
    'size':(390, 255), 
    },

] # end components
} # end background
] # end backgrounds
} }
