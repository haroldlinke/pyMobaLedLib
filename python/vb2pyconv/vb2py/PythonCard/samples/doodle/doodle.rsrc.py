
{ 'application':{ 'type':'Application',
            'name':'Doodle',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgDoodle',
    'title':'Doodle PythonCard Application',
    'size':( 310, 300 ),
    'style':['resizeable'],

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
                  'name':'menuFileOpen',
                  'label':'&Open...\tCtrl+O' },
                { 'type':'MenuItem',
                  'name':'menuFileSaveAs',
                  'label':'Save &As...' },
                { 'type':'MenuItem', 'name':'fileSep1', 'label':'-' },
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ] },
            { 'type':'Menu',
              'name':'menuEdit',
              'label':'&Edit',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuEditCopy',
                  'label':'&Copy\tCtrl+C'},
                { 'type':'MenuItem',
                  'name':'menuEditPaste',
                  'label':'&Paste\tCtrl+V'},
                { 'type':'MenuItem', 'name':'editSep1', 'label':'-' },
                { 'type':'MenuItem',
                  'name':'menuEditClear',
                  'label':'&Clear',
                  'command':'editClear'}
                ] }
        ]       
    },

   'components':
   [ 
    { 'type':'Button',
      'name':'btnColor',
      'position':(0, 0),
      'label':'Color' },
    { 'type':'BitmapCanvas',
      'name':'bufOff',
      'position':(0, 30),
      'size':(300, 230) },
   ]
  }
 ]
 }
 }

