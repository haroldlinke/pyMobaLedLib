#!/usr/bin/env python
"""
__version__ = "$Revision: 1.28 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"

translation of Dan Winkler's PythonCard demo from 
Tk to wxWindows (wxPythonCard.py) by Neil Hodgson
wxWindows to PythonCard by Kevin Altis

the first version also used ZODB, but since I've been trying to track
  down what I think is an error related to ZODB, I may go ahead and
  blow away ZODB or just comment it out and use something else since
  right now the stack is getting corrupted. I haven't gone back yet
  to see if this happens with Neil's initial port.
changed self.stack references to self.wstack (winkler stack) to avoid
  name collision with PythonCard stack variable
changed wxTextCtrl method calls to dot notation PythonCard TextArea calls
renamed the methods called during menu events to be command events
this also shows off doing command events for the Edit menu items which
  are otherwise identical to the ones in the searchexplorer sample

"""

from PythonCard import configuration, dialog, model

import wx
import time
from journal import *
import ZODB
from Persistence import Persistent
from ZODB.PersistentList import PersistentList
from ZODB import DB, FileStorage
import BTrees
from BTrees import OOBTree
import re
import string
import os


class CardStack(Persistent):

    def __init__(self):
        self._v_current_card = 0
        self._v_text = None
        self._v_cardNumber = None        
        self.last_id = 0
        self.card_list = PersistentList()
        self.to_be_indexed = PersistentList()
        self.card_store = OOBTree.OOBTree()
        self.hint_store = OOBTree.OOBTree()
        self.CreateCard(at_end=1, and_set=0)

    def SetHints(self, id, hints):
        if self.to_be_indexed[0] == id:
            self.hint_store[id] = hints
            del self.to_be_indexed[0]
        else: print "Not saving hints for card id", id, "because card has been deleted."

    def StoreText(self, id, text):
        self.card_store[id] = self.Compress(text)
        self.hint_store[id] = None
        if id not in self.to_be_indexed:
            self.to_be_indexed.append(id)
        get_transaction().commit()

    def GetText(self, id):
        return self.Decompress(self.card_store[id])

    def DeleteCard(self):
        if len(self.card_list) <= 1: return
        id = self.card_list[self._v_current_card]
        del self.card_list[self._v_current_card]
        del self.card_store[id]
        del self.hint_store[id]
        self.SetCard(self._v_current_card)
 
    def NewCard(self):
        self.SaveCurrentCard()
        self.CreateCard()

    def CreateCard(self, at_end=0, text="", and_set=1):
        id = self.last_id + 1
        self.last_id = id
        if at_end:
            self.card_list.append(id)
        else:
            self.card_list.insert(self._v_current_card + 1, id)
        self.StoreText(id, text)
        if and_set:
            self.SetCard(self._v_current_card + 1)

    def SetCard(self, card_num):
        if card_num >= len(self.card_list):
            card_num = len(self.card_list) - 1
        if card_num < 0: card_num = 0
        self._v_current_card = card_num
        id = self.card_list[card_num]
        card_text = self.GetText(id)
        self._v_text.text = card_text
        self._v_cardNumber.text = 'Card: ' + str(card_num + 1)
        print "Card", card_num + 1, "of", len(self.card_list)

    def SaveCurrentCard(self):
        text = self._v_text.text
        id = self.card_list[self._v_current_card]
        self.StoreText(id, text)

    def Decompress(self, text):
        if len(text) == 0: return text
        flag_index = len(text)-1
        flag = text[flag_index]
        if flag == chr(0): return text[0:-1]
        from zlib import decompress
        return decompress(text[0:-1])

    def Compress(self, text):
        old_len = len(text)
        if old_len == 0: return text
        from zlib import compress
        start_time = time.time()
        compressed = compress(text, 9)
        elapsed_time = time.time() - start_time
        new_len = len(compressed)
        if new_len < old_len:
            print "compressed", old_len, "bytes by", old_len - new_len, "bytes"
            return compressed + chr(1)
        print "leaving text of len", old_len, "uncompressed."
        return text + chr(0)

    def GoNext(self, dummy=""):
        self.SaveCurrentCard()
        self.SetCard(self._v_current_card + 1)

    def GoPrev(self, dummy=""):
        self.SaveCurrentCard()
        self.SetCard(self._v_current_card - 1)

    def GoFirst(self):
        self.SaveCurrentCard()
        self.SetCard(0)

    def GoLast(self):
        self.SaveCurrentCard()
        self.SetCard(len(self.card_list)-1)

    def ImportStack(self):
        """imports stacks of the format described in
        Managing Gigabytes
        Compressing and Indexing Documents and Images
        Second Edition, 1999
        http://www.cs.mu.oz.au/mg/
        source at http://www.cs.mu.oz.au/mg/mg-1.2.1.tar.gz
        """
        wildcard = "stack files (*.stack)|*.stack|All Files (*.*)|*.*"
        result = dialog.openFileDialog(None, "Import which stack?", '', '', wildcard)
        if result.accepted:
            path = result.paths[0]
            file = open(path, "r")
            cards = file.read().split(str(chr(2)))
            for text in cards:
                self.CreateCard(at_end=1, text=re.sub("\r", "\n", text), and_set=0)
            file.close()
            self.SetCard(0)

