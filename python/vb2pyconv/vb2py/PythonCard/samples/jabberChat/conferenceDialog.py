
"""
__version__ = "$Revision: 1.5 $"
__date__ = "$Date: 2004/08/12 19:18:53 $"
"""

from PythonCard import model
import os

class ConferenceDialog(model.CustomDialog):
    def __init__(self, parent, room='', server=None, nickname=''):
        model.CustomDialog.__init__(self, parent)
        
        # if some special setup is necessary, do it here
        self.components.fldRoomName.text = room
        if server:
            self.components.cmbRoomServer.stringSelection = server
        self.components.fldNickname.text = nickname

def conferenceDialog(parent, room='', server=None, nickname=''):
    dlg = ConferenceDialog(parent, room, server, nickname)
    result = dlg.showModal()
    result.room = dlg.components.fldRoomName.text
    result.server = dlg.components.cmbRoomServer.stringSelection
    result.nickname = dlg.components.fldNickname.text
    dlg.destroy()
    return result
