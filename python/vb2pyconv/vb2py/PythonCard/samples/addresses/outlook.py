#!/usr/bin/python
"""
I need a more generic way of dealing with these modules that may not be available.
Also, if the MSOutlook __init__ can't be completed, what's an appropriate failure
mechanism?
"""
__version__ = "$Revision: 1.6 $"
__date__ = "$Date: 2005/12/13 11:13:21 $"

try:
    import win32com.server.util
    import win32com.client
    import pythoncom
    import pywintypes
    import winerror
    
    WIN32_FOUND = 1
except ImportError:
    WIN32_FOUND = 0

import traceback
import sys

class MSOutlook:
    def __init__(self):
        self.outlookFound = 0
        if WIN32_FOUND:
            #oOutlookApp = win32com.client.Dispatch("Outlook.Application.9")
            #self.oOutlookApp = win32com.client.Dispatch("Outlook.Application")
            # use gencache.EnsureDispatch to make sure makepy is run if necessary
            # this dramatically speeds up usage of the COM object
            self.oOutlookApp = win32com.client.gencache.EnsureDispatch("Outlook.Application")
            self.outlookFound = 1
        else:
            #print "unable to load Outlook"
            pass
        self.olFolderInbox = 6
        self.olContactItem = 2
        self.olFolderContacts = 10
        self.olContact = 40
        self.olFolderDisplayNormal = 0
        self.olMinimized = 1
        self.olNormalWindow = 2
        self.records = []        

    def loadRecords(self):
        if not self.outlookFound:
            return
        # this should use more try/except blocks or nested blocks
        onMAPI = self.oOutlookApp.GetNamespace("MAPI")
        ofContacts = onMAPI.GetDefaultFolder(self.olFolderContacts)
        #print "number of contacts:", len(ofContacts.Items)
        for oc in range(len(ofContacts.Items)):
            contact = ofContacts.Items.Item(oc + 1)
            if contact.Class == self.olContact:
                record = {}
                record['FullName'] = contact.FullName
                record['CompanyName'] = contact.CompanyName
                record['MailingAddressStreet'] = contact.MailingAddressStreet
                record['MailingAddressCity'] = contact.MailingAddressCity
                record['MailingAddressState'] = contact.MailingAddressState
                record['MailingAddressPostalCode'] = contact.MailingAddressPostalCode
                record['HomeTelephoneNumber'] = contact.HomeTelephoneNumber
                record['BusinessTelephoneNumber'] = contact.BusinessTelephoneNumber
                record['MobileTelephoneNumber'] = contact.MobileTelephoneNumber
                record['Email1Address'] = contact.Email1Address
                record['Body'] = contact.Body
                self.records.append(record)
        #print "InterfaceCount/GatewayCount %d/%d" % (pythoncom._GetInterfaceCount(), pythoncom._GetGatewayCount())