class Hinter:

    min_stem = 3
    max_stem = 4
    strip_chars = ""
    spaces = None
    table = None

    def __init__(self, stack, id):
        self.start_time = time.time()
        self.wstack = stack
        self.id = id
        self.stage = 0
        self.hints = 0
        if self.strip_chars == "":
            for char in range(0,256):
                if not chr(char) in (string.letters + string.digits):
                    self.strip_chars = self.strip_chars + chr(char)
            self.spaces = " " * len(self.strip_chars)
            self.table = string.maketrans(self.strip_chars, self.spaces)
        text = stack.GetText(id)
        self.words = text.translate(self.table).split()       
 
    def GetNextStem(self):
        if self.curr_stem < len(self.stems):
            stem = self.stems[self.curr_stem]
            self.curr_stem = self.curr_stem + 1
            return stem
        return ""

    def ComputeHint(self, stem):
        import whrandom
        generator = whrandom.whrandom()
        generator.seed(ord(stem[0]), ord(stem[1]), ord(stem[2]))
        nbits = 0
        try_count = 0

        hint_bits = 0
        while nbits < self.codeword_set and try_count < self.codeword_set * 20:
            try_count = try_count + 1
            bit_num = generator.randint(0, self.codeword_len*8-1)
            bit_mask = 1L << bit_num
            if not hint_bits & bit_mask: # not yet set
                hint_bits = hint_bits | bit_mask
                nbits = nbits + 1

        return hint_bits

    def StemNextWord(self):
        # trim, lowercase, uniq
        stem = self.words[self.curr_word][0:self.max_stem]
        self.curr_word = self.curr_word + 1
        if len(stem) >= self.min_stem:
          stem = stem.lower()
          self.stems[stem] = 1;

    def DoOneIdleStep(self):
        step_start_time = time.clock()
        if self.stage == 0:
            # set up to compute stems
            self.curr_word = 0
            self.stems = {}
            self.stage = 1
            return 0 # not done
        elif self.stage == 1:
            # compute a few stems
            while time.clock() - step_start_time < 0.01:
                if self.curr_word < len(self.words):
                    self.StemNextWord()
                else:
                    # done computing stems, set up for computing hints
                    self.words = None
                    self.stems = self.stems.keys()
                    print len(self.stems), "unique stems"
                    from math import log
                    pf = 1.0/1000
                    w = (1/log(2)*log(1/pf))
                    m = (1/log(2))**2*len(self.stems)*log(1/pf)
                    self.codeword_len = int(round(m/8)) 
                    self.codeword_set = int(round(w))
                    print self.codeword_len, "hint bytes for this card"
                    print self.codeword_set, "bits set per stem"
                    self.curr_stem = 0
                    self.stage = 2
                    return 0 # not done
            return 0 # not done
        elif self.stage == 2:
            # compute a few  hints
            while time.clock() - step_start_time < 0.01:
                stem = self.GetNextStem()
                if stem <> "":
                    self.hints = self.hints | self.ComputeHint(stem)
                else:
                    #print self.hints
                    print "indexed card id", self.id, "in", \
                          round(time.time() - self.start_time,2), "seconds"
                    self.wstack.SetHints(self.id, self.hints)
                    return 1 # done
            return 0 # not done

