{ 'application':{ 'type':'Application',
            'name':'worldclock',

    'backgrounds':
 [ 
  {'type':'Background',
   'name':'World Clock bg',
    'title':'World Clock',
    'size':(309, 208),
   'components':
   [ 
    {'type':'Image',  'name':'imageButtonWorld', 'position':( 0, 20 ), 'label':'', 'file':'night.jpg'},
    {'type':'StaticText', 'name':'staticTextClock', 'position':(255, 3)},
    {'type':'StaticText', 'name':'staticTextDate', 'position':(1, 3), 'size':(175, -1)},    
#    {'type':'TextField', 'name':'staticTextClock', 'position':(255, 3), 'editable':0, 'border':'none'},
#    {'type':'TextField', 'name':'staticTextDate', 'position':(1, 3), 'size':(175, -1), 'editable':0, 'border':'none'},    
   ]
  }
 ]
 }
 }

