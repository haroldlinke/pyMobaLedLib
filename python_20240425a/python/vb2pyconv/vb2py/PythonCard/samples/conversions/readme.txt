conversions provides conversion between english <-> morse code and celsius
<-> fahrenheit. 

The conversion framework is implemented so that it should
be relatively easy to add other conversions. The base class handles
renaming the widgets for a particular conversion.

The sample has now been expanded to include a currency conversion sample. This currently only converts between Australian Dollars and US Dollars. It uses a similar SOAP model to the stockprice sample and the server at:
  http://www.xmethods.net/

This could be generalised to convert between any two available currencies but would require a little more customisation of the interface.

It requires the SOAP.py module from SOAP.py 0.9.7 available at:
  http://sourceforge.net/projects/pywebsvcs
Also see the SOAP.py authors article at:
  http://www-106.ibm.com/developerworks/webservices/library/ws-pyth2/

The SOAP service used is documented at:
  http://www.xmethods.net/ve2/ViewListing.po;jsessionid=uasjc2zKRJYzpJGd55tR0xN8(QhxieSRM)?serviceid=5
