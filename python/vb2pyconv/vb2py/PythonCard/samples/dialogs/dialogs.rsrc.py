{'application':{'type':'Application',
          'name':'Dialogs',
    'backgrounds': [
    {'type':'Background',
          'name':'bg1',
          'title':'Dialogs',
          'size':(403, 343),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'File',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'List', 
    'name':'listDialogs', 
    'position':(5, 5), 
    'size':(145, 290), 
    'items':['alert', 'color', 'directory', 'file', 'find', 'font', 'message', 'multiple choice', 'open file', 'save file', 'single choice', 'scrolled message', 'text entry', 'minimal'], 
    },

{'type':'TextArea', 
    'name':'fldResults', 
    'position':(155, 5), 
    'size':(240, 290), 
    },

] # end components
} # end background
] # end backgrounds
} }
