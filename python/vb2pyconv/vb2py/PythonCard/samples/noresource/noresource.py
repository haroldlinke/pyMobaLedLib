#!/usr/bin/python

"""
__version__ = "$Revision: 1.6 $"
__date__ = "$Date: 2004/08/17 19:46:06 $"
"""

from PythonCard import model

rsrc = {'application':{'type':'Application',
          'name':'Minimal',
    'backgrounds': [
    {'type':'Background',
          'name':'bgMin',
          'title':'Minimal PythonCard Application',
          'size':(200, 100),
         'components': [

] # end components
} # end background
] # end backgrounds
} }

class Minimal(model.Background):

    def on_initialize(self, event):
        self.components['field1'] = {'type':'TextField',
                                     'name':'field1',
                                     'position':(5, 5),
                                     'size':(150, -1),
                                     'text':'Hello PythonCard'}

if __name__ == '__main__':
    app = model.Application(Minimal, None, rsrc)
    app.MainLoop()
