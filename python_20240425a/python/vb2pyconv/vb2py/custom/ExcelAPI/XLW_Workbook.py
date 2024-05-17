# -*- coding: utf-8 -*-
#
#         Workbook
#
# * Version: 4.03
# * Author: Harold Linke
# * Date: January 8, 2022
# * Copyright: Harold Linke 2021
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *  
# * https://github.com/Hardi-St/MobaLedLib
# *
# * MobaLedCheckColors is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * MobaLedCheckColors is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  if not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************

#------------------------------------------------------------------------------
# CHANGELOG:
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release
# 2022-01-08 V4.03 HL: - added Workbook Save and Load
# 2022-04-02 LX4.18 HL: update to MLL V3.1.0F4, removed keyword "exit_on_error" and annotation for global variables
# 2022-04-03 LX4.19 HL: added platformcheck

xlFormulas = 0
xlWhole = 0
xlByRows = 0
xlNext = 0
msoTextOrientationHorizontal = 0
msoSegmentLine = 0
msoEditingAuto = 0






pyProgfile_dir = "\\LEDs_AutoProg\\pyProg_Generator_MobaLedLib"

shift_key = False

guifactor  = 1.55

hook_char = int("*")

global_worksheet_dict = {}

def checkplatform(checkstr):
    pass

def get_home_dir():
    pass


def Dir(filepath,dummy=None):
    pass


def Date_str():
    pass

def Time_str():
    pass

def Center_Form(form):
    return

def Shell(cmd):
    pass

def updateWindow():
    pass

def TimeValue(Duration):
    pass

def getvalue(row,column):
    pass

def ActiveCell():
    pass
def activate_workbook(workbookname):
    pass

def set_activeworkbook(p_workbook):
    pass

def create_workbook(frame=None, path=None,pyProgPath=None,workbookName=None,workbookFilename=None,sheetdict=None,start_sheet=None,p_global_controller=None,width=None,height=None):
    pass

def IsError(testval):
    return False

def Cells(row:int, column:int,ws=None):
    pass    


def Range(cell1=None,cell2=None,ws=None):
    pass

def Sheets(sheetname):
    pass
def Rows(row=None,ws=None):
    pass

def Columns(col:int):
    pass

def IsEmpty(obj):
    pass

def val(value):
    pass

def VarType(obj):
    pass

def Unload(UserForm):
    pass
def ChDrive(srcdir):
    pass

def Format(value,formatstring):
    pass


def MsgBox(ErrorMessage:str, msg_type:int, ErrorTitle:str):
    pass

def InputBox(Message:str, Title:str, Default=None):
    pass

def Time():
    pass
def Date():
    pass

def Run(cmd):
    pass

def set_statusmessage(message):
    pass

__VK_LBUTTON = 0x1
__VK_RBUTTON = 0x2
__VK_MBUTTON = 0x4
__VK_UP = 0x26
__VK_DOWN = 0x28
__VK_RETURN = 0xD
__VK_ESCAPE = 0x1B
__VK_CONTROL = 0x11
__VK_SHIFT = 0x10
VK_SHIFT = 0x10

def GetAsyncKeyState(key):

    pass


def GetCursorPos():
    pass

def SetCursorPos(x,y):
    pass

def DoEvents():
    pass

class Worksheet(object):
    """Placeholder for Worksheettype"""
    def __init__(self):
        self.Name = "Dummy"

