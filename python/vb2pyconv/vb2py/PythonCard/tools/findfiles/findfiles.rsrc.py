{'application':{'type':'Application',
          'name':'Find Files',

    'backgrounds': [
    {'type':'Background',
         'name':'FindFiles',
          'title':'Find Files',
          'size':(700, 550),
          'visible':0,
          'style':['resizeable'],
          'statusBar':1,

    'menubar': {'type':'MenuBar',
         'menus': [
            {'type':'Menu',
              'name':'File',
              'label':'&File',
              'items': [
                  {'type':'MenuItem',
                   'name':'menuFileOpen',
                   'label':'&Open\tCtrl+O',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileSaveAs',
                   'label':'Save &As...',
                  },
                  {'type':'MenuItem',
                   'name':'fileSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
               ]
             },
             {'type':'Menu',
             'name':'menuHelp',
             'label':'&Help',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFindFilesDocumentation',
                   'label':'&findfiles Documentation...\tF1',
                   'command':'showFindFilesDocumentation',
                  },
                  {'type':'MenuItem',
                   'name':'menuPythonCardDocumentation',
                   'label':'&PythonCard Documentation...',
                   'command':'showPythonCardDocumentation',
                  },
              ]
             },
         ]
     },

         'components': [

{'type':'StaticText', 
    'name':'lblSearchFor', 
    'position':(5, 5), 
    'text':'Search for:', 
    },

{'type':'StaticText', 
    'name':'lblDirectories', 
    'position':(5, 35), 
    'text':'Directories:', 
    },

{'type':'StaticText', 
    'name':'lblFileTypes', 
    'position':(5, 65), 
    'text':'File types:', 
    },

{'type':'ComboBox', 
    'name':'fldSearchPattern', 
    'position':(65, 2), 
    'size':(280, -1), 
    },

{'type':'Button', 
    'name':'btnSearch', 
    'position':(555, 2), 
    'label':'Search',
    'default':1,
    },

{'type':'Button', 
    'name':'btnCancel', 
    'position':(655, 2), 
    'label':'Cancel',
    },

{'type':'TextField', 
    'name':'fldDirectories', 
    'position':(65, 32), 
    'size':(480, -1), 
    },

{'type':'Button', 
    'name':'btnAddDirs', 
    'position':(555, 32), 
    'label':'Add Dirs', 
    },

{'type':'TextField', 
    'name':'fldWildcard', 
    'position':(65, 62), 
    'size':(180, -1), 
    },

{'type':'CheckBox', 
    'name':'chkCaseSensitive', 
    'position':(65, 90), 
    'label':'Case sensitive', 
    },

{'type':'CheckBox', 
    'name':'chkSearchSubdirectories', 
    'position':(189, 90), 
    'checked':1, 
    'label':'Search subdirectories', 
    },

{'type':'CheckBox', 
    'name':'chkVerbose', 
    'position':(341, 90), 
    'label':'Verbose', 
    'visible':0,
    },

{'type':'CheckBox', 
    'name':'chkOpenWithResourceEditor', 
    'position':(341, 90), 
    'checked':0, 
    'label':'Open .rsrc.py files with resourceEditor', 
    },

{'type':'Button', 
    'name':'btnViewFile', 
    'position':(541, 90), 
    'label':'Open Selected File', 
    },

{'type':'List', 
    'name':'listResults', 
    'position':(5, 114), 
    'size':(680, 150), 
    'font':{'size': 9, 'family': 'monospace'}, 
    },

] # end components
} # end background
] # end backgrounds
} }
