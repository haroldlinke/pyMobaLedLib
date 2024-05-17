
{ 'application':{ 'type':'Application',
            'name':'Ataxx',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgAtaxx',
    'title':'Ataxx Game',
    'size':( 350, 350 ),
    'statusBar':True,

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
                  'name':'menuFileNewGame',
                  'label':'&New Game\tCtrl+N' },
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ] },
            { 'type':'Menu',
              'name':'mnuStrategy',
              'label':'&Strategy',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuStrategyFlipMostPieces',
                  'label':'Flip Most Pieces',
                  'checkable':1,
                  'checked':1 },
                { 'type':'MenuItem',
                  'name':'menuStrategyRandom',
                  'label':'Random',
                  'checkable':1,
                  'checked':0},
                ]
              }
        ]       
    },

   'components':
   [ 
    { 'type':'BitmapCanvas',
      'name':'bufOff',
      'position':(0, 30),
      'size':(300, 300),
      'backgroundColor':'lightgray',
    },
   ]
  }
 ]
 }
 }