class CWorkbook(object):
    def __init__(self, frame=None,path=None,pyProgPath=None,workbookName=None, workbookFilename=None, sheetdict=None,init_workbook=None,open_workbook=None,start_sheet=None,controller=None,width=None,height=None):
        pass
    pass

    def init_workbook(self):
        pass


    def open(self):
        pass

    def Delay(self,dSeconds):
        pass
    def delete_sheet(self,sheetname):

        pass

    def add_sheet(self,sheetname ,from_sheet=None,After=None,nocontrols=False,noredraw=False):


        pass

    def new_sheet(self,sheetname,tabframe,from_sheet=None) :
        pass


    def TabChanged(self,_event=None):
        pass  

    def Sheets(self,name=None) :

        return None

    def Worksheets(self,name):

        return None

    def Activate(self):
        return

    def notimplemented(self,command):
        pass

    def Save(self,filename=None):
        pass


    def Load(self,filename=None):
        pass
    def is_datasheet(self,ws):

        pass
    def LoadExcelWorkbook(self,filename=None):

        pass
    def LoadSheetfromExcelWorkbook(self,worksheet, filename, fieldnames):
        pass

    def SavePGF(self,filename=None):
        pass
        return

    def LoadPGF(self,filename=None):
        """load PGF from a file"""
        pass
        return       

    def SaveWorkbook(self,filename,allsheets=False):
        pass

    def LoadWorkbook(self,filename: str,workbookname=""):
        pass

    def update_library(self):
        pass

    def install_Betatest(self):
        pass

    def library_status(self):
        pass

    def install_fast_bootloader(self):
        pass

    def start_patternconf(self):
        pass

    def send_to_patternconf(self):
        pass

    def receiver_from_patternconf(self):
        pass

    def check_Data_Changed(self):
        pass
    def Call_EventProc(self,eventname):
        pass
    def Evt_Workbook_Open(self):
        pass
    def Evt_Workbook_BeforeClose(self, event):
        pass
    def Evt_SheetTableUpdate(self,sheet,target):
        pass
    def Evt_SheetCalculate(self, sheet, target):
        pass
    def Evt_SheetBeforeDoubleClick(self, sheet,target, cancel):
        pass
    def Evt_SheetChange(self, event):
        pass

    def Evt_SheetSelectionChange(self,event):
        pass

    def Evt_SheetActivate(self, event):
        pass

    def Evt_SheetDeactivate(self, event):
        pass         

    def Evt_NewSheet(self, event):
        pass

    def Evt_SheetReturnKey(self, event):
        pass

    def Evt_SheetOpen(self, event):
        pass

    def Synch_Evt_SheetSelectionChange(self,widget):
        pass

    def Synch_Evt_SheetChange(self, widget):
        pass

    def Synch_Evt_SheetReturnKey(self):
        pass

    def Evt_Redraw_Sheet(self, sheet):
        pass

class CCellsFind(object):
    def __init__(self,ws=None):
        pass

    def Find(self,What="", After=None, LookIn=xlFormulas, LookAt= xlWhole, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False):

        pass
        return None

class CButtons(object):
    def __init__(self,ws=None):
        pass

    def Add(self,l,t,w,h):
        pass
    
