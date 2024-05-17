
{ 'application':{ 'type':'Application',
            'name':'MulticolumnExample',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgMulticolumnExample',
    'title':'Multicolumn Example PythonCard Application',
    'size':( 620, 500 ),

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
                  'name':'menuFileExit',
                  'label':'E&xit\tAlt+X',
                  'command':'exit' } ] }
        ]       
    },

   'components':
   [ 
{'type':'Button', 
    'name':'demoButton', 
    'position':(510, 5), 
    'size':(85, 25), 
    'label':'Load Demo', 
    },

{'type':'Button', 
    'name':'clearButton', 
    'position':(510, 30), 
    'size':(85, 25), 
    'label':'Clear', 
    },

{'type':'Button', 
    'name':'loadButton', 
    'position':(510, 55), 
    'size':(85, 25), 
    'label':'Load CSV', 
    },

{'type':'Button', 
    'name':'appendButton', 
    'position':(510, 80), 
    'size':(85, 25), 
    'label':'Append CSV', 
    },

{'type':'Button', 
    'name':'swapButton', 
    'position':(510, 105), 
    'size':(85, 25), 
    'label':'Swap Lists', 
    },

{'type':'Button', 
    'name':'prevButton', 
    'position':(510, 130), 
    'size':(85, 25), 
    'label':'Prev', 
    },

{'type':'Button', 
    'name':'nextButton', 
    'position':(510, 155), 
    'size':(85, 25), 
    'label':'Next', 
    },

{'type':'Button', 
    'name':'exitButton', 
    'position':(510, 180), 
    'size':(85, 25), 
    'label':'Exit', 
    },

{'type':'MultiColumnList', 
    'name':'theList', 
    'position':(3, 3),  #10, 305
    'size':(500, 390), 
    'columnHeadings': ['Example List'],
    'items':['Example 1','Example 2','Example 3'], 
    },
{'type':'TextArea', 
    'name':'displayArea', 
    'position':(3, 398), 
    'size':(500, 40), 
    'font':{'family': 'monospace', 'size': 12}, 
    },
    
{'type':'TextArea', 
    'name':'countArea', 
    'position':(507, 398), 
    'size':(85, 40), 
    'font':{'family': 'monospace', 'size': 12}, 
    },

   ]
  }
 ]
 }
 }

