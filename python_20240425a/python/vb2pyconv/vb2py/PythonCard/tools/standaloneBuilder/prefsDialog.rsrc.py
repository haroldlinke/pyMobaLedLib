{'type':'CustomDialog',
    'name':'prefsDialog',
    'title':'standaloneBuilder Preferences',
    'position':(123, 38),
    'size':(665, 415),
    'components': [

{'type':'TextField', 
    'name':'resEditPath', 
    'position':(165, 25), 
    'size':(405, -1), 
    'userdata':'Select the location on your computer where the PythonCard resource editor is installed.', 
    },

{'type':'Button', 
    'name':'resEditPathBtn', 
    'position':(580, 25), 
    'size':(25, -1), 
    'label':'...', 
    },

{'type':'Button', 
    'name':'resEditPathHelpBtn', 
    'position':(610, 25), 
    'size':(25, -1), 
    'label':'?', 
    },

{'type':'TextField', 
    'name':'srcEditPath', 
    'position':(165, 55), 
    'size':(405, -1), 
    'userdata':'Select the location on your computer where the PythonCard source code editor is installed.\n', 
    },

{'type':'Button', 
    'name':'srcEditPathBtn', 
    'position':(580, 55), 
    'size':(25, -1), 
    'label':'...', 
    },

{'type':'Button', 
    'name':'srcEditPathHelpBtn', 
    'position':(610, 55), 
    'size':(25, -1), 
    'label':'?', 
    },

{'type':'TextField', 
    'name':'txtEditPath', 
    'position':(165, 85), 
    'size':(405, -1), 
    'userdata':'Select the location on your computer where the PythonCard source code editor is installed.\n', 
    },

{'type':'Button', 
    'name':'txtEditPathBtn', 
    'position':(580, 85), 
    'size':(25, -1), 
    'label':'...', 
    },

{'type':'Button', 
    'name':'txtEditPathHelpBtn', 
    'position':(610, 85), 
    'size':(25, -1), 
    'label':'?', 
    },

{'type':'TextField', 
    'name':'pixmapEditPath', 
    'position':(165, 115), 
    'size':(405, -1), 
    'userdata':'Select the location on your computer where your preferred pixmap editor is installed.\n', 
    },

{'type':'Button', 
    'name':'pixmapEditPathBtn', 
    'position':(580, 115), 
    'size':(25, -1), 
    'label':'...', 
    },

{'type':'Button', 
    'name':'pixmapEditPathHelpBtn', 
    'position':(610, 115), 
    'size':(25, -1), 
    'label':'?', 
    },

{'type':'TextField', 
    'name':'compilerPath', 
    'position':(165, 145), 
    'size':(405, -1), 
    'userdata':'Select the location on your computer where the Inno setup compiler is installed.', 
    },

{'type':'Button', 
    'name':'compilerPathBtn', 
    'position':(580, 145), 
    'size':(25, -1), 
    'label':'...', 
    },

{'type':'Button', 
    'name':'compilerPathHelpBtn', 
    'position':(610, 145), 
    'size':(25, 25), 
    'label':'?', 
    },

{'type':'TextField', 
    'name':'projectsPath', 
    'position':(165, 175), 
    'size':(405, -1), 
    'userdata':'Select the location on your computer where you normally keep your PythonCard projects.', 
    },

{'type':'Button', 
    'name':'projectsPathBtn', 
    'position':(580, 175), 
    'size':(25, -1), 
    'label':'...', 
    },

{'type':'Button', 
    'name':'projectsPathHelpBtn', 
    'position':(610, 175), 
    'size':(25, -1), 
    'label':'?', 
    },

{'type':'Choice', 
    'name':'buildTool', 
    'position':(165, 245), 
    'size':(130, -1), 
    'items':[u'py2exe', u'pyInstaller'], 
    'stringSelection':'pyInstaller', 
    'userdata':'Select the tool which you would prefer to use when building the executables for your projects.', 
    },

{'type':'Button', 
    'name':'buildToolHelpBtn', 
    'position':(610, 245), 
    'size':(25, -1), 
    'label':'?', 
    },

{'type':'TextField', 
    'name':'installerPath', 
    'position':(165, 275), 
    'size':(405, -1), 
    'userdata':'Select the location on your computer where the pyInstaller software is installed. Note that standaloneBuilder assumes that you have already configured this according to the documentation that comes with it.\n', 
    },

{'type':'Button', 
    'name':'installerPathBtn', 
    'position':(580, 275), 
    'size':(25, -1), 
    'label':'...', 
    },

{'type':'Button', 
    'name':'installerPathHelpBtn', 
    'position':(610, 275), 
    'size':(25, -1), 
    'label':'?', 
    },

{'type':'TextField', 
    'name':'appPublisher', 
    'position':(165, 305), 
    'size':(405, -1), 
    'userdata':"Defines the name which will be used to add an 'AppPublisher' entry to your Inno script file. This name will appear when someone does a right click on your standalone executable and selects 'properties'.", 
    },

{'type':'Button', 
    'name':'appPublisherHelpBtn', 
    'position':(610, 305), 
    'size':(25, -1), 
    'label':'?', 
    },

{'type':'Button', 
    'id':5100, 
    'name':'btnOK', 
    'position':(495, 355), 
    'label':'OK', 
    },

{'type':'Button', 
    'id':5101, 
    'name':'btnCancel', 
    'position':(575, 355), 
    'label':'Cancel', 
    },

{'type':'StaticText', 
    'name':'StaticText2', 
    'position':(70, 180), 
    'text':'Projects directory:', 
    },

{'type':'StaticText', 
    'name':'StaticText7', 
    'position':(60, 150), 
    'text':'Inno setup compiler:', 
    },

{'type':'StaticText', 
    'name':'StaticText5', 
    'position':(40, 120), 
    'text':'Preferred pixmap editor:', 
    },

{'type':'StaticText', 
    'name':'StaticText9', 
    'position':(80, 90), 
    'text':'Plain text editor:', 
    },

{'type':'StaticText', 
    'name':'StaticText4', 
    'position':(40, 60), 
    'text':'PythonCard code editor:', 
    },

{'type':'StaticText', 
    'name':'StaticText3', 
    'position':(20, 30), 
    'text':'PythonCard resource editor:', 
    },

{'type':'StaticBox', 
    'name':'StaticBox1', 
    'position':(5, 0), 
    'size':(645, 215), 
    'label':'Paths to external files', 
    },

{'type':'StaticText', 
    'name':'StaticText6', 
    'position':(80, 310), 
    'text':'Publisher name:', 
    },

{'type':'StaticText', 
    'name':'StaticText1', 
    'position':(65, 280), 
    'text':'Path to pyInstaller:', 
    },

{'type':'StaticText', 
    'name':'StaticText8', 
    'position':(60, 250), 
    'text':'Preferred build tool:', 
    },

{'type':'StaticBox', 
    'name':'StaticBox2', 
    'position':(5, 220), 
    'size':(645, 125), 
    'label':'Other settings', 
    },

] # end components
} # end CustomDialog
