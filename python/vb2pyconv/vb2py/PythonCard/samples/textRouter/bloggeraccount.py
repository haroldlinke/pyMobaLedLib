from PythonCard import dialog
import xmlrpclib
import wx
from trTransport import trURLlibTransport

"""
__version__ = "$Revision: 1.19 $"
__date__ = "$Date: 2004/08/15 17:55:36 $"
"""

## ===================== ##
## Blogger Account Class ##
## ===================== ##
# Encapsualtes the functionality we need for Blogger accounts.

class BloggerAccount:
    "Encapsulate one blogger account details and user preferences"

    def __init__(self, proxy=""):
        self.prefs    = {"username" : "", "password" : "", "rpcserver" : "http://plant.blogger.com/api/RPC2",\
                         "activeBlog" : -1}
        self.blogs    = []
        self.settings = {"appkey" : "4621527933BBFAB9CBE39BAFFD41313009CBEB1E"}
        self.loggedIn = 0

        self.currentPostId  = -1    # used only when we fetch an existing post for editting.
        self.previousPosts  = []
        
        self.sessionPassword  = ""  # used to store the password when the user
                                    # doesn't want it saved to a config file. 
        self.lastErrorMessage = ""
        self.errorOccured = 0

        self.currentPostID = -1

        #print "ba: useProxy: " + proxy
        self.proxy = proxy

    def createBloggerSite(self):
        """Set's up the xmlrpclib site object."""
        self.bloggerSite = xmlrpclib.Server(self.prefs["rpcserver"], \
                                           transport=trURLlibTransport(self.proxy))        
    def setProxy(self, proxy):
        """Set's the proxy."""
        self.proxy = proxy

    def bloggerLogin(self):
        """Logs in to a blogger server.

        Returns 1 on success, 0 on failure."""
        # check the settings have been entered.
        if (not self.checkSetupOK(1)):
            return 0

        if self.getPassword() == "":
            result = dialog.textEntryDialog(None, \
                                         'Please enter your Blogger password (It will not be saved to the config): ',                                                              
                                         "Password entry...",
                                         '', wx.TE_PASSWORD)
            if not result.accepted:
                self.setErrorMessage("You must enter a password to continue.")
                return 0
            self.sessionPassword = result.text

        if not self.getLoggedIn():
            #if self.useProxy == "yes":
            #    print "created with proxy"
            #    self.bloggerSite = xmlrpclib.Server(self.prefs["rpcserver"], transport=UrllibTransport())
            #else:
            #    print "created without proxy"
            self.createBloggerSite()

            try:
                self.blogs = self.bloggerSite.blogger.getUsersBlogs(self.settings["appkey"], \
                                                                    self.prefs["username"], \
                                                                    self.getPassword())
                #print self.blogs
                if len(self.blogs) > 0 and self.prefs["activeBlog"] == -1:
                    self.prefs["activeBlog"] = 0
            except xmlrpclib.Fault, e:
                self.setErrorMessage("Error logging in: %s" % e.faultString)
                return 0
            
            self.setLoggedIn(1)
        else:
            self.setErrorMessage("Already logged in.")
            return 0
        return 1
            

    def bloggerBlogText(self, text):
        """Blogs the text to the chosen blog within the current Blogger account."""
        boolTrue = xmlrpclib.Boolean(1)

        if (not self.checkSetupOK()):
            return

        if text == "":
            self.setErrorMessage("Text to blog can't be blank. (You may want to check the output mode.)")
            return 0
        
        try:
            postid = self.bloggerSite.blogger.newPost(self.settings["appkey"], \
                                                      self.blogs[self.prefs["activeBlog"]-1]["blogid"], \
                                                      self.prefs["username"], \
                                                      self.getPassword(), \
                                                      text,
                                                      boolTrue) 
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error adding text to homepage: %s" % e.faultString)
            return 0

        if self.prefs["weblogsPing"] == "Yes":
            #print "pinging weblogs.com"
            try:
                #print self.blogs[self.prefs["activeBlog"]-1]["blogName"]
                #print self.blogs[self.prefs["activeBlog"]-1]["url"]
                
                weblogsCom = xmlrpclib.Server("http://rpc.weblogs.com/RPC2", \
                                              transport=trURLlibTransport(self.proxy))

                weblogsCom.weblogUpdates.ping(self.blogs[self.prefs["activeBlog"]-1]["blogName"], \
                                              self.blogs[self.prefs["activeBlog"]-1]["url"])
                self.setErrorMessage("")
            except xmlrpclib.Fault, e:
                self.setErrorMessage("Blog successfully updated.  But error while 'pinging' weblogs.com:" % e.faultString)
                return 0
        #else:
            #print "NOT pinging weblogs.com"
            
                

        self.currentPostId = -1
        return postid


    def bloggerFetchPreviousPosts(self, number = 10):
        """Fetchs a list of previous posts from the Blogger server."""
        boolTrue = xmlrpclib.Boolean(1)
        
        if (not self.checkSetupOK()):
            return 0

        try:
            self.blogs[self.prefs["activeBlog"]-1]["previousPosts"] = \
                   self.bloggerSite.blogger.getRecentPosts(self.settings["appkey"], \
                                                           self.blogs[self.prefs["activeBlog"]-1]["blogid"],\
                                                           self.prefs["username"], \
                                                           self.getPassword(), \
                                                           number)
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error downloading previous posts: %s" % e.faultString)
            return 0

        return 1


    def bloggerGetTemplate(self, type = "main"):
        """Gets a template for the current blog."""
        boolTrue = xmlrpclib.Boolean(1)
        
        if (not self.checkSetupOK()):
            return

        try:
            self.blogs[self.prefs["activeBlog"]-1]["template"] = \
                   self.bloggerSite.blogger.getTemplate(self.settings["appkey"], \
                                                        self.blogs[self.prefs["activeBlog"]-1]["blogid"],\
                                                        self.prefs["username"], \
                                                        self.getPassword(), \
                                                        type)
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error downloading template: %s" % e.faultString)
            return

        return self.blogs[self.prefs["activeBlog"]-1]["template"]


    def bloggerSetTemplate(self, type, text):
        """Sets a template for the current blog."""
        boolTrue = xmlrpclib.Boolean(1)
        
        if (not self.checkSetupOK()):
            return 0

        try:
            self.bloggerSite.blogger.setTemplate(self.settings["appkey"], \
                                                 self.blogs[self.prefs["activeBlog"]-1]["blogid"],\
                                                 self.prefs["username"], \
                                                 self.getPassword(), \
                                                 text,
                                                 type)
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error saving template: %s" % e.faultString)
            return 0

        return 1


    def bloggerGetPost(self, postid):
        """Fetches a single post from the server."""
        
        if (not self.checkSetupOK()):
            return 0

        try:
            post = self.bloggerSite.blogger.getPost(self.settings["appkey"], \
                                                    postid, \
                                                    self.prefs["username"], \
                                                    self.getPassword())

            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error fetching post: %s" % e.faultString)
            return 0
        return post


    def bloggerDeletePost(self, index):
        """Deletes a post."""
        boolTrue = xmlrpclib.Boolean(1)
        postid = self.blogs[self.prefs["activeBlog"] - 1]["previousPosts"][index]["postid"]
        
        if (not self.checkSetupOK()):
            return 0

        try:
            self.bloggerSite.blogger.deletePost(self.settings["appkey"], \
                                                postid, \
                                                self.prefs["username"], \
                                                self.getPassword(), \
                                                boolTrue)

            self.blogs[self.prefs["activeBlog"]-1]["previousPosts"][index:index+1] = []
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error deleting post: %s" % e.faultString)
            return 0

        return 1


    def bloggerUpdatePost(self, content):
        """Updates a post with the content given."""
        boolTrue = xmlrpclib.Boolean(1)

        if (not self.checkSetupOK()):
            return 0

        try:
            self.bloggerSite.blogger.editPost(self.settings["appkey"], \
                                              self.currentPostId, \
                                              self.prefs["username"], \
                                              self.getPassword(), \
                                              content, \
                                              boolTrue)
            self.setErrorMessage("")
        except xmlrpclib.Fault, e:
            self.setErrorMessage("Error updating post: %s" % e.faultString)
            return 0

        return 1
        

    def setPrefs(self, rpcserver="", username="", password="", weblogsPing=""):
        """Sets the user specific settings from the arguments"""
        self.prefs["rpcserver"] = rpcserver
        self.prefs["username"] = username
        self.prefs["password"] = password
        self.prefs["weblogsPing"] = weblogsPing
                

    def checkSetupOK(self, toCheck = 0):
        """Checks that the setup is OK for contacting a server.

        Accepts an integer arguement, each bit specifies corresponds to one check, if the bit is
        one the check is done.  If the argument is 0, all checks are done.
        Returns 1 if the checks are passed, 0 if one fails."""

        # do we need to have the settings entered ?
        if toCheck == 0 or toCheck & 1:
            if self.prefs['username'] == "" or self.prefs['rpcserver'] == "":
                self.setErrorMessage("You must setup the Blogger account details first.") 
                return 0

        # do we need to be logged in ?
        if toCheck == 0 or toCheck & 2:
            if self.getLoggedIn() == 0:
                self.setErrorMessage("You must login first.") 
                return 0

        # do we need to have an activeBlog chosen ?
        if toCheck == 0 or toCheck & 4:
            if self.getActiveBlog() == -1:
                self.setErrorMessage("You must choose a blog first.") 
                return 0
            
        # do we need to have downloaded list of previous posts
        if toCheck & 8:
            #if self.blogs[self.prefs["activeBlog"]-1]["previousPosts"] == []:
            if ("previousPosts" not in self.blogs[self.prefs["activeBlog"]-1]) or \
                   self.blogs[self.prefs["activeBlog"]-1]["previousPosts"] == []:
                self.setErrorMessage("You must download the previous posts first.") 
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


    def setActiveBlog(self, activeBlog):
        """Sets the active blog"""
        # we need to check here that the given blog number is in range:
        try:
            activeBlog = int(activeBlog)
        except ValueError, e:
            self.setErrorMessage("Value entered must be a number.")
            return 0
            
        if activeBlog > len(self.blogs) or activeBlog < 1:
            self.setErrorMessage("Chosen blog number (%d) is out of range." % activeBlog)
            return 0

        self.prefs["activeBlog"] = activeBlog
        return 1

    def getActiveBlog(self):
        """Returns the number of the currently active blog"""
        return self.prefs["activeBlog"]


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
