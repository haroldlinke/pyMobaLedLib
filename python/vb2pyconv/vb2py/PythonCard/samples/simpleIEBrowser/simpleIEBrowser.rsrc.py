
{ 'application':{ 'type':'Application',
            'name':'SimpleIEBrowser',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgMin',
    'title':'SimpleIEBrowser PythonCard Application',
    'size':(800, 600),
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
                  'label':'&Open\tCtrl+O' },
                { 'type':'MenuItem', 'name':'fileSep1', 'label':'-' },
                { 'type':'MenuItem',
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ] }
        ]       
    },

   'components':
   [ 
{'type':'ComboBox', 
    'name':'fldURL', 
    'position':(200, 0), 
    'size':(300, -1), 
    #'text':'http://www.python.org/',
    },
{'type':'Button', 
    'name':'btnGo', 
    'position':(550, 0), 
    'label':'Go',
    'default':1,
    'command':'goURL',
    },
{'type':'Button', 
    'name':'btnBack', 
    'position':(0, 0), 
    'label':'Back',
    'command':'goBack',
    },
{'type':'Button', 
    'name':'btnForward', 
    'position':(100, 0), 
    'label':'Forward',
    'command':'goForward',
    },
{'type':'Button', 
    'name':'btnReload', 
    'position':(200, 0), 
    'label':'Reload',
    'command':'goReload',
    },
    { 'type':'IEHtmlWindow',
      'name':'htmlDisplay',
      'position':(0, 30),
      'size':(750, 550),
      #'text':'<html><head><title>Hello</title></head><body>Hello HTML World</body></html>'
      #'text':'index.html'
      #'text':'http://diveintopython.org/toc.html'
      #'text':'http://www.python.org/doc/current/lib/lib.html'
      },
   ]
  }
 ]
 }
 }

