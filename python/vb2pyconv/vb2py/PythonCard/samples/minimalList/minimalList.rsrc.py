
{ 'application':{ 'type':'Application',
            'name':'Minimal',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgMin',
    'title':'Minimal PythonCard Application',
    'size':( 400, 400 ),

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'menuFile',
              'label':'File',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ] }
        ]       
    },

   'components':
   [ 
    { 'type':'MultiColumnList',
      'name':'list',
      'position':(0, 30),
      'size':(350, 200),
      'columns':3,
      'rules':0
      },
   ]
  }
 ]
 }
 }

