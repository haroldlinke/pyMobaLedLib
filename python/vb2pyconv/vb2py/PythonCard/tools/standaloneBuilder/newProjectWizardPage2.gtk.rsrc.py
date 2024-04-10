{'type':'CustomDialog',
    'name':'Template',
    'title':'New Project Wizard',
    'position':(171, 401),
    'size':(600, 310),
    'components': [

{'type':'StaticText', 
    'name':'page2text1', 
    'position':(175, 0), 
    'actionBindings':{}, 
    'font':{'faceName': 'Tahoma', 'family': 'sansSerif', 'size': 20}, 
    'text':'New project wizard', 
    'userdata':'page2', 
    },

{'type':'StaticText', 
    'name':'page2text2', 
    'position':(175, 60), 
    'actionBindings':{}, 
    'text':'Project description', 
    'userdata':'page2', 
    },

{'type':'TextField', 
    'name':'projectDesc', 
    'position':(175, 80), 
    'size':(415, -1), 
    'actionBindings':{}, 
    'userdata':'page2', 
    },

{'type':'Image', 
    'name':'Image1', 
    'position':(-5, -5), 
    'size':(174, 324), 
    'actionBindings':{}, 
    'file':'pixmaps/newproject.png', 
    },

] # end components
} # end CustomDialog
