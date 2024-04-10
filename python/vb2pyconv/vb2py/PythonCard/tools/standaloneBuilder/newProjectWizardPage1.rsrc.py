{'type':'CustomDialog',
    'name':'Template',
    'title':'New Project Wizard',
    'position':(171, 401),
    'size':(600, 330),
    'components': [

{'type':'StaticText', 
    'name':'page1text1', 
    'position':(175, 0), 
    'font':{'faceName': 'Tahoma', 'family': 'sansSerif', 'size': 20}, 
    'text':'New project wizard', 
    'userdata':'page1', 
    },

{'type':'StaticText', 
    'name':'page1text2', 
    'position':(175, 60), 
    'text':'Project name', 
    'userdata':'page1', 
    },

{'type':'TextField', 
    'name':'projectName', 
    'position':(250, 55), 
    'size':(340, -1), 
    'userdata':'page1', 
    },

{'type':'Image', 
    'name':'Image1', 
    'position':(-5, -5), 
    'size':(174, 324), 
    'file':'pixmaps/newproject.png', 
    },

] # end components
} # end CustomDialog
