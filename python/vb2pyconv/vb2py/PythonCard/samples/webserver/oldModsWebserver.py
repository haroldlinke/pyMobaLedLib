#!/usr/bin/python

"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"
"""

import wx
from PythonCard import configuration, model
import os, sys
import shutil
from BaseHTTPServer import HTTPServer
import CGIHTTPServer
from CGIHTTPServer  import CGIHTTPRequestHandler
import threading 
import Queue
import ConfigParser
import socket

# imports needed code is moved back into standard libs
import urllib
import select

CONFIG_FILE = 'webserver.ini'

# a backwards compatible date_time_string function
# with the one in BaseHTTPRequestHandler
# it seems like this should be moved and made a function
# as I've done below

import time
import rfc822

weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

monthname = [None,
             'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def date_time_string(t=None):
    global weekdayname, monthname
    """Return the current date and time formatted for a message header."""
    if not t:
        t = time.time()
    # assume user supplied time value will be local, not gmt!
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(t)
    s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
            weekdayname[wd],
            day, monthname[month], year,
            hh, mm, ss)
    return s


class MyRequestHandler(CGIHTTPRequestHandler):
    # the server variable contains the reference back to the view
    def log_message(self, format, *args):
        msg = "%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args)
        if format.startswith('"%s"'):
            self.server._notify_window.msgQueue.put(msg)
            wx.WakeUpIdle()
            # just log to the GUI now, this could go to a file as well
        else:
            # don't put CGI error and exit status messages in the main log
            print msg

    cgi_extensions = [".py", ".pyw", ".cgi"]

    def is_python(self, path):
        """Test whether argument path is a Python script."""
        head, tail = os.path.splitext(path)
        return tail.lower() in self.cgi_extensions

    # this is a modification to run_cgi in CGIHTTPRequestHandler
    # to deal with the IE POST bug which should get fixed in
    # Python 2.2.2 and 2.3
    # the only additions are under the comment starting with KEA
    def run_cgi(self):
        """Execute a CGI script."""
        dir, rest = self.cgi_info
        i = rest.rfind('?')
        if i >= 0:
            rest, query = rest[:i], rest[i+1:]
        else:
            query = ''
        i = rest.find('/')
        if i >= 0:
            script, rest = rest[:i], rest[i:]
        else:
            script, rest = rest, ''
        scriptname = dir + '/' + script
        scriptfile = self.translate_path(scriptname)
        if not os.path.exists(scriptfile):
            self.send_error(404, "No such CGI script (%s)" % `scriptname`)
            return
        if not os.path.isfile(scriptfile):
            self.send_error(403, "CGI script is not a plain file (%s)" %
                            `scriptname`)
            return
        ispy = self.is_python(scriptname)
        if not ispy:
            if not (self.have_fork or self.have_popen2 or self.have_popen3):
                self.send_error(403, "CGI script is not a Python script (%s)" %
                                `scriptname`)
                return
            # KEA 2002-09-17
            # it is a pain to have to chmod on CGIs
            # and this is a personal server, so skip this check
            #if not self.is_executable(scriptfile):
            #    self.send_error(403, "CGI script is not executable (%s)" %
            #                    `scriptname`)
            #    return

        # Reference: http://hoohoo.ncsa.uiuc.edu/cgi/env.html
        # XXX Much of the following could be prepared ahead of time!
        env = {}
        env['SERVER_SOFTWARE'] = self.version_string()
        env['SERVER_NAME'] = self.server.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PROTOCOL'] = self.protocol_version
        env['SERVER_PORT'] = str(self.server.server_port)
        env['REQUEST_METHOD'] = self.command
        uqrest = urllib.unquote(rest)
        env['PATH_INFO'] = uqrest
        env['PATH_TRANSLATED'] = self.translate_path(uqrest)
        env['SCRIPT_NAME'] = scriptname
        if query:
            env['QUERY_STRING'] = query
        host = self.address_string()
        if host != self.client_address[0]:
            env['REMOTE_HOST'] = host
        env['REMOTE_ADDR'] = self.client_address[0]
        # XXX AUTH_TYPE
        # XXX REMOTE_USER
        # XXX REMOTE_IDENT
        if self.headers.typeheader is None:
            env['CONTENT_TYPE'] = self.headers.type
        else:
            env['CONTENT_TYPE'] = self.headers.typeheader
        length = self.headers.getheader('content-length')
        if length:
            env['CONTENT_LENGTH'] = length
        accept = []
        for line in self.headers.getallmatchingheaders('accept'):
            if line[:1] in "\t\n\r ":
                accept.append(line.strip())
            else:
                accept = accept + line[7:].split(',')
        env['HTTP_ACCEPT'] = ','.join(accept)
        ua = self.headers.getheader('user-agent')
        if ua:
            env['HTTP_USER_AGENT'] = ua
        co = filter(None, self.headers.getheaders('cookie'))
        if co:
            env['HTTP_COOKIE'] = ', '.join(co)
        # XXX Other HTTP_* headers
        if self.have_fork:
            # KEA 2002-09-15
            # make sure CGIs have access to os.environ
            env.update(os.environ)
        else:
            # Since we're setting the env in the parent, provide empty
            # values to override previously set values
            for k in ('QUERY_STRING', 'REMOTE_HOST', 'CONTENT_LENGTH',
                      'HTTP_USER_AGENT', 'HTTP_COOKIE'):
                env.setdefault(k, "")

        self.send_response(200, "Script output follows")

        decoded_query = query.replace('+', ' ')

        if self.have_fork:
            # Unix -- fork as we should
            args = [script]
            if '=' not in decoded_query:
                args.append(decoded_query)
            # KEA 2002-09-15
            # we want to run as the same user
            # that started the server so we have access
            # to their files
            #nobody = CGIHTTPServer.nobody_uid()
            # KEA
            # not supposed to flush on Mac OS X
            #self.rfile.flush() # Always flush before forking
            self.wfile.flush() # Always flush before forking
            pid = os.fork()
            if pid != 0:
                # Parent
                pid, sts = os.waitpid(pid, 0)
                # throw away additional data [see bug #427345]
                while select.select([self.rfile], [], [], 0)[0]:
                    waste = self.rfile.read(1)
                if sts:
                    self.log_error("CGI script exit status %#x", sts)
                return
            # Child
            try:
                # KEA 2002-09-15
                # see nobody comment above
                #try:
                #    os.setuid(nobody)
                #except os.error:
                #    pass
                os.dup2(self.rfile.fileno(), 0)
                os.dup2(self.wfile.fileno(), 1)
                os.execve(scriptfile, args, env)
            except Exception, msg: # Should test for a particular Exception
                self.server.handle_error(self.request, self.client_address)
                os._exit(127)

        elif self.have_popen2 or self.have_popen3:
            # Windows -- use popen2 or popen3 to create a subprocess
            import shutil
            if self.have_popen3:
                popenx = os.popen3
            else:
                popenx = os.popen2
            os.environ.update(env)
            cmdline = scriptfile
            if self.is_python(scriptfile):
                interp = sys.executable
                if interp.lower().endswith("w.exe"):
                    # On Windows, use python.exe, not pythonw.exe
                    interp = interp[:-5] + interp[-4:]
                cmdline = "%s -u %s" % (interp, cmdline)
            if '=' not in query and '"' not in query:
                cmdline = '%s "%s"' % (cmdline, query)
            self.log_message("command: %s", cmdline)
            try:
                nbytes = int(length)
            except Exception, msg: # Should test for a particular Exception
                nbytes = 0
            files = popenx(cmdline, 'b')
            fi = files[0]
            fo = files[1]
            if self.have_popen3:
                fe = files[2]
            if self.command.lower() == "post" and nbytes > 0:
                data = self.rfile.read(nbytes)
                fi.write(data)
                # KEA now throw away data past Content-length
                while select.select([self.rfile._sock], [], [], 0)[0] != []:
                    waste = self.rfile._sock.recv(1)
            fi.close()
            shutil.copyfileobj(fo, self.wfile)
            if self.have_popen3:
                errors = fe.read()
                fe.close()
                if errors:
                    self.log_error('%s', errors)
            sts = fo.close()
            if sts:
                self.log_error("CGI script exit status %#x", sts)
            else:
                self.log_message("CGI script exited OK")

        else:
            # Other O.S. -- execute script in this process
            os.environ.update(env)
            save_argv = sys.argv
            save_stdin = sys.stdin
            save_stdout = sys.stdout
            save_stderr = sys.stderr
            try:
                try:
                    sys.argv = [scriptfile]
                    if '=' not in decoded_query:
                        sys.argv.append(decoded_query)
                    sys.stdout = self.wfile
                    sys.stdin = self.rfile
                    execfile(scriptfile, {"__name__": "__main__"})
                finally:
                    sys.argv = save_argv
                    sys.stdin = save_stdin
                    sys.stdout = save_stdout
                    sys.stderr = save_stderr
            except SystemExit, sts:
                self.log_error("CGI script exit status %s", str(sts))
            else:
                self.log_message("CGI script exited OK")

    # replacement for SimpleHTTPServer.SimpleHTTPRequestHandler.send_head
    # which should eventually make its way back into the
    # SimpleHTTPServer in Python 2.2.2 and 2.3
    # this version handles If-Modified-Since and 304 responses and
    # sends the Content-Length
    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        """Version of send_head that support CGI scripts"""
##        print self.command
##        print self.request_version
##        print self.path
##        print self.headers
        
        if self.is_cgi():
            return self.run_cgi()
        #else:
        #    return SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)

        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)

        if ctype.startswith('text/'):
            mode = 'r'
        else:
            mode = 'rb'
        try:
            f = open(path, mode)
        except IOError:
            self.send_error(404, "File not found")
            return None

        try:
            s = os.stat(path)
            # the os.stat modified time should be local
            # mdt is only used for comparisons below now
            mdt = time.gmtime(s[8])
            lastModified = date_time_string(s[8])
            size = str(s[6])
        except Exception, msg: # Should test for a particular exception
            mdt = None
            lastModified = None
            size = None

        ims = self.headers.getheader('if-modified-since')
        not_modified = 0
        if ims and mdt:
            # items 6, 7, 8 of parsedate will be usable
            # so those aren't used in the comparison below
            # see http://www.python.org/doc/current/lib/module-rfc822.html
            sdt = rfc822.parsedate(ims.split(';')[0])
            if mdt[:6] <= sdt[:6]:
                not_modified = 1
                # don't send back a file if 304
                f = None
        if not_modified:
            self.send_response(304)
        else:
            # note that send_response doesn't currently
            # accept an optional size parameter, so it can't
            # pass on the size to log_request
            # I've provided a backward-compatible version below that uses
            # a named argument
            self.send_response(200, size=size)
            if lastModified:
                self.send_header("Last-Modified", lastModified)
            if size:
                self.send_header("Content-Length", size)
            self.send_header("Content-type", ctype)
        self.end_headers()
        return f

    # replacement for send_response in BaseHTTPRequestHandler
    # that accepts a named size parameter
    def send_response(self, code, message=None, size=None):
        """Send the response header and log the response code.

        Also send two standard headers with the server software
        version and the current date.

        """
        if size:
            self.log_request(code, size)
        else:
            self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s %s %s\r\n" %
                             (self.protocol_version, str(code), message))
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

class WebServer(HTTPServer):
    def __init__(self, notify_window, server_address, RequestHandlerClass, validIPList=None):
        self._notify_window = notify_window 
        # this list will come from a config file
        # and there will be a dialog to edit the valid IP addresses
        if validIPList:
            self.validIPList = validIPList
        else:
            self.validIPList = ['127.0.0.1']
        # add host IP address that this server is running on
        self.validIPList.append(socket.gethostbyname(socket.gethostname()))
        self.allowAny = 0
        HTTPServer.__init__(self, server_address, RequestHandlerClass)

    def verify_request(self, request, client_address):
        if self.allowAny or client_address[0] in self.validIPList:
            return 1
        else:
            return 0

    # just a guess that this is how we should use threads
    def server(self):
        self.serve_forever()


class WebServerView(model.Background):

    def on_initialize(self, event):
        self.initSizers()

        self.loadConfig()
        
        # if you wanted to limit the on screen log size, then set
        # this to something other than 0
        self.maxSizeLog = 0
        
        # Set up event handler for any worker thread results 
        """
        Robin said:
        The Queue class is thread-safe, using a mutex and semaphore to protect
        access to its contents, so is ideally suited for something like this.
        """
        self.msgQueue = Queue.Queue()
            
        os.chdir(self.htdocs)
        self.srvraddr = ('', self.port)
        # give the server and request handlers 
        # a reference back to the view for logging
        self.webServer = WebServer(self, self.srvraddr, MyRequestHandler, self.validIPList)
        self.thread = threading.Thread(target = self.webServer.server)
        # I think this allows Python to kill the thread when we quit wxPython
        # setDaemon must be called before start
        self.thread.setDaemon(1)
        self.thread.start()

    def loadConfig(self):
        self.configPath = os.path.join(configuration.homedir, 'webserver')
        if not os.path.exists(self.configPath):
            os.mkdir(self.configPath)
        configPath = os.path.join(self.configPath, CONFIG_FILE)
        defaultPath = os.path.join(self.application.applicationDirectory, CONFIG_FILE)
        if not os.path.exists(configPath):
            shutil.copy2(defaultPath, configPath)
        parser = ConfigParser.ConfigParser()
        parser.read(configPath)
        self.htdocs = parser.get('ConfigData', 'htdocs')
        self.port = int(parser.get('ConfigData', 'port'))
        ips = parser.get('ConfigData', 'iplist')
        self.validIPList = ips.split(',')

    def initSizers(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.components.fldLog, 1, wx.EXPAND)

        sizer1.Fit(self)
        sizer1.SetSizeHints(self)
        self.panel.SetSizer(sizer1)
        self.panel.SetAutoLayout(1)
        self.panel.Layout()

    def on_idle(self, event):
        if not self.msgQueue.empty():
            msg = self.msgQueue.get()
            self.doLogResult(msg)
            event.RequestMore()

    def doLogResult(self, data):
        if data is not None:
            # code borrowed from the Message Watcher event history display
            log = self.components.fldLog
            log.SetReadOnly(0)
            if self.maxSizeLog and log.GetLength() > self.maxSizeLog:
                # delete many lines at once to reduce overhead
                text = log.GetText()
                endDel = text.index('\n', self.maxSizeLog / 10) + 1
                log.SetTargetStart(0)
                log.SetTargetEnd(endDel)
                log.ReplaceTarget("")
            log.GotoPos(log.GetLength())
            log.AddText(data)
            log.GotoPos(log.GetLength())
            log.SetReadOnly(1)
        else:
            pass

    def on_menuOptionsAllowAny_select(self, event):
        self.webServer.allowAny = self.menuBar.getChecked('menuOptionsAllowAny')


if __name__ == '__main__':
    app = model.Application(WebServerView)
    app.MainLoop()
