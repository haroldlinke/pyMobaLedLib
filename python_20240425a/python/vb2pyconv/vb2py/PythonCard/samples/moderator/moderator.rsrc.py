{'application':{'type':'Application',
          'name':'Moderator',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'Python Moderation Tool',
          'size':(443, 600),

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

{'type':'Button', 
    'name':'btnAddSpeaker', 
    'position':(250, 539), 
    'size':(151, -1), 
    'label':'Add Speaker', 
    },

{'type':'List', 
    'name':'lstDelegates', 
    'position':(242, 169), 
    'size':(171, 365), 
    'font':{'faceName': 'Microsoft Sans Serif', 'family': 'sansSerif', 'size': 12}, 
    'items':[], 
    },

{'type':'List', 
    'name':'lstQueue', 
    'position':(15, 169), 
    'size':(210, 365), 
    'font':{'faceName': 'Microsoft Sans Serif', 'family': 'sansSerif', 'size': 14}, 
    'items':[], 
    },

{'type':'Button', 
    'name':'btnPause', 
    'position':(106, 91), 
    'size':(99, -1), 
    'label':'Pause', 
    },

{'type':'Button', 
    'name':'btnNext', 
    'position':(244, 90), 
    'size':(151, -1), 
    'label':'Next Speaker', 
    },

{'type':'StaticText', 
    'name':'lblDelegates', 
    'position':(249, 151), 
    'text':'Delegates:', 
    },

{'type':'StaticText', 
    'name':'lblWaiting', 
    'position':(17, 151), 
    'text':'Waiting to Speak:', 
    },

{'type':'TextField', 
    'name':'txtSpeaker', 
    'position':(16, 23), 
    'size':(378, 43), 
    'editable':False, 
    'font':{'faceName': 'Microsoft Sans Serif', 'family': 'sansSerif', 'size': 22}, 
    },

{'type':'StaticText', 
    'name':'lblSpeaking', 
    'position':(17, -1), 
    'text':'Now Speaking:', 
    },

{'type':'StaticText', 
    'name':'lblTimeLeft', 
    'position':(18, 71), 
    'size':(203, -1), 
    'text':'Time Left:', 
    },

{'type':'TextField', 
    'name':'txtTime', 
    'position':(16, 89), 
    'size':(79, 42), 
    'editable':False, 
    'font':{'faceName': 'Microsoft Sans Serif', 'family': 'sansSerif', 'size': 24}, 
    'text':'3:00', 
    },

] # end components
} # end background
] # end backgrounds
} }
