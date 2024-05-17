This app is a playground of sorts for testing XML-RPC, the Blogger API, and SOAP using a local Radio Userland 8 server. The interface is designed for easy testing and experimenting in Python, so it is not particularly user friendly. If you know the IP address, username, and password for a remote server, radioclient can also talk to that box by changing the following line in the on_openBackground method:

        # username, password, server url
        self.blog = RadioBloggerSite('', '', 'http://127.0.0.1:5335/RPC2')

*** A WARNING ***
This is not a commercial tool supported by Userland or connected in any way with the Radio Userland 8 product. This is a development app done by open source developers that use Radio and is part of the PythonCard samples designed to help stress and show off the PythonCard framework.

Since this app is talking to a live server, you are viewing, adding, editing, and deleting real data. If you are using the default Radio settings, your changes will be upstreamed to the public Radio server as changes are made. You should keep backups of your data, templates, and generated pages.
*** YOU HAVE BEEN WARNED ***

WINDOWS ONLY
Radio 8 is only available for Windows and the Macintosh. PythonCard, which relies on wxPython, works on Windows and Linux/GTK, but isn't available on the Mac yet, except using a Windows emulator or running wxGTK on Mac OS X. So, for the time being this sample is effectively just for Windows users that also have Radio 8.

RADIO AND THE BLOGGER API
Radio implements the Blogger API as defined at http://plant.blogger.com/api/index.html
As of Radio 8.0.2
  it doesn't implement getUserInfo
  getUsersBlogs returns info about the public Radio server not the local server
  getTemplate and setTemplate appear to only work with the 'main' template
This test app will be updated as changes are made to the blogger api in Radio


Over time, this app might be expanded to include additional tests against other XML-RPC, Blogger API, and SOAP web services. The tests folder contains interactive shell sessions using various web service libraries.

Note that wxPython has a great multi-column list control called wxListCtrl that will eventually be supported in PythonCard. Until then, the columns are being simulated with tabs and/or spaces in a plain List.



WEBLOGS PING
Mark is supposed to just wrap this one-liner into blogger.py, so I'm not going
to add it to my own wrapper classes unless he doesn't do that soon.

http://diveintomark.org/archives/00000054.html
"Actually, XML-RPC is easier in Python than almost any other language, because the XML-RPC library uses a very cool feature of Python called "dynamic binding" to create a kind of virtual proxy that lets you call remote functions with exactly the same syntax as calling local functions.

import xmlrpclib
remoteServer = xmlrpclib.Server("http://rpc.weblogs.com/RPC2")
remoteServer.weblogUpdates.ping(SITE_NAME, SITE_URL)

This short example pings weblogs.com to tell it that your weblog has changed. I use this script to connect this Greymatter weblog to the weblogs.com community (since Greymatter has no weblogs.com support built in). But the point here is the syntax of that third line: it's the same syntax as calling a local function. Once the proxy (remoteServer) is set up, the XML-RPC library makes the object act as if it has a weblogUpdates object within it and a ping method within that. It's all a lie, of course; under the covers it's constructing an XML-RPC request and sending it off, and then receiving an XML-RPC response and parsing it and returning a native Python object. But I, as a Python developer, don't have to worry about all that if I don't want to, and I don't have to learn a new syntax for calling remote functions."


REFERENCES

Python
http://www.python.org/

win32 extensions
http://starship.python.net/crew/mhammond/win32/Downloads.html

wxPython
http://www.wxpython.org/
windows binaries at: http://www.wxpython.org/download.php#binaries

PythonCard
http://pythoncard.sourceforge.net/

xmlrpclib (use 0.9.9 if you have Python 2.1.x, it is included as part of Python 2.2)
http://www.pythonware.com/downloads/index.htm#xmlrpc

pyblogger
http://sourceforge.net/projects/pyblogger/

The Blogger API
http://plant.blogger.com/api/index.html

Radio Userland 8
http://radio.userland.com/

emulatingBloggerInRadio
http://radio.userland.com/emulatingBloggerInRadio

emulatingBloggerInManila
http://scriptingnews.userland.com/backissues/2001/08/24#manilaSupportsTheBloggerApi
http://frontier.userland.com/emulatingBloggerInManila
http://bloggerapitest.manilasites.com/

textRouter (a manila/blogger app written in PythonCard by Simon Kittle)
http://simon.kittle.info/textrouter

Python.Scripting: Python, XML-RPC and SOAP
http://python.scripting.com/

Python and XML: An Introduction
http://www.infector.com/Paul/Python/XML_intro.html


Revision: $Revision: 1.2 $
Date:     $Date: 2002/12/19 01:24:45 $
