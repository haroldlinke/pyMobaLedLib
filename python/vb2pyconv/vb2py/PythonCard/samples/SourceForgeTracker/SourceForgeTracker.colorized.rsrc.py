# Changes - 7/25/01 - RDS
#   -Added 'label' item to Menu and MenuItem definitions.
#   -StaticText.label => StaticText.text
#
{ 
    'application':
    { 
        'type':'Application',
        'name':'SourceForgeTracker',

    'backgrounds':
    [ 
        { 
            'type':'Background',
            'name':'bgTracker',
            'title':'SourceForge Tracker',
            'size':( 400, 510 ),
            'backgroundColor':'aliceblue',

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

            'components':
            [ 
                {'type':'StaticLine', 'name':'staticMenuUnderline', 'position':( 0, 0 ), 'size':( 500, -1 ) },
                { 'type':'StaticText', 'name':'staticStatus', 'position':( 280, 48 ), 'size':(100, -1), 'text':'', 'alignment':'right', 'backgroundColor':'#B9DAF5' },
                { 'type':'Button', 'name':'buttonDownload', 'label':'Update Local Copy', 'position':( 265, 10 ), 'size':(115, -1) },
                { 'type':'Choice', 'name':'choiceGroups', 'position':( 12, 10 ), 'items':['PyChecker', 'PyCrust', 'Python', 'PythonCard', 'wxPython'], 'stringSelection':'PythonCard' },
                { 'type':'Choice', 'name':'choiceCategories', 'position':( 130, 10 ), 'items':['Bug Reports', 'Feature Requests'], 'stringSelection':'Bug Reports'},
                {'type':'Image', 'name':'imgChoices', 'position':( 3, 4 ), 'size':( 386, 35 ), 'file':'', 'backgroundColor':'#6996E0' },
                { 'type':'StaticText', 'name':'staticTopics', 'position':( 8, 48 ), 'text':'Topics', 'backgroundColor':'#B9DAF5' },
                {'type':'Image', 'name':'imgTopics', 'position':( 5, 45 ), 'size':( 383, 18 ), 'file':'', 'backgroundColor':'#B9DAF5' },
                { 'type':'List', 'name':'topicList', 'position':( 4, 65 ), 'size':( 384, 115 ) },
                { 'type':'StaticText', 'name':'staticDetail', 'position':( 8, 192 ), 'text':'Details', 'backgroundColor':'#B9DAF5' },
                {'type':'Image', 'name':'imgDetail', 'position':( 5, 190 ), 'size':( 383, 18 ), 'file':'', 'backgroundColor':'#B9DAF5' },
                { 'type':'TextArea', 'name':'topicDetail', 'position':( 4, 210 ), 'size':( 384, 250 ), 'editable':0 }
            ]
        } 
    ]
}
}

