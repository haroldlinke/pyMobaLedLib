"""
__version__ = "$Revision: 1.7 $"
__date__ = "$Date: 2005/09/18 03:59:21 $"
"""

import wx
import sndhdr

class SoundFileError(Exception):
    pass

class Sound:
    """
    Feeble beginnings of a class for playing sounds.
    The goal is to be able to provide a filename and then be able
    to play the sound without worrying about sound formats or particular
    OS capabilities. I haven't investigated the Python Standard Libraries
    much yet.
    """
    
    def __init__(self, filename) :
        self._filename = filename
        self._sndType = sndhdr.what(filename)
        if self._sndType:
            self._sndType = self._sndType[0]
        if self._sndType in ['wav']:
            try:
                self._sound = wx.Sound(filename)    # support resources?
            except:
                self._sndType = None
        else:
            self._sndType = None
        if not self._sndType:
            raise SoundFileError, 'This is not a valid sound file'

    def play(self, async=True, looped=False) :
        if self._sndType:
            if async:
                if looped:
                    flags = wx.SOUND_ASYNC | wx.SOUND_LOOP
                else:
                    flags = wx.SOUND_ASYNC
            else:
                flags = wx.SOUND_SYNC
            self._sound.Play(flags)

    def stop(self):
        if self._sndType:
            self._sound.Stop()
