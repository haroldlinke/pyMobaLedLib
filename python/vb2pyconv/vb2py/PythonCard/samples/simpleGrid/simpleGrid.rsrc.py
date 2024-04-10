
{ 'application':{ 'type':'Application',
            'name':'SimpleGrid',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgMin',
    'title':'Simple Grid PythonCard Application',
    'size':( 600, 400 ),
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
    { 'type':'Grid',
      'name':'mygrid',
      'position':(0, 0),
      'size':(400, 300),
    },
   ]
  }
 ]
 }
 }