class CWorksheet(object):

    def __init__(self,Name,workbook=None,csv_filepathname=None,frame=None,fieldnames=None,formating_dict=None,Sheettype="",callback=False,tabid=0,width=None, height=None):

        pass
    
    def init_data(self):

        pass

    def sheet_was_modified(self, event: dict):
        pass

    def update_table_properties(self):

        pass

    def EventSH_cellselected(self, event):
        pass
    
    def Calculate(self):
        pass
    

    def Delete(self):
        pass

    def set_left_click_callback(self,callback):
        pass
    
    def handle_hidden_cells(self, param):
        pass
    
    def handle_hidden_rows(self, param):
        pass
    def is_row_hidden(self, row):
        pass
    def handle_protected_cells(self, spanlist):
        pass
    def handle_formating(self, param):
        pass
    
    def handle_gridlist(self, param):
        pass
    
    def handle_ColumnAlignment(self, param):
        pass
    def handle_ColumnWidth(self, param):
        pass

    def add_controls(self,controls_dict):
        pass
    
    def AddControl(self,control):
        pass
    
    def set_control_val(self, control,value,disable=False):
        pass
    def get_control_val(self, control):
        pass
    def SavePersistentControls(self):
        pass
    
    def SetPersistentControls(self):
        pass
    
    def LED_flash(self,row,col):
        pass


    def LED_flash_seq(self,row,col):
        pass

    def left_click_callback(self,value1,value2,callertype="cell"):
        pass

    def EnableMousePosition(self):
        pass

    def getSelectedRow(self):
        pass
    def getSelectedCell(self):
        pass
    def getRowCount(self):
        pass
    
    def getColumnCount(self):
        pass
    
    def getSelectedColumn(self):
        pass
    def setSelectedCells(self, r1, r2, c1, c2):
        pass
    
    def setSelectedShapes(self,shape):
        pass
    
    def getSelectedShapes(self):
        pass
    
    def is_column_hidden(self, col):
        pass
    
    def set_hiderow(self,row,newval):
        pass
    def set_hidecolumn(self,col,newval):
        pass
    
    def addrow_if_needed(self,row=None):
        pass
    

    def addrow_before_current_row(self,copy=False):
        pass

    def deleterows(self):
        pass

    def int_moveRows(self, sc_rowlist, destrow):
        pass
    def prepare_moveRows(self):
        pass
    
    def do_moveRows(self):
        pass
    

    def UsedRange_Rows(self):
        pass

    def get_LastUsedRow(self):
        pass

    def set_LastUsedRow(self,value):
        pass

    LastUsedRow = property(get_LastUsedRow, set_LastUsedRow, doc='Last used row')

    def get_LastUsedColumn(self):
        pass

    def set_LastUsedColumn(self,value):
        pass

    LastUsedColumn = property(get_LastUsedColumn, set_LastUsedColumn, doc='Last used row')
    End = property(get_LastUsedColumn, set_LastUsedColumn, doc='Last used row')

    def get_UsedRange(self):
        pass

    def set_UsedRange(self,value):
        pass

    UsedRange = property(get_UsedRange, set_UsedRange, doc='used range')
    MaxRange  = property(get_UsedRange, set_UsedRange, doc='used range')

    def get_Shape(self,shapename):
        pass

    def deleteShapeatPos(self,x1,y1,x2,y2):
        pass

    def deleteShapeatRow(self,y1,y2):
        pass

    def copyShape(self,shape,newY=None):
        pass

    def moveShapesVertical(self,y1,y2=-1,deltaY=0,copy=False,cY1=0):
        pass 

    def moveshapes(self,delta_width,asofpos):
        pass

    def findshape(self,name):
        pass

    def addShape(self, name, shapetype, Left, Top, Width, Height, Fillcolor, Text="",controls_dict=None):
        pass

    def addLabel(self, textorientation, Left, Top, Width, Height):
        pass

    def addConnector(self, contype, BeginX, Beginy, Width, Height):
        pass 

    def addPicture(self, name, Left, Top, Width, Height, Text=None):
        pass

    def deleteshape(self,shape):
        pass

    def redraw_shapes(self, saved_shapelist):
        pass

    def recreate_shapes(self):
        pass

    def drawShapes(self,force=False):
        pass

    def drawShape(self,shape,force=False):
        pass

    def getShape(self,index):
        pass

    def setDataChanged(self):
        pass

    def data_row_to_displayed(self, row):
        pass

    def displayed_row_to_data(self, row):
        pass

    def data_column_to_displayed(self, col):
        pass

    def displayed_column_to_data(self, col):
        pass

    def importCSV(self, filename=None, sep=',',fieldnames=None):
        pass

    def importCSV_int(self, filename, sep=',',fieldnames=None):
        pass

    def importDict(self, newdata):
        pass
    def Cells(self,row=None, col=None):
        pass
    def Rows(self,row):
        pass

    def get_cellvalue_direct(self,sheet,row,col):
        pass

    def find_RangeName(self,rangestr,ws=None):
        pass

    def Range(self,cell1,cell2=None,ws=None):
        pass

    def Range_set(self,rangestr,value):
        pass

    def Unprotect(self,Password=""):
        pass

    def Protect(self, DrawingObjects=True, Contents=True, Scenarios=True, AllowFormattingCells=True, AllowInsertingHyperlinks=True):
        pass

    def Columns(col:int):
        pass

    def EnableDisableAllButtons(self,value):
        return

    def SetChangedCallback(self,callback):
        pass

    def SetSelectedCallback(self,callback):
        pass

    def SetCalculationCallback(self,callback):
        pass

    def SetInitDataFunction(self,func):
        pass

    def EventWScalculate(self,changecell=None):
        pass

    def EventWSchanged(self, changedcell):
        pass

    def EventWSselected(self, selectedcell):
        pass

    def EventWSselected_orig(self, selectedcell):
        pass   

    def EventWSdoubleclick(self, event):
        pass

    def EventWSLeftClick(self, event):
        pass

    def Redraw_table(self,do_bindings=False):
        pass

    def set_value_in_cell(self,row,column,newval):
        pass

    def create_search_colcache(self,searchcol):
        pass

    def find_in_col_ret_col_val(self,searchtext, searchcol, resultcol,cache=True):
        pass

    def getCellRecord(self, row, col):
        pass

    def getCellCoords(self, r,c):
        pass

    def calc_row_from_y(self, y):
        pass

    def calc_col_from_x(self, x):
        pass 

    def find_in_col_ret_row(self,searchtext, searchcol, cache=True):
        pass

    def find_in_col_set_col_val(self,searchtext, searchcol, setcol,setval,cache=False):
        pass

    def Activate(self):
        pass
        return

    def Copy(self,SheetName=None,After=None):
        pass

    def do_bindings(self):
        pass

    def remove_bindings(self):
        pass

    def Select(self):
        pass

    def Visible(self,value):
        pass

        return    
    def getData(self):
        pass

    def setData(self,data):
        pass

    def clearData(self):
        pass

    def clearSheet(self):
        pass

    def check_Data_Changed(self):
        pass

    def add_new_attr(self,attr):
        setattr(self,attr,attr)

    def add_UI_object(self,ui_object_name,UI_object):
        setattr(self,ui_object_name, UI_object)

    def changeGrid(self, gridno, diditem):
        #test needs update
        pass

    def get_selection(self):
        return 

    def set_selection(self, value):
        ActiveSheet.get_selection().Value=value

    Selection = property(get_selection, set_selection, doc='Selection')             

