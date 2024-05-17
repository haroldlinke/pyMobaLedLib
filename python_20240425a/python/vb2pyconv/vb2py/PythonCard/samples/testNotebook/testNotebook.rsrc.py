
{ 'application':{ 'type':'Application',
            'name':'Minimal',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgMin',
    'title':'Notebook Test',
    'size':( 800, 600 ),
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
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ] }
        ]       
    },

   'components':
   [ 
    { 'type':'Notebook',
      'name':'notebook',
      'position':(5, 5),
      'size':(785, 540),
    },
   ]
  }
 ]
 }
 }

