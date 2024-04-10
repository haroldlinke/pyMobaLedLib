# eventually this will do the proxy stuff, when I can get it to work.  the
# exmaple proxy code at the bottom was found on the net somewhere, but it
# seems to only work intermitentaly.
# arg.

import xmlrpclib

class trURLlibTransport(xmlrpclib.Transport):
    
    # client identifier (may be overridden)
    user_agent = "textRouter/0.58"

    def __init__(self, proxy=""):
        self.proxy = proxy
        
    def request(self, host, handler, request_body, verbose=0):
        # issue XML-RPC request

        if self.proxy != "":
            h = self.make_connection(self.proxy)
        else:
            h = self.make_connection(host)

        if verbose:
            h.set_debuglevel(1)

        if self.proxy != "":
            self.send_request(h, "http://" + host + handler, request_body)
        else:
            self.send_request(h, handler, request_body)
            
        self.send_host(h, host)
        self.send_user_agent(h)
        self.send_content(h, request_body)

        errcode, errmsg, headers = h.getreply()

        if errcode != 200:
            raise xmlrpclib.ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
                )

        self.verbose = verbose

        return self.parse_response(h.getfile())