class CFreeForm(object):
    def __init__(self, EditingType, X1, Y1):
        pass

    def AddNodes(self,SegmentType, EditingType, X2, Y2, *args):
        pass

    def ConvertToShape(self):
        pass

class CShapeList(object):
    def __init__(self,ws=None):
        pass
    #def convTShape2CShape(self,tshape):
    #    pass

    def getShape(self,index):
        pass

    def getlist(self):
        pass

    def AddShape(self, shapetype, Left, Top, Width, Height, Row=None, Col=None, Fill=0,text="",name="",control_dict=None,Init_Value=None):
        pass
    
    def AddLabel(self, TextOrientation=msoTextOrientationHorizontal, Left=0, Top=0 , Width=0, Height=0):
        pass

    def AddTextBox(self, Name="TextBox1", TextOrientation=msoTextOrientationHorizontal, Left=0, Top=0 , Width=0, Height=0,Text=""):
        pass


    def AddConnector(self, ConType, BeginX, BeginY, EndX, EndY):
        pass

    def AddPicture(self, PicName, linktofile=False, savewithdocument=True, Left=0 , Top=0 , Width=0, Height=0):
        pass

    def BuildFreeform(self, EditingType, X1, Y1):
        pass

    def Delete(self,shape):
        pass

    def Count(self):
        pass

    def Range(self,input_array):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass
    
class CRangeList(list):
    def __init__(self, *args):
        pass
    
    def get_count(self):
        pass

    def set_count(self,range):
        pass        

    Count = property(get_count, set_count, doc='number of rows included in range')     

