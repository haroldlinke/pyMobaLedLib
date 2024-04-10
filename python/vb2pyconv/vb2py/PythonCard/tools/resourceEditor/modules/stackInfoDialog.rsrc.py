{'type':'CustomDialog',
          'name':'stackInfo',
          'title':'Stack Info',
          'size':(270, 100),
          'components': [

{'type':'StaticText', 
    'name':'stcName', 
    'position':(10, 10), 
    'size':(45, -1), 
    'text':'Name:', 
    },

{'type':'TextField', 
    'name':'fldName', 
    'position':(60, 5), 
    'size':(188, -1), 
    },

{'type':'Button', 
    'name':'btnOK', 
    'position':(10, 40), 
    'label':'OK',
    'default':1,
    'id':5100,
    },

{'type':'Button', 
    'name':'btnCancel', 
    'position':(115, 40), 
    'label':'Cancel',
    'id':5101,
    },

] # end components
} # end CustomDialog
