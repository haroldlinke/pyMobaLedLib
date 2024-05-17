
{ 'application':{ 'type':'Application',
            'name':'Template',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgTemplate',
    'title':'Standard Template with full menus',
    'size':( 400, 300 ),
    'style':['resizeable'],
    'statusBar':1,

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'menuFile',
              'label':'&File',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuFileNew',
                  'label':'&New\tCtrl+N' },
                { 'type':'MenuItem',
                  'name':'menuFileOpen',
                  'label':'&Open\tCtrl+O' },
                { 'type':'MenuItem',
                  'name':'menuFileSave',
                  'label':'&Save\tCtrl+S' },
                { 'type':'MenuItem',
                  'name':'menuFileSaveAs',
                  'label':'Save &As...' },
                { 'type':'MenuItem', 'name':'fileSep1', 'label':'-' },
                { 'type':'MenuItem',
                  'name':'menuFilePageSetup',
                  'label':'Page Set&up...' },
                { 'type':'MenuItem',
                  'name':'menuFilePrint',
                  'label':'&Print...\tCtrl+P' },
                { 'type':'MenuItem',
                  'name':'menuFilePrintPreview',
                  'label':'Print Pre&view' },
                { 'type':'MenuItem', 'name':'fileSep2', 'label':'-' },
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit', } ] },
            # most of the edit menu was copied from the searchexplorer sample
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
                        ] },
            { 'type':'Menu',
              'name':'menuHelp',
              'label':'&Help',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuHelpAbout',
                  'label':'&About ...',
                  'command':'doHelpAbout'},
                ] },
        ]       
    },

   'components':
   [ 
   ]
  }
 ]
 }
 }

