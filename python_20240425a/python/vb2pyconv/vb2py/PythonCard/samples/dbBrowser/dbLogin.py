#!/usr/bin/python

"""
App Name: dbBrowser
Description: Provide a login dialog for the dbBrowser application
"""
__version__ = '$Revision: 1.14 $'[11:-2]
__date__ = "16th September, 2002"
__author__ = "Andy Todd <andy47@halfcooked.com>"

import os
from PythonCard import dialog, model

dbHandlers = { 'MySQL': 'mySQLBrowse'
              ,'Oracle': 'oracleBrowse'
              ,'Gadfly': 'gadflyBrowse'
              ,'MetaKit': 'metakitBrowse'
              ,'PySQLite': 'pysqliteBrowse'
              ,'PySQLite2': 'pysqlite2Browse'
              ,'PostgreSQL': 'postgreBrowse'
              ,'CSV': 'csvBrowse' }

class dbLogin(model.CustomDialog):
    def __init__(self, aBg):
        "Initialise the dialog"
        model.CustomDialog.__init__(self, aBg)
        self.parent = aBg
        self.components.txtUsername.setFocus()

    def on_btnConnect_mouseClick(self, event):
        """
        Database connection is a dictionary so we can adapt the members
        depending on the RDBMS we select (in v1.0, natch)
        """
        self.parent.statusBar.text = "Connecting ..."
        dbHandler = __import__(dbHandlers[self.components.choice.stringSelection])
        dbClass = dbHandler.browse
        selection = self.components.choice.stringSelection
        connection = {}
        if selection in ('Gadfly', 'Metakit', 'PySQLite', 'PySQLite2', 'CSV'):
            connection['databasename'] = self.components['txtUsername'].text
            connection['directory'] = self.components['txtPassword'].text
        else:
            connection['username'] = self.components['txtUsername'].text
            connection['password'] = self.components['txtPassword'].text
            connection['database'] = self.components['txtDatabase'].text
        self.parent.connection = connection
        # Get the choice widget and add the available database tables to it
        self.parent._database=dbClass(self.parent.connection)

        if self.parent._database._cursor:
            self.parent.components.chsTables.items=self.parent._database.getTables()
            # Change focus to the chsTables widget, if we have any tables
            if self.parent.components.chsTables.items:
                self.parent.components.chsTables.stringSelection=self.parent.components.chsTables.items[0]
            self.parent.components.chsTables.setFocus()
            self.parent.statusBar.text = "Connected"
        else: # The connection do the data source has failed
            self.parent.showAlert('Error: Could not connect to database', 'Database Error')
            self.parent.statusBar.text = "Connection failed"
        event.skip()

    def on_btnFile_mouseClick(self, event):
        if self.components.choice.stringSelection == 'Gadfly':
            wildcard = wildcard = "Gadfly files (*.gfd)|*.gfd"
            result = dialog.openFileDialog(wildcard=wildcard)
        elif self.components.choice.stringSelection == 'CSV':
            wildcard = "CSV files (*.csv)|*.csv"
            result = dialog.openFileDialog(wildcard=wildcard)
        else:
            result = dialog.openFileDialog()
        if result.accepted:
            dir, filename = os.path.split(result.paths[0])
            if self.components.choice.stringSelection == 'Gadfly':
                filename = os.path.splitext(filename)[0]
            self.components.txtUsername.text = filename
            self.components.txtPassword.text = dir

    def on_choice_select(self, event):
        "Display the appropriate widgets for the selected database"
        if self.components.choice.stringSelection in ('Gadfly', 'MetaKit', 'PySQLite', 'PySQLite2'):
            self.components.lblUsername.text = 'DB Name'
            self.components.lblPassword.text = 'DB Directory'
            self.components.lblDatabase.visible = False
            self.components.txtDatabase.visible = False
            self.components.btnFile.visible = True
        elif self.components.choice.stringSelection in ('CSV'):
            self.components.lblUsername.text = "File"
            self.components.lblPassword.text = "Directory"
            self.components.lblDatabase.visible = False
            self.components.txtDatabase.visible = False
            self.components.btnFile.visible = True
        else:
            self.components.lblUsername.text = 'Username'
            self.components.lblPassword.text = 'Password'
            self.components.lblDatabase.visible = True
            self.components.txtDatabase.visible = True
            self.components.btnFile.visible = False
        event.skip()
