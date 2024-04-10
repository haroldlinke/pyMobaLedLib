{'application':{'type':'Application',
          'name':'Lexicon',
    'backgrounds': [
    {'type':'Background',
          'name':'bgLexicon',
          'title':'Lexicon',
          'size':(466, 270),

         'components': [

{'type':'Button', 
    'name':'btnLoad', 
    'position':(376, 196), 
    'label':'Load', 
    },

{'type':'StaticText', 
    'name':'stcSize', 
    'position':(157, 200), 
    'text':'Size:', 
    },

{'type':'CodeEditor', 
    'name':'fldDescription', 
    'position':(155, 0), 
    'size':(300, 191), 
    'editable':0,
    },

{'type':'List', 
    'name':'lstPatterns', 
    'position':(0, 0), 
    'size':(150, 221), 
    'items':[], 
    },

] # end components
} # end background
] # end backgrounds
} }
