#!/usr/bin/python

"""
Moderator, as you may have guessed, is a moderation tool. 

As someone raises their hand to speak, the moderator clicks their name and it goes on the list of people waiting to speak, in order. When someone is speaking, they have a certain number of minutes to speak. It works best when there's a projector, so everyone can see they're on the list and the speaker can see how much time they have left.

Contributed to the PythonCard community 4/23/2004 by Bruce Eckel
"""
__version__ = "$Revision: 1.9 $"
__date__ = "$Date: 2005/12/13 11:13:23 $"

import sys
from PythonCard import dialog, model, timer

# maximum time per speaker in seconds
MAX_TIME = 5 * 60
#MAX_TIME = 180
DELEGATE_FILE = "delegates.txt"

class Moderator(model.Background):
    def on_initialize(self, event):
        self.clockTimer = timer.Timer(self.components.txtTime, -1)
        self.clockModel = CountdownClockModel(MAX_TIME)        
        self.delegates = ModeratorModel()
        if len(sys.argv) > 1:
            fname = sys.argv[1]
        else:
            fname = DELEGATE_FILE
        try:
            lines = open(fname).readlines()
        except IOError:
            lines = []
        for delegate in lines:
            if delegate.strip():
                self.delegates.add(delegate.strip())            
        self.update()

    def on_close(self, event):
        self.clockTimer.stop()
        event.skip()
        
    def shift(self):
        if self.delegates.queue():
            self.delegates.shift()
            self.clockModel.reset()
            self.clockTimer.start(1000)
        else:
            self.clockTimer.stop()
        self.update()
    
    def on_timer(self, event):
        self.clockModel.tick()
        if self.clockModel.done():
            self.shift()
        self.update()
    
    def on_lstDelegates_select(self, event):
        delegate = self.components.lstDelegates.stringSelection
        if not delegate:
            return
        self.delegates.enqueue(delegate)
        if not self.clockTimer.isRunning():
            self.shift()
        self.update()

    def on_lstQueue_select(self, event):
        delegate = self.components.lstQueue.stringSelection
        if not delegate:
            return
        self.delegates.dequeue(delegate)
        self.update()

    def on_btnPause_mouseClick(self, event):
        self.clockModel.pause()

    def on_btnNext_mouseClick(self, event):
        self.shift()
    
    def update(self):
        if self.components.lstDelegates.items != self.delegates.idle():
            self.components.lstDelegates.items = self.delegates.idle()
        if self.components.lstQueue.items != self.delegates.queue():  
            self.components.lstQueue.items = self.delegates.queue()      
        if self.components.txtSpeaker.text != self.delegates.speaker():
            self.components.txtSpeaker.text = self.delegates.speaker()
        if self.components.txtTime.text != self.clockModel.readout():
            self.components.txtTime.text = self.clockModel.readout()

    def on_btnAddSpeaker_mouseClick(self, event):
        result = dialog.textEntryDialog(self, 'Speaker:', 'Add Speaker', 'First Last')
        if result.accepted:
            text = result.text
            #self.components.lstDelegates.append(text)
            self.delegates.add(text.strip())
            self.update()

class CountdownClockModel:
    def __init__(self, max):
        assert max > 0
        self.max = max
        self.reset()

    def tick(self):
        if not self.paused:
            self.count += 1

    def pause(self):
        self.paused = not self.paused

    def reset(self):
        self.count = 0
        self.paused = 0
        
    def done(self):
        return self.count == self.max
    
    def readout(self):
        remaining = self.max - self.count
        return "%d:%02d" % (remaining / 60, remaining % 60)

class ModeratorModel:
    def __init__(self):
        self._idle = []
        self._queue = []
        self._speaker = ""
    
    def add(self, delegate):
        assert delegate
        self._idle.append(delegate)
    
    def enqueue(self, delegate):
        assert delegate
        self._idle.remove(delegate)
        self._queue.append(delegate)
    
    def dequeue(self, delegate):
        assert delegate
        self._queue.remove(delegate)
        self._idle.append(delegate)
    
    def shift(self):
        if self._speaker:
            self._idle.append(self._speaker)
            
        if self._queue:          
            self._speaker = self._queue.pop(0)        
        else:
            self._speaker = ""
            
    def speaker(self):
        return self._speaker
    
    def queue(self):
        return self._queue
    
    def idle(self):
        return self._idle

if __name__ == '__main__':
    app = model.Application(Moderator)
    app.MainLoop()
