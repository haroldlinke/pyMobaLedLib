#!/usr/bin/python

"""
App Name: dbBrowser
Description: A PythonCard sample application to browse data from external data
stores. These are mainly relational databases but may also include data files 
in future releases. The data sources currently supported are;
    MySQL - release 3.23.36 and above with MySQLdb 0.3.5 and above
    Oracle - release 8.0.5, 8.1.6, and 8.1.7 with cx_Oracle 2.3

Changes in this release;
16.09.2001 - Moved the dbLogin dialog code into its own module
20.11.2001 - Moved icon setting code to the framework
10.11.2001 - Added support for Oracle as well as MySQL. Changed the version
             numbering to reflect the CVS revision number
0.3 - Moved the login and database selection functionality to the dbLogin modal
dialog. Added an application icon (inspired by the Windows icon used by Oracle)
0.2 - Added dynamic event handling for the navigation buttons/menu items. This 
means only one method is needed to do the work but it is bound to two widgets.
Changed the layout of data widgets to one label and data item per line.
Used 'setFocus' to place the cursor in the table choice widget when the database
connection has been completed.

Known bugs/Things to do;
When you choose to browse a table with no rows the navigation functions should be disabled. They are currently enabled and pressing 'Next Row' or 'Previous Row' will produce errors in the console window.
When switching between different databases the dynamically created widgets should be cleared up, they currently do not get changed until a table from the new database is selected.
"""
__version__ = '$Revision: 1.33 $'[11:-2]
__date__ = "20th November, 2001"
__author__ = "Andy Todd <andy47@halfcooked.com>"

from PythonCard import configuration, model, dialog
#import wx
import os
import dbLogin

browsingButtons=['btnFirstRow', 'btnPreviousRow', 'btnNextRow', 'btnLastRow']

class DbBrowser(model.Background):
    def on_initialize(self, event):
        "Initialise the dbBrowser main window"
        # Display the dbLogin modal dialog
        self.on_connect_command(None)
        # Set up the readme for the help|about menu 
        try:
            self.readme=open('readme.txt').read()
        except IOError:
            self.readme=__doc__

    def _enableButton(self, enabled):
        "Hide or show the browsing control buttons"
        for button in browsingButtons:
            self.components[button].enabled=enabled

    def disableButtons(self):
        "Hide the browsing control buttons"
        self._enableButton(0)

    def enableButtons(self):
        "Show the browsing control buttons"
        self._enableButton(1)

    def getARow(self, selectedTable):
        "Get a row from the table and put the values in our widgets"
        row=self._database.getRow(selectedTable)
        if row:
            self._row.append(row)
            self.showRow(self._index)
        else:
            self._index-=1

    def showRow(self, index):
        "Show retrieved row number <index>"
        widgetCount=0
        for item in self._widgets:
            # All of our widgets are text, watch out for those date conversions!
            self.components[item].text=str(self._row[index][widgetCount])
            widgetCount+=1
        self.statusBar.text = "Row %d of %d" % (index+1, len(self._row))

    def showAlert(self, aMessage, aTitle):
        "Show Alert dialog with aMessage and aTitle"
        dialog.alertDialog(self, aMessage, aTitle)

    def on_close(self, event):
        # Common exit code - should close DB connection here
        # In the meantime, just call the parent method
        event.skip()

    def on_btnBrowse_mouseClick(self, event):
        selectedTable=self.components["chsTables"].stringSelection
        if selectedTable:
            if hasattr(self, "_widgets"):
                # Remove the currently painted widgets
                # This is a complete bodge and will be replaced in version x
                for i in self._widgets:
                    del self.components[i]
                    del self.components['lbl'+i[3:]]
            self._widgets=[] # This will hold the names of the dynamically created widgets
            rowHeight=25
            # By setting xPosWidget to 240 we assume our labels are no more than
            # 30 characters (30 * 8 = 240)
            xPosLabel, xPosWidget, yPos=1, 240, 106
            # Get all of the columns for this table and create a widget for each
            # NB this should really be put into a seperate function
            for columns in self._database.getColumns(selectedTable):
                # Column name are of the form 'word_word_word', we will 
                # slightly change this to 'WordWordWord'
                columnName=columns[0].title().replace("_", "")
                columnTitle = columns[0]
                columnType = columns[1]
                columnPrecision = columns[2]
                # Form a widget per column, as well as some boilerplate
                widgetDefn={'type':'StaticText',
                            'name':'lbl'+columnName,
                            'position':(xPosLabel, yPos),
                            'text':columnTitle}
                self.components[widgetDefn['name']]=widgetDefn
                # catch any unbounded or overly large columns
                if not columnPrecision or columnPrecision > 100:
                    columnPrecision = 30
                widgetDefn={'type':'TextField',
                            'name':'txt'+columnName,
                            'position':(xPosWidget, yPos),
                            'text':'',
                            'size':(columnPrecision*9, -1)} # replace 8 with a constant
                self.components[widgetDefn['name']]=widgetDefn
                self._widgets.append('txt'+columnName)
                # Put each label and widget on its own line
                yPos+=26
            """ 
            Now that we've painted the screen initialise the cursor and get 
            the first row. Note that this assumes that the columns returned 
            by getRow are in the same order as the call to getColumns above
            """
            self._index=0
            self._row=[]
            self.getARow(selectedTable)
            self.enableButtons()

    def on_connect_command(self, event):
        # Display the dbLogin.rsrc.py modal dialog
        dlg = dbLogin.dbLogin(self)
        dlg.showModal()
        dlg.destroy()

    def on_nextRecord_command(self, event):
        "Get the next row from the database"
        length=len(self._row)-1
        if self._index<length:
            self._index+=1
            self.showRow(self._index)
        elif self._index==length:
            selectedTable=self.components["chsTables"].stringSelection
            self._index+=1
            self.getARow(selectedTable)

    def on_previousRecord_command(self, event):
        "Show the previous row"
        if self._index:
            if self._index>len(self._row):
                self._index-=1
            self._index-=1
            self.showRow(self._index)

    def on_firstRecord_command(self, event):
        "Show the first row (if we've already got it)"
        self._index=0
        self.showRow(self._index)

    def on_lastRecord_command(self, event):
        "Show the last row we have fetched so far"
        if self._index<(len(self._row)-1):
            self._index=(len(self._row)-1)
            self.showRow(self._index)

    def on_mnuExit_select(self, event):
        self.close()

    def on_mnuAbout_select(self, event):
        dialog.scrolledMessageDialog(self, self.readme, 'About')

if __name__=="__main__":
    app=model.Application(DbBrowser)
    app.MainLoop()
