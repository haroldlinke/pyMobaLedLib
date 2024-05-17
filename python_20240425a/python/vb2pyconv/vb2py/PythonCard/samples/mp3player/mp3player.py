#!/usr/bin/python

"""
We should try and make this work on platforms other than the Mac. 
"""
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"

from PythonCard import dialog, model
import os

class MyBackground(model.Background):

    def on_initialize(self, event):
        # KEA 2004-08-03
        # this is only going to work on the Mac
        # so it will need to be generalized later
        home = os.environ['HOME']
        self.buildList(os.path.join(home, 'Music/iTunes/iTunes Music'))

    # http://www.pygame.org/docs/ref/Movie.html

    def on_load_mouseClick(self, event):
        filename = self.components.filename.text
        path, filename = os.path.split(filename)
        wildcard = "MP3 files (*.mp3)|*.mp3"
        result = dialog.openFileDialog(self, 'Open', path, filename, wildcard )
        if result.accepted:
            path = result.paths[0]
            self.components.filename.text = path
        
    def on_play_mouseClick(self, event):
        filename = self.components.filename.text
        ## NOTE WE DON'T IMPORT PYGAME UNTIL NOW.  Don't put "import pygame" at the top of the file.
        import pygame
        self.movie = pygame.movie.Movie(filename)
        self.movie.play()
        
        # it was a good idea at first, but mixer simply doesn't work, at least on the Mac
##        assert os.path.exists(filename)
##        from pygame import mixer
##        mixer.init(44100, 2)
##        mixer.music.load(filename)
##        mixer.music.play()
##        print mixer.music.get_busy()
##        #time.sleep(5)
##        #mixer.music.stop()

    def on_pause_mouseClick(self, event):
        try:
            self.movie.pause()
        except:
            pass

    def on_stop_mouseClick(self, event):
        try:
            self.movie.stop()
            self.movie.rewind()
        except:
            pass

    def buildList(self, path):
        mp3s = []
        names = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith('.mp3'):
                    mp3s.append((root, name))
                    names.append(name)
        self.mp3s = mp3s
        self.components.mp3s.items = names

    def on_mp3s_select(self, event):
        sel = event.target.selection
        self.components.filename.text = os.path.join(self.mp3s[sel][0], self.mp3s[sel][1])

if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
