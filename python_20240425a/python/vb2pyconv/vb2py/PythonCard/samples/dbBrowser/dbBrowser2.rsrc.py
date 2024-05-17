{ 'application':{ 'type':'Application',
            'name':'DbBrowser2', 

    'backgrounds':
 [ 
  {'type':'Background',
   'name':'DbBrowser',
    'title':'DbBrowser', 
    'position':( 100, 100 ), 
    'size':( 610, 570 ),
    'statusBar':1,
    'icon':'dbBrowser.ico',

    'menubar': 
    {   'type':'MenuBar',
        'menus': 
        [
            {'type':'Menu',
             'name':'mnuFile', 
             'label':'&File',
             'items': [ { 'type':'MenuItem',
                          'name':'mnuOpen',
                          'label':'&Open\tCtrl+O',
                          'command':'connect' }, 
                        { 'type':'MenuItem',
                          'name':'mnuExit',
                          'label':'E&xit\tAlt+X' } ] },
            {'type':'Menu',
             'name':'mnuHelp',
             'label':'&Help',
             'items': [ { 'type':'MenuItem',
                          'name':'mnuAbout',
                          'label':'&About dbBrowser...' } ] }
        ]
    },

   'components':
   [ 
    {'type':'StaticText', 'name':'lblTables', 'position':(5, 26), 'text':'Table' },
    {'type':'Choice', 'name':'chsTables', 'position':(60, 26), 'size':(150, -1), 'items':[], 'stringSelection':None},
    {'type':'Button', 'name':'btnBrowse', 'position':(415, 26), 'size':(-1, -1), 'label':'Browse', 'toolTip':'Browse the table data'},
    {'type':'StaticLine', 'name':'lnButtons', 'position':(5, 64), 'size':(590, -1) },
    {'type':'Grid', 'name':'myGrid', 'position':(0, 110), 'size':(600, 390),},
   ]
  }
 ]
 }
 }

