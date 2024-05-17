{'application':{'type':'Application',
          'name':'Dialogs',
    'backgrounds': [
    {'type':'Background',
          'name':'bg1',
          'title':'Twisted PythonCard PB Echo Client',
          'size':(375, 270),
          'statusBar':1,

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'File',
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

{'type':'StaticText', 
    'name':'StatusStaticText', 
    'position':(284, 215), 
    'backgroundColor':(0, 255, 127), 
    'font':{'family': 'sansSerif', 'size': 10}, 
    'text':'CONNECTED', 
    'visible':0, 
    },

{'type':'Button', 
    'name':'buttonLogin', 
    'position':(22, 140), 
    'size':(117, -1), 
    'label':'Login', 
    },

{'type':'TextField', 
    'name':'SendTextField', 
    'position':(20, 180), 
    'size':(330, -1), 
    'alignment':'left', 
    },

{'type':'TextArea', 
    'name':'ReceivedTextArea', 
    'position':(20, 0), 
    'size':(330, 125), 
    'alignment':'left', 
    },

{'type':'Button', 
    'name':'buttonSend', 
    'position':(151, 140), 
    'size':(125, -1), 
    'label':'Send', 
    },

] # end components
} # end background
] # end backgrounds
} }
