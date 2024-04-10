{ 'application':{ 'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':'Stock Price Getter',
          'size':(394, 222),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit',
                   'command':'exit',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'TextField', 
    'name':'fldStockSymbol', 
    'position':(150, 5), 
    'size':(60, -1), 
    },

{'type':'Choice', 
    'name':'chcCurrency', 
    'position':(150, 35), 
    'size':(-1, 21), 
    'items':['United States'], 
    'stringSelection':'United States', 
    },

{'type':'Button', 
    'name':'btnGetPrice', 
    'position':(150, 65), 
    'label':'Get price',
    'default':1, 
    },

{'type':'TextField', 
    'name':'fldStockPrice', 
    'position':(150, 105), 
    'size':(75, -1), 
    'editable':0, 
    },

{'type':'TextField', 
    'name':'fldDate', 
    'position':(150, 140), 
    'size':(231, -1), 
    'editable':0, 
    },

{'type':'StaticText', 
    'name':'stcDate', 
    'position':(5, 145), 
    'size':(100, -1), 
    'font':{'family': 'sansSerif', 'style': 'bold'}, 
    'text':'Date:', 
    },

{'type':'StaticText', 
    'name':'stcStockPrice', 
    'position':(5, 110), 
    'size':(130, -1), 
    'font':{'family': 'sansSerif', 'style': 'bold'}, 
    'text':'Latest Stock price:', 
    },

{'type':'StaticText', 
    'name':'stcCurrencyType', 
    'position':(5, 40), 
    'size':(141, -1), 
    'font':{'family': 'sansSerif', 'style': 'bold'}, 
    'text':'Choose Currency:', 
    },

{'type':'StaticText', 
    'name':'stcStockSymbol', 
    'position':(5, 10), 
    'size':(135, -1), 
    'font':{'family': 'sansSerif', 'style': 'bold'}, 
    'text':'Enter Stock Symbol:', 
    },

] # end components
} # end background
] # end backgrounds
} }
