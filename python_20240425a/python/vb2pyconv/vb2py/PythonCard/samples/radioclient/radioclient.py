#!/usr/bin/python

from PythonCard import configuration, dialog, model
import xmlrpclib
import blogger
import os, time
import wx
from htmlpreview import HtmlPreview

"""
__version__ = "$Revision: 1.26 $"
__date__ = "$Date: 2004/08/12 19:18:57 $"
"""

class BloggerSite:
    def __init__(self, blogID, username, password, serverURL=None):
        self.blogID = blogID
        self.username = username
        self.password = password
        self.serverURL = serverURL

    def deletePost(self, postID, publish=1):
        return blogger.deletePost(postID, self.username, self.password, publish, self.serverURL)

    def editPost(self, postID, text, publish=1):
        return blogger.editPost(postID, self.username, self.password, text, publish, self.serverURL)

    def getPost(self, postID):
        return blogger.getPost(postID, self.username, self.password, self.serverURL)

    def getRecentPosts(self, n=20):
        return blogger.getRecentPosts(self.blogID, self.username, self.password, n, self.serverURL)

    def getTemplate(self, templateType="main"):
        return blogger.getTemplate(self.blogID, self.username, self.password, templateType, self.serverURL)

    def getUsersBlogs(self):
        return blogger.getUsersBlogs(self.username, self.password, self.serverURL)

    def getUserInfo(self):
        return blogger.getUserInfo(self.username, self.password, self.serverURL)
    
    def newPost(self, text, publish=1):
        return blogger.newPost(self.blogID, self.username, self.password, text, publish, self.serverURL)

    def setTemplate(self, text, templateType="main"):
        blogger.setTemplate(self.blogID, self.username, self.password, text, templateType, self.serverURL)


class RadioSite(BloggerSite):
    def __init__(self, blogID, username, password, serverURL):
        self.blogID = 'home'
        self.serverURL = serverURL
        self.username = username
        self.password = password


class ManilaSite(BloggerSite):
    def __init__(self, blogID, username, password, serverURL):
        self.blogID = blogID
        self.serverURL = serverURL
        self.username = username
        self.password = password

        
class RadioClient(model.Background):

    def on_initialize(self, event):
        # sizers are not part of PythonCard yet
        # so we're just doing some wxPython directly
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizerflags = wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL
        sizer2.Add(self.components.btnRecentPosts, 0, sizerflags, 5)
        sizer2.Add(self.components.btnNewPost, 0, sizerflags, 5)
        sizer2.Add(self.components.btnPreviewPost, 0, sizerflags, 5)
        sizer2.Add(self.components.btnEditPost, 0, sizerflags, 5)
        sizer1.Add(sizer2)
        sizer1.Add(self.components.listPosts, 0, wx.EXPAND)
        sizer1.Add(self.components.fldContent, 1, wx.EXPAND)

        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

        self.previewWindow = model.childWindow(self, HtmlPreview)
        # override resource position
        self.previewWindow.SetPosition((425, -1))
        self.previewWindow.visible = True

        self.application.shell.autoComplete = self.menuBar.getChecked('menuOptionsAutoComplete')

        if self.components.fldContent.canPaste():
            self.components.fldContent.paste()

        """
        Then define RadioSite, BloggerSite, ManilaSite, MovableTypeSite, and DrupalSite classes
        that contain all the eccentricities of each server.  Then (pay attention, this is cool)
        you can create an instance of the correct class with a line like this:

        blogclass = globals()[bloggerType + "Site"]
        self.blog = blogclass(blogid, username, password, url)
        """

        # blogID, username, password, server url
        # blogID is ignored
        self.blog = RadioSite('home', '', '', 'http://127.0.0.1:5335/RPC2')


    def on_radioGetTemplate_command(self, event):
        # 'main' seems like the only template that can be retrieved
        # are other names defined like 'home', 'day', etc.?
        self.components.fldContent.text = self.blog.getTemplate()

    def on_radioSetTemplate_command(self, event):
        self.blog.setTemplate(self.components.fldContent.text)

    def on_radioGetRecentPosts_command(self, event):
        # cache the most recent posts
        # it would probably be better to just grab each post on the fly
        # so this might change
        self.posts = self.blog.getRecentPosts()
        self.posts.reverse()
        self.components.listPosts.clear()
        self.components.fldContent.text = ""
        for p in self.posts:
            dateCreated = time.strftime("%c", p['dateCreated'])
            firstLine = p['content'].split('\n')[0]
            self.components.listPosts.append(p['postid'] + '  ' + dateCreated + '  ' + firstLine.rstrip())

    def getContent(self, postId):
        content = None
        for p in self.posts:
            if postId == p['postid']:
                content = p['content']
                break
        return content

    def on_listPosts_select(self, event):
        # the first item is assumed to be the topic id
        topic = event.target.stringSelection.split(' ', 1)[0]
        content = self.getContent(topic)
        if content is None:
            self.components.fldContent.text = ""
        else:
            self.components.fldContent.text = content

    def on_radioNewPost_command(self, event):
        # post fldContent as a new post
        postID = self.blog.newPost(self.components.fldContent.text)
        # go ahead and rebuild the recent posts list  and then select
        # the new post
        # there are several ways we could do this, but the line below
        # shows an example of calling event handlers directly
        self.on_radioGetRecentPosts_command(None)
        # the list is in reverse order, so select and display the first topic
        self.components.listPosts.selection = 0
        self.components.fldContent.text = self.getContent(postID)

    def on_radioEditPost_command(self, event):
        sel = self.components.listPosts.stringSelection
        if sel == "":
            return

        selLine = self.components.listPosts.selection
        postID = int(sel.split(' ')[0])
        self.blog.editPost(postID, self.components.fldContent.text)
        # now get the recent posts again just to be safe
        self.on_radioGetRecentPosts_command(None)
        # restore the previous selection
        self.components.listPosts.selection = selLine
        self.components.fldContent.text = self.getContent(str(postID))

    def on_radioDeletePost_command(self, event):
        sel = self.components.listPosts.stringSelection
        if sel == "":
            return

        items = sel.split(' ')
        postID = items[0]
        # the split creates an item for each double-space so the list
        # looks something like
        # ['6', '', '02/06/2002', '10:42:46', 'AM', '', 'this', 'is', 'a', 'test']
        dateTime = items[2] + " at " + items[3]
        msg = "Are you sure want to delete post %s made on %s?" % (postID, dateTime)
        result = dialog.messageDialog(self, msg, 'Delete Post',
                                   wx.ICON_EXCLAMATION | wx.YES_NO | wx.NO_DEFAULT)
        if result.accepted:
            self.blog.deletePost(int(postID))
            # now get the recent posts again just to be safe
            self.on_radioGetRecentPosts_command(None)

    def on_menuOptionsAutoComplete_select(self, event):
        self.application.shell.autoComplete = self.menuBar.getChecked('menuOptionsAutoComplete')

    def on_radioPreviewPost_command(self, event):
        self.previewWindow.visible = True
        txt = self.components.fldContent.text
        self.previewWindow.components.html.text = '<html><body>' + txt + '</body></html>'


if __name__ == '__main__':
    # now force the shell to be enabled
    configuration.setOption('showShell', True)

    app = model.Application(RadioClient)
    app.MainLoop()
