
{ 'application':{ 'type':'Application',
            'name':'Conversions',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgConversions',
    'title':'Conversions',
    'size':( 400, 350 ),

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'mnuFile',
              'label':'&File',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit',
                  'command':'exit' } ] },
            { 'type':'Menu',
              'name':'mnuConvert',
              'label':'&Convert',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuConvertMorseCode',
                  'label':'Morse Code',
                  'checkable':1 },
                { 'type':'MenuItem',
                  'name':'menuConvertTemperature',
                  'label':'Temperature',
                  'checkable':1,
                  'checked':1},
                { 'type':'MenuItem',
                  'name':'menuConvertCurrencyUKUS',
                  'label':'Currency - UK <-> US',
                  'checkable':1 },
                { 'type':'MenuItem',
                  'name':'menuConvertCurrencyAUSUS',
                  'label':'Currency - AUS <-> US',
                  'checkable':1 },
                ]
              }
        ]       
    },

   'components':
   [ 
    { 'type':'StaticLine', 'name':'staticlineH', 'position':(0, 0), 'size':(400, -1)},
    { 'type':'StaticText', 'name':'labelUp', 'position':(5, 5), 'text': 'one'},
    { 'type':'StaticText', 'name':'labelDown', 'position':(5, 165), 'text': 'two'},
    { 'type':'TextArea',
      'name':'field1',
      'position':(5, 25),
      'size':(390, 100),
      'text':'' },
    { 'type':'TextArea',
      'name':'field2',
      'position':(5, 190),
      'size':(390, 100),
      'text':'' },
    { 'type':'Button',
      'name':'btnConvertUp',
      'position':(175, 160),
      'size':(200, -1),
      'label':'Convert to' },
    { 'type':'Button',
      'name':'btnConvertDown',
      'position':(175, 130),
      'size':(200, -1),
      'label':'Convert to' },
   ]
  }
 ]
 }
 }

