# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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

from vb2py.vbfunctions import *
# fromx vb2py.vbdebug import *
import sys
import ExcelAPI.XLW_Workbook as X02
#import mlpyproggen.Pattern_Generator as PG
import pattgen.M09_Language as M09
import pattgen.M30_Tools as M30

#**************************
#'  Port handling functions
#**************************

def port_is_busy(port):
    
    if type(port)==int:
        return port <0
    elif type(port)==str:
        return port.startswith("*")
    
def port_is_available(port):
    if type(port)==int:
        return port > 0
    elif type(port)==str or type(port)==X02.CRange:
        return not (port.startswith("*") or port=="COM?" or port==" " or port=="NO DEVICE")
    return False
    
def port_reset(port):
    if port.startswith("*"):
        return(port[1:])
    else:
        return port
    
def port_check_format(port):
    if IsNumeric(port):
        return "COM"+port
    else:
        return port
    
def port_set_busy(port):
    if port.startswith("*"):
        return(port)
    else:
        return "*"+port
    
   
def is_64bit() -> bool:
    return sys.maxsize > 2**32

def Create_New_Sheet(SheetName, Add_to_Duplicate_Name='_Copy_', AfterSheetName=""):
    #---------------------------------------------------------------------------------------------------------------------------------------
    
    OrgName = SheetName
    SheetName = M30.Unic_SheetName(SheetName, Add_to_Duplicate_Name)
    #ThisWorkbook.Activate
    # 12.06.20: Prevent crash if prog. is started an other excel is open
    #AfterSheet = X02.Sheets(X02.Sheets.Count) #*HL
    #if M30.SheetEx(OrgName):
    #    AfterSheet = X02.Sheets(OrgName)
    #if AfterSheetName != '':
    #    AfterSheet = X02.Sheets(AfterSheetName) #*HL
    
    AfterSheet=AfterSheetName #*HL
    X02.Sheets(AfterSheetName).Copy(SheetName=SheetName,After=AfterSheet)
    #PG.ThisWorkbook.Activate()
    #X02.ActiveSheet.Name = SheetName
    X02.Sheets(SheetName).Select()

def New_Sheet():
    CopyFromSheet = ""
    Name = ""
    #---------------------
    # Is called if the "Neues Blatt" Button is pressed
    #_select8 = X02.MsgBox(M09.Get_Language_Str('Sollen die Einstellungen des aktuellen Blatts übernommen werden?'), vbYesNoCancel + vbQuestion, M09.Get_Language_Str('Neues Blatt anlegen'))
    #if (_select8 == vbCancel):
    #    return
    #elif (_select8 == vbYes):
    CopyFromSheet = X02.ActiveSheet.Name
    Name = X02.InputBox(M09.Get_Language_Str('Name des neuen Blattes?'), M09.Get_Language_Str('Neues Blatt anlegen'), M30.Unic_SheetName(CopyFromSheet, '_'))
    if Name != '':
        #if CopyFromSheet != '':
            #TempName = PG.ThisWorkbook.Path + '\\' + M01.ExampleDir + '\\TempExample.MLL_pcf'
            #pattgen.M07_Save_Sheet_Data.Save_One_Sheet(X02.Sheets(CopyFromSheet), TempName, False, M30.Unic_SheetName(Name, '_'))
            #Load_Sheets(TempName, '', AfterSheetName=CopyFromSheet)
        #else:
        Create_New_Sheet(Name, Add_to_Duplicate_Name='_', AfterSheetName=CopyFromSheet)
            #X02.RangeDict[M01.Macro_N_Rng] = M30.Replace_Illegal_Char(X02.ActiveSheet.Name)
            #Add_by_Hardi()
        #X02.Range(M01.FirstLEDTabRANGE).Select()
        #M30.Protect_Active_Sheet()




