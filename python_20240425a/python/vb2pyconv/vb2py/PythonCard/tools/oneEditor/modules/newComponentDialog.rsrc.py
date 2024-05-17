{'type':'CustomDialog',
    'name':'Template',
    'title':'Dialog Template',
    'size':(300, 170),
    'components': [

{'type':'TextField', 
    'name':'fldName', 
    'position':(60, 9), 
    'size':(230, -1), 
    },

{'type':'TextField', 
    'name':'fldLabelOrText', 
    'position':(60, 40), 
    'size':(230, -1), 
    },

{'type':'CheckBox', 
    'name':'chkHorizontal', 
    'position':(10, 80), 
    'label':'Offset Horizontally', 
    },

{'type':'CheckBox', 
    'name':'chkVertical', 
    'position':(170, 80), 
    'label':'Offset Vertically', 
    },

{'type':'Button', 
    'id':5100, 
    'name':'btnOK', 
    'position':(30, 110), 
    'label':'OK', 
    },

{'type':'Button', 
    'id':5101, 
    'name':'btnCancel', 
    'position':(130, 110), 
    'label':'Cancel', 
    },

{'type':'StaticText', 
    'name':'lblLabelOrText', 
    'position':(5, 40), 
    'size':(50, -1), 
    'alignment':'right', 
    'text':'Label:', 
    },

{'type':'StaticText', 
    'name':'lblName', 
    'position':(5, 10), 
    'size':(50, -1), 
    'alignment':'right', 
    'text':'Name:', 
    },

] # end components
} # end CustomDialog
