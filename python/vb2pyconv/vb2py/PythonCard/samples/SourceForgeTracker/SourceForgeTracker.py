#!/usr/bin/python

"""
Currently only displays Open topic items. Providing more options
and displaying the full info set from the tracker database is left
as an exercise for the reader. I did the hard part. ;-)

Thanks to Mark Pilgrim for the DOM parsing code.
http://diveintopython.org/kgp_divein.html
Thanks to Mark Pilgrim and Martin Martin v. Loewis for help
with XML and UNICODE issues.
http://aspn.activestate.com/ASPN/Mail/Message/xml-sig/967244
"""
__version__ = "$Revision: 1.23 $"
__date__ = "$Date: 2005/12/13 11:13:21 $"

from PythonCard import configuration, model
import os

from xml.dom import minidom
import urllib
import webbrowser

BUGS = 'Bug Reports'
FEATURE_REQUESTS = 'Feature Requests'
TOPIC_SEPARATOR = "  :  "


def getText(node):
    return "".join([c.data for c in node.childNodes if c.nodeType == c.TEXT_NODE]).encode('ascii', 'ignore')

def doParse(xml):
    xml = xml.replace(chr(19), '')
    xmldoc = minidom.parseString(xml)
    artifacts = xmldoc.getElementsByTagName('artifact')
    trackerDict = {}
    for a in artifacts:
        key = a.attributes["id"].value
        trackerDict[key] = \
            {"summary":getText(a.getElementsByTagName("summary")[0]),
             "detail":getText(a.getElementsByTagName("detail")[0]),
             "status":getText(a.getElementsByTagName("status")[0])}
        try:
            followups = a.getElementsByTagName('item')
            for f in followups:
                trackerDict[key]['detail'] += '\n\n\n' + \
                'Sender: ' + getText(f.getElementsByTagName("sender")[0]) + '\n' + \
                getText(f.getElementsByTagName("text")[0])
        except IndexError:
            pass
    return trackerDict

class Tracker(model.Background):

    def on_initialize(self, event):
        self.configPath = os.path.join(configuration.homedir, 'sourceforgetracker')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)

        self.baseSFUrl = 'http://sourceforge.net/export/sf_tracker_export.php?'
        self.groupIds = {'Boa':1909,
                         'PyChecker':24686, 'PyCrust':31263,
                         'Python': 5470, 'PythonCard':19015,
                         'Scintilla':2439,
                         'wxPython':10718
                         }
        self.categoryIds = {'Boa': {BUGS:101909, FEATURE_REQUESTS:351909},
                            'PyChecker': {BUGS:382217, FEATURE_REQUESTS:382220},
                            'PyCrust': {BUGS:401706, FEATURE_REQUESTS:401709},
                            'Python': {BUGS:105470, FEATURE_REQUESTS:355470},
                            'PythonCard': {BUGS:119015, FEATURE_REQUESTS:369015},
                            'Scintilla': {BUGS:102439, FEATURE_REQUESTS:352439},
                            'wxPython': {BUGS:310718, FEATURE_REQUESTS:360718}
                            }
        self.defaultGroup = 'PythonCard'
        self.defaultCategory = FEATURE_REQUESTS

        temp = self.groupIds.keys()
        temp.sort()
        self.components.choiceGroups.items = temp
        self.components.choiceGroups.stringSelection = self.defaultGroup
        self.components.choiceCategories.stringSelection = self.defaultCategory

        #self.parser = None
        self.trackerDict = {}
        self.displayTopics(self.defaultGroup, self.defaultCategory)

    def status(self, txt):
        self.components.staticStatus.text = txt

    def buildUrl(self, group, category):
        groupId = self.groupIds[group]
        atId = self.categoryIds[group][category]
        return self.baseSFUrl + 'atid=' + str(atId) + '&group_id=' + str(groupId)

    def buildFilename(self, group, category):
        name = group + '_' + category.replace(' ', '') + '.xml'
        return os.path.join(self.configPath, name)

    def loadXML(self, group, category):
        filename = self.buildFilename(group, category)
        try:
            fp = open(filename, 'rb')
            xml = fp.read()
            fp.close()
            return xml
        except IOError:
            return ''

    def displayTopics(self, group, category):
        self.components.topicList.clear()
        filename = self.buildFilename(group, category)
        if not os.path.exists(filename):
            url = self.buildUrl(group, category)
            #print "downloading", filename, url
            self.downloadFile(url, filename)
        xml = self.loadXML(group, category)
        self.status('Parsing XML...')
        self.trackerDict = doParse(xml)

        self.status('Display Topics...')
        topics = []
        for artifact in self.trackerDict:
            # handling other variations is left as an exercise for the reader
            if self.trackerDict[artifact]['status'] == 'Open':
                topics.append(artifact + TOPIC_SEPARATOR + self.trackerDict[artifact]['summary'])
        topics.sort()
        self.components.topicList.clear()
        for t in topics:
            self.components.topicList.append(t)
        self.status('')

    def downloadFile(self, url, filename):
        try:
            #print "url", url
            self.status("Downloading...")
            fp = urllib.urlopen(url)
            xml = fp.read()
            fp.close()
            #print "downloaded", url

            self.status("Writing file...")
            #print filename
            op = open(filename, 'wb')
            # fix SourceForge malformed XML
            op.write('<?xml version="1.0" encoding="iso-8859-1" ?>\n')
            op.write(xml)
            op.close()
            #print "wrote", filename
        except IOError:
            pass
            # show a warning dialog one of these days
        self.status('')

    def on_choiceGroups_select(self, event):
        group = event.target.stringSelection
        category = self.components.choiceCategories.stringSelection
        self.displayTopics(group, category)

    def on_choiceCategories_select(self, event):
        group = self.components.choiceGroups.stringSelection
        category = event.target.stringSelection
        self.displayTopics(group, category)

    def on_topicList_select(self, event):
        artifact, summary = event.target.stringSelection.split(TOPIC_SEPARATOR)
        self.components.topicDetail.text = self.trackerDict[str(artifact)]['detail']

    def doLaunch(self, url):
        # launch a new browser window and autoraise it
        # there appears to be a bug in webbrowser.py because
        # if a window already exists, a new one isn't being created ?!
        webbrowser.open(url, 1, 1)

    def on_topicList_mouseDoubleClick(self, event):
        # http://sourceforge.net/tracker/index.php?func=detail&aid=446264&group_id=19015&atid=119015
        selection = event.target.stringSelection
        if selection != "":
            artifactId, summary = event.target.stringSelection.split(TOPIC_SEPARATOR)
            group = self.components.choiceGroups.stringSelection
            groupId = self.groupIds[group]
            category = self.components.choiceCategories.stringSelection
            categoryId = self.categoryIds[group][category]
            url = 'http://sourceforge.net/tracker/index.php?func=detail&aid=' + \
                  str(artifactId) + '&group_id=' + str(groupId) + '&atid=' + str(categoryId)
            self.doLaunch(url)

    def on_buttonDownload_mouseClick(self, event):
        group = self.components.choiceGroups.stringSelection
        category = self.components.choiceCategories.stringSelection
        filename = self.buildFilename(group, category)
        url = self.buildUrl(group, category)
        #print filename
        #print url
        self.downloadFile(url, filename)
        self.displayTopics(group, category)


if __name__ == '__main__':
    app = model.Application(Tracker)
    # use the following initialization instead
    # if you don't like the colorized layout
    #app = model.Application(Tracker, 'SourceForgeTracker.original.rsrc.py')
    app.MainLoop()

