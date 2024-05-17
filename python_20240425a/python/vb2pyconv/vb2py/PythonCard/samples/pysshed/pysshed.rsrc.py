{'application':{'type':'Application',
          'name':'Minimal',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'SSH Session Manager',
          'position':(-1, -1),
          'size':(360, 240),

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
             'name':'menuSessions',
             'label':'&Sessions',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuSessionConnect',
                   'label':'&Connect\tAlt+C',
                   'command':'connectBtn',
                  },
                  {'type':'MenuItem',
                   'name':'menuSessionAdd',
                   'label':'&Add...\tAlt+A',
                   'command':'addBtn',
                  },
                  {'type':'MenuItem',
                   'name':'menuSessionModify',
                   'label':'&Modify...\tAlt+M',
                   'command':'modifyBtn',
                  },
                  {'type':'MenuItem',
                   'name':'menuSessionDelete',
                   'label':'&Delete\tAlt+D',
                   'command':'delBtn',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuHelp',
             'label':'&Help',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuHelpAbout',
                   'label':'A&bout...\tAlt+B',
                   'command':'helpAbout',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'Button', 
    'name':'quitBtn', 
    'position':(270, 160), 
    'command':'exit', 
    'label':'Quit', 
    },

{'type':'Button', 
    'name':'delBtn', 
    'position':(270, 100), 
    'command':'delBtn', 
    'label':'Delete...', 
    },

{'type':'Button', 
    'name':'modifyBtn', 
    'position':(270, 70), 
    'command':'modifyBtn', 
    'label':'Modify...', 
    },

{'type':'Button', 
    'name':'addBtn', 
    'position':(270, 40), 
    'command':'addBtn', 
    'label':'Add...', 
    },

{'type':'Button', 
    'name':'connectBtn', 
    'position':(270, 10), 
    'command':'connectBtn', 
    'label':'Connect', 
    },

{'type':'List', 
    'name':'sessionList', 
    'position':(10, 10), 
    'size':(252, 174), 
    'items':[], 
    },

] # end components
} # end background
] # end backgrounds
} }
