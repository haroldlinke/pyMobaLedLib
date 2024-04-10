{'application':{'type':'Application',
          'name':'Chat',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'Chat PythonCard Application',
          'size':(510, 482),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit'
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'StaticText', 
    'name':'stcYourIP', 
    'position':(170, 316), 
    'text':'Your IP Address:', 
    },

{'type':'StaticText', 
    'name':'stcIPAddress', 
    'position':(2, 341), 
    'text':'Send to IP addresses:', 
    },

{'type':'StaticText', 
    'name':'stcNickName', 
    'position':(2, 316), 
    'text':'Nick Name:', 
    },

{'type':'TextArea', 
    'name':'fldTranscript', 
    'position':(0, -2), 
    'size':(500, 311), 
    'editable':0, 
    },

{'type':'TextField', 
    'name':'fldNickname', 
    'position':(67, 312), 
    'size':(77, -1), 
    'text':'YourName', 
    },

{'type':'TextField', 
    'name':'fldYourIPAddress', 
    'position':(258, 312), 
    'size':(85, -1), 
    'text':'127.0.0.1', 
    },

{'type':'TextField', 
    'name':'fldSendAddresses', 
    'position':(112, 335), 
    'size':(274, -1), 
    'text':'127.0.0.1', 
    },

{'type':'TextArea', 
    'name':'fldInput', 
    'position':(-2, 358), 
    'size':(388, 79), 
    },

{'type':'Button', 
    'name':'btnSend', 
    'position':(410, 410), 
    'label':'Send', 
    },

] # end components
} # end background
] # end backgrounds
} }
