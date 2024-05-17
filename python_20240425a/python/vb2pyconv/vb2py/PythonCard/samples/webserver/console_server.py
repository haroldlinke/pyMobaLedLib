#!/usr/bin/python
############################################
# implement a HTTP server in Python which 
# knows how to run server-side CGI scripts;
# change root dir for your server machine
############################################

import os
from BaseHTTPServer import HTTPServer
from CGIHTTPServer  import CGIHTTPRequestHandler
import socket

class MyRequestHandler(CGIHTTPRequestHandler):
    def is_python(self, path):
        """Test whether argument path is a Python script."""
        head, tail = os.path.splitext(path)
        return tail.lower() in (".py", ".pyw", ".cgi")

class localServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        self.allowAny = 0
        self.validIPList = ['127.0.0.1']
        # add host IP address that this server is running on
        self.validIPList.append(socket.gethostbyname(socket.gethostname()))
        HTTPServer.__init__(self, server_address, RequestHandlerClass)

    def verify_request(self, request, client_address):
        if self.allowAny or client_address[0] in self.validIPList:
            return 1
        else:
            return 0

if __name__ == '__main__':
    os.chdir("html")
    # my hostname, portnumber
    srvraddr = ('', 8000)     
    srvrobj  = localServer(srvraddr, MyRequestHandler)
    # run as perpetual demon
    srvrobj.serve_forever()
