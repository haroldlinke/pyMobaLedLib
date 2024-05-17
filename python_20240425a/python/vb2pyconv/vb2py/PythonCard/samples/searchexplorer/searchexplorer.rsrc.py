{ 'application':{ 'type':'Application',
            'name':'SearchExplorer',

    'backgrounds':
 [ 
  {'type':'Background',
   'name':'SearchExplorer Test',
    'title':'SearchExplorer',
    'size':(400, 300), 

    'menubar': 
    {   'type':'MenuBar', 
        'menus': 
        [
            {'type':'Menu',
             'name':'File',
             'label':'&File',
             'items': [ { 'type':'MenuItem',
                          'name':'menuFileExit',
                          'label':'E&xit\tAlt+X',
                          'command':'exit'} ] },
            {'type':'Menu',
             'name':'Edit',
             'label':'&Edit',
             'items': [ { 'type':'MenuItem',
                          'name':'menuEditUndo',
                          'label':'&Undo\tCtrl+Z'},
                        { 'type':'MenuItem',
                          'name':'menuEditRedo',
                          'label':'&Redo\tCtrl+Y'},
                        { 'type':'MenuItem', 'name':'editSep1', 'label':'-' },
                        { 'type':'MenuItem',
                          'name':'menuEditCut',
                          'label':'Cu&t\tCtrl+X'},
                        { 'type':'MenuItem',
                          'name':'menuEditCopy',
                          'label':'&Copy\tCtrl+C'},
                        { 'type':'MenuItem',
                          'name':'menuEditPaste',
                          'label':'&Paste\tCtrl+V'},
                        { 'type':'MenuItem', 'name':'editSep2', 'label':'-' },
                        { 'type':'MenuItem',
                          'name':'menuEditClear',
                          'label':'Cle&ar\tDel'},
                        { 'type':'MenuItem',
                          'name':'menuEditSelectAll',
                          'label':'Select A&ll\tCtrl+A'}
                        ] }
        ]       
    },

   'components':
   [ 
    {'type':'TextField', 'name':'fldSearch', 'position':(5, 4), 'size':(300, -1), 'text':''},
    {'type':'Button', 'name':'btnSearch', 'position':(310, 4), 'size':(-1, -1), 'label':'Search','default':1},
    {'type':'StaticText', 'name':'lblSites', 'position':(5, 40), 'size':(-1, -1), 'text':'Sites'},
    {'type':'StaticText', 'name':'lblPastSearches', 'position':(145, 40), 'size':(-1, -1), 'text':'Past Searches'},
    {'type':'List', 'name':'listSites', 'position':(5, 60 ), 'size':(130, 150),'items':[]},
    {'type':'List', 'name':'listPastSearches', 'position':(145, 60), 'size':(240, 150),'items':[]},
    {'type':'CheckBox', 'name':'chkExitAfterSearch', 'position':(5, 230), 'size':(-1, -1), 'label':'Exit after Search', 'checked':1},
    {'type':'Button', 'name':'btnRemoveSearch', 'position':(250, 220 ), 'size':(-1, -1), 'label':'Remove Search'}
   ]
  }
 ]
 }
 }

