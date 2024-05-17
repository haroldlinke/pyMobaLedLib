
{ 'application':{ 'type':'Application',
            'name':'PictureViewer',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgPictureViewer',
    'title':'pictureViewer PythonCard Application',
    'size':( 310, 300 ),
    'style':['resizeable'],
    'visible':0,

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
                ] },
            { 'type':'Menu',
              'name':'menuImage',
              'label':'&Image',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuImageHalfSize',
                  'label':'&Half Size\tCtrl+1'},
                { 'type':'MenuItem',
                  'name':'menuImageNormalSize',
                  'label':'&Normal Size\tCtrl+2'},
                { 'type':'MenuItem',
                  'name':'menuImageDoubleSize',
                  'label':'&Double Size\tCtrl+3'},
                { 'type':'MenuItem',
                  'name':'menuImageFillScreenSize',
                  'label':'&Fill Screen\tCtrl+4'},
                { 'type':'MenuItem',
                  'name':'menuImageScaleSize',
                  'label':'&Resize...\tCtrl+5'},
                ] },
        ]
    },

   'components':
   [ 
    { 'type':'BitmapCanvas',
      'name':'bufOff',
      'position':(0, 0),
      'size':(150, 150) },
   ]
  }
 ]
 }
 }

