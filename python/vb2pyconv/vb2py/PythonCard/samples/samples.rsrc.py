{'application':{'type':'Application',
          'name':'Samples',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'PythonCard Samples Launcher',
          'size':(600, 502),
          'style':['resizeable'],
          'visible':0,

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt-X',
                   'command':'exit',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuHelp',
             'label':'&Help',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuHelpPythonCardHomePage',
                   'label':'PythonCard &Home Page',
                  },
                  {'type':'MenuItem',
                   'name':'menuHelpOnlineDocumentation',
                   'label':'Online &Documentation',
                  },
                  {'type':'MenuItem',
                   'name':'menuHelpSep1',
                   'label':'-',
                  },
                  {'type':'MenuItem',
                   'name':'menuHelpAbout',
                   'label':'&About samples...',
                  },
                  {'type':'MenuItem',
                   'name':'menuHelpAboutPythonCard',
                   'label':'About PythonCard...',
                   'command':'doHelpAboutPythonCard',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'List', 
    'name':'listSamples', 
    'position':(0, 0), 
    'size':(150, 218), 
    'items':['addresses', 'ataxx', 'chat', 'companies', 'conversions', 'custdb', 'dbBrowser', \
             'dialogs', 'doodle', 'flatfileDatabase', 'flock', 'gadflyDatabase', 'gravity', \
             'hopalong', 'jabberChat', 'life', 'lsystem', 'minimal', 'minimalList', 'minimalTree', \
             'moderator', 'montyhall', 'mp3player', 'multicolumnexample', 'noresource', \
             'pictureViewer', 'proof', 'pysshed', 'radioclient', 'redemo', 'reversi', 'rpn', \
             'samples', 'saveClipboardBitmap', 'searchexplorer', \
             'simpleBrowser', 'simpleIEBrowser', 'slideshow', 'sounds', 'SourceForgeTracker', \
             'spirograph', 'spirographInteractive', 'stockprice', 'sudoku', 'textIndexer', 'textRouter', \
             'tictactoe', 'turtle', 'twistedEchoClient', \
             'webgrabber', 'webserver', 'widgets', 'worldclock'], 
    'stringSelection':'minimal', 
    },

{'type':'CheckBox', 
    'name':'chkDebugMenu', 
    'position':(160, 22), 
    'label':'Debug Menu (-d)', 
    },

{'type':'CheckBox', 
    'name':'chkLogging', 
    'position':(160, 22), 
    'label':'Logging (-l)', 
    },

{'type':'StaticText', 
    'name':'stcCmdLineArgs', 
    'position':(160, 2), 
    'text':'Command line options', 
    },

{'type':'CheckBox', 
    'name':'chkMessageWatcher', 
    'position':(160, 46), 
    'label':'Message Watcher (-m)', 
    },

{'type':'CheckBox', 
    'name':'chkNamespaceViewer', 
    'position':(160, 72), 
    'label':'Namespace Viewer (-n)', 
    },

{'type':'CheckBox', 
    'name':'chkPropertyEditor', 
    'position':(160, 98), 
    'label':'Property Editor (-p)', 
    },

{'type':'CheckBox', 
    'name':'chkShell', 
    'position':(160, 126), 
    'label':'Shell (-s)', 
    },

{'type':'Button', 
    'name':'btnLaunch', 
    'position':(158, 194), 
    'label':'Launch', 
    'command':'launch'
    },

{'type':'Button', 
    'name':'btnDescription', 
    'position':(268, 194), 
    'command':'showDescription', 
    'label':'Show Description', 
    },

{'type':'Button', 
    'name':'btnSource', 
    'position':(378, 194), 
    'command':'showSource', 
    'label':'Show Source', 
    },

{'type':'Button', 
    'name':'btnResource', 
    'position':(488, 194), 
    'command':'showResource', 
    'label':'Show Resource', 
    },

{'type':'StaticText', 
    'name':'stcDescription', 
    'position':(1, 230), 
    'text':'Description', 
    },

{'type':'TextArea', 
    'name':'fldDescription', 
    'position':(1, 246), 
    'size':(594, 211), 
    'editable':0, 
    },

{'type':'CodeEditor', 
    'name':'fldSource', 
    'position':(1, 246), 
    'size':(594, 211), 
    'editable':0, 
    'visible':0,
    },

] # end components
} # end background
] # end backgrounds
} }
