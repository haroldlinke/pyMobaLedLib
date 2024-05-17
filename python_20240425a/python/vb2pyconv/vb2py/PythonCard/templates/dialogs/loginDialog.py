
"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2004/08/12 19:12:39 $"
"""

from PythonCard import model

class LoginDialog(model.CustomDialog):
    def __init__(self, parent, host="127.0.0.1", port=80, username="guest", password="guest"):
        model.CustomDialog.__init__(self, parent)
        
        self.components.fldHost.text = host
        self.components.fldPort.text = str(port)
        self.components.fldUsername.text = username
        self.components.fldPassword.text = password

#def myDialog(parent, txt):
def loginDialog(parent, host="127.0.0.1", port=80, username="guest", password="guest"):
    dlg = LoginDialog(parent, host, port, username, password)
    result = dlg.showModal()
    result.host = dlg.components.fldHost.text
    result.port = int(dlg.components.fldPort.text)
    result.username = dlg.components.fldUsername.text
    result.password = dlg.components.fldPassword.text
    dlg.destroy()
    return result
