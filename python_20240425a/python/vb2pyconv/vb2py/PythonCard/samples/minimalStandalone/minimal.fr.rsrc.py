
{ 'application':{ 'type':'Application',
            'name':'Minimal',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgMin',
    'title':'Application PythonCard minimum',
    'size':( 200, 100 ),

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'menuFile',
              'label':'Fichier',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'Q&uitter\tAlt+Q',
                  'command':'exit' } ] }
        ]       
    },

   'components':
   [ 
    { 'type':'TextField',
      'name':'field1',
      'position':(5, 5),
      'size':(150, -1),
      'text':'Bonjour PythonCard' },
   ]
  }
 ]
 }
 }

