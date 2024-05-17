"""
Twisted PythonCard PbEchoClient
"""

from PythonCard import model, twistedModel
from twisted.cred.credentials import UsernamePassword
from twisted.spread import pb
from twisted.internet import reactor

from PythonCard.templates.dialogs.loginDialog import loginDialog

class DefinedError(pb.Error):
    pass

class EchoClient(model.Background):
    """
    TPC PB Echo GUI Panel
    """
    
    def on_initialize(self, event):
        self.pbfactory = pb.PBClientFactory()
        # KEA the Send button and SendTextField should be disabled
        # until a successful login
        self.components.SendTextField.enabled = False
        self.components.buttonSend.enabled = False

    def on_SendTextField_keyPress(self, event):
        # if user presses return, send text
        if event.keyCode == 13:
            self.sendAndClearText()
        else:
            event.skip()

    # KEA 2004-04-27
    # this should popup a custom dialog
    # to prompt the user for the host, port number,
    # username, and password
    # with defaults of "localhost", pb.portno
    # "guest", and "guest"
    # this dialog is going to be pretty common so we'll stick
    # in PythonCard/templates/dialogs to simplify usage from
    # other twisted apps
    def on_buttonLogin_mouseClick(self, event):
        result = loginDialog(self, port=pb.portno)
        if result.accepted:
            # verify input here?
            host = result.host
            port = result.port
            username = result.username
            password = result.password
            reactor.connectTCP(host, port, self.pbfactory)
            self.pbfactory.login(
                UsernamePassword(username, password)
                    ).addCallbacks(self.loginsuccess,
                                   self.loginfailure)

    def loginsuccess(self, perspective):
        self.statusBar.text = 'Connected'
        self.components.SendTextField.enabled = True
        self.components.buttonSend.enabled = True
        self.components.SendTextField.setFocus()
        self.perspective = perspective

    def loginfailure(self, error):
        self.displaycontent("Error on login: %s" % error)

    def sendAndClearText(self):
        fld = self.components.SendTextField
        self.perspective.callRemote('echo', fld.text
            ).addCallbacks(self.echosuccess,
                           self.echofailure)
        fld.text = ""

    def on_buttonSend_mouseClick(self, event):
        self.sendAndClearText()

    def echosuccess(self, message):
        self.displaycontent(message)

    def echofailure(self, error):
        t = error.trap(DefinedError)
        self.displaycontent("error received"+t)

    def displaycontent(self, text):
        self.components.ReceivedTextArea.appendText(text + "\n")


if __name__ == '__main__':
    app = twistedModel.TwistedApplication(EchoClient)
    app.MainLoop()

