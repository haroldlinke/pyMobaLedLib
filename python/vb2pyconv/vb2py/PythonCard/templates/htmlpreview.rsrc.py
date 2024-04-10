
{ 'application':{ 'type':'Application',
            'name':'HtmlPreview',

    'backgrounds':
 [ 
  { 'type':'Background',
    'name':'bgMin',
    'title':'HTML Preview',
    #'size':(800, 600),
    'statusBar':1,
    'style':['resizeable'],

   'components':
   [ 
    { 'type':'HtmlWindow',
      'name':'html',
      'size':(400, 200),
      'text':''
      },
   ]
  }
 ]
 }
 }

