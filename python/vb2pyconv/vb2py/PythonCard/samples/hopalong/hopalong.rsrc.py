{'application':{'type':'Application',
          'name':'Hopalong',

    'backgrounds': [
    {'type':'Background',
         'name':'bgDoodle',
          'title':'Hopalong',
          'size':(800, 600),
          'statusBar':1,
          'style':['resizeable'],

    'menubar': {'type':'MenuBar',
         'menus': [
            {'type':'Menu',
              'name':'menuFile',
              'label':'&File',
              'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit\tAlt+X',
                   'command':'exit'
                  },
               ]
             },
            {'type':'Menu',
              'name':'menuEdit',
              'label':'&Edit',
              'items': [
                  {'type':'MenuItem',
                   'name':'menuEditClear',
                   'label':'&Clear',
                   'command':'editClear',
                  },
               ]
             },
         ]
     },

         'components': [

{'type':'BitmapCanvas', 
    'name':'bufOff', 
    'position':(0, 30),
    'size':(790, 500),
    'backgroundColor':(255, 255, 255), 
    },

{'type':'TextField', 
    'name':'fldA', 
    'position':(16, 4), 
    'size':(34, -1), 
    'text':'30.0', 
    },

{'type':'TextField', 
    'name':'fldB', 
    'position':(74, 4), 
    'size':(34, -1), 
    'text':'1.0', 
    },

{'type':'TextField', 
    'name':'fldC', 
    'position':(134, 4), 
    'size':(34, -1), 
    'text':'0.9', 
    },

{'type':'TextField', 
    'name':'fldIterations', 
    'position':(238, 4), 
    'size':(58, -1), 
    'text':'100000', 
    },

{'type':'TextField', 
    'name':'fldXOffset', 
    'position':(354, 4), 
    'size':(50, -1), 
    'text':'300', 
    },

{'type':'TextField', 
    'name':'fldYOffset', 
    'position':(468, 4), 
    'size':(50, -1), 
    'text':'300', 
    },

{'type':'TextField', 
    'name':'fldScale', 
    'position':(572, 4), 
    'size':(50, -1), 
    'text':'10.0', 
    },

{'type':'TextField', 
    'name':'fldColors', 
    'position':(672, 4), 
    'size':(50, -1), 
    'text':'1000', 
    },

{'type':'Button', 
    'name':'btnDraw', 
    'position':(702, 2), 
    'label':'Draw', 
    },

{'type':'Button', 
    'name':'btnCancel', 
    'position':(702, 2), 
    'label':'Cancel', 
    'enabled':0,
    },

{'type':'StaticText', 
    'name':'stcA', 
    'position':(4, 10), 
    'text':'a:', 
    },

{'type':'StaticText', 
    'name':'stcB', 
    'position':(62, 10), 
    'text':'b:', 
    },

{'type':'StaticText', 
    'name':'stcC', 
    'position':(120, 10), 
    'text':'c:', 
    },

{'type':'StaticText', 
    'name':'stcIterations', 
    'position':(184, 10), 
    'text':'Iterations:', 
    },

{'type':'StaticText', 
    'name':'stcXOffset', 
    'position':(312, 10), 
    'text':'XOffset:', 
    },

{'type':'StaticText', 
    'name':'stcYOffset', 
    'position':(418, 10), 
    'text':'YOffset:', 
    },

{'type':'StaticText', 
    'name':'stcScale', 
    'position':(534, 10), 
    'text':'Scale:', 
    },

{'type':'StaticText', 
    'name':'stcColors', 
    'position':(638, 10), 
    'text':'Colors:', 
    },

] # end components
} # end background
] # end backgrounds
} }
