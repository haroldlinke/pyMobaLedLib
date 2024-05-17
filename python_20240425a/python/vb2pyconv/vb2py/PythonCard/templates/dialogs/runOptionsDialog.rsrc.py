{'type':'CustomDialog',
          'name':'runOptions',
          'title':'Run Options',
          'size':(200, 220),
         'components': [

{'type':'StaticText', 
    'name':'stcCmdLineArgs', 
    'position':(10, 5), 
    'text':'Command line options:', 
    },

{'type':'CheckBox', 
    'name':'chkDebugMenu', 
    'position':(10, 25), 
    'label':'Debug Menu (-d)', 
    },

{'type':'CheckBox', 
    'name':'chkLogging', 
    'position':(10, 25), 
    'label':'Logging (-l)', 
    },

{'type':'CheckBox', 
    'name':'chkMessageWatcher', 
    'position':(10, 50), 
    'label':'Message Watcher (-m)', 
    },

{'type':'CheckBox', 
    'name':'chkNamespaceViewer', 
    'position':(10, 75), 
    'label':'Namespace Viewer (-n)', 
    },

{'type':'CheckBox', 
    'name':'chkPropertyEditor', 
    'position':(10, 100), 
    'label':'Property Editor (-p)', 
    },

{'type':'CheckBox', 
    'name':'chkShell', 
    'position':(10, 120), 
    'label':'Shell (-s)', 
    },

{'type':'StaticText', 
    'name':'stcOtherArgs', 
    'text':'Other args:', 
    },

{'type':'TextField', 
    'name':'fldOtherArgs', 
    'size':(200, -1),
    'text':'', 
    },

{'type':'Button', 
    'name':'btnOK', 
    'position':(8, 152), 
    'default':1,
    'id':5100,
    'label':'OK', 
    },

{'type':'Button', 
    'name':'btnCancel', 
    'position':(105, 152), 
    'id':5101,
    'label':'Cancel', 
    },

] # end components
}
