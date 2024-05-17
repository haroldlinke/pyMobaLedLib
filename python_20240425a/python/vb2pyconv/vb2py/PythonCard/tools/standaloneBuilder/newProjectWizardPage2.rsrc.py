{'type':'CustomDialog',
    'name':'Template',
    'title':'New Project Wizard',
    'position':(171, 401),
    'size':(600, 330),
    'components': [

{'type':'StaticText', 
    'name':'page2text1', 
    'position':(175, 0), 
    'font':{'faceName': 'Tahoma', 'family': 'sansSerif', 'size': 20}, 
    'text':'New project wizard', 
    'userdata':'page2', 
    },

{'type':'StaticText', 
    'name':'page2text2', 
    'position':(175, 60), 
    'text':'Project description', 
    'userdata':'page2', 
    },

{'type':'TextField', 
    'name':'projectDesc', 
    'position':(275, 55), 
    'size':(315, -1), 
    'userdata':'page2', 
    },

{'type':'Image', 
    'name':'Image1', 
    'position':(-5, -5), 
    'size':(174, 324), 
    'file':'pixmaps/newproject.png', 
    },

] # end components
} # end CustomDialog
