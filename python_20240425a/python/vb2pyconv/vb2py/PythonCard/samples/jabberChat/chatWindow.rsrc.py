{'application':{'type':'Application',
          'name':'Chat',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'',
          'size':(500, 482),
          'style':['resizeable'],

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileSend',
                   'label':'&Send\tCtrl+S',
                   'command':'doSend',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileClose',
                   'label':'Close',
                  },
             ],
             },
             {'type':'Menu',
             'name':'menuOptions',
             'label':'Options',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuOptionsSendOnReturn',
                   'label':'Send on &Return\tCtrl+R',
                   'checkable':1,
                   'checked':1,
                  },
              ],
             },
         ]
     },
         'components': [

{'type':'TextArea', 
    'name':'fldTranscript', 
    #'position':(0, -2), 
    'size':(400, 300), 
    'editable':0, 
    },

{'type':'TextArea', 
    'name':'fldInput', 
    #'position':(-2, 358), 
    'size':(300, 100), 
    },

{'type':'Button', 
    'name':'btnSend', 
    'position':(410, 410), 
    'label':'Send', 
    'command':'doSend',
    },

] # end components
} # end background
] # end backgrounds
} }
