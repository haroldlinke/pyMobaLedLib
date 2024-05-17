{'type':'CustomDialog',
    'name':'dlgFind',
    'title':'Find dialog',
    'size':(370, 120),
    'components': [

{'type':'StaticText', 
    'name':'stcFindWhat', 
    'position':(7, 10), 
    'text':'Find What:', 
    },

{'type':'TextField', 
    'name':'fldFind', 
    'position':(70, 7), 
    'size':(195, -1), 
    },

{'type':'Button', 
    'name':'btnFindNext', 
    'position':(280, 5), 
    'label':'Find Next',
    'id':5100,
    'default':1,
    },

{'type':'Button', 
    'name':'btnCancel', 
    'position':(280, 35), 
    'label':'Cancel',
    'id':5101,
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

] # end components
} # end CustomDialog
