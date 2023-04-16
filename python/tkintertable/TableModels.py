# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
    Module implementing the TableModel class that manages data for
    it's associated TableCanvas.

    Created Oct 2008
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from __future__ import absolute_import, division, print_function
from .TableFormula import Formula
from . import Filtering
from types import *
from collections import OrderedDict
import operator
import string, types, copy
import pickle, os, sys, csv

class TableModel(object):
    """A base model for managing the data in a TableCanvas class"""

    keywords = {'columnnames':'columnNames', 'columntypes':'columntypes',
               'columnlabels':'columnlabels', 'columnorder':'columnOrder',
               'colors':'colors',"nodisplay":"nodisplay","protected_cells":"protected_cells",
               "format_cells":"format_cells","columnwidths":"columnwidths","shapelist":"shapelist"}


    def __init__(self, newdict=None, rows=None, columns=None,tablename=None):
        """Constructor"""
        self.initialiseFields()
        self.modelname = tablename
        self.setupModel(newdict, rows, columns)
        return

    def setupModel(self, newdict, rows=None, columns=None):
        """Create table model"""

        if newdict != None:
            self.data = copy.deepcopy(newdict)
            for k in self.keywords:
                if k in self.data:
                    self.__dict__[self.keywords[k]] = self.data[k]
                    del self.data[k]
            #read in the record list order
            if 'reclist' in self.data:
                temp = self.data['reclist']
                del self.data['reclist']
                self.reclist = temp
            else:
                self.reclist = self.data.keys()
        else:
            #just make a new empty model
            self.createEmptyModel()

        if not set(self.reclist) == set(self.data.keys()):
            print ('reclist does not match data keys')
        #restore last column order
        if hasattr(self, 'columnOrder') and self.columnOrder != None:
            self.columnNames=[]
            for i in self.columnOrder.keys():
                self.columnNames.append(self.columnOrder[i])
                i=i+1
        self.defaulttypes = ['text', 'number']
        #setup default display for column types
        self.default_display = {'text' : 'showstring',
                                'number' : 'numtostring'}
        #set default sort order as first col
        if len(self.columnNames)>0:
            self.sortkey = self.columnNames[0]
        else:
            self.sortkey = None
        #add rows and cols if they are given in the constructor
        if newdict == None:
            if rows != None:
                self.autoAddRows(rows)
            if columns != None:
                self.autoAddColumns(columns)
        else:
            self.setLastUsedRow=0
            for rowIndex in self.data.keys():
                rec=self.data[rowIndex]
                if not self.isRecEmpty(rec):
                    self.updateLastUsedRow(rowIndex)
                    
                    
        self.filteredrecs = None
        return

    def initialiseFields(self):
        """Create base fields, some of which are not saved"""
        self.data = None    # holds the table dict
        self.colors = {}    # holds cell colors
        self.colors['fg']={}
        self.colors['bg']={}
        #default types
        self.defaulttypes = ['text', 'number']
        #list of editable column types
        #self.editable={}
        self.nodisplay = []
        self.hiderowslist = []
        self.rowheightlist = {}
        self.default_rowheight = 12
        self.ColumnAlignment = {}
        self.protected_cells = [] #*HL  list of cells that are not editable ("*",col) and (row,"*") for rows and columns
        self.shapelist = [] #*HL list of shapes
        self.format_cells = {}
        self.gridlist = []
        self.columnwidths={}  #used to store col widths, not held in saved data
        self.rowwidths={}  #used to store row widths, not held in saved data
        self.lastUsedRow = 0
        self.DataChanged = False
        return

    def createEmptyModel(self):
        """Create the basic empty model dict"""

        self.data = {}
        # Define the starting column names and locations in the table.
        self.columnNames = []
        self.columntypes = {}
        self.columnOrder = None
        #record column labels for use in a table header
        self.columnlabels={}
        for colname in self.columnNames:
            self.columnlabels[colname]=colname
        self.reclist = list(self.data.keys())
        return
    
    def isRecEmpty(self,rec):
        
        for colname in self.columnNames:
            if rec.get(colname,"")!="":
                return False
        return True

    def importCSV(self, filename, sep=',',fieldnames=None):
        """Import table data from a comma separated file."""

        if not os.path.isfile(filename) or not os.path.exists(filename):
            print ('no such file', filename)
            return None

        #takes first row as field names
        dictreader = csv.DictReader(open(filename, "r",encoding="utf8"), delimiter=sep,fieldnames=fieldnames)
        dictdata = {}
        count=0
        for rec in dictreader:
            dictdata[count]=rec
            count=count+1
        self.importDict(dictdata)
        self.modelname=filename
        return

    def importDict(self, newdata):
        """Try to create a table model from a dict of the form
           {{'rec1': {'col1': 3, 'col2': 2}, ..}"""

        #get cols from sub data keys
        colnames = []
        self.setLastUsedRow(0)
        for k in newdata:
            fields = newdata[k].keys()
            for f in fields:
                if not f in colnames:
                    colnames.append(f)
                if f!=None and newdata[k][f]!="":
                    self.updateLastUsedRow(k)
        for c in colnames:
            self.addColumn(c)
        #add the data
        self.data.update(newdata)
        self.reclist = list(self.data.keys())
        self.setDataChanged()
        #self.lastUsedRow = self.getRowCount()
        return

    def getDefaultTypes(self):
        """Get possible field types for this table model"""
        return self.defaulttypes

    def getData(self):
        """Return the current data for saving"""

        data = copy.deepcopy(self.data)
        data['colors'] = self.colors
        data['columnnames'] = self.columnNames
        #we keep original record order
        data['reclist'] = self.reclist
        #record current col order
        data['columnorder']={}
        i=0
        for name in self.columnNames:
            data['columnorder'][i] = name
            i=i+1
        data['columntypes'] = self.columntypes
        data['columnlabels'] = self.columnlabels
        data["nodisplay"] = self.nodisplay
        data["protected_cells"] = self.protected_cells
        data["format_cells"]=self.format_cells
        data["columnwidths"]=self.columnwidths
        data["rowheightlist"]=self.rowheightlist
        data["rowwidths"]=self.rowwidths
        data["shapelist"]=self.shapelist
        #print("GetData****Shapelist************")
        #repr(self.shapelist)
        return data

    def getAllCells(self):
        """Return a dict of the form rowname: list of cell contents
          Useful for a simple table export for example"""

        records={}
        for row in range(len(self.reclist)):
            recdata=[]
            for col in range(len(self.columnNames)):
                recdata.append(self.getValueAt(row,col))
            records[row]=recdata
        return records

    def getColCells(self, colIndex):
        """Get the viewable contents of a col into a list"""

        collist = []
        if self.getColumnType(colIndex) == 'Link':
            return ['xxxxxx']
        else:
            for row in range(len(self.reclist)):
                v = self.getValueAt(row, colIndex)
                collist.append(v)
        return collist

    def getlongestEntry(self, columnIndex):
        """Get the longest cell entry in the col"""

        collist = self.getColCells(columnIndex)
        maxw=5
        for c in collist:
                lines=c.split("\n")
                for line in lines:
                    try:
                        w = len(str(line))
                    except UnicodeEncodeError:
                        pass
                    if w > maxw:
                        maxw = w
        #print 'longest width', maxw
        return maxw

    def getRecordAtRow(self, rowIndex):
        """Get the entire record at the specifed row."""

        name = self.getRecName(rowIndex)
        record = self.data[name]
        return record

    def getCellRecord(self, rowIndex, columnIndex):
        """Get the data held in this row and column"""

        value = None
        colname = self.getColumnName(columnIndex)
        coltype = self.columntypes[colname]
        name = self.getRecName(rowIndex)
        #print self.data[name]
        if colname in self.data[name]:
            celldata=self.data[name][colname]
        else:
            celldata=None
        return celldata
    
    def getCellAlignment(self,row,col):
        colalignment = self.ColumnAlignment.get(col,"w")
        return colalignment
    
    def deleteShapeatPos(self,x1,y1,x2,y2):
                
        deleteList=[]
        index=0
        for shape in self.shapelist:
            if shape.Left in range(int(x1),int(x2)) and shape.Top in range(int(y1),int(y2)):
                deleteList.insert(0, index)
        if len(deleteList)>0:
            for item in deleteList:
                del self.shapelist[item]
           
                

    def deleteCellRecord(self, rowIndex, columnIndex):
        """Remove the cell data at this row/column"""

        colname = self.getColumnName(columnIndex)
        coltype = self.columntypes[colname]
        name = self.getRecName(rowIndex)
        if colname in self.data[name]:
            del self.data[name][colname]
        return

    def getRecName(self, rowIndex):
        """Get record name from row number"""
        if len(self.reclist)==0:
            return None
        if self.filteredrecs != None:
            if rowIndex<len(self.filteredrecs):
                name = self.filteredrecs[rowIndex]
            else:
                name=self.reclist[rowIndex]
        else:
            name = self.reclist[rowIndex]
        return name


    def setRecName(self, newname, rowIndex):
        """Set the record name to another value - requires re-setting in all
           dicts that this rec is referenced"""

        if len(self.reclist)==0:
            return None
        currname = self.getRecName(rowIndex)
        self.reclist[rowIndex] = newname
        temp = copy.deepcopy(self.data[currname])
        self.data[newname] = temp
        #self.data[newname]['Name'] = newname
        del self.data[currname]
        for key in ['bg', 'fg']:
            if currname in self.colors[key]:
                temp = copy.deepcopy(self.colors[key][currname])
                self.colors[key][newname] = temp
                del self.colors[key][currname]
        #print ('renamed')
        #would also need to resolve all refs to this rec in formulas here!
        return

    def getRecordAttributeAtColumn(self, rowIndex=None, columnIndex=None,
                                        recName=None, columnName=None):
        """Get the attribute of the record at the specified column index.
           This determines what will be displayed in the cell"""

        value = None
        if columnName != None and recName != None:
            if columnName not in self.data[recName]:
                return ''
            cell = self.data[recName][columnName]
        else:
            cell = self.getCellRecord(rowIndex, columnIndex)
            columnName = self.getColumnName(columnIndex)
        if cell == None:
            cell=''
        # Set the value based on the data record field
        coltype = self.columntypes[columnName]
        if Formula.isFormula(cell) == True:
            value = self.doFormula(cell)
            return value

        if not type(cell) is dict:
            if coltype == 'text' or coltype == 'Text':
                value = cell
            elif coltype == 'number':
                value = str(cell)
            else:
                value = 'other'
        else:
            value = cell #*HL
        if value==None:
            value=''
        return value

    def getRecordIndex(self, recname):
        rowIndex = int(self.reclist.index(recname))
        return rowIndex

    def setSortOrder(self, columnIndex=None, columnName=None, reverse=0):
        """Changes the order that records are sorted in, which will
           be reflected in the table upon redrawing"""

        if columnName != None and columnName in self.columnNames:
            self.sortkey = columnName
        elif columnIndex != None:
            self.sortkey = self.getColumnName(columnIndex)
        else:
            return
        self.reclist = list(self.createSortMap(self.reclist, self.sortkey, reverse))
        if self.filteredrecs != None:
            self.filteredrecs = self.createSortMap(self.filteredrecs, self.sortkey, reverse)
        return

    def createSortMap(self, names, sortkey, reverse=0):
        """Create a sort mapping for given list"""

        recdata = []
        for rec in names:
            recdata.append(self.getRecordAttributeAtColumn(recName=rec, columnName=sortkey))
        #try create list of floats if col has numbers only
        try:
            recdata = self.toFloats(recdata)
        except:
            pass
        smap = zip(names, recdata)
        #sort the mapping by the second key
        smap = sorted(smap, key=operator.itemgetter(1), reverse=reverse)
        #now sort the main reclist by the mapping order
        sortmap = map(operator.itemgetter(0), smap)
        return sortmap

    def toFloats(self, l):
        x=[]
        for i in l:
            if i == '':
                x.append(0.0)
            else:
                x.append(float(i))
        return x

    '''def getSortIndex(self):
        """Return the current sort order index"""
        if self.sortcolumnIndex:
            return self.sortcolumnIndex
        else:
            return 0'''

    def moveColumn(self, oldcolumnIndex, newcolumnIndex):
        """Changes the order of columns"""
        self.oldnames = self.columnNames
        self.columnNames=[]

        #write out a new column names list - tedious
        moved = self.oldnames[oldcolumnIndex]
        del self.oldnames[oldcolumnIndex]
        #print self.oldnames
        i=0
        for c in self.oldnames:
            if i==newcolumnIndex:
                self.columnNames.append(moved)
            self.columnNames.append(c)
            i=i+1
        #if new col is at end just append
        if moved not in self.columnNames:
            self.columnNames.append(moved)
        return

    def getNextKey(self):
        """Return the next numeric key in the dict"""
        num = len(self.reclist)+1
        return num

    def addRow(self, key=None, **kwargs):
        """Add a row"""
        if key == '':
            return
        if key==None:
            key = self.getNextKey()
        if key in self.data or key in self.reclist:
            print ('name already present!!')
            return
        self.data[key]={}
        for k in kwargs:
            if not k in self.columnNames:
                self.addColumn(k)
            self.data[key][k] = str(kwargs[k])
        self.reclist.append(key)
        self.setDataChanged()
        return key
    
    def deleteShapeatRow(self,y1,y2):
        #deleteList=[]
        #index=0
        for shape in self.shapelist:
            if shape.Top in range(y1,y2):
                shape.set_activeflag(False)
        #        deleteList.insert(0, index)
        #if len(deleteList)>0:
        #    for item in deleteList:
        #        self.shapelist[item].Active=False
        self.moveShapesVertical(y1,deltaY=y1-y2)
        self.setDataChanged()


    def deleteRow(self, rowIndex=None, key=None, update=True,y1=-1,y2=-1):
        """Delete a row"""
        if key == None or not key in self.reclist:
            key = self.getRecName(rowIndex)
        if rowIndex==None:
            rowIndex = self.getRecordIndex(key)
        if y1>=0 and y2>=0:
            self.deleteShapeatRow(y1, y2)
        del self.data[key]
        if update==True:
            self.reclist.remove(key)
        self.removeRowfromLastUsedRow(rowIndex)
        self.setDataChanged()
        return

    def deleteRows(self, rowlist=None,y1=-1,y2=-1):
        """Delete multiple or all rows"""
        if rowlist == None:
            rowlist = range(len(self.reclist))
        names = [self.getRecName(i) for i in rowlist]
        for name in names:
            self.deleteRow(key=name, update=True)
        if y1>=0 and y2>=0:   
            self.deleteShapeatRow(y1, y2)
        return

    def addColumn(self, colname=None, coltype=None):
        """Add a column"""
        index = self.getColumnCount()+ 1
        if colname == None:
            colname=str(index)
        if colname in self.columnNames:
            #print 'name is present!'
            return
        self.columnNames.append(colname)
        self.columnlabels[colname] = colname
        if coltype == None:
            self.columntypes[colname]='text'
        else:
            self.columntypes[colname]=coltype
        self.setDataChanged()

    def deleteColumn(self, columnIndex):
        """delete a column"""
        colname = self.getColumnName(columnIndex)
        self.columnNames.remove(colname)
        del self.columnlabels[colname]
        del self.columntypes[colname]
        #remove this field from every record
        for recname in self.reclist:
            if colname in self.data[recname]:
                del self.data[recname][colname]
        if self.sortkey != None:
            currIndex = self.getColumnIndex(self.sortkey)
            if columnIndex == currIndex:
                self.setSortOrder(0)
        self.setDataChanged()
        #print 'column deleted'
        #print 'new cols:', self.columnNames
        return

    def deleteColumns(self, cols=None):
        """Remove all cols or list provided"""
        if cols == None:
            cols = self.columnNames
        if self.getColumnCount() == 0:
            return
        for col in cols:
            self.deleteColumn(col)
        return
    
    def moveRows(self,src_rowlist,dest_rowindex,minY1=None,maxY1=0,deltaY=0,deleteY=0):
        if src_rowlist[0]<dest_rowindex:
            dest_rowindex = dest_rowindex-len(src_rowlist)
        names = [self.getRecName(i) for i in src_rowlist]
        self.moveRow(srckeylist=names,destindex=dest_rowindex,minY1=minY1,maxY1=maxY1,deltaY=deltaY,deleteY=deleteY)
    
    def moveRow(self,srckeylist=None,destindex=None,minY1=None,maxY1=0,deltaY=0,deleteY=0):
        if srckeylist and destindex:
            #print("MoveRow:",srckeylist,destindex)
            for key in srckeylist:
                self.reclist.remove(key)
            self.reclist[destindex:destindex]=srckeylist
            self.updateLastUsedRow(destindex+len(srckeylist))

            self.moveShapesVertical(minY1, y2=maxY1, deltaY=deltaY)
            self.moveShapesVertical(minY1,deltaY=-deleteY)
            self.setDataChanged()
            #print(self.reclist)
            #print(self.data)
            
    def copyShape(self,shape,newY=None):
        newshape = copy.copy(shape)
        newshape.Top = newY
        self.shapelist.append(newshape)
        self.setDataChanged()
            
    def moveShapesVertical(self,y1,y2=-1,deltaY=0,copy=False,cY1=0):
        tmp_Shapelist = self.shapelist.copy()
        for shape in tmp_Shapelist:
            if y2==-1:
                if shape.Top >=y1:
                    if shape.Top == cY1+1 and copy:
                        self.copyShape(shape,newY=shape.Top+deltaY)
                    else:
                        shape.Top += deltaY
            else:
                if shape.Top in range(y1,y2+1):
                    if copy:
                        self.copyShape(shape,newY=shape.Top+deltaY)
                    else:
                        shape.Top += deltaY                

    def autoAddRows(self, numrows=None, atrow=None,copyfromrow=None):
        """Automatically add x number of records"""
        rows = self.getRowCount()
        ints = [i for i in self.reclist if isinstance(i, int)]
        if len(ints)>0:
            start = max(ints)+1
        else:
            start = 0
        #we don't use addRow as it's too slow
        keys = range(start,start+numrows)
        #make sure no keys are present already
        keys = list(set(keys)-set(self.reclist))
        newdata = {}
        if copyfromrow==None:
            for k in keys:
                newdata[k] = {}
        else:
            for k in keys:
                newdata[k] = copy.deepcopy(self.data[self.reclist[copyfromrow]])
                copyfromrow = copyfromrow+1
        self.data.update(newdata)
        if atrow != None: # insert newdata list in reclist at atrow position
            self.reclist[atrow:atrow]=newdata.keys()
            pass
        else:
            self.reclist.extend(newdata.keys())
        self.setDataChanged()
        return keys

    def autoAddColumns(self, numcols=None):
        """Automatically add x number of cols"""

        #alphabet = string.lowercase[:26]
        alphabet = string.ascii_lowercase
        currcols=self.getColumnCount()
        #find where to start
        start = currcols + 1
        end = currcols + numcols + 1
        new = []
        for n in range(start, end):
            new.append(str(n))
        #check if any of these colnames present
        common = set(new) & set(self.columnNames)
        extra = len(common)
        end = end + extra
        for x in range(start, end):
            self.addColumn(str(x))
        self.setDataChanged()
        return

    def relabel_Column(self, columnIndex, newname):
        """Change the column label - can be used in a table header"""
        colname = self.getColumnName(columnIndex)
        self.columnlabels[colname]=newname
        self.setDataChanged()
        return

    def getColumnType(self, columnIndex):
        """Get the column type"""
        colname = self.getColumnName(columnIndex)
        coltype = self.columntypes[colname]
        return coltype

    def getColumnCount(self):
        """Returns the number of columns in the data model."""
        return len(self.columnNames)

    def getColumnName(self, columnIndex):
        """Returns the name of the given column by columnIndex."""
        return self.columnNames[columnIndex]

    def getColumnLabel(self, columnIndex):
        """Returns the label for this column"""
        colname = self.getColumnName(columnIndex)
        return self.columnlabels[colname]

    def getColumnIndex(self, columnName):
        """Returns the column index for this column"""
        colindex = self.columnNames.index(columnName)
        return colindex

    def getColumnData(self, columnIndex=None, columnName=None,
                        filters=None):
        """Return the data in a list for this col,
            filters is a tuple of the form (key,value,operator,bool)"""
        if columnIndex != None and columnIndex < len(self.columnNames):
            columnName = self.getColumnName(columnIndex)
        names = Filtering.doFiltering(searchfunc=self.filterBy,
                                         filters=filters)
        coldata = [self.data[n][columnName] for n in names]
        return coldata

    def getColumns(self, colnames, filters=None, allowempty=True):
        """Get column data for multiple cols, with given filter options,
            filterby: list of tuples of the form (key,value,operator,bool)
            allowempty: boolean if false means rows with empty vals for any
            required fields are not returned
            returns: lists of column data"""

        def evaluate(l):
            for i in l:
                if i == '' or i == None:
                    return False
            return True
        coldata=[]
        for c in colnames:
            vals = self.getColumnData(columnName=c, filters=filters)
            coldata.append(vals)
        if allowempty == False:
            result = [i for i in zip(*coldata) if evaluate(i) == True]
            coldata = zip(*result)
        return coldata

    def getDict(self, colnames, filters=None):
        """Get the model data as a dict for given columns with filter options"""
        data={}
        names = self.reclist
        cols = self.getColumns(colnames, filters)
        coldata = zip(*cols)
        for name,cdata in zip(names, coldata):
            data[name] = dict(zip(colnames,cdata))
        return data

    def filterBy(self, filtercol, value, op='contains', userecnames=False,
                     progresscallback=None):
        """The searching function that we apply to the model data.
           This is used in Filtering.doFiltering to find the required recs
           according to column, value and an operator"""

        funcs = Filtering.operatornames
        floatops = ['=','>','<']
        func = funcs[op]
        data = self.data
        #coltype = self.columntypes[filtercol]
        names=[]
        for rec in self.reclist:
            if filtercol in data[rec]:
                #try to do float comparisons if required
                if op in floatops:
                    try:
                        #print float(data[rec][filtercol])
                        item = float(data[rec][filtercol])
                        v = float(value)
                        if func(v, item) == True:
                            names.append(rec)
                        continue
                    except:
                        pass
                if filtercol == 'name' and userecnames == True:
                    item = rec
                else:
                    item = str(data[rec][filtercol])
                if func(value, item):
                    names.append(rec)
        return names
    
    def removeRowfromLastUsedRow(self,rowIndex):
        if rowIndex<=self.lastUsedRow:
            self.lastUsedRow-=1
        self.setDataChanged()
    
    def getLastUsedRow(self):
        return self.lastUsedRow
    
    def setLastUsedRow(self,value):
        self.lastUsedRow = value
    
    def updateLastUsedRow(self,rowIndex):
        if rowIndex>self.lastUsedRow:
            self.lastUsedRow=rowIndex

    def getRowCount(self):
        """Returns the number of rows in the table model."""
        return len(self.reclist)

    def getValueAt(self, rowIndex, columnIndex):
        """Returns the cell value at location specified
            by columnIndex and rowIndex."""
        value = self.getRecordAttributeAtColumn(rowIndex, columnIndex)
        #print("getValueAt:",rowIndex,columnIndex,value)
        return value

    def setValueAt(self, value, rowIndex, columnIndex):
        """Changed the dictionary when cell is updated by user"""
        if value==None:
            value=""
        name = self.getRecName(rowIndex)
        colname = self.getColumnName(columnIndex)
        coltype = self.columntypes[colname]
        if coltype == 'number':
            try:
                if value == '': #need this to allow deletion of values
                    self.data[name][colname] = ''
                else:
                    self.data[name][colname] = float(value)
            except:
                pass
        else:
            if type(value) != str and type(value) != int:
                print(str(type(value)))
                #print("Set Value at error:",name,colname,value)
            self.data[name][colname] = value
        self.updateLastUsedRow(rowIndex)
        self.setDataChanged()
        return

    def setFormulaAt(self, f, rowIndex, columnIndex):
        """Set a formula at cell given"""
        name = self.getRecName(rowIndex)
        colname = self.getColumnName(columnIndex)
        coltype = self.columntypes[colname]
        rec = {}
        rec['formula'] = f
        self.data[name][colname] = rec
        self.setDataChanged()
        return
    
    def getCellFormatAt(self, rowIndex, columnIndex):
        """Return color of that record field for the table"""
        foundcellformat = self.format_cells.get("default",None)
        if self.format_cells != {}:
            for cellformat_nr in self.format_cells:
                cellformatdict = self.format_cells.get(cellformat_nr,None)
                if cellformatdict:
                    cells = cellformatdict.get("Cells",[])
                    if ("*","*") in cells or ("*",columnIndex) in cells or (rowIndex,"*") in cells or (rowIndex,columnIndex) in cells:
                        foundcellformat = cellformatdict
                        break
            if foundcellformat:
                fgcolor = foundcellformat.get("fg",None)
                bgcolor = foundcellformat.get("bg",None)
                font    = foundcellformat.get("font",None)
            else:
                fgcolor = None
                bgcolor = None
                font    = None
        else:
            fgcolor = None
            bgcolor = None
            font    = None
        
        return fgcolor,bgcolor,font
        

    def getColorAt(self, rowIndex, columnIndex, key='bg'):
        """Return color of that record field for the table"""
        name = self.getRecName(rowIndex)
        colname = self.getColumnName(columnIndex)
        if name in self.colors[key] and colname in self.colors[key][name]:
            return self.colors[key][name][colname]
        else:
            #return None
            fgcolor,bgcolor,font = self.getCellFormatAt(rowIndex, columnIndex)
            if key=="bg":
                return bgcolor
            elif key=="font":
                return font
            else:
                return fgcolor
        
        

    def setColorAt(self, rowIndex, columnIndex, color, key='bg'):
        """Set color"""
        name = self.getRecName(rowIndex)
        colname = self.getColumnName(columnIndex)
        if not name in self.colors[key]:
            self.colors[key][name] = {}
        self.colors[key][name][colname] = str(color)
        self.setDataChanged()
        return

    def resetcolors(self):
        """Remove all color formatting"""
        self.colors={}
        self.colors['fg']={}
        self.colors['bg']={}
        return

    def getRecColNames(self, rowIndex, ColIndex):
        """Returns the rec and col name as a tuple"""
        recname = self.getRecName(rowIndex)
        colname = self.getColumnName(ColIndex)
        return (recname, colname)

    def getRecAtRow(self, recname, colname, offset=1, dim='y'):
        """Get the record name at a specified offset in the current
           table from the record given, by using the current sort order"""
        thisrow = self.getRecordIndex(recname)
        thiscol = self.getColumnIndex(colname)
        #table goto next row
        if dim == 'y':
            nrow = thisrow + offset
            ncol = thiscol
        else:
            nrow = thisrow
            ncol = thiscol + offset

        newrecname, newcolname = self.getRecColNames(nrow, ncol)
        #print ('recname, colname', recname, colname)
        #print ('thisrow, col', thisrow, thiscol)
        return newrecname, newcolname

    def appendtoFormula(self, formula, rowIndex, colIndex):
        """Add the input cell to the formula"""
        cellRec = getRecColNames(rowIndex, colIndex)
        formula.append(cellRec)
        self.setDataChanged()
        return

    def doFormula(self, cellformula):
        """Evaluate the formula for a cell and return the result"""
        value = Formula.doFormula(cellformula, self.data)
        return value

    def copyFormula(self, cellval, row, col, offset=1, dim='y'):
        """Copy a formula down or across, using the provided offset"""
        import re
        frmla = Formula.getFormula(cellval)
        #print 'formula', frmla

        newcells=[]
        cells, ops = Formula.readExpression(frmla)

        for c in cells:
            #print (c)
            if type(c) is not ListType:
                nc = c
            else:
                recname = c[0]
                colname = c[1]
                nc = list(self.getRecAtRow(recname, colname, offset, dim=dim))
            newcells.append(nc)
        newformula = Formula.doExpression(newcells, ops, getvalues=False)
        self.setDataChanged()
        return newformula

    def merge(self, model, key='name', fields=None):
        """Merge another table model with this one based on a key field,
           we only add records from the new model where the key is present
           in both models"""
        if fields == None: fields = model.columnNames
        for rec in self.reclist:
            if not key in self.data[rec]:
                continue
            for new in model.reclist:
                if not key in model.data[new]:
                    continue
                if self.data[rec][key] == model.data[new][key]:
                #if new == rec:
                    for f in fields:
                        if not f in model.data[rec]:
                            continue
                        if not f in self.columnNames:
                            self.addColumn(f)
                        self.data[rec][f] = model.data[rec][f]
        self.setDataChanged()
        return

    def save(self, filename=None):
        """Save model to file"""
        if filename == None:
            return
        data = self.getData()
        fd = open(filename,'wb')
        pickle.dump(data,fd)
        fd.close()
        return

    def load(self, filename):
        """Load model from pickle file"""
        fd=open(filename,'rb')
        data = pickle.load(fd)
        self.setupModel(data)
        self.setDataChanged()
        return

    def copy(self):
        """Return a copy of this model"""
        M = TableModel()
        data = self.getData()
        M.setupModel(data)
        return M
    
    def setDataChanged(self):
        self.DataChanged = True
        
    def checkDataChanged(self):
        return self.DataChanged
    
    def resetDataChanged(self):
        self.DataChanged = False   

    def __repr__(self):
        return 'Table Model with %s rows' %len(self.reclist)
