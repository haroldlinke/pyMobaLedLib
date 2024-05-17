{'application':{'type':'Application',
          'name':'Minimal',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'redemo PythonCard Application',
          'size':(380, 450),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
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
                   'name':'menuHelpReModule',
                   'label':'re module documentation...',
                  },
                  {'type':'MenuItem',
                   'name':'menuHelpReHowTo',
                   'label':'Regular Expression HOWTO...',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'StaticText', 
    'name':'stcStatusMessage', 
    'position':(5, 90), 
    },

{'type':'StaticText', 
    'name':'stcPattern', 
    'position':(5, 0), 
    'text':'Enter a Perl-style regular expression:', 
    },

{'type':'TextField', 
    'name':'fldPattern', 
    'position':(0, 19), 
    'size':(370, -1), 
    },

{'type':'CheckBox', 
    'name':'chkIGNORECASE', 
    'position':(3, 45), 
    'label':'IGNORECASE', 
    },

{'type':'CheckBox', 
    'name':'chkLOCALE', 
    'position':(107, 45), 
    'label':'LOCALE', 
    },

{'type':'CheckBox', 
    'name':'chkMULTILINE', 
    'position':(191, 45), 
    'label':'MULTILINE', 
    },

{'type':'CheckBox', 
    'name':'chkDOTALL', 
    'position':(3, 65), 
    'label':'DOTALL', 
    },

{'type':'CheckBox', 
    'name':'chkVERBOSE', 
    'position':(107, 65), 
    'label':'VERBOSE', 
    },

{'type':'StaticText', 
    'name':'stcSource', 
    'position':(5, 110),
    'text':'Enter a string to search:', 
    },

{'type':'RadioGroup', 
    'name':'radSearchString', 
    'position':(5, 125), 
    'size':(365, -1), 
    'items':['Highlight first match', 'Highlight all matches'], 
    'layout':'horizontal', 
    'max':1, 
    'stringSelection':'Highlight first match', 
    },

{'type':'TextArea', 
    'name':'fldSource', 
    'position':(1, 168), 
    'size':(370, 100), 
    },

{'type':'List', 
    'name':'listGroups', 
    'position':(1, 269), 
    'size':(370, 85), 
    'items':[], 
    },


] # end components
} # end background
] # end backgrounds
} }
