from PythonCard import dialog
import xmlrpclib
#from socket import gaierror
import wx
import time

from trTransport import trURLlibTransport


"""
__version__ = "$Revision: 1.23 $"
__date__ = "$Date: 2004/08/15 17:55:36 $"
"""

## ===================== ##
## Manila Account  Class ##
## ===================== ##
# Encapsualtes the functionality we need for Manila accounts.

class ManilaAccount:
    "Encapsulate one manila site settings and access info"

    def __init__(self, proxy=""):
        self.prefs    = {"username" : "", "password" : "", "siteurl" : "", "rpcserver" : "", "weblogOPML" : ""}
        self.settings = {}
        self.loggedIn = 0
        self.msgs = []

        self.currentHPMsgNum   = -1
        self.currentHPContent = {'subject':''}
        self.storiesList = {}
        self.stories = {}
        self.currentStory = -1

        self.sessionPassword  = ""  # used to store the password when the user
                                    # doesn't want it saved to a config file. 
        self.lastErrorMessage = ""
        self.errorOccured = 0
        self.proxy = proxy


    def createManilaSite(self):
        """Set's up the xmlrpclib site object."""
        self.manilaSite = xmlrpclib.Server(self.prefs["rpcserver"], \
                                           transport=trURLlibTransport(self.proxy))        
    def setProxy(self, proxy):
        """Set's the proxy."""
        self.proxy = proxy

    def manilaLogin(self):
        """Logs in to a Manila server.

        Returns 1 on success, 0 on failure."""
        if (not self.checkSetupOK(1)):
            return 0

        if self.getPassword() == "":
            result = dialog.textEntryDialog(None, \
                                         'Please enter your Manila password (It will not be saved to the config): ',                                                              
                                         "Password entry...",
                                         '', wx.TE_PASSWORD)
            if not result.accepted:
                self.setErrorMessage("You must enter a password to continue.")
                return 0
            self.sessionPassword = result.text

        if not self.getLoggedIn():
            try:
                self.createManilaSite()
                
                self.settings["sitename"] = self.manilaSite.manila.getSiteName(self.prefs["siteurl"])
                self.storiesList = self.manilaSite.manila.message.listStories(self.prefs["username"], \
                                                                              self.getPassword(), \
                                                                              self.settings["sitename"])
                self.setLoggedIn(1)
            except xmlrpclib.Fault, e:
                self.sessionPassword = ""
                self.setErrorMessage("Error logging in: %s" % e.faultString)
                return 0
        else:
            self.setErrorMessage("Already logged in.")
            return 0
        return 1
            

    def manilaGetStoryList(self):
        """Gets the latest story list from the server."""
        if (not self.checkSetupOK()):
            return
        try:
            self.storiesList = self.manilaSite.manila.message.listStories(self.prefs["username"], \
                                                                          self.getPassword(), \
                                                                          self.settings["sitename"])
            #print self.storiesList
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error getting story list: %s" % e.faultString)


    def manilaCreateMsg(self, subject, body, bodyType):
        """Creates a message."""
        if (not self.checkSetupOK()):
            return 0

        try:
            boolTrue = xmlrpclib.Boolean(1)
            renderInfo = { "name" : "pikeRenderer",
                           "flRenderOnEntry" : boolTrue }
            msg = self.manilaSite.manila.message.create(self.prefs["username"], \
                                                        self.getPassword(), \
                                                        self.settings["sitename"],
                                                        subject, body, bodyType, 0, 0, renderInfo)
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error creating message: %s" % e.faultString)
            return 0
        return msg


    def manilaAttachPicture(self, msgNum, pictureFilename, mimeType):
        """Reads in an image from a file, and attaches it to the specified message."""
        if (not self.checkSetupOK()):
            return 0
        
        try:
            file = open(pictureFilename, "rb")
            picData = file.read()
            file.close()
        except IOError, e:
            self.status("Couldn't open image file '%s'." % pictureFilename)
            return

        picture = xmlrpclib.Binary(picData)
        
        try:
            boolTrue = xmlrpclib.Boolean(1)
            self.manilaSite.manila.message.attachPicture(self.prefs["username"], \
                                                         self.getPassword(), \
                                                         self.settings["sitename"], \
                                                         msgNum, \
                                                         mimeType, \
                                                         picture )

            self.manilaSite.manila.message.addToPicturesList(self.prefs["username"], \
                                                         self.getPassword(), \
                                                         self.settings["sitename"], \
                                                         msgNum,)

            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error attaching picture to message: %s" % e.faultString)

    def manilaAddToStoriesList(self, msg):
        """Add's a message to the story list."""
        if (not self.checkSetupOK()):
            return 0

        try:
            msgNum = msg["msgnum"]
            self.manilaSite.manila.message.addToStoriesList(self.prefs["username"], \
                                                            self.getPassword(), \
                                                            self.settings["sitename"],
                                                            msgNum)
            
            self.storiesList[msgNum] = [ msg["subject"], msg["member"] ]
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error adding message to stories list: %s" % e.faultString)


    def manilaDownloadStory(self, msgNum):
        """Downloads a story."""
        if (not self.checkSetupOK()):
            return
        try:
            self.stories[msgNum] = self.manilaSite.manila.message.get(self.prefs["username"], \
                                                                      self.getPassword(), \
                                                                      self.settings["sitename"],
                                                                      msgNum)
            #print self.stories[msgNum]
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error downloading story: %s" % e.faultString)
            return
        return self.stories[msgNum]


    def manilaUploadStory(self, msgNum, subject, body, bodyType):
        """Uploads a story."""

        if (not self.checkSetupOK()):
            return
        try:
            boolTrue = xmlrpclib.Boolean(1)

            self.manilaSite.manila.message.set(self.prefs["username"], \
                                               self.getPassword(), \
                                               self.settings["sitename"], \
                                               msgNum, \
                                               subject, \
                                               body, \
                                               bodyType, \
                                               0, {'name' : 'pikeRenderer', 'flRenderOnEntry' : boolTrue} )
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error uploading story: %s" % e.faultString)


    def manilaFlipHomepage(self):
        """Flips the homepage of the Manila server."""
        if (not self.checkSetupOK()):
            return
        try:
            self.manilaSite.manila.homepage.flip(self.prefs["username"], \
                                                 self.getPassword(), \
                                                 self.settings["sitename"])
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error flipping homepage: %s" % e.faultString)
        

    def manilaAddTextToHP(self, text):
        """Adds given text to the homepage of the Manila server."""
        if (not self.checkSetupOK()):
            return 0

        if text == "":
            self.setErrorMessage("Text to blog can't be blank. (You may want to check the output mode.)")
            return
        
        if self.prefs["usePostedLine"] == "Yes":
            text = text + "<br />" + time.strftime(self.prefs["postedLine"], time.localtime())

        try:
            self.manilaSite.manila.homepage.addToHomepage(self.prefs["username"], \
                                                          self.getPassword(), \
                                                          self.prefs["siteurl"], \
                                                          text.replace("\n\n", "\n\n<p>"))
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error adding text to homepage: %s" % e.faultString)
            return 0
        return 1


    def manilaGetHP(self):
        """Gets the current text of the homepage."""
        if (not self.checkSetupOK()):
            return 0

        try:
            self.currentHPMsgNum  = self.manilaSite.manila.homepage.getMsgNum(self.prefs["username"], \
                                                                              self.getPassword(), \
                                                                              self.settings["sitename"])

            self.currentHPContent = self.manilaSite.manila.message.get(self.prefs["username"], \
                                                                       self.getPassword(), \
                                                                       self.settings["sitename"], \
                                                                       self.currentHPMsgNum)
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error getting current Manila homepage: %s" % e.faultString)
            return 0
        
        return 1

    def manilaSetHP(self, text, autoRender="Yes"):
        """Sets the Manila homepage to be the current text."""
        boolTrue = xmlrpclib.Boolean(1)

        if (not self.checkSetupOK()):
            return 0

        if text == "":
            self.setErrorMessage("Text to blog can't be blank. (You may want to check the output mode.)")
            return

        try:
            self.currentHPMsgNum  = self.manilaSite.manila.homepage.getMsgNum(self.prefs["username"], \
                                                                              self.getPassword(), \
                                                                              self.settings["sitename"])
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error getting current homepage message number: %s" % e.faultString)
            return 0
        
        
        defRendererInfo = { 'flRenderOnEntry' : boolTrue, 'name' : 'pikeRenderer' }
        defWindowInfo ={'height' : 100, 'width' : 100, 'top' : 10, 'left' : 10, 'right' : 110, 'bottom' : 110,\
                        'scrollLine' : 1, 'expansionState' : 1}
        defBodyType = "text/x-outline-tabbed"
        
        #print self.currentHPContent
        if ("msgnum" in self.currentHPContent) and (self.currentHPMsgNum == self.currentHPContent["msgnum"]):
            subject = ("subject" in self.currentHPContent) and \
                      self.currentHPContent["subject"]
            bodyType = ("bodyType" in self.currentHPContent) and \
                      self.currentHPContent["bodyType"] or defBodyType
            windowInfo = ("windowInfo" in self.currentHPContent) and \
                         self.currentHPContent["windowInfo"] or defWindowInfo

            if autoRender == "Yes":
                rendererInfo = ("rendererInfo" in self.currentHPContent) and \
                               self.currentHPContent["rendererInfo"] or defRendererInfo
            else:
                #print "no"
                # we were gonna sort out a renderer that doesn't insert "<BR>"'s here, but one could not
                # be found.  it needs investigating futher.
                rendererInfo = defRendererInfo

        else:
            subject = ""
            bodyType = defBodyType
            windowInfo = defWindowInfo
            if autoRender == "Yes":
                rendererInfo = defRendererInfo
            else:
                #print "no"
                rendererInfo = defRendererInfo
                
            
        #print subject
        #print bodyType
        #print windowInfo
        #print rendererInfo

        try:
            self.manilaSite.manila.message.set(self.prefs["username"], \
                                               self.getPassword(), \
                                               self.settings["sitename"], \
                                               self.currentHPMsgNum, \
                                               subject, \
                                               text, \
                                               bodyType,\
                                               windowInfo,\
                                               rendererInfo)
            
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error setting current Manila homepage: %s" % e.faultString)
            return 0
        
        return 1


    def manilaSetHomepageFromMSG(self, msgNum):
        """Set's the homepage from the given message number."""
        if (not self.checkSetupOK()):
            return
        try:
            self.manilaSite.manila.homepage.setMsgNum(self.prefs["username"], \
                                                      self.getPassword(), \
                                                      self.settings["sitename"], \
                                                      msgNum)
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error setting homepage from story: %s" % e.faultString)


    def manilaSetHPFromOutline(self, filename):
        """Sets the Manila homepage from an OPML file."""
        boolTrue = xmlrpclib.Boolean(1)

        if (not self.checkSetupOK()):
            return 0

        try:
            file = open(filename, "r")
            opmlDoc = file.read()
            #print opmlDoc
            file.close()
        except IOError, e:
            self.setErrorMessage("Couldn't open file '%s' for sending to Manila server." % filename)
            return

        try:
            self.currentHPMsgNum  = self.manilaSite.manila.homepage.getMsgNum(self.prefs["username"], \
                                                                              self.getPassword(), \
                                                                              self.settings["sitename"])
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error getting current homepage message number: %s" % e.faultString)
            return 0
        
        
        rendererInfo = { 'flRenderOnEntry' : boolTrue, 'name' : 'pikeRenderer' }
        bodyType = "text/x-opml"
        
        try:
            self.manilaSite.manila.message.set(self.prefs["username"], \
                                               self.getPassword(), \
                                               self.settings["sitename"], \
                                               self.currentHPMsgNum, \
                                               "Weblog", \
                                               opmlDoc, \
                                               bodyType,\
                                               {},
                                               rendererInfo)
            
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error setting Manila homepage: %s" % e.faultString)
            return 0
        
        return 1


    def setPrefs(self, siteurl="", rpcserver="", username="", password="", \
                 weblogOPML="", usePostedLine="No", postedLine="" ):
        """Sets the user specific settings from the arguments"""
        self.prefs["siteurl"] = siteurl
        self.prefs["rpcserver"] = rpcserver
        self.prefs["username"] = username
        self.prefs["password"] = password
        self.prefs["weblogOPML"] = weblogOPML
        self.prefs["usePostedLine"] = usePostedLine
        self.prefs["postedLine"] = postedLine
                

    def checkSetupOK(self, toCheck = 0):
        """Checks that the setup is OK for contacting a server.

        Accepts an integer arguement, each bit specifies corresponds to one check, if the bit is
        one the check is done.  If the argument is 0, all checks are done.
        Returns 1 if the checks are passed, 0 if one fails."""
        if toCheck == 0 or toCheck & 1:
            if self.prefs['username'] == "" or \
                   self.prefs['rpcserver'] == "" or self.prefs['siteurl'] == "":
                self.setErrorMessage("You must setup the Manila server details first.") 
                return 0

        if toCheck == 0 or toCheck & 2:
            if self.getLoggedIn() == 0:
                self.setErrorMessage("You must login first.") 
                return 0

        if toCheck & 4:
            if self.currentHPMsgNum == -1:
                self.setErrorMessage("You must download the current homepage before you can set it.") 
                return 0
            
        self.setErrorMessage("")
        return 1


    def getPassword(self):
        """Returns the password, if one is set in the config that is returned, else the session password is checked"""
        if self.prefs["password"] != "":
            return self.prefs["password"]
        return self.sessionPassword


    def setLoggedIn(self, loggedIn):
        """Sets the state of the 'logged-in-ness'"""
        self.loggedIn = loggedIn


    def getLoggedIn(self):
        """Returns the state of the 'logged-in-ness'"""
        return self.loggedIn


    def setErrorMessage(self, msg):
        """Sets the last error message variable and the 'errorOccured' flag"""
        self.lastErrorMessage = msg
        if self.lastErrorMessage != "":
            self.errorOccured = 1
        else:
            self.errorOccured = 0


    def getErrorMessage(self):
        """Returns a string describing the last error to occur."""
        return self.lastErrorMessage


    def anErrorOccured(self):
        """Returns 0 if last operation was a success, 1 if last operation failed."""
        return (self.errorOccured)