class CRange(str):
    def __new__(cls,t1=None,t2=None,ws=None,value="",parenttype="",parent=None):
        pass

    # Attributes
    def dummy(self,value):
        pass

    def get_address(self):
        pass
    def set_address(self,range):
        pass
    Address = property(get_address, set_address, doc='adress of first cell in range')

    def set_cells(self,rowlist):
        pass

    def get_cells(self):
        pass

    Cells = property(get_cells, set_cells, doc='rows included in range')   

    def get_column(self):
        pass
    
    def set_column(self,range):
        pass 
    Column = property(get_column, set_column, doc='row of first cell in range')

    def set_columns(self,rowlist):
        pass

    def get_columns(self):
        pass

    Columns = property(get_columns, set_columns, doc='Columns in Range')

    def get_columnwidth(self):
        pass

    def set_columnwidth(self, width):
        pass
    ColumnWidth = property(get_columnwidth, set_columnwidth, doc='ColumnWidth of CRange')

    def get_count(self):
        pass
    def set_count(self,p_range):
        pass         
    Count = property(get_count, set_count, doc='number of cells in range')

    def get_entirecolumn(self):
        pass
    def set_entirecolumn(self,param):
        pass
    EntireColumn = property(get_entirecolumn, set_entirecolumn, doc='entirecolumn of range')

    def get_entirerow(self):
        pass
    
    def set_entirerow(self,param):
        pass
    EntireRow = property(get_entirerow, set_entirerow, doc='entirerow of range')

    def _Height(self):
        pass
    Height  = property(_Height, dummy, doc='Height of cell')

    def get_Hidden(self):
        pass

    def _set_hiderow(self,row,newval):
        ActiveSheet.set_hiderow(row, newval)

    def _set_hidecolumn(self,col,newval):
        pass

    def set_Hidden(self,hide):
        pass
    Hidden = property(get_Hidden, set_Hidden, doc='hidden attribute of range')

    def _Left(self):
        pass
        
    Left = property(_Left, dummy, doc='Left coordinates of cell')

    def get_row(self):
        pass
    def set_row(self,range):
        pass
    Row = property(get_row, set_row, doc='row of first cell in range')

    def get_rows(self):
        pass
    
    def set_rows(self,rowlist):
        pass
    Rows = property(get_rows, set_rows, doc='rows included in range')

    def set_columns(self,rowlist):
        pass
    
    def get_columns(self):
        pass
        
    Columns = property(get_columns, set_columns, doc='Columns in Range')    

    def get_text(self):
        pass
    def set_text(self,value):
        pass
    
    Text = property(get_text, set_text, doc='value of Textvalue of Range')

    def _Top(self):
        pass
    Top  = property(_Top, dummy, doc='Top coordinates of cell')

    def get_value(self):
        pass

    def set_value(self,value):
        pass
    Value = property(get_value, set_value, doc='value of first Cell in Range')

    def _Width(self):
        pass
    Width = property(_Width, dummy, doc='Width of cell')

    def _set_rowheight(self,row,newval):
        pass

    def _get_rowheight(self,row):
        pass

    def set_RowHeight(self, newval):
        pass

    def get_RowHeight(self):
        pass

    RowHeight = property(get_RowHeight, set_RowHeight, doc='CRange RowHeight')

    def Insert(self, Shift=0, CopyOrigin=0):
        pass

