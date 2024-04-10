from wx import grid

class DBTable(grid.PyGridTableBase):
    """Class to wrap a database table that can be assigned to a grid
    
    Inspired by wxPyDBAPITable by Nathan R Yergler
    """
    def __init__(self, db, tableName):
        grid.PyGridTableBase.__init__(self)
        self.__db=db
        self.tableName=tableName
        self.getData(tableName)

    def getData(self, tableName):
        "Execute <stmt> and return the rows to our internal data structure"
        # Should tableName be a method argument or should we use self.tableName?
        self.__rows=self.__db.getRows(tableName)
        self._rowCount=len(self.__rows)
        self._colNames=[col[0] for col in self.__db.getColumns(tableName)]
        self._colCount=len(self._colNames)

    # Table level methods
    def GetNumberRows(self):
        return self._rowCount

    def GetNumberCols(self):
        return self._colCount

    def AppendRows(self, numRows=1):
        # Implement this when we want to modify data
        # Should just be a simple insert (?)
        return True

    # Cell level values
    def IsEmptyCell(self, row, col):
        if self.__rows[row][col] == "" or self.__rows[row][col] is None:
            return True
        else:
            return False

    def GetValue(self, row, col):
        return self.__rows[row][col]

    def SetValue(self, row, col, valstr):
        # Implement this when we want to modify data
        # Should just be a simple update (?)
        return True

    # Label methods
    def GetRowLabelValue(self, row):
        # A record number will do fine, thanks
        return row+1

    def GetColLabelValue(self, col):
        return self._colNames[col]

    def SetRowLavelValue(self, row, label):
        # Disable this for now
        pass

    def SetColLabelValue(self, row, label):
        # Disable this for now
        pass

    # Miscellaneous methods
    def refresh(self):
        if self.__stmt:
            self.getData(self.__stmt)

    def GetRowLabelList(self):
        # Not today thank you
        pass

    def GetColLabelList(self):
        return self._colNames
