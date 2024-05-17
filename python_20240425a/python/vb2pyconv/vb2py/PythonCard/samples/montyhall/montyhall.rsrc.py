{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':'Monty Hall Game',
          'size':(396, 465),
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

{'type':'TextArea', 
    'name':'txtBox', 
    'position':(70, 170), 
    'size':(237, 146), 
    'alignment':'left', 
    'font':{'faceName': 'MS Shell Dlg', 'family': 'sansSerif', 'size': 10}, 
    },

{'type':'Button', 
    'name':'bResults', 
    'position':(235, 380), 
    'enabled':False, 
    'label':'Results', 
    },

{'type':'Button', 
    'name':'bAgain', 
    'position':(75, 380), 
    'enabled':False, 
    'label':'Play Again', 
    },

{'type':'StaticText', 
    'name':'StaticText2', 
    'position':(120, 320), 
    'font':{'faceName': 'Microsoft Sans Serif', 'family': 'sansSerif', 'size': 12}, 
    'text':'Change Your Guess?', 
    },

{'type':'Button', 
    'name':'bNo', 
    'position':(195, 345), 
    'size':(150, -1), 
    'enabled':False, 
    'label':'NO', 
    },

{'type':'Button', 
    'name':'bYes', 
    'position':(40, 345), 
    'size':(150, -1), 
    'enabled':False, 
    'label':'YES', 
    },

{'type':'Button', 
    'name':'bThree', 
    'position':(250, 145), 
    'size':(95, -1), 
    'label':'THREE', 
    },

{'type':'Button', 
    'name':'bTwo', 
    'position':(145, 145), 
    'size':(105, -1), 
    'label':'TWO', 
    },

{'type':'StaticText', 
    'name':'StaticText1', 
    'position':(155, 120), 
    'font':{'faceName': 'Microsoft Sans Serif', 'family': 'sansSerif', 'size': 12}, 
    'text':'Pick a Door', 
    },

{'type':'Image', 
    'name':'image3', 
    'position':(240, 10), 
    'backgroundColor':(255, 255, 255), 
    'file':'closed3.jpg', 
    },

{'type':'Image', 
    'name':'image2', 
    'position':(145, 10), 
    'backgroundColor':(255, 255, 255), 
    'file':'closed2.jpg', 
    },

{'type':'Image', 
    'name':'image1', 
    'position':(45, 10), 
    'backgroundColor':(255, 255, 255), 
    'file':'closed1.jpg', 
    },

{'type':'Button', 
    'name':'bOne', 
    'position':(40, 145), 
    'size':(105, -1), 
    'label':'ONE', 
    },

] # end components
} # end background
] # end backgrounds
} }
