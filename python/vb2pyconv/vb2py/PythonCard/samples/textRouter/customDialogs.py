from PythonCard import dialog, resource
from PythonCard.model import CustomDialog

import wx 
from wx import Yield
from string import whitespace
from time import sleep

import webbrowser
import pprint

from wordwrap import wrap_string

"""
__version__ = "$Revision: 1.27 $"
__date__ = "$Date: 2004/08/12 19:19:02 $"
"""

# --------------------- #
#    Custom Dialogs     #
# --------------------- #

# This file contains all the custom dialogs (each based on CustomDialog) used by textRouter.


class AboutDialog(CustomDialog):
    """Displays a simple about screen."""

    def __init__(self, aBg, title, description, links) :
        """Initialize the defaults for the input boxes."""

        self.links = links
        
        # build the resource which describes this particular preferences window
        aDialogRsrc = self.buildAboutResource(title, description, links)

        CustomDialog.__init__(self, aBg, aDialogRsrc)

        self.parent = aBg
        
    def buildAboutResource(self, title, description, links):
        """This builds a string containing a resource description as you find in a .rsrc files"""

        description = description.replace("\n", "\\n")
        description = description.replace("'", "\\'")
        
        # build the body of the About dialog resourece string.  done first so we know the
        # total height of the whole window when we write out the main string at the end.
        bodyRSRC = " {'type':'StaticText', 'name':'labelDesc', 'position':(10,10)," + \
                  "'alignment':'center','size':(360,30),'text':'" + title + "'},"
        bodyRSRC = bodyRSRC + " {'type':'TextArea', 'name':'labelDesc', 'position':(10,40)," + \
                   "'size':(360,80),'text':'" + description + "'},"

        vert = 140

        for i in range(len(links)):
            link = links[i]
            bodyRSRC = bodyRSRC + " {'type':'StaticText', 'name':'labelLinkDesc%d', " % i + \
                      "'position':(10,%d)," % (vert) + \
                      "'text':'" + link[0] + "'},"
            vert += 20
            bodyRSRC = bodyRSRC + " {'type':'StaticText', 'name':'labelLink%d', " % i + \
                      "'position':(10,%d)," % (vert) + \
                      "'foregroundColor':'blue', 'text':'" + link[1] + "'},"
            vert += 30

        bodyRSRC = bodyRSRC + \
                  "{'type':'Button', 'name':'btnOK', 'position':(10, %d), " % vert + \
                  "'label':'OK', 'id':5100 }" + \
                  " ] } "

        vert += 60
        # construct the final resource string.
        dlgRSRC = "{'type':'CustomDialog','name':'dlgAbout'," + \
                  " 'title':'About " + title + "...','position':(-1,-1),'size':(390, %d),\n\n'components': [" % vert
        
        dlgRSRC += bodyRSRC
        
        # eval the resource string, pass it to Resource() and return it.
        return resource.Resource( eval(dlgRSRC) )
        
    def on_mouseUp(self, event):
        target = event.target
        if target._name[0:9] == "labelLink":
            self.doLaunchURL(int(target._name[9:]))
        else:
            event.skip()
        
    def doLaunchURL(self, num):
        """Launch a URL."""
        try:
            webbrowser.open(self.links[num][1], 1, 1)
        except webbrowser.Error, e:
            result = dialog.messageDialog(self, "Could not find a runable browser.", "Error launching URL", \
                                       wx.ICON_INFORMATION | wx.OK)
            

    # these shouldn't be necessary ... (see textEditor.pyw)
    def on_btnOK_mouseClick(self, event):
        event.skip()





