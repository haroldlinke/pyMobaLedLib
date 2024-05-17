{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'outputWindow',
          'title':'Rebuild project',
          'size':(400, 300),
          'visible':0,

         'components': [

{'type':'TextArea', 
    'name':'importError', 
    'position':(10, 10), 
    'size':(375, 205), 
    'enabled':False, 
    'visible':False, 
    },

{'type':'Button', 
    'name':'clipBoardBtn', 
    'position':(90, 225), 
    'label':'Clipboard', 
    'toolTip':'Click here to copy the PythonCard component imports line to the Windows clipboard', 
    'visible':False, 
    },

{'type':'Button', 
    'name':'closeBtn', 
    'position':(10, 225), 
    'label':'Close', 
    },

{'type':'StaticText', 
    'name':'txt5', 
    'position':(10, 90), 
    'text':'Returned messages:', 
    },

{'type':'TextArea', 
    'name':'returnedText', 
    'position':(10, 105), 
    'size':(375, 110), 
    },

{'type':'StaticText', 
    'name':'txt4c', 
    'position':(145, 70), 
    'text':'please wait...', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt4b', 
    'position':(145, 70), 
    'font':{'style': 'bold', 'faceName': 'Verdana', 'family': 'sansSerif', 'size': 8}, 
    'text':'Done', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt4a', 
    'position':(10, 70), 
    'text':'Rebuilding distributable:', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt3c', 
    'position':(145, 50), 
    'text':'please wait...', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt3b', 
    'position':(145, 50), 
    'font':{'style': 'bold', 'faceName': 'Verdana', 'family': 'sansSerif', 'size': 8}, 
    'text':'Done', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt3a', 
    'position':(10, 50), 
    'text':'Rebuilding application:', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt2b', 
    'position':(145, 30), 
    'font':{'style': 'bold', 'faceName': 'Verdana', 'family': 'sansSerif', 'size': 8}, 
    'text':'Done', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt2a', 
    'position':(10, 30), 
    'text':'Rebuilding versioninfo file:', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt1b', 
    'position':(145, 10), 
    'font':{'style': 'bold', 'faceName': 'Verdana', 'family': 'sansSerif', 'size': 8}, 
    'text':'Done', 
    'visible':False, 
    },

{'type':'StaticText', 
    'name':'txt1a', 
    'position':(10, 10), 
    'text':'Rebuilding spec file:', 
    'visible':False, 
    },

] # end components
} # end background
] # end backgrounds
} }
