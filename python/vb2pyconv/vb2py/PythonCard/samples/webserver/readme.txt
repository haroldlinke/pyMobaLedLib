webserver is a simple front-end to the HTTP server classes. It supports HEAD, 
GET, and POST requests for files and CGI scripts. An example CGI script is 
provided to test environment variables. Place any files you want to serve
in the HTML directory or change the default HTML directory to another location.

After you've started the server you should be able to connect to it from 
your machine using the URL http://localhost:8000/ or http://127.0.0.1:8000/

You'll need to add additional IP addresses to the validIPList if you would 
like other machines on your LAN or friends on the Internet to connect to your 
machine for exchanging files, etc. The reason the server is restrictive about 
what IP addresses are allowed to connect is that the server and CGI 
implementation provided in the Python Standard Libraries may have security 
holes. It is a bad idea to allow arbitrary connections to your machine.

On Windows I think you need to start python with the -u option, 
unbuffered binary stdout and stderr (also PYTHONUNBUFFERED=x) for CGIs 
that process or output binary data to work correctly, but this may 
no longer be necessary with Python 2.2.1 or later.

For comparison, I've also provided a console_server.py file which will run 
without a GUI. When ConfigParser support is added to the GUI front-end server 
the console_server.py file will be updated to read the same configs.

For more information see:
http://www.python.org/doc/current/lib/module-BaseHTTPServer.html
http://www.python.org/doc/current/lib/module-SimpleHTTPServer.html
http://www.python.org/doc/current/lib/module-CGIHTTPServer.html


Mac OS X and Linux Notes:
In order to run CGI scripts on Mac OS X or Linux you will first have to do 
a chmod +x on the CGI scripts. You may also have to change the #!/usr/bin/python
at the top of each CGI script.


2002-06-09
I added Mark Pilgrim's PyWebServices scripts, so the webserver can
now act as an XML-RPC server too. After starting up the webserver
sample you can test the XML-RPC server capabilities by running the
radioclient sample, which automatically shows the shell and imports
the xmlrpclib module. Then try this in the shell:

>>> server = xmlrpclib.Server('http://localhost:8000/cgi-bin/webservices.py')
>>> server.system.listMethods()
{'sample.helloWorld()': 'None', 'examples.getStateName(stateIndex)': 'None', 'system.listMethods()': 'None'}
>>> server.sample.helloWorld()
'Hello World!'
>>> server.examples.getStateName(1)
'Alabama'
>>> server.examples.getStateName(50)
'Wyoming'


For more information see:
http://diveintomark.org/archives/2002/02/07.html#python_web_services
http://www.python.org/doc/current/lib/module-xmlrpclib.html
http://www.python.org/doc/current/lib/serverproxy-objects.html
