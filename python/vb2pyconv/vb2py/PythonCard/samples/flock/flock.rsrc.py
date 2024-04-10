
{ 'application':{ 'type':'Application',
            'name':'Flock',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgFlock',
    'title':'Flock PythonCard Application',
    'size':( 310, 300 ),
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
      'name':'btnNewBoid',
      'position':(5, 5),
      'label':'New Boid' },
    { 'type':'Button',
      'name':'btnAnimate',
      'position':(100, 5),
      'label':'Animate' },
    { 'type':'Button',
      'name':'btnStop',
      'position':(200, 5),
      'label':'Stop' },
    { 'type':'BitmapCanvas',
      'name':'bufOff',
      'position':(0, 30),
      'visible':True,
      'size':(300, 230) },
   ]
  }
 ]
 }
 }

