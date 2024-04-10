mp3player is a quick sample I wrote during one of the VanPy Workshop '04 presentations. mp3player uses the Movie class of PyGame to do all the real work.

http://www.pygame.org/docs/ref/Movie.html

It might make more sense to just roll MP3 support into the PythonCard.sound module except that it will require PyGame to work and Movie has a lot more playback options than the WAV file playback in wxPython.
