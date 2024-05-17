#!/usr/bin/python

"""
App Name: dbBrowser2
Description: A PythonCard sample application to browse data from external data
stores. These are mainly relational databases but may also include data files 
in future releases. The data sources currently supported are;
    MySQL - release 3.23.36 and above with MySQLdb 0.3.5 and above
    Oracle - release 9.2, 8.0.5, 8.1.6, and 8.1.7 with cx_Oracle or DCOracle2
    Gadfly - release 1.0
    SQLite - using PySQLite
    Metakit -

This sample differs from the original dbBrowser by presenting data using a wxGrid
Because this provides a different interface I've removed the browsing buttons
that were present in the original application.

Changes in this release;

Known bugs/Things to do;
"""
__author__ = "Andy Todd <andy47@halfcooked.com>"
__date__ = "3rd May, 2003"
__version__ = '$Revision: 1.10 $'[11:-2]

from PythonCard import model, dialog
import os
import dbLogin
from dbTable import DBTable

class DbBrowser(model.Background):
    def on_initialize(self, event):
        "Initialise the dbBrowser main window"
        # Display the dbLogin modal dialog
        self.on_connect_command(None)
        # Set up the readme for the help|about menu 
        try:
            self.readme=open('readme.txt').read()
        except IOError:
            self.readme=''

    def showAlert(self, aMessage, aTitle):
        "Show Alert dialog with aMessage and aTitle"
        dialog.alertDialog(self, aMessage, aTitle)

    def on_close(self, event):
        # Common exit code - should close DB connection here
        # In the meantime, just call the parent method
        event.skip()

    def on_btnBrowse_mouseClick(self, event):
        # Completely re-written for dbBrowser2
        selectedTable=self.components["chsTables"].stringSelection
        if selectedTable:
            # This is a bit of a cop out, just delete and re-create the grid
            gridDefn={'name':'myGrid', 'type':'Grid'}
            gridDefn['position']=self.components.myGrid.position
            gridDefn['size']=self.components.myGrid.size
            del self.components[gridDefn['name']]
            self.components[gridDefn['name']]=gridDefn
            self.dbTable=DBTable(self._database, selectedTable)
            self.components.myGrid.SetTable(self.dbTable)
            self.components.myGrid.AutoSizeColumns()
            self.components.myGrid.AdjustScrollbars()

    def on_connect_command(self, event):
        # Display the dbLogin.rsrc.py modal dialog
        dlg = dbLogin.dbLogin(self)
        dlg.showModal()
        dlg.destroy()

    def on_mnuExit_select(self, event):
        self.close()

    def on_mnuAbout_select(self, event):
        dialog.scrolledMessageDialog(self, self.readme, 'About')

if __name__=="__main__":
    app=model.Application(DbBrowser)
    app.MainLoop()
