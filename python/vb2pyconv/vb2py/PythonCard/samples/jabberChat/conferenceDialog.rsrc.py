{'type':'CustomDialog',
    'name':'ConferenceDialog',
    'title':'Join Conference',
    'size':(238, 156),
    'components': [

{'type':'TextField', 
    'name':'fldRoomName', 
    'position':(85, 5), 
    'size':(140, -1), 
    },

{'type':'Choice', 
    'name':'cmbRoomServer', 
    'position':(85, 35), 
    'size':(140, 21), 
    'items':['conference.jabber.org', 'private.jabber.org'], 
    'stringSelection':'conference.jabber.org', 
    },

{'type':'TextField', 
    'name':'fldNickname', 
    'position':(85, 65), 
    'size':(140, -1), 
    },

{'type':'StaticText', 
    'name':'stcNickname', 
    'position':(10, 70), 
    'text':'Nickname:', 
    },

{'type':'StaticText', 
    'name':'stcRoomServer', 
    'position':(10, 40), 
    'text':'Room Server:', 
    },

{'type':'StaticText', 
    'name':'stcRoomName', 
    'position':(10, 10), 
    'text':'Room Name:', 
    },

{'type':'Button', 
    'id':5100, 
    'name':'btnOK', 
    'position':(36, 99), 
    'label':'OK', 
    },

{'type':'Button', 
    'id':5101, 
    'name':'btnCancel', 
    'position':(126, 99), 
    'label':'Cancel', 
    },

] # end components
} # end CustomDialog
