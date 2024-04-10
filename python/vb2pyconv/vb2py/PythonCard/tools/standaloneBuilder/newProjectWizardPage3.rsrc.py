{'type':'CustomDialog',
    'name':'Template',
    'title':'New Project Wizard',
    'position':(171, 401),
    'size':(600, 330),
    'components': [

{'type':'StaticText', 
    'name':'page3text1', 
    'position':(175, 0), 
    'font':{'faceName': 'Tahoma', 'family': 'sansSerif', 'size': 20}, 
    'text':'New project wizard', 
    'userdata':'page3', 
    },

{'type':'StaticText', 
    'name':'page3text2', 
    'position':(175, 60), 
    'text':'Base directory', 
    'userdata':'page3', 
    },

{'type':'TextField', 
    'name':'baseDir', 
    'position':(255, 55), 
    'size':(300, -1), 
    'userdata':'page3', 
    },

{'type':'Button', 
    'name':'baseDirBtn', 
    'position':(560, 55), 
    'size':(25, 25), 
    'label':'...', 
    'userdata':'page3', 
    },

{'type':'Image', 
    'name':'Image1', 
    'position':(-5, -5), 
    'size':(174, 324), 
    'file':'pixmaps/newproject.png', 
    },

] # end components
} # end CustomDialog
