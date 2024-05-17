{'type':'CustomDialog',
    'name':'stringDialog',
    'title':'String Editor',
    'size':(480, 300),
    'components': [

{'type':'List', 
    'name':'listStrings', 
    'position':(0, 0), 
    'size':(185, 185), 
    'items':[], 
    },

{'type':'Button', 
    'name':'btnNew', 
    'position':(5, 190), 
    'label':'New', 
    },

{'type':'Button', 
    'name':'btnDelete', 
    'position':(108, 191), 
    'label':'Delete', 
    },

{'type':'StaticText', 
    'name':'stcName', 
    'position':(200, 10), 
    'text':'Name:', 
    },

{'type':'StaticText', 
    'name':'stcValue', 
    'position':(200, 35), 
    'text':'Value:', 
    },

{'type':'TextField', 
    'name':'fldListIndex', 
    'position':(460, 5), 
    'visible':0, 
    },

{'type':'TextField', 
    'name':'fldName', 
    'position':(260, 5), 
    'size':(188, -1), 
    },

{'type':'TextArea', 
    'name':'fldValue', 
    'position':(260, 35), 
    'size':(188, 197), 
    },

{'type':'Button', 
    'name':'btnOK', 
    'position':(10, 240), 
    'label':'OK',
    'default':1,
    'id':5100,
    },

{'type':'Button', 
    'name':'btnCancel', 
    'position':(115, 240), 
    'label':'Cancel',
    'id':5101,
    },

] # end components
} # end CustomDialog
