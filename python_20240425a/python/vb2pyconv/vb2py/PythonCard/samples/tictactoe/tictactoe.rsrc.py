# Changes - 7/25/01 - RDS
#   -Added 'label' item to Menu and MenuItem definitions.
#   -StaticText.label => StaticText.text
#
{ 'application':{ 'type':'Application',
            'name':'TicTacToe',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bg1',
    'title':'Tic Tac Toe',
    'size':( 390, 470 ),
    'image':'lines.jpg',

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            { 'type':'Menu',
              'name':'mnuFile',
              'label':'&File',
              'items': [ 
                { 'type':'MenuItem', 'name':'menuFileExit', 'label':'E&xit', 'command':'exit' } ] }
        ]       
    },

   'components':
   [ 
    { 'type':'CheckBox', 'name':'chkComputerFirst', 'position':( 20, 380 ), 'label':'Mr. Gumby goes first', 'checked':0, 'backgroundColor':'white' },
    { 'type':'Button', 'name':'btnNewGame', 'position':( 280, 380 ), 'label':'New Game' },
    #{ 'type':'Button', 'name':'btnNewGame', 'position':( 5, 450 ), 'label':'New Game' },
    { 'type':'StaticText', 'name':'staticTurn', 'position':( 100, 410 ), 'size':(200, -1), 'text': '', 'alignment':'center', 'backgroundColor':'white' },

    { 'type':'Image',  'name':'btn0', 'position':( 20, 20 ), 'size':(-2,-2), 'file':'empty.gif'},
    
    { 'type':'Image',  'name':'btn1', 'position':( 140, 20 ), 'size':(-2,-2), 'file':'empty.gif'},

    { 'type':'Image',  'name':'btn2', 'position':( 260, 20 ), 'size':(-2,-2), 'file':'empty.gif'},

    { 'type':'Image',  'name':'btn3', 'position':( 20, 140 ), 'size':(-2,-2), 'file':'empty.gif'},

    { 'type':'Image',  'name':'btn4', 'position':( 140, 140 ), 'size':(-2,-2), 'file':'empty.gif'},

    { 'type':'Image',  'name':'btn5', 'position':( 260, 140 ), 'size':(-2,-2), 'file':'empty.gif'},

    { 'type':'Image',  'name':'btn6', 'position':( 20, 260 ), 'size':(-2,-2), 'file':'empty.gif'},

    { 'type':'Image',  'name':'btn7', 'position':( 140, 260 ), 'size':(-2,-2), 'file':'empty.gif'},

    { 'type':'Image',  'name':'btn8', 'position':( 260, 260 ), 'size':(-2,-2), 'file':'empty.gif'}
   ]
  }
 ]
 }
 }

