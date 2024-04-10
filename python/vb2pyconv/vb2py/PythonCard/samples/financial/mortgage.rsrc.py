{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':'Mortgage Calculator',
          'size':(400, 300),
          'style':['resizeable'],

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit',
                   'command':'exit',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'StaticText', 
    'name':'Result', 
    'position':(115, 150), 
    'size':(65, -1), 
    },

{'type':'Button', 
    'name':'Calculate', 
    'position':(115, 105), 
    'label':'Calculate', 
    },

{'type':'TextField', 
    'name':'Principal', 
    'position':(115, 10), 
    'size':(70, -1), 
    'text':'100000', 
    },

{'type':'TextField', 
    'name':'InterestRate', 
    'position':(115, 35), 
    'size':(35, -1), 
    'text':'7.5', 
    },

] # end components
} # end background
] # end backgrounds
} }
