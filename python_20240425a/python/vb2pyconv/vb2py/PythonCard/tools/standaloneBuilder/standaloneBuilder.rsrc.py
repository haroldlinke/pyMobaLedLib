{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'standaloneBuilder',
          'title':'PythonCard standaloneBuilder',
          'size':(800, 594),
          'statusBar':1,

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileNew',
                   'label':'&New\tCtrl+N',
                   'command':'newBtn',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileOpen',
                   'label':'&Open\tCtrl+O',
                   'command':'openBtn',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileSave',
                   'label':'&Save\tCtrl+S',
                   'command':'saveBtn',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileSaveAs',
                   'label':'Save &As...',
                  },
                  {'type':'MenuItem',
                   'name':'fileSep2',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'menuFileExit',
                  },
              ]
             },
             {'type':'Menu',
             'name':'Edit',
             'label':'&Edit',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuEditMainScript',
                   'label':u'&Main script...',
                   'command':'EditMainScript',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditChglog',
                   'label':u'&Changelog...',
                   'command':'editChgLog',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditReadme',
                   'label':u'&README...',
                   'command':'editReadme',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditSpecfile',
                   'label':u'&Spec file...',
                   'command':'editSpecFile',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditInnoFile',
                   'label':u'&Inno script...',
                   'command':'editInnoFile',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditProps',
                   'label':u'&Project properties...',
                   'command':'editProps',
                  },
                  {'type':'MenuItem',
                   'name':'editSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuEditPrefs',
                   'label':u'&Preferences...',
                   'command':'editPrefs',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuTools',
             'label':'&Tools',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuToolsLogAdd',
                   'label':u'A&dd changelog entry...\tShift++',
                   'command':'menuToolsLogAdd',
                  },
                  {'type':'MenuItem',
                   'name':'menuToolsChkImport',
                   'label':u'&Check component imports',
                   'command':'menuToolsChkImport',
                  },
                  {'type':'MenuItem',
                   'name':'toolSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuToolsAddScript',
                   'label':u'Add &script...',
                   'command':'addScript',
                  },
                  {'type':'MenuItem',
                   'name':'menuToolsAddResource',
                   'label':u'Add &resource...',
                   'command':'addResource',
                  },
                  {'type':'MenuItem',
                   'name':'menuToolsAddPixmap',
                   'label':u'Add &pixmap...',
                   'command':'addPixmap',
                  },
                  {'type':'MenuItem',
                   'name':'menuToolsAddOther',
                   'label':u'Add &other...',
                   'command':'addOther',
                  },
                  {'type':'MenuItem',
                   'name':'toolSep2',
                   'label':u'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuToolsRunMain',
                   'label':u'Run &main script',
                   'command':'runMainScript',
                  },
                  {'type':'MenuItem',
                   'name':'toolSep3',
                   'label':u'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuToolsRebuild',
                   'label':'R&ebuild\tCtrl+R',
                   'command':'rebuildCmd',
                  },
                  {'type':'MenuItem',
                   'name':'menuToolsRelease',
                   'label':u'&Release\tCtrl+M',
                   'command':'releaseCmd',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuHelp',
             'label':'&Help',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuHelpManual',
                   'label':u'&Manual',
                   'command':'menuHelpManual',
                  },
                  {'type':'MenuItem',
                   'name':'menuHelpAbout',
                   'label':u'&About standaloneBuilder...',
                   'command':'menuHelpAbout',
                  },
              ]
             },
         ]
     },
         'strings': {
         u'testString':u'This is a test string',
         },

         'components': [

{'type':'ImageButton', 
    'name':'newBtn', 
    'position':(5, 5), 
    'size':(32, 32), 
    'backgroundColor':(255, 255, 255), 
    'border':'3d', 
    'command':'newBtn', 
    'file':'pixmaps/new.png', 
    'toolTip':'Create a new project', 
    'userdata':'frozen', 
    },

{'type':'ImageButton', 
    'name':'openBtn', 
    'position':(40, 5), 
    'size':(32, 32), 
    'backgroundColor':(255, 255, 255), 
    'border':'3d', 
    'command':'openBtn', 
    'file':'pixmaps/open.png', 
    'toolTip':'Open an existing project', 
    'userdata':'frozen', 
    },

{'type':'ImageButton', 
    'name':'saveBtn', 
    'position':(75, 5), 
    'size':(32, 32), 
    'backgroundColor':(255, 255, 255), 
    'border':'3d', 
    'command':'saveBtn', 
    'file':'pixmaps/save.png', 
    'toolTip':'Save the current project', 
    'userdata':'frozen', 
    },

{'type':'ImageButton', 
    'name':'prefsBtn', 
    'position':(705, 5), 
    'size':(32, 32), 
    'backgroundColor':(255, 255, 255), 
    'border':'3d', 
    'command':'editPrefs', 
    'file':'pixmaps/prefs.png', 
    'toolTip':'standaloneBuilder preferences', 
    'userdata':'frozen', 
    },

{'type':'ImageButton', 
    'name':'quitBtn', 
    'position':(750, 5), 
    'size':(32, 32), 
    'backgroundColor':(255, 255, 255), 
    'border':'3d', 
    'command':'quitBtn', 
    'file':'pixmaps/exit.png', 
    'toolTip':'Quit the program', 
    'userdata':'frozen', 
    },

{'type':'TextField', 
    'name':'projectName', 
    'position':(95, 60), 
    'size':(250, -1), 
    },

{'type':'TextField', 
    'name':'projectIcon', 
    'position':(500, 60), 
    'size':(250, -1), 
    },

{'type':'Button', 
    'name':'iconBtn', 
    'position':(755, 60), 
    'size':(22, 22), 
    'label':'...', 
    },

{'type':'TextField', 
    'name':'baseDir', 
    'position':(95, 90), 
    'size':(250, -1), 
    },

{'type':'Button', 
    'name':'baseDirBtn', 
    'position':(350, 90), 
    'size':(22, 22), 
    'label':'...', 
    },

{'type':'TextField', 
    'name':'projectDesc', 
    'position':(500, 90), 
    'size':(250, -1), 
    },

{'type':'TextField', 
    'name':'mainScript', 
    'position':(95, 120), 
    'size':(250, -1), 
    },

{'type':'Button', 
    'name':'mainScriptBtn', 
    'position':(350, 120), 
    'size':(22, 22), 
    'label':'...', 
    },

{'type':'Button', 
    'name':'mainScriptEditBtn', 
    'position':(375, 120), 
    'size':(50, 22), 
    'command':'EditMainScript', 
    'label':'Edit...', 
    },

{'type':'List', 
    'name':'scriptList', 
    'position':(15, 185), 
    'size':(360, 95), 
    'items':[], 
    },

{'type':'Button', 
    'name':'scriptAddBtn', 
    'position':(15, 285), 
    'size':(-1, 22), 
    'command':'addScript', 
    'label':'Add...', 
    },

{'type':'Button', 
    'name':'scriptDelBtn', 
    'position':(95, 285), 
    'size':(-1, 22), 
    'label':'Remove', 
    },

{'type':'Button', 
    'name':'scriptEditBtn', 
    'position':(175, 285), 
    'size':(-1, 22), 
    'label':'Edit...', 
    },

{'type':'Button', 
    'name':'scriptDelAllBtn', 
    'position':(300, 285), 
    'size':(-1, 22), 
    'label':'Clear all', 
    },

{'type':'List', 
    'name':'resList', 
    'position':(415, 185), 
    'size':(360, 95), 
    'items':[], 
    },

{'type':'Button', 
    'name':'resAddBtn', 
    'position':(415, 285), 
    'size':(-1, 22), 
    'command':'addResource', 
    'label':'Add..', 
    },

{'type':'Button', 
    'name':'resDelBtn', 
    'position':(495, 285), 
    'size':(-1, 22), 
    'label':'Remove', 
    },

{'type':'Button', 
    'name':'resEditBtn', 
    'position':(575, 285), 
    'size':(-1, 22), 
    'label':'Edit...', 
    },

{'type':'Button', 
    'name':'resDelAllBtn', 
    'position':(700, 285), 
    'size':(-1, 22), 
    'label':'Clear all', 
    },

{'type':'List', 
    'name':'pixmapList', 
    'position':(15, 340), 
    'size':(360, 95), 
    'items':[], 
    },

{'type':'Button', 
    'name':'pixmapAddBtn', 
    'position':(14, 440), 
    'size':(-1, 22), 
    'command':'addPixmap', 
    'label':'Add...', 
    },

{'type':'Button', 
    'name':'pixmapDelBtn', 
    'position':(95, 440), 
    'size':(-1, 22), 
    'label':'Remove', 
    },

{'type':'Button', 
    'name':'pixmapEditBtn', 
    'position':(175, 440), 
    'size':(-1, 22), 
    'label':'Edit...', 
    },

{'type':'Button', 
    'name':'pixmapDelAllBtn', 
    'position':(300, 440), 
    'size':(-1, 22), 
    'label':'Clear all', 
    },

{'type':'List', 
    'name':'otherList', 
    'position':(415, 340), 
    'size':(360, 95), 
    'items':[], 
    },

{'type':'Button', 
    'name':'docAddBtn', 
    'position':(414, 440), 
    'size':(-1, 22), 
    'command':'addOther', 
    'label':'Add...', 
    },

{'type':'Button', 
    'name':'docDelBtn', 
    'position':(495, 440), 
    'size':(-1, 22), 
    'label':'Remove', 
    },

{'type':'Button', 
    'name':'docEditBtn', 
    'position':(575, 440), 
    'size':(-1, 22), 
    'label':'Edit...', 
    },

{'type':'Button', 
    'name':'docDelAllBtn', 
    'position':(700, 440), 
    'size':(-1, 22), 
    'label':'Clear all', 
    },

{'type':'Button', 
    'name':'propertiesBtn', 
    'position':(15, 475), 
    'size':(74, 22), 
    'command':'editProps', 
    'label':'Props...', 
    'toolTip':'Change your projects properties', 
    },

{'type':'Button', 
    'name':'changelogBtn', 
    'position':(95, 475), 
    'size':(76, 22), 
    'command':'editChgLog', 
    'label':'Chglog...', 
    'toolTip':'Edit the changelog file', 
    },

{'type':'Button', 
    'name':'readmeBtn', 
    'position':(95, 500), 
    'size':(-1, 22), 
    'command':'editReadme', 
    'label':'README...', 
    'toolTip':'Edit the README file', 
    },

{'type':'Button', 
    'name':'specBtn', 
    'position':(175, 475), 
    'size':(-1, 22), 
    'command':'editSpecFile', 
    'label':'Spec file...', 
    'toolTip':'Edit the applications spec file', 
    },

{'type':'Button', 
    'name':'innoBtn', 
    'position':(175, 500), 
    'size':(76, 22), 
    'command':'editInnoFile', 
    'label':'Inno script...', 
    'toolTip':'Edit the Inno setup script for your application', 
    },

{'type':'Button', 
    'name':'runBtn', 
    'position':(300, 475), 
    'size':(-1, 22), 
    'command':'runMainScript', 
    'label':'Run...', 
    'toolTip':'Run the application', 
    },

{'type':'Button', 
    'name':'rebuildBtn', 
    'position':(700, 475), 
    'size':(-1, 22), 
    'command':'rebuildCmd', 
    'label':'Rebuild', 
    'toolTip':'Rebuild the standalone version of your application', 
    'userdata':'frozen', 
    },

{'type':'Button', 
    'name':'releaseBtn', 
    'position':(700, 500), 
    'size':(-1, 22), 
    'command':'releaseCmd', 
    'label':'Release', 
    'toolTip':'Make a release of your finished application', 
    'userdata':'frozen', 
    },

{'type':'StaticText', 
    'name':'versionString', 
    'position':(500, 125), 
    'text':'n/a', 
    },

{'type':'StaticBox', 
    'name':'StaticBox2', 
    'position':(5, 165), 
    'size':(380, 150), 
    'label':'Script files:', 
    },

{'type':'StaticBox', 
    'name':'StaticBox3', 
    'position':(405, 165), 
    'size':(380, 150), 
    'label':'Resource files:', 
    },

{'type':'StaticBox', 
    'name':'StaticBox4', 
    'position':(5, 320), 
    'size':(380, 150), 
    'label':'Pixmap files:', 
    },

{'type':'StaticBox', 
    'name':'StaticBox5', 
    'position':(405, 320), 
    'size':(380, 150), 
    'label':'Other files:', 
    },

{'type':'StaticBox', 
    'name':'StaticBox1', 
    'position':(5, 40), 
    'size':(780, 125), 
    'label':'Project:', 
    },

{'type':'StaticText', 
    'name':'StaticText5', 
    'position':(15, 125), 
    'text':'Main script file', 
    },

{'type':'StaticText', 
    'name':'StaticText4', 
    'position':(395, 95), 
    'text':'Project description', 
    },

{'type':'StaticText', 
    'name':'StaticText9', 
    'position':(435, 65), 
    'text':'Icon (Win)', 
    },

{'type':'StaticText', 
    'name':'StaticText8', 
    'position':(450, 125), 
    'text':'Version', 
    },

{'type':'StaticText', 
    'name':'StaticText7', 
    'position':(15, 95), 
    'text':'Base directory', 
    },

{'type':'StaticText', 
    'name':'StaticText6', 
    'position':(15, 65), 
    'text':'Name', 
    },

] # end components
} # end background
] # end backgrounds
} }