# Methods
    def Activate(self):
        pass

    def CellsFct(self,row,column):
        pass 


    def ClearContents(self):
        pass

    def Copy(self,dst):
        pass

    def End(self,param):
        pass

    def Find(self,What="", after=None, LookIn=xlFormulas, LookAt= xlWhole, SearchOrder=xlByRows, SearchDirection=xlNext, MatchCase= True, SearchFormat= False):
        pass

    def Offset(self, offset_row, offset_col):
        pass   

    def offset(self, offset_row, offset_col):
        pass

    def Select(self):
        pass

    def check_if_empty_row(self):
        pass

    def __iter__(self):
    #returning __iter__ object
        pass

    def __next__(self):
        pass

    def __eq__(self,other):
        pass
    
    def __lt__(self,other):
        pass

    def __gt__(self,other):
        pass

    def __le__(self,other):
        pass

    def __ge__(self,other):
        pass

    def __int__(self):
        pass

    def __str__(self):
        pass

    def __pow__(self, other):
        pass

    def __rpow__(self, other):
        pass

    def __add__(self,other):
        pass
        

    def __radd__(self,other):
        pass
        

    def __sub__(self,other):
        pass

    def __rsub__(self,other):
        pass
    def __mul__(self,other):
        pass

    def __rmul__(self,other):
        pass

# other functions    
    def upper(self):
        pass

# internal functions

    def _get_LastRow(self):
        pass

    def _get_LastColumn(self):
        pass

class CShapeRange(object):
    def __init__(self,ws=None):
        pass

    def __getitem__(self, k):
        pass

    def __setitem__(self,k,value):
        pass

    def set_Name(self, newval):
        pass

    def get_Name(self):
        pass

    Name = property(get_Name, set_Name, doc='ShapeRange-Name')

class CColumns(object):

    def __init__(self,startcol=None,lastcol=None,parent=None,ws=None):
        pass
    
    def get_Count(self):
        pass

    def set_Count(self,value):
        pass

    Count = property(get_Count,set_Count,doc="Selection Count")

    #python substitute function

    def __iter__(self):
        pass

    def __next__(self):
        pass
class CSelection(object):
    def __init__(self,selrange=None,ws=None):
        pass

    def _selectedRow(self):
        pass

    def get_entirerow(self):
        pass

    def set_entirerow(self,param):
        pass

    EntireRow = property(get_entirerow, set_entirerow, doc='entirerow of selection')

    def Rows(self):
        pass

    def Select(self):
        pass

    def set_ShapeRange(self, newval):
        pass

    def get_ShapeRange(self):
        pass

    ShapeRange = property(get_ShapeRange, set_ShapeRange, doc='ShapeRange')

    def set_RowRange(self, newval):
        pass

    def get_RowRange(self):
        pass

    rowrange = property(get_RowRange, set_RowRange, doc='RowRange')

    ShapeRange = property(get_ShapeRange, set_ShapeRange, doc='ShapeRange')

    def set_ColRange(self, newval):
        pass

    def get_ColRange(self):
        pass

    colrange = property(get_ColRange, set_ColRange, doc='ColRange')

    def set_Column(self, newval):
        pass

    def get_Column(self):
        pass

    Column = property(get_Column, set_Column, doc='Column')

    def set_Columns(self, newval):
        pass

    def get_Columns(self):
        pass

    Columns = property(get_Columns, set_Columns, doc='Columns')

    def set_Cells(self, newval):
        pass

    def get_Cells(self):
        pass

    Cells = property(get_Cells, set_Cells, doc='Selection-Cells')

    def set_Row(self, newval):
        pass

    def get_Row(self):
        pass
    Row = property(get_Row, set_Row, doc='Selection-Row')


class CRow(object):
    def __init__(self,rownumber,rowrange=None):
        pass

    def Select(self):
        pass

    def _set_hiderow(self,row,newval):
        pass
    
    def _set_rowheight(self,row,newval):
        pass

    def _get_rowheight(self,row):
        pass

    def set_Hidden(self, newval):
        pass
    def get_Hidden(self):
        pass

    Hidden = property(get_Hidden, set_Hidden, doc='Hiddenvalue of CRow')

    def set_RowHeight(self, newval):
        pass

    def get_RowHeight(self):
        pass

    RowHeight = property(get_RowHeight, set_RowHeight, doc='Hiddenvalue of CRow')

