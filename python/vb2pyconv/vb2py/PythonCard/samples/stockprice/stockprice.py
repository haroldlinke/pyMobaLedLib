#!/usr/bin/python

"""
__version__ = "$Revision: 1.12 $"
__date__ = "$Date: 2005/09/18 03:59:22 $"

This sample is a clone of the AppleScript Studio example at: 
  http://www.oreillynet.com/pub/a/mac/2002/02/01/applescript_macosx.html

It requires the SOAP.py module from SOAP.py 0.9.7 available at:
  http://sourceforge.net/projects/pywebsvcs

Also see the SOAP.py authors article at:
  http://www-106.ibm.com/developerworks/webservices/library/ws-pyth2/
"""

from PythonCard import dialog, model
import time
try:
    from SOAP import SOAPProxy
    FOUND_SOAP = 1
except ImportError, msg:
    try:
        from SOAPpy import SOAPProxy
        FOUND_SOAP = 1
    except ImportError, msg:
        FOUND_SOAP = 0

# KEA 2001-12-11
# if you want to build a standalone executable using py2exe
# then uncomment the import line below
# due to the way the dynamic imports of components work, each
# component that an app uses needs to be imported statically when
# doing a py2exe build
#from PythonCard.components import button, choice, statictext, textfield

"""
# http://services.xmethods.net/soap/urn:xmethods-delayed-quotes.wsdl
>>> server = SOAPProxy('http://services.xmethods.net/soap',
namespace='urn:xmethods-delayed-quotes')
>>> server.getQuote('MSFT')
62.659999999999997

I want to use this service
# http://soaptest.activestate.com/
# http://soaptest.activestate.com/StockQuotePlus.wsdl
# how am I supposed to know what country names are valid?!!!
# this service is down, so I haven't been able to get the right incantation yet
>>> server = SOAPProxy("http://soaptest.activestate.com:8080/PerlEx/soap.plex",
namespace="uri:http://activestate.com/", soapaction="urn:activestate")
>>> server.StockQuoteInCountry("SUNW", "United States")

but it is currently down, so I can't test against it. I chose an alternative stock
price service from the list of SOAP web services at:
http://www.xmethods.net/
"""

# need a decent way of handling timeouts here
# look at options in SOAP.py
def getStockPrice(symbol, country='United States'):
    price = -1
    try:
        server = SOAPProxy('http://services.xmethods.net/soap',
                            namespace='urn:xmethods-delayed-quotes')
        price = server.getQuote(symbol)
    except Exception, msg:
        pass
    return price

    
class Minimal(model.Background):

    def on_initialize(self, event):
        if not FOUND_SOAP:
            # alert user, then exit cleanly
            result = dialog.alertDialog(self,
                "Can't find SOAP.py module, exiting application...",
                'Error: Missing module')
            self.close()

    def displayDateTime(self, t):
        dateStr = time.strftime("%A, %B %d, %Y,  %I:%M %p", t)
        self.components.fldDate.text = dateStr
        
    def on_btnGetPrice_mouseClick(self, event):
        symbol = self.components.fldStockSymbol.text
        country = self.components.chcCurrency.stringSelection
        self.components.fldStockPrice.text = str(getStockPrice(symbol, country))
        now = time.localtime(time.time())
        self.displayDateTime(now)


if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
