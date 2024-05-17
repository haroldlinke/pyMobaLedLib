simpleIEBrowser is based on the simpleBrowser sample, but 
instead of the using the htmlWindow (wxHtmlWindow) control, 
it uses the new wxIEHtmlWin control in wxPython 2.3.3.1. 
This will only work under MS Windows, but since wxIEHtmlWin
wraps the Internet Explorer COM control, you get a full-featured
browser window.

simpleIEBrowser is not designed to be a full web browser.

