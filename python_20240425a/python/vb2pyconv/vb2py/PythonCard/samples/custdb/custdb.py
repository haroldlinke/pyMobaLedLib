#!/usr/bin/python

"""
__version__ = "$Revision: 1.10 $"
__date__ = "$Date: 2005/12/13 11:13:22 $"
"""

"""
use a comma separated value file as a database

Author: Juergen Rauch
eMail: juergen@yebu.de
Date: 21-Mar-02

"""

import PythonCard
from PythonCard import dialog, model

configFile = 'custdb.ini'
columns = [ 'name',
            'firstName',
            'title',
            'gender',
            'function',
            'company',
            'telBusi',
            'telPriv',
            'telFax',
            'telMobi',
            'email',
            'homepage',
            'zipCode',
            'city',
            'street',
            'notes',
            'res1',
            'res2',
            'res3']

def sortByCompany(a,b):
    if a['company'] > b['company']:
        return 1
    if a['company'] == b['company']:
        return 0
    if a['company'] < b['company']:
        return -1
   
def sortByName(a,b):
    if a['name'] > b['name']:
        return 1
    if a['name'] == b['name']:
        return 0
    if a['name'] < b['name']:
        return -1

class CustDbStack(model.Background):

    def on_initialize(self, event):
        import ConfigParser
        self.parser = ConfigParser.ConfigParser()
        self.parser.read( configFile )
        "put the company list into the listbox"
        self.dataFile = self.parser.get('ConfigData','data')
        rows = open(self.dataFile,'r').readlines()
        self.selected = self.parser.getint('ConfigData','selected')
        self.rowsDict = []
        line = 0
        for r in rows:
            line += 1
            r = r[:-1]  # remove the \n here
            r = r.replace(r'\012','\n') # convert coded 012 back to \n
            if r.count(',') == 18:
                d = {}
                i = 0
                values = r.split(',')
                for k in columns:
                    d[k]=values[i].replace(r'\054',',') # kk convert octal coded comma to real comma
                    i+=1
                self.rowsDict.append(d)
            else:
                msg = "Data inconsistent: number of commas = %s in line: %s in file: %s"%(r.count(','), line, self.dataFile)
                dlg = dialog.alertDialog(self, msg, '%s inconsistent'%self.dataFile)
                self.close()
        self.components.companyList.insertItems(self.getCompanyList(), 0)
        self.components.sortBy.stringSelection = self.parser.get('ConfigData','sortBy')
        self.showSelected()
      
    def getCompanyList(self):
        l = []
        if self.parser.get('ConfigData','sortBy') == 'name':
            self.rowsDict.sort(sortByName)
        else:
            self.rowsDict.sort(sortByCompany)
        for r in self.rowsDict:
            if self.parser.get('ConfigData','sortBy') == 'name':
                if not r['name']:
                    l.append(', '+r['company'])
                else:
                    l.append(r['name']+', '+r['firstName'])
            else:
                l.append( '%s, %s'%(r['company'], r['name']))
        return l
    
    def showSelected(self):
        if self.selected <0:
            self.selected = 0
        if self.selected >= len(self.rowsDict):
            self.selected = len(self.rowsDict)-1
        self.components.firstName.text = self.rowsDict[self.selected]['firstName']
        self.components.name.text = self.rowsDict[self.selected]['name']
        self.components.street.text = self.rowsDict[self.selected]['street']
        self.components.zipCode.text = self.rowsDict[self.selected]['zipCode']
        self.components.city.text = self.rowsDict[self.selected]['city']
        self.components.email.text = self.rowsDict[self.selected]['email']
        self.components.company.text = self.rowsDict[self.selected]['company']
        self.components.notes.text = self.rowsDict[self.selected]['notes']
        self.components.title.text = self.rowsDict[self.selected]['title']
        self.components.function.text = self.rowsDict[self.selected]['function']
        self.components.telMobi.text = self.rowsDict[self.selected]['telMobi']
        self.components.telBusi.text = self.rowsDict[self.selected]['telBusi']
        self.components.telFax.text = self.rowsDict[self.selected]['telFax']
        self.components.telPriv.text = self.rowsDict[self.selected]['telPriv']
        self.components.homepage.text = self.rowsDict[self.selected]['homepage']
        self.components.selectedFld.text = str(self.selected)
       
        self.components.companyList._setSelection(int(self.selected))
        self.parser.set('ConfigData','selected',self.selected)
        self.parser.write(open(configFile,'w'))
       
    def on_sortBy_select(self, event):
        self.parser.set('ConfigData','sortBy', event.target.stringSelection)
        self.parser.write(open(configFile,'w'))
        # change the content of the companyList
        self.components.companyList.clear()
        self.components.companyList.insertItems(self.getCompanyList(), 0)

    def on_companyList_select(self, event):
        self.selected = event.target.selection
        self.showSelected()

    def on_loseFocus(self, event):
        if event.target.name in ['firstName', 'name', 'street', 'zipCode',
                                 'city', 'email', 'company', 'title',
                                 'function', 'telMobi', 'telBusi', 'telFax',
                                 'telPriv', 'homepage', 'notes']:
            self.rowsDict[self.selected][event.target.name] = event.target.text
            self.store()

    def on_selectedFld_keyUp(self, event):
        try:
           self.selected = int(event.target.text)
        except ValueError:
           self.selected = 0
        self.showSelected()
              
    def on_nextButt_mouseDown(self, event):
        self.selected += 1
        self.showSelected()
       
    def on_prevButt_mouseDown(self, event):
        self.selected -= 1
        self.showSelected()

    def on_newButt_mouseDown(self, event):
        d = {}
        i = 0
        for k in columns:
           d[k]= ''
        d['gender'] = 'm' # default
        self.rowsDict.append(d)
        self.selected = len(self.rowsDict)
        self.showSelected()

    def on_delButt_mouseUp(self, event):
        result = dialog.messageDialog(self, 'Are you sure you want to delete the entry: %s ?'%self.rowsDict[self.selected]['name'], 'Delete Entry.' )
        if result.accepted:
           print "messageDialog result:\naccepted: %s\nreturnedString: %s" % (result.accepted, result.returnedString)
           del self.rowsDict[self.selected]
           self.selected -= 1
           self.showSelected()
           self.store()

    def store(self):
        lines = []
        for r in self.rowsDict:
           l = ''
           for c in columns:
               txt=r[c].replace(',',r'\054') # convert comma to ocal representation
               l = l + txt  + ','
           l = l.replace('\n',r'\012') # convert \n to it's octal coding
           lines.append(l[:-1]+'\n')   # give'em the \n back
        lines.sort()                   # this is not quite right because it sorts 'A-Za-z'
        file = open(self.dataFile,'wb') # so we'll independantly of os terminate w/ \n
        file.writelines(lines)
        file.close()


if __name__ == '__main__':
    app = model.Application(CustDbStack)
    app.MainLoop()

