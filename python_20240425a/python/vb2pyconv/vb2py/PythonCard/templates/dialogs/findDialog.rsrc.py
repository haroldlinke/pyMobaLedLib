{'type':'CustomDialog',
    'name':'dlgFind',
    'title':'Find dialog',
    'size':(380, 130),
    'components': [

{'type':'StaticText', 
    'name':'stcFindWhat', 
    'position':(7, 10), 
    'text':'Find What:', 
    },

{'type':'TextField', 
    'name':'fldFind', 
    'position':(80, 7), 
    'size':(195, -1), 
    },

{'type':'Button', 
    'id':5100, 
    'name':'btnFindNext', 
    'position':(285, 5), 
    'default':1, 
    'label':'Find Next', 
    },

{'type':'Button', 
    'id':5101, 
    'name':'btnCancel', 
    'position':(285, 35), 
    'label':'Cancel', 
    },

{'type':'CheckBox', 
    'name':'chkMatchWholeWordOnly', 
    'position':(7, 35), 
    'label':'Match whole word only', 
    },

{'type':'CheckBox', 
    'name':'chkMatchCase', 
    'position':(7, 55), 
    'label':'Match case', 
    },

{'type':'Choice', 
    'name':'popSearchField', 
    'position':(102, 80), 
    'size':(162, 21), 
    'items':[], 
    },

{'type':'StaticText', 
    'name':'stcSearchField', 
    'position':(7, 80), 
    'text':'Search Field:', 
    },

] # end components
} # end CustomDialog
