#!/usr/bin/python

"""
__version__ = "$Revision: 1.15 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
"""

from PythonCard import dialog, model, sound
import os.path

class Sounds(model.Background) :
    def on_btnPlay_mouseClick(self, event):
        filename = self.components.fldFilename.text
        async = self.components.chkAsync.checked
        loop = self.components.chkLoop.checked
        # I don't know how to stop a looped sound playing!
        try:
            snd = sound.Sound(filename)
            snd.play(async, loop)
        except sound.SoundFileError:
            base = os.path.basename(filename)
            dialog.alertDialog(self, 'The sound file "%s" is not in a format I can understand.' % base, 'Unknown File Type')
    
    def on_btnFile_mouseClick(self, event):
        # wildcard = "JPG files (*.jpg;*.jpeg)|*.jpg;*.jpeg|GIF files (*.gif)|*.gif|All Files (*.*)|*.*"
        wildcard = "Wave files (*.wav)|*.wav;*.WAV"
        path = ''
        filename = ''
        result = dialog.openFileDialog(wildcard=wildcard)
        if result.accepted:
            s = result.paths[0]
            self.components.fldFilename.text = s


if __name__ == '__main__':
    app = model.Application(Sounds)
    app.MainLoop()
