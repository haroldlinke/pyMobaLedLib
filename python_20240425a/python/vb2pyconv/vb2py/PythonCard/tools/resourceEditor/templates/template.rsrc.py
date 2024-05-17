
{ 'application':{ 'type':'Application',
            'name':'Template',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgTemplate',
    'title':'Standard Template with File->Exit menu',
    'size':( 400, 300 ),
    'style':['resizeable'],
    'statusBar':0,

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
                  'name':'menuFileExit',
                  'label':'E&xit',
                  'command':'exit', } ] }
        ]       
    },

   'components':
   [ 
   ]
  }
 ]
 }
 }

