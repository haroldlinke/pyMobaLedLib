{'type':'CustomDialog',
    'name':'Template',
    'title':'New Project Wizard',
    'position':(171, 401),
    'size':(600, 310),
    'components': [

{'type':'StaticText', 
    'name':'page1text1', 
    'position':(175, 0), 
    'actionBindings':{}, 
    'font':{'faceName': 'Tahoma', 'family': 'sansSerif', 'size': 20}, 
    'text':'New project wizard', 
    'userdata':'page1', 
    },

{'type':'StaticText', 
    'name':'page1text2', 
    'position':(175, 60), 
    'actionBindings':{}, 
    'text':'Project name', 
    'userdata':'page1', 
    },

{'type':'TextField', 
    'name':'projectName', 
    'position':(175, 80), 
    'size':(415, -1), 
    'actionBindings':{}, 
    'userdata':'page1', 
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
