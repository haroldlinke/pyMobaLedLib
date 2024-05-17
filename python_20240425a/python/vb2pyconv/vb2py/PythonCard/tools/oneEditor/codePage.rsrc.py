{'application':{'type':'Application',
          'name':'codeEditor',
    'backgrounds': [
    {'type':'Background',
          'name':'bgCodeEditor',
          'title':'Code Page PythonCard Application',
          'position':(132, 132),
          'size':(407, 308),
          'statusBar':1,
          'visible':0,
          'style':['resizeable'],

         'strings': {
         'saveAs':'Save As',
         'openFile':'Open file',
         'chars':'chars',
         'gotoLine':'Goto line',
         'gotoLineNumber':'Goto line number:',
         'sample':'codeEditor sample',
         'codeEditor':'codeEditor',
         'words':'words',
         'documentChangedPrompt':'The text in the %s file has changed.\n\nDo you want to save the changes?',
         'saveAsWildcard':'All files (*.*)|*.*|Python scripts (*.py;*.pyw)|*.pyw;*.PY;*.PYW;*.py|Text files (*.txt;*.text)|*.text;*.TXT;*.TEXT;*.txt|HTML and XML files (*.htm;*.html;*.xml)|*.htm;*.xml;*.HTM;*.HTML;*.XML;*.html',
         'about':'About codeEditor...',
         'document':'Document',
         'lines':'lines',
         'untitled':'Untitled',
         'replaced':'Replaced %d occurances',
         'scriptletWildcard':'Python files (*.py)|*.py|All Files (*.*)|*.*',
         },

         'components': [

{'type':'CodeEditor', 
    'name':'document', 
    'position':(2, 2), 
    'size':(386, 246), 
    'backgroundColor':(255, 255, 255), 
    },

] # end components
} # end background
] # end backgrounds
} }
