# Changes - 7/25/01 - RDS
#   -Added 'label' item to Menu and MenuItem definitions.
#   -StaticText.label => StaticText.text
#
{ 'application':{ 'type':'Application',
            'name':'Proof',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bg1',
    'title':'PC Proof of Concept',
    'size':( 400, 300 ),
    #'image':'background.jpg',
    'image':'tile.bmp',
    'tiled':1,

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'mnuFile',
              'label':'&File',
              'items': [ 
                #{ 'type':'MenuItem', 'name':'mnuOpenStack', 'label': 'Open Stack', 'command':'OpenStack' },
                #{ 'type':'MenuItem', 'name':'-', 'label':'-' },
                { 'type':'MenuItem', 'name':'mnuExit', 'label':'Exit' } ] }
        ]       
    },

   'components':
   [ 
    { 'type':'TextField', 'name':'field1', 'position':( 5, 4 ), 'size':(200, -1) },
    
    { 'type':'TextArea', 'name':'field2', 'position':( 225, 4 ), 'size':( 150, 100 ), 'text':'' },
    
    { 'type':'Button', 'style':'3d', 'name':'button1', 'position':( 5, 50 ), 'size':( 80, 20 ), 'label':'Button 1' },
    
    { 'type':'PasswordField', 'name':'password1', 'position':( 225, 115 ), 'size':( -1, -1 ), 'text':'' },
    
    { 'type':'Button', 'name':'button2', 'position':( 100, 50 ), 'size':( 80, 20 ), 'label':'Button 2' },
    
    { 'type':'StaticText', 'name':'label', 'position':( 5, 210 ), 'size':( 80, 20 ), 'text': 'some text', 'alignment':'center' },
    
    { 'type':'RadioGroup', 'name':'radiogroup', 'position':( 5, 100 ), 'label':'A RadioBox', 'items':[ 'one', 'two', 'five', 'three, sir' ], 'stringSelection':'two', 'layout':'vertical'},
    
    { 'type':'Choice', 'name':'choice', 'position':( 120, 190 ), 'size':( 80, 20 ),'label':'A Choice', 'items':[ 'one', 'two', 'five', 'three, sir' ], 'stringSelection':'five' },
    
    { 'type':'List', 'name':'list', 'position':( 120, 100 ), 'size':( 80,80 ),'items':[ 'one', 'two', 'five', 'three, sir' ], 'stringSelection':'three, sir' },
    
    { 'type':'CheckBox', 'name':'checkbox', 'position':( 5, 230 ), 'size':( 80, 20 ), 'label':'Check box', 'checked':0 },
    
    { 'type':'Slider', 'name':'aSlider', 'position':( 285, 220 ), 'size':( 100, 15 ), 'min':1, 'max':100, 'value':1, 'layout':'horizontal' },
    
    { 'type':'Image', 'name':'image', 'position':( 120, 220 ), 'size':( -2, -2 ), 'file':'trash.gif'},
    
    { 'type':'ImageButton',  'name':'imagebtn', 'position':( 200, 220 ), 'size':( -2, -2 ), 'file':'edit.gif'},

    { 'type':'StaticLine', 'name':'staticlineV', 'position':( 215, 5 ), 'size':( -1, 200 ), 'layout':'vertical' },

    { 'type':'StaticLine', 'name':'staticlineH', 'position':( 5, 80 ), 'size':( 200, -1 ) }
   ]
  }
 ]
 }
 }

