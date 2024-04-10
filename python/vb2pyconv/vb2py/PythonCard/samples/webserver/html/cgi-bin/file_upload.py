#!/usr/bin/python

import cgi, sys, os

UPLOADSSDIR = '..' + os.sep + 'uploads'

form = cgi.FieldStorage()
fileitem = form["input_file"]

print "Content-type: text/html\r\n\r\n",

print "<HTML><HEAD><TITLE>File Upload Result</TITLE></HEAD><BODY>"

if fileitem.filename and fileitem.file:
    # it is important to restrict uploads to a particular
    # user-specified directory rather than using
    # the path of the uploaded file
    # the extension could still be bogus or the contents
    # could contain a virus, trojan, etc., but that
    # is something the user has to watch out for
    
    dir = UPLOADSSDIR
    
    target = fileitem.filename
    target = target.replace(':', '/')
    target = target.replace('\\', '/')
    filename = target.split('/')[-1]

    try:
        path = os.path.join(dir, filename)
        # we could check for file existance and not write the file
        # if it already exists
        fp = open(path, 'wb')
        fp.write(fileitem.file.read())
        fp.close()

        print "Upload of file %s was successful." % filename
    except Exception, msg: # Should check for a particular Exception
        print "Upload of file %s failed." % filename
        
else:
    print "Please provide a file to upload. Hit the Back button in your browser to try again."

print "</BODY></HTML>"