class AutoTextScrollerDialog(CustomDialog):
    """Set's up a speed reading window."""

    def __init__(self, aBg, title, prefs, text) :
        """Initialize the defaults for the input boxes."""

        self.reading = 0
        self.location = 0
        self.text = text

        self.delay = ("textScrollerDelay" in prefs) and prefs["textScrollerDelay"] or 0.3
        self.words = ("textScrollerWords" in prefs) and prefs["textScrollerWords"] or 1

        self.font  = ("textScrollerFont" in prefs) and prefs["textScrollerFont"] or \
                     "{'style': 'bold', 'faceName': 'helvetica', 'family': 'sansSerif', 'size': 24}"
        
        # build the resource which describes this particular preferences window
        aDialogRsrc = self.buildSpeedReaderResource(title, prefs)
        CustomDialog.__init__(self, aBg, aDialogRsrc)
        self.parent = aBg
        
    def on_btnStart_mouseClick(self, event):
        """Starts the speed reading going."""
        if self.reading == 1:
            return
        self.reading = 1
        self.doReading()

    def on_btnPause_mouseClick(self, event):
        """Pauses the speed reading."""
        self.reading = 0
        
    def doReading(self):
        while self.components.theWords.text[-5:-1] != "-end":
            if self.reading == 0:
                break
            self.components.theWords.text = self.getNextWords()
            Yield()
            sleep(self.delay)
        self.reading = 0
        
    def getNextWords(self):
        """Gets the next set of words."""
        str = ""
        for i in range(self.words):
            str += self.getNextWord()
            if str[-5:-1] == "-end":
                break
        return str
    
    def getNextWord(self):
        start = self.location
        if start >= len(self.text):
            return "-end-"
        for i in range(start, len(self.text)):
            #if not (curses.ascii.isalnum(self.text[i]) or self.text[i] == "-"):
            if not (self.text[i].isalpha() or self.text[i] == "-"):
                break
        self.location = i + 1
        return self.text[start:i+1]


    # these shouldn't be necessary ... (see textEditor.pyw)
    def on_btnClose_mouseClick(self, event):
        self.reading = 0
        Yield()
        event.skip()

    def buildSpeedReaderResource(self, title, prefs):
        """This builds a string containing a resource description as you find in a .rsrc files"""

        # main StaticText whcih holds each word 
        bodyRSRC = " {'type':'StaticText', 'name':'theWords', 'position':(10,100)," + \
                  "'alignment':'center','font':" + self.font + ",'size':(520,110),'text':'-'},"

        # the buttons
        bodyRSRC = bodyRSRC + \
                  "{'type':'Button', 'name':'btnStart', 'position':(10, 260)," + \
                  "'label':'Start',  'toolTip':'Starts Speed Reading' }, " + \
                  "{'type':'Button', 'name':'btnPause', 'position':(110, 260)," + \
                  "'label':'Pause',  'toolTip':'Pauses Speed Reading' }, " + \
                  "{'type':'Button', 'name':'btnClose', 'position':(210, 260), " + \
                  "'label':'Close', 'id':5100 }," + \
                  " ] } "

        # construct the final resource string.
        dlgRSRC = "{'type':'CustomDialog','name':'dlgAutoTextScroller'," + \
                  " 'title':'" + title + "','position':(100,100),'size':(540, 320),\n\n'components': ["
        dlgRSRC += bodyRSRC
        
        # eval the resource string, pass it to Resource() and return it.
        return resource.Resource( eval(dlgRSRC) )




class ChooserDialog(CustomDialog):
    """Presents a dialog with a list of things to choose from in it."""

    def __init__(self, aBg, title, caption, options, defOption) :
        """Initialize the defaults for the input boxes"""

        # build the resource which describes this particular preferences window
        self.options = options
        aDialogRsrc = self.buildChooserResource(title, caption, options, defOption)

        CustomDialog.__init__(self, aBg, aDialogRsrc)

        self.parent = aBg

        
    def buildChooserResource(self, title, caption, options, defOption):
        """This builds a string containing a resource description as you find in a .rsrc files"""

        # dynamically build each of the list choices
        optionsStr = "["
        for opt in options:
            txt = opt.replace("'", "\\'")
#            optionsStr = optionsStr + "'" + opt.replace("'", "\\'") + "',"
            optionsStr = optionsStr + "'" + txt + "',"
        optionsStr = optionsStr + "]"


        # construct the resource string.
        dlgRSRC = "{'type':'CustomDialog','name':'dlgChooser'," + \
                  " 'title':'" + title + "','position':(100,50),'size':(445, 330),\n\n'components': ["
        
        
        dlgRSRC = dlgRSRC + " {'type':'StaticText', 'name':'labelCaption', 'position':(10,10)," + \
                  "'text':'" + caption.replace("'", "\\'") + "'},"

        dlgRSRC = dlgRSRC + " {'type':'List', 'name':'options', 'position':(10,30),'size':(415,200)," + \
                  "'items':" + optionsStr + ",'stringSelection':'" + defOption.replace("'", "\\'") + "'},"

        dlgRSRC = dlgRSRC + \
                  "{'type':'Button', 'name':'btnOK', 'position':(10, 260), " + \
                  "'label':'OK', 'id':5100, 'default':1, 'toolTip':'Update Preferences'}," + \
                  "{'type':'Button', 'name':'btnCancel', 'position':(110, 260)," + \
                  "'label':'Cancel', 'id':5101, 'toolTip':'Discard Preferences Changes' } " + \
                  " ] } "

        # eval the resource string, pass it to Resource() and return it.
        return resource.Resource( eval(dlgRSRC) )
        
    # these shouldn't be necessary ... (see textEditor.pyw)
    def on_btnOK_mouseClick(self, event):
        event.skip()
    def on_btnCancel_mouseClick(self, event):
        event.skip()


## ===================== ##
##  Preferences  Class   ##
## ===================== ##
# This is used to create all the Preference settings windows at run time.  The dialog
# is generated on the fly at run time and its contents depends on an array, preferences, 
# which is passed to the class at initialization

