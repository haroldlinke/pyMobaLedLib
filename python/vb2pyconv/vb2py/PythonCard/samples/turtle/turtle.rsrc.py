# Revision: $Revision: 1.12 $
# Date:     $Date: 2004/05/10 05:02:45 $

{ 'application':{ 'type':'Application',
            'name':'Turtle',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgTurtle',
    'title':'Turtle Test',
    'size':( 750, 600 ),
    'statusBar':1,
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
                  'name':'menuFileOpen',
                  'label':"&Open File...\tCtrl+O" },
                { 'type':'MenuItem',
                  'name':'menuFileDrawTurtle',
                  'label':"Draw &Turtle\tCtrl+T" },
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ] },
            { 'type':'Menu',
              'name':'menuCommands',
              'label':'&Commands',
              'items': [ 
                { 'type':'MenuItem',
                  'name':'menuCommandsClear',
                  'label':"Clear Screen" },
                { 'type':'MenuItem', 'name':'commandsSep1', 'label':'-' },
                { 'type':'MenuItem',
                  'name':'menuCommandsAutoRefresh',
                  'label':'Auto Refresh',
                  'checkable':1,
                  'checked':1},
                ] }
        ]       
    },

   'components':
   [ 
    { 'type':'BitmapCanvas',
      'name':'bufOff',
      'position':(0, 30),
      'size':(750, 600) },
    #{ 'type':'Button', 'name':'btnRun', 'position':(5, 5), 'label':'Run' },
    #{ 'type':'StaticLine', 'name':'sep1', 'position':(0, 0), 'size':(750, -1) },
   ]
  }
 ]
 }
 }