#class CardFrame(wx.Frame):
class CardFrame(model.Background):

    def on_initialize(self, event):
        self.configPath = os.path.join(configuration.homedir, 'textindexer')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        self.filename = os.path.join(self.configPath, 'zhome.stack')
        
        self.storage = FileStorage.FileStorage(self.filename)
        db = DB(self.storage)
        self.connection = conn = db.open()
        dbroot = conn.root()
        if not dbroot.has_key('stack'):
            dbroot['stack'] = CardStack()
        stack = dbroot['stack']
        self._v_idle_tasks = []
        self.wstack = stack
        self.CreateParts()
        stack.SetCard(0)
        wx.EVT_IDLE(self, self.Idler)

    def CreateParts(self):
        self.wstack._v_text = self.components.field1
        self.wstack._v_cardNumber = self.components.stcCardNumber

        #self.CreateStatusBar()

    def CompactStack(self):
        self.wstack.SaveCurrentCard()
        self.connection._db.pack()

    def on_compactStack_command(self, event):
        self.CompactStack()

    def on_importStack_command(self, event):
        self.wstack.SaveCurrentCard()
        self.wstack.ImportStack()

    def on_exit_command(self, event):
        # KEA Shutdown wasn't being called before, maybe that
        # caused the .stack file corruption?
        self.Shutdown()
        self.close(True)

    def on_editUndo_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canUndo():
            widget.undo()

    def on_editRedo_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canRedo():
            widget.redo()

    def on_editCut_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCut():
            widget.cut()

    def on_editCopy_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canCopy():
            widget.copy()

    def on_editPaste_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable') and widget.canPaste():
            widget.paste()
        
    def on_editClear_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            if widget.canCut():
                # delete the current selection,
                # if we can't do a Cut we shouldn't be able to delete either
                # which is why i used the test above
                sel = widget.replaceSelection('')
            else:
                ins = widget.getInsertionPoint()
                widget.replace(ins, ins + 1, '')

    def on_editSelectAll_command(self, event):
        widget = self.findFocus()
        if hasattr(widget, 'editable'):
            widget.setSelection(0, widget.getLastPosition())

    def on_editNewCard_command(self, event):
        self.wstack.NewCard()

    def on_editDeleteCard_command(self, event):
        self.wstack.DeleteCard()

    def on_goNext_command(self, event):
        self.wstack.GoNext()

    def on_goPrev_command(self, event):
        self.wstack.GoPrev()

    def on_goFirst_command(self, event):
        self.wstack.GoFirst()

    def on_goLast_command(self, event):
        self.wstack.GoLast()

    
    def findNext(self, searchText):
        startCard = self.wstack._v_current_card
        numCards = len(self.wstack.card_list)-1
        
        # move to the next card and repeat the search until a match
        # or we come back to the card we started on
        doneSearching = 0
        while not doneSearching:
            if self.wstack._v_current_card == numCards:
                self.wstack.GoFirst()
            else:
                self.wstack.GoNext()

            if self.wstack._v_current_card == startCard:
                doneSearching = 1

            fieldText = self.components.field1.text.lower()
            offset = fieldText.find(searchText)
            if offset != -1:
                offset += fieldText.count('\n', 0, offset)
                self.components.field1.setSelection(offset, offset + len(searchText))
                self.components.field1.setFocus()
                doneSearching = 1
        

    def on_doFind_command(self, event):
        searchText = self.components.fldFind.text.lower()
        fieldText = self.components.field1.text.lower()
        offset = fieldText.find(searchText)
        if offset != -1:
            self.components.field1.setSelection(offset, offset + len(searchText))
            self.components.field1.setFocus()
        else:
            self.findNext(searchText)

    def on_doFindNext_command(self, event):
        searchText = self.components.fldFind.text.lower()
        fieldText = self.components.field1.text.lower()
        
        selOffset = self.components.field1.getSelection()[1]
        offset = fieldText[selOffset:].find(searchText)
        
        if offset != -1:
            offset += selOffset
            self.components.field1.setSelection(offset, offset + len(searchText))
            self.components.field1.setFocus()
        else:
            self.findNext(searchText)
        

    def AddIdleTask(self, task):
        self._v_idle_tasks.append(task)

    def Shutdown(self):
        self.wstack.SaveCurrentCard()

    def Idler(self, event):
        #print "idling"
        if len(self._v_idle_tasks) > 0:
            done = self._v_idle_tasks[0].DoOneIdleStep()
            if done: del self._v_idle_tasks[0]
        elif len(self.wstack.to_be_indexed) > 0:
            id = self.wstack.to_be_indexed[0]
            print "indexing card id", id
            if id in self.wstack.card_list:
                hinter = Hinter(self.wstack, id)
                self.AddIdleTask(hinter)
            else:
                print "not indexing card id", id, "because it has been deleted"
                del self.wstack.to_be_indexed[0] # card has been deleted


if __name__ == '__main__':
    app = model.Application(CardFrame)
    app.MainLoop()
