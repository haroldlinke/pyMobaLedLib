{'type':'CustomDialog',
    'name':'Minimal',
    'title':'Minimal dialog',
    'size':(200, 100),
    'components': [

{ 'type':'TextField',
  'name':'field1',
  'position':(0, 0),
  'text':'Hello PythonCard' },

{'type':'Button', 
    'name':'btnOK', 
    'position':(10, 35), 
    'label':'OK',
    'id':5100,
    'default':1,
    },

{'type':'Button', 
    'name':'btnCancel', 
    'position':(100, 35), 
    'label':'Cancel',
    'id':5101,
    },

] # end components
} # end CustomDialog
