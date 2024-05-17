{ 'application':{ 'type':'Application',
            'name':'DbBrowser', 

    'backgrounds':
 [ 
  {'type':'Background',
   'name':'DbBrowser',
    'title':'DbBrowser', 
    'position':( 100, 100 ), 
    'size':( 500, 500 ),
    'statusBar':1,
    'icon':'dbBrowser.ico',
    'style':['resizeable'],
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
             'name':'mnuAction',
             'label':'&Action',
             'items': [ { 'type':'MenuItem',
                          'name':'mnuFirst',
                          'label':'&First Record',
                          'command':'firstRecord' },
                        { 'type':'MenuItem',
                          'name':'mnuPrevious',
                          'label':'&Previous Record',
                          'command':'previousRecord' },
                        { 'type':'MenuItem',
                          'name':'mnuNext',
                          'label':'&Next Record',
                          'command':'nextRecord' },
                        { 'type':'MenuItem',
                          'name':'mnuLast',
                          'label':'&Last Record',
                          'command':'lastRecord' } ] },
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
    # The rows in my layout are each 25 pixels high with starting points at
    # 1, 26, 51, 76, 101, 126, 151, 176, 201, 226, etc.
    # {'type':'StaticText', 'name':'lblUsername', 'position':(5, 1), 'text':'Username'},
    # {'type':'TextField', 'name':'txtUsername', 'position':(60, 1), 'size':(75, -1), 'text':'', 'toolTip':'User Name'},
    # {'type':'StaticText', 'name':'lblPassword', 'position':(140, 1), 'text':'Password'},
    # {'type':'PasswordField', 'name':'txtPassword', 'position':(195, 1), 'size':(75, -1), 'text':'', 'toolTip':'Password'},
    # {'type':'StaticText', 'name':'lblDatabase', 'position':(275, 1), 'text':'Database'},
    # {'type':'TextField', 'name':'txtDatabase', 'position':(330, 1), 'size':(75, -1), 'text':'', 'toolTip':'Database name'},
    # {'type':'Button', 'name':'btnConnect', 'position':(415, 1), 'size':(-1, -1), 'label':'Connect', 'toolTip':'Connect to Database'},
    {'type':'StaticText', 'name':'lblTables', 'position':(5, 26), 'text':'Table' },
    {'type':'Choice', 'name':'chsTables', 'position':(60, 26), 'size':(150, -1), 'items':[], 'stringSelection':None},
    {'type':'Button', 'name':'btnBrowse', 'position':(415, 26), 'size':(-1, -1), 'label':'Browse', 'toolTip':'Browse the table data'},
    {'type':'StaticLine', 'name':'lnButtons', 'position':(5, 64), 'size':(490, -1) },
    {'type':'Button', 'name':'btnFirstRow', 'position':(60, 76), 'size':(-1, -1), 'label':'First Row', 'enabled':0, 'command':'firstRecord'},
    {'type':'Button', 'name':'btnPreviousRow', 'position':(147, 76), 'size':(-1, -1), 'label':'Previous Row', 'enabled':0, 'command':'previousRecord'},
    {'type':'Button', 'name':'btnNextRow', 'position':(260, 76), 'size':(-1, -1), 'label':'Next Row', 'enabled':0, 'command':'nextRecord'},
    {'type':'Button', 'name':'btnLastRow', 'position':(351, 76), 'size':(-1, -1), 'label':'Last Row', 'enabled':0, 'command':'lastRecord'}
   ]
  }
 ]
 }
 }

