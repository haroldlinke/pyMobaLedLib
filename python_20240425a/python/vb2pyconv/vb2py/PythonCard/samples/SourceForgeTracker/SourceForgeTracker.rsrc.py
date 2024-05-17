# Changes - 7/25/01 - RDS
#   -Added 'label' item to Menu and MenuItem definitions.
#   -StaticText.label => StaticText.text
#
{ 
    'application':
    { 
        'type':'Application',
        'name':'SourceForgeTracker',

    'menubar': 
    { 
        'type':'MenuBar',
        'menus': 
        [
            {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': 
                [ 
                    {'type':'MenuItem',
                     'name':'menuFileExit',
                     'label':'E&xit\tAlt+X',
                     'command':'exit'}
                    ]
                }
            ]       
    },

    'backgrounds':
    [ 
        { 
            'type':'Background',
            'name':'bgTracker',
            'title':'SourceForge Tracker',
            'size':( 400, 500 ),
            'components':
            [ 
                {'type':'StaticLine', 'name':'staticMenuUnderline', 'position':( 0, 0 ), 'size':( 500, -1 ) },
                { 'type':'StaticText', 'name':'staticStatus', 'position':( 280, 40 ), 'size':(100, -1), 'text':'', 'alignment':'right' },
                { 'type':'Button', 'name':'buttonDownload', 'label':'Update Local Copy', 'position':( 270, 5 ) },
                { 'type':'Choice', 'name':'choiceGroups', 'position':( 10, 5 ), 'items':['PyChecker', 'PyCrust', 'Python', 'PythonCard', 'wxPython'], 'stringSelection':'PythonCard' },
                { 'type':'Choice', 'name':'choiceCategories', 'position':( 130, 5 ), 'items':['Bug Reports', 'Feature Requests'], 'stringSelection':'Bug Reports'},
                { 'type':'StaticText', 'name':'staticTopics', 'position':( 5, 40 ), 'text':'Topics' },
                { 'type':'List', 'name':'topicList', 'position':( 0, 55 ), 'size':( 390, 115 ) },
                { 'type':'StaticText', 'name':'staticDetail', 'position':( 5, 185 ), 'text':'Details' },
                { 'type':'TextArea', 'name':'topicDetail', 'position':( 0, 200 ), 'size':( 390, 250 ), 'editable':0 }
            ]
        } 
    ]
}
}