class PreferencesDialog(CustomDialog):
    """Produces the main preferences custom dialog where user can enter generic settings."""

    def __init__(self, aBg, title = "", preferences = []) :
        """Initialize the defaults for the input boxes"""

        # build the resource which describes this particular preferences window
        self.prefs = preferences
        aDialogRsrc = self.buildPrefsResource(title, preferences)
        
        CustomDialog.__init__(self, aBg, aDialogRsrc)

        self.values = {}
        self.parent = aBg

    def on_printHelpString_command(self, event):
        itemName = event.target._name[3:]
        for pref in self.prefs:
            if itemName == pref[0]:
                helpText = wrap_string(pref[2], 70)
                result = dialog.messageDialog(self, helpText, \
                                           "Settings Help", wx.ICON_INFORMATION | wx.OK)
        
    def buildPrefsResource(self, title, preferences):
        """This builds a string containing a resource description as you find in a .rsrc files"""
        
        location = 15
        height = 80
        prefsResString = ""

        # dynamically build each of the preference choices.
        for preference in preferences:
            escapedDefaultPref = preference[3]
            if preference[4] != 2 and preference[4] != 6 and preference[4] != 7:
                escapedDefaultPref = escapedDefaultPref.replace("'", "\\'")
            
            prefsResString = prefsResString + \
                             "{'type':'StaticText', 'name':'lab" + preference[0] + "', " + \
                             "'position':(45, %d), "  % (location) + \
                             "'text':'" + preference[1].replace("'", "\\'") + "'}," + \
                             "{'type':'Button', 'name':'btn" + preference[0] + "', " + \
                             "'position':(15, %d), 'size':(18,-1),"  % (location-3) + \
                             "'label':'?','command':'printHelpString'},"

            # prefernce needs a text box for normal string.
            if preference[4] == 1:    # 1
                prefsResString = prefsResString + \
                                 "{'type':'TextField', 'name':'" + preference[0] + "', " + \
                                 "'size':(200,-1), 'position':(220, %d), "  % (location-3) + \
                                 "'text':'" + escapedDefaultPref + "'},"

            # text box, but for a number
            elif preference[4] == 2 or preference[4] == 6:  # was 4
                prefsResString = prefsResString + \
                                 "{'type':'TextField', 'name':'" + preference[0] + "', " + \
                                 "'size':(200,-1), 'position':(220, %d), "  % (location-3) + \
                                 "'text':'%s'}," % escapedDefaultPref
            # password field
            elif preference[4] == 3:  # 3
                prefsResString = prefsResString + \
                                 "{'type':'PasswordField', 'name':'" + preference[0] + "', " + \
                                 "'size':(200,-1), 'position':(220, %d), "  % (location-3) + \
                                 "'text':'" + preference[3] + "'},"

            # "Yes"/"No" choice box
            elif preference[4] == 4:  # was 2  - I changed the order so it made more sense.
                prefsResString = prefsResString + \
                                 "{'type':'Choice', 'name':'" + preference[0] + "', " + \
                                 "'size':(80,-1), 'position':(220, %d), "  % (location-3) + \
                                 "'items':['Yes','No'],'stringSelection':'" + escapedDefaultPref + "'},"
                
            # Custom choice box
            elif preference[4] == 5:  #
                prefsResString = prefsResString + \
                                 "{'type':'Choice', 'name':'" + preference[0] + "', " + \
                                 "'size':(80,-1), 'position':(220, %d), "  % (location-3) + \
                                 "'items':["
                for item in preference[5]:
                    prefsResString = prefsResString + "'%s'," % item
                prefsResString = prefsResString + "], 'stringSelection':'" + escapedDefaultPref + "'},"

            # Font preference
            elif preference[4] == 7:  
                prefsResString = prefsResString + \
                                 "{'type':'Button', 'name':'" + preference[0] + "', " + \
                                 "'size':(60,-1), 'label':'Choose','position':(220, %d), "  % (location-3) + \
                                 "'command':'fontChoose'},"
                
                
            location = location + 35
            height = height + 35
        
        
        # construct the resource string.
        dlgRSRC = "{'type':'CustomDialog','name':'dlgPrefs'," + \
                  " 'title':'" + title + "','position':(100,50),'size':(440, %d),\n\n'components': [" % height
        
        dlgRSRC = dlgRSRC + prefsResString

        dlgRSRC = dlgRSRC + \
                  "{'type':'Button', 'name':'btnOK', 'position':(15, %d), "  % (height - 55) + \
                  "'label':'OK', 'id':5100, 'default':1, 'toolTip':'Update Preferences'}," + \
                  "{'type':'Button', 'name':'btnCancel', 'position':(115, %d)," % (height - 55) + \
                  "'label':'Cancel', 'id':5101, 'toolTip':'Discard Preferences Changes' } " + \
                  " ] } "

        # eval the resource string, pass it to Resource() and return it.
        return resource.Resource( eval(dlgRSRC) )
    

    def on_fontChoose_command(self, event):
        pp = pprint.PrettyPrinter(indent=4)
        result = dialog.fontDialog(self)
        if result.accepted:
            self.values[event.target._name] = pp.pformat(result.font).replace("\n", "")

    # these shouldn't be necessary ... (see textEditor.pyw)
    def on_btnOK_mouseClick(self, event):
        event.skip()
    def on_btnCancel_mouseClick(self, event):
        event.skip()
