                            TextRouter README
                            =================


What is it ?
============

  TextRouter is a generic weblogging and text "routing" client.  It's
  main use is for posting to Blogger and/or Manila maintained weblogs. 
  It is designed to be the sort of app which is kept running the whole
  time; the idea being that if you find a piece of text you'd like to
  send somewhere, you can simply copy and paste it into TextRouter and
  send it on its way.

  Some screen shots are available at:
  http://simon.kittle.info/stories/storyReader$116

  There is now a textRouter mailing list which you are welcome to post
  questions, comments, bugs, feature requests, etc, to.  It is at :
  http://groups.yahoo.com/group/textrouter.

Features
========

  The aim of TextRouter is to be as convinient as possible.  Features
  that exist to help make TextRouter reach this goal include:

    1 Posting to Blogger and Manila.

    2 Multiple Blogger and multiple Manila accounts supported.

    3 Blogger support includes: new/edit/delete posts and
    upload/downloading of templates.

    4 Automatic weblogs.com "pinging" for Blogger accounts. (Manila has
    support for this buil in)

    5 Manila support includes: homepage flip/add/get/set, stories
    new/edit, uploading of pictures and uploading of OPML files direct
    to the homepage.

    6 Input/Output "modes" which allow you to select what portion of
    text the next operation (loading/saving/blogging/cutting/pasting)
    works on.

    7 Common editing functionality; make bold/italic, center, inserting
    hyperlink, stripping HTML, formatting paragraphs.

    8 Drag + Drop for URL's; turning them automatically in to links.

    9 Shortcuts (Manila style, implemented locally for Blogger)

    10 Proxy support. (This is a little experimental at the moment, but
    should work.)

  Things that are planned:

    1 Movable Type support. (Once the XML-RPC interface is done)

    2 LiveJournal support.

    3 Support for more Manila specific features.

    4 Routing to RSS Files on the local disk

Blogger
=======

  Blogger (http://www.blogger.com) is a free service which allows a
  user to easily maintain a weblog on their website.  When you update
  your weblog (either via a web based form or a client like this one)
  Blogger takes care of updating all the HTML, archiving old posts, and
  FTP'ing the data to your website.

Manila
======

  Manila (http://manila.userland.com) is a Content Management System
  from Userland Software, Inc. While Manila can manage whole websites,
  it has a number of specific features for maintaining weblog type
  sites.  There is a list of companies that provide Manila hosting at:
  http://www.edithere.com/directory/22/websiteHostingServices/manila.

Requirements
============

  TextRouter is written using the PythonCard framework
  (http://pythoncard.sourceforge.net), if you want to run it on *nix
  systems you will need to download PythonCard. (There is an exe
  package for Windows which is self-contained.)

  PythonCard requires version 2.0 or higher of Python and wxPython
  2.3.x (http://www.wxpython.org). As soon as 2.3.2 is available, that
  will probably be the minimum wxPython requirement.

  The only other requirement is the Python XML-RPC library from
  PythonWare (http://www.pythonware.com/products/xmlrpc/).

  Note that you need the latest development version of the XML-RPC
  library, the 0.9.8 stable version is not good enough.  (In 0.9.9 the
  Transport() classes were all changed, which made proxy stuff easier
  to do, but is also incompatible with earlier Transport() classes).

Downloading
===========

  NOTE: This software is released under the Python License, it comes
  with no warranty, etc, etc.  See
  http://www.python.org/2.2/license.html for details.

  If you are on Windows by far the simplest and quickest way to get
  TextRouter is to download this zip package:
  http://www.tswoam.co.uk/files/textrouter/textrouter-0.58.zip.  This
  is self contained and so has everything you ened to run TextRouter
  including the documentation.

  If you are on a Linux/Unix system, or if you are on Windows but want
  to run the very latest version, then you need to first get Python 2.x
  and wxPython 2.3.x.  Once these are working then you just need to
  download PythonCard.	For this go to the PythonCard homepage and
  either download a ZIP'ed release of PythonCard, or get the very
  latest version from anonymous CVS.  (Instructions for CVS are on the
  SourceForge site)

  Note: If you are running it from the source code, you will need
  version 2.3.2b7 of wxPython to use the drag + drop URL functionality.

  Note: This will only work with Python2.1 if you download and install
  the xmlrpc library from http://www.pythonware.com/products/xmlrpc/

Details
=======

  Last Updated: Tue, 27 Nov 2001 11:15:21 GMT

  Contact: simon@kittle.co.uk

  Latest info: http://simon.kittle.info/textrouter

  Mailing List: http://groups.yahoo.com/group/textrouter

