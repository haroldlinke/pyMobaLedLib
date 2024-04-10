{'type':'CustomDialog',
    'name':'dlgAbout',
    'title':'About PySSHed:',
    'position':(-1, -1),
    'size':(410, 300),
    'components': [

{'type':'StaticText', 
    'name':'StaticText', 
    'position':(10, 20), 
    'font':{'style': 'bold', 'family': 'sansSerif', 'size': 12}, 
    'text':'PySSHed (Python SSH Session Editor) Ver 0.3.2', 
    },

{'type':'Button', 
    'name':'AboutBtn', 
    'position':(10, 50), 
    'label':'About', 
    },

{'type':'Button', 
    'name':'AuthorBtn', 
    'position':(95, 50), 
    'label':'Author', 
    },

{'type':'Button', 
    'name':'LicenseBtn', 
    'position':(180, 50), 
    'label':'License', 
    },

{'type':'HtmlWindow', 
    'name':'HtmlWindow', 
    'position':(5, 80), 
    'size':(395, 155), 
    'backgroundColor':(255, 255, 255), 
    },

{'type':'Button', 
    'id':5100, 
    'name':'btnOK', 
    'position':(325, 245), 
    'label':'Close', 
    },

] # end components
} # end CustomDialog