class CEntireRow(object):
    def __init__(self,rownumber,colrange=None,ws=None):
        pass

    def _set_hiderow(self,row,newval):
        pass

    def set_Hidden(self, newval):
        pass
    
    def get_Hidden(self):
        pass

    Hidden = property(get_Hidden, set_Hidden, doc='Hiddenvalue of CRow')

    def set_value(self, newval):
        pass
    
    def get_value(self):
        pass

    Value = property(get_value, set_value, doc='Entirerow Value')    

class CColumn(object):
    def __init__(self,colnumber,rowrange=None):
        pass

    def get_columnwidth(self):
        pass

    def set_columnwidth(self, value):
        pass

    def get_cells(self):
        pass

    def set_cells(self, value):
        pass

    def _set_hidecolumn(self,col,newval):
        pass

    ColumnWidth = property(get_columnwidth, set_columnwidth, doc='Column Width')

    Cells = property(get_cells, set_cells, doc='Cells in Column')

class CEntireColumn(object):
    def __init__(self,colnumber):
        pass

class CInterior(object):
    def __init__(self,parent=None):
        pass

    def get_color(self):
        pass

    def set_color(self, value):
        pass
    Color = property(get_color, set_color, doc='Cell Color')    

class CDisplayFormat(object):
    def __init__(self,parent=None):
        pass

class CColor(object):
    def __init__(self,color,shape=None,tksheet=None,line=None,cell=None,fg=False):
        pass

    def tkcolor(self):
        pass

    def get_rgb(self):
        pass

    def set_rgb(self, value):
        pass

    rgb = property(get_rgb, set_rgb, doc='Color RGB')

class CLine(object):
    def __init__(self,linecolor=0,shape=None):
        pass

    def get_EndArrowheadStyle(self):
        pass

    def set_EndArrowheadStyle(self,newval):
        pass
    
    EndArrowheadStyle = property(get_EndArrowheadStyle,set_EndArrowheadStyle,doc="EndArrowheadStyle")

    def get_BeginArrowheadStyle(self):
        pass

    def set_BeginArrowheadStyle(self,newval):
        pass

    BeginArrowheadStyle = property(get_BeginArrowheadStyle,set_BeginArrowheadStyle,doc="BeginArrowheadStyle")    

class CFill(object):
    def __init__(self,Fill="",shape=None):
        pass

    def get_transparency(self):
        pass

    def set_transparency(self,newval):
        pass

    Transparency = property(get_transparency,set_transparency,doc="Transparency")

    def Solid(self):
        pass

class CShape(object):
    def __init__(self, name, shapetype, Left, Top, Width=0, Height=0, Fillcolor=0, Text="",Row=None, Col=None, rotation=0,orientation=msoTextOrientationHorizontal,AlternativeText="",ws=None,nodelist=None,control_dict=None,Init_Value=None,linecolor=None,zorder=0,segmenttype=msoSegmentLine,editingtype=msoEditingAuto):
        pass

    def updateShape(self,Fill=None,Text=None):
        pass
    
    def Delete(self):
        pass

    def ZOrder(self,zorder):
        pass

    def set_activeflag(self,value):
        pass

    def get_activeflag(self):
        pass

    def Select(self):
        pass

    def get_visible(self):
        pass

    def set_visible(self, value):
        pass

    Visible = property(get_visible, set_visible, doc='Visible Status')

    def get_name(self):
        pass

    def set_name(self, value):
        pass
    Name = property(get_name, set_name, doc='Shape-Name')

    def get_left(self):
        pass

    def set_left(self, value):
        pass

    Left = property(get_left, set_left, doc='Shape-Left')

    def get_top(self):
        pass

    def set_top(self, value):
        pass

    Top = property(get_top, set_top, doc='Shape-Top')    

    def get_TopLeftCell(self):
        pass

    def set_TopLeftCell(self, value):
        pass

    TopLeftCell = property(get_TopLeftCell, set_TopLeftCell, doc='Shape-Name')

    def get_OnAction(self):
        pass

    def set_OnAction(self, value):
        pass

    OnAction = property(get_OnAction, set_OnAction, doc='Shape-OnAction')        

