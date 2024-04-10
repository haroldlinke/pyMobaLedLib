{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':'simple mp3player',
          'size':(404, 380),

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

{'type':'List', 
    'name':'mp3s', 
    'position':(10, 10), 
    'size':(384, 168), 
    'items':[], 
    },

{'type':'Button', 
    'name':'pause', 
    'position':(190, 310), 
    'size':(109, -1), 
    'label':'Pause/Resume', 
    },

{'type':'TextArea', 
    'name':'filename', 
    'position':(15, 190), 
    'size':(370, 100), 
    },

{'type':'Button', 
    'name':'load', 
    'position':(15, 310), 
    'size':(74, -1), 
    'label':'Load', 
    },

{'type':'Button', 
    'name':'play', 
    'position':(105, 310), 
    'size':(74, -1), 
    'label':'Play', 
    },

{'type':'Button', 
    'name':'stop', 
    'position':(310, 310), 
    'size':(74, -1), 
    'label':'Stop', 
    },

] # end components
} # end background
] # end backgrounds
} }
