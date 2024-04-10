#!/usr/bin/python

"""
__version__ = "$Revision: 1.6 $"
__date__ = "$Date: 2004/05/05 16:53:25 $"
"""

from PythonCard import model
import threading 
import Queue
import wx

# EchoServer derived
# from echo server example in Programming Python by Mark Lutz

# get socket constructor and constants
import socket
# server machine, '' means local host
myHost = ''
# listen on a non-reserved port number
myPort = 50007

class EchoServer:
    def __init__(self, parent):
        self._parent = parent
        self.keepRunning = 1

    def server(self):
        # make a TCP socket object
        sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind it to server port number
        sockobj.bind((myHost, myPort))
        # listen, allow 5 pending connects
        sockobj.listen(5)                            

        # listen until process killed
        while self.keepRunning:
            #print 'outer loop'
            connection, address = sockobj.accept()   # wait for next client connect
            #print 'Server connected by', address     # connection is a new socket
            while self.keepRunning:
                #print 'inner loop'
                # read next line on client socket
                data = connection.recv(1024)         
                if not data: break
                self._parent.msgQueue.put(data)
                wx.WakeUpIdle()
            connection.close() 

# The same port as used by the server
PORT = myPort

def echoSend(host, port, txt):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(txt)
    s.close()

class Chat(model.Background):

    def on_initialize(self, event):
        self.msgQueue = Queue.Queue()
        self.components.fldYourIPAddress.text = socket.gethostbyname(socket.gethostname())
        self.echoServer = EchoServer(self)
        self.thread = threading.Thread(target = self.echoServer.server)
        # I think this allows Python to kill the thread when we quit wxPython
        # setDaemon must be called before start
        self.thread.setDaemon(1)
        self.thread.start() 

    def on_idle(self, event):
        if not self.msgQueue.empty():
            msg = self.msgQueue.get()
            self.doDisplayMsgReceived(msg)
            event.RequestMore()

    def doDisplayMsgReceived(self, data):
        if data is not None:
            self.components.fldTranscript.appendText(data + '\n')
        else:
            pass

    def on_btnSend_mouseClick(self, event):
        #print "btnSend", self.components.fldSendAddresses.text, PORT, self.components.fldInput.text
        txt = self.components.fldNickname.text + \
            " (" + self.components.fldYourIPAddress.text + "): " + \
            self.components.fldInput.text
        addresses = self.components.fldSendAddresses.text.split(',')
        #print addresses
        for ip in addresses:
            echoSend(ip.strip(), PORT, txt)
        self.components.fldTranscript.appendText(txt + '\n')
        self.components.fldInput.text = ""
        #print "after send"

    def on_close(self, event):
        self.echoServer.keepRunning = 0
        event.skip()


if __name__ == '__main__':
    app = model.Application(Chat)
    app.MainLoop()