class CTShapeX(object):
    def __init__(self, name, shapetype, Left, Top, Width, Height, FillTKcolor="", LineTKcolor="",Text="",Row=None, Col=None, rotation=0,orientation=1,nodelist=None,ws=None, tablecanvas=None,control_dict=None,Init_Value=None,zorder=0,segmenttype=0,editingtype=msoEditingAuto):
        pass

    def shape_button_1(self,event=None):
        pass

    def updateShape(self,Fillcolor=None,Text=None,AltText=None):
        pass
    def Delete(self):
        pass

    def ZOrder(self,zorder):
        pass

    def set_activeflag(self,value):
        pass
    def get_activeflag(self):
        pass

    def Select(self):
        pass

    def get_visible(self):
        pass
    def set_visible(self, value):
        pass

    Visible = property(get_visible, set_visible, doc='Visible Status')

    def get_top(self):
        pass

    def set_top(self, value):
        pass
    Top = property(get_top, set_top, doc='Shape-Top')

    def get_text(self):
        pass
    def set_text(self, value):
        pass

    Text = property(get_text, set_text, doc='Shape-Text')

class CCellDict():
    def __init__ (self,ws=None):
        pass

    def __getitem__(self, k):
        pass

    def __setitem__(self,k,value):
        pass


class CWorksheetFunction:
    def __init__(self):
        pass
    def RoundUp(v1,v2):
        pass

class CApplication:
    def __init__(self):
        pass

    def set_canvas_leftclickcmd(self,cmd):
        pass


    def OnTime(self,time,cmd):
        pass

    def RoundUp(v1,v2):
        pass


    def GetSaveAsFilename(self,InitialFileName="", fileFilter="", Title="" ):
        pass

    def GetOpenFilename(self,InitialFileName="", fileFilter="", Title="" ):
        pass

    def setActiveWorkbook(self,workbookName):
        pass

    def Quit(self):
        pass

locale2msoid={"de":1,
              "en":2,
              "nl":3,
              "fr":4,
              "it":5,
              "es":6,
              "da":7
              }
msoid_list = ("de","en","nl","fr","it","es","da")

class CLanguageSettings:
    def __init__(self):
        pass

    def LanguageID(self,id):
        pass

class CFont:
    def __init__(self,name,size):
        pass

class CActiveWindow:
    def __init__(self):
        pass       

class SoundLines:
    def __init__(self):
        pass

    def Exists(self,Channel:int):
        pass

    def Add(Channel, Pin_playerClass):
        pass

class CButton:
    def __init__(self,name):
        pass


class CControl:
    def __init__(self,value):
        pass


def rgbtohex(r,g,b):
    pass


# global variables

ActiveWorkbook = None # :CWorkbook

ThisWorkbook = None # :CWorkbook

Worksheet = None

ActiveSheet = None #:CWorksheet

#WorksheetFunction = CWorksheetFunction()

Application = CApplication() #:CApplication

CellDict = CCellDict() # :CCellDict

def get_selection(self):
        
    return ActiveSheet.get_selection()
    
def set_selection(self, value):
    ActiveSheet.get_selection().Value=value
        
    
Selection = CSelection() #property(get_selection, set_selection, doc='Selection') 

Workbooks =[]

Worksheets = []

ActiveWindow = CActiveWindow()

#Date = "1.1.2022"
#Time = "12:00"


Now = 0

#---------------------------------------
# Event
#---------------------------------------
def Workbook_Open(workbook):
    # Occurs when the workbook is opened.
    pass

def Workbook_Activate(workbook):
    # Occurs when a workbook, worksheet, chart sheet, or embedded chart is activated.
    pass

def Worksheet_Activate(workbook):
    # Occurs when a workbook, worksheet, chart sheet, or embedded chart is activated.
    pass
