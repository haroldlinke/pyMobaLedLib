
"""
__version__ = "$Revision: 1.17 $"
__date__ = "$Date: 2004/05/13 02:40:24 $"
"""

import wx
from wx import html 
from PythonCard import event, log, widget

class HtmlWindowSpec(widget.WidgetSpec):
    def __init__(self):
        events = []
        attributes = {
            'size' : { 'presence' : 'optional', 'default' : [ 50, 50 ] },
            'text' : { 'presence' : 'optional', 'default' : '' },
        }
        widget.WidgetSpec.__init__(self, 'HtmlWindow', 'Widget', events, attributes )
       

class HtmlWindow(widget.Widget, html.HtmlWindow):
    """
    An HTML window.
    """

    _spec = HtmlWindowSpec()

    def __init__(self, aParent, aResource):
        self._addressField = None

        html.HtmlWindow.__init__(
            self,
            aParent, 
            widget.makeNewId(aResource.id),
            aResource.position, 
            aResource.size,
            #style = wx.HW_SCROLLBAR_AUTO | wx.CLIP_SIBLINGS,
            name = aResource.name 
        )

        widget.Widget.__init__(self, aParent, aResource)

        self._setText(aResource.text)
        
        self._bindEvents(event.WIDGET_EVENTS)

    def setAddressField(self, field):
        self._addressField = field

    def _getText(self) :
        return self.GetOpenedPage()

    def _setText(self, aString):
        if aString == '' or aString[0] == '<':
            self.SetPage(aString)
        else:
            # filename
            self.LoadPage(aString)
        #self._delegate.Refresh()

    def base_LoadPage(self, url):
        log.debug("base_LoadPage " + url)
        if self._addressField is not None:
            self._addressField.text = url
            log.debug("loaded")
        html.HtmlWindow.base_LoadPage(self, url)

    def LoadPage(self, url):
        log.debug("LoadPage " + url)
        if self._addressField is not None:
            self._addressField.text = url
            log.debug("loaded")
        html.HtmlWindow.LoadPage(self, url)

    def SetPage(self, text):
        log.debug("SetPage " + text)
        #if self._addressField is not None:
        #    self._addressField.text = text
        #    log.debug("set")
        html.HtmlWindow.SetPage(self, text)

    def OnLinkClicked(self, link):
        log.debug("OnLinkClicked " + str(link))
        if self._addressField is not None:
            url = self.GetOpenedPage()
            log.debug("url: " + url)
            baseURL = url[:url.rfind('/')]
            log.debug("baseURL: " + baseURL)
            href = link.GetHref()
            log.debug("href: " + href)
            if href.find('://') != -1:
                self._addressField.text = href
            else:
                self._addressField.text = baseURL + '/' + href
            log.debug("full url: " + self._addressField.text)
        # Virtuals in the base class have been renamed with base_ on the front.
        html.HtmlWindow.base_OnLinkClicked(self, link)

    text = property(_getText, _setText)


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].HtmlWindow)

