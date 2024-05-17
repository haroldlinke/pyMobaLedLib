{ 'application':{ 'type':'Application',
            'name':'Test Sounds',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'Test Sounds',
    'title':'Test Sounds',
    'position':( 5, 5 ),
    'size':( 300, 200 ),

    'menubar': 
    {   
        'type':'MenuBar', 
        'menus': 
        [
            { 'type':'Menu', 
              'name':'File', 
              'label':'&File', 
              'items': [ 
                { 'type':'MenuItem',  'name':'menuFileExit', 'label':'Exit', 'command':'exit' } ] }
        ]       
    },

   'components':
   [ 
    { 'type':'TextField', 'name':'fldFilename', 'position':( 5, 4 ), 'size':( 200, -1 ), 'text':'anykey.wav' },
    { 'type':'Button', 'name':'btnFile', 'position':( 210, 5 ), 'size':( -1, -1), 'label':'Select File' },
    { 'type':'Button', 'name':'btnPlay', 'position':( 5, 40 ), 'size':( -1, -1 ), 'label':'Play' },
    { 'type':'CheckBox', 'name':'chkAsync', 'position':( 5, 70 ), 'size':( -1, -1 ), 'label':'Async I/O', 'checked':0 },
    { 'type':'CheckBox', 'name':'chkLoop', 'position':( 5, 90 ), 'size':( -1, -1 ), 'label':'Loop sound', 'checked':0 },
   ]
  }
 ]
 }
 }

