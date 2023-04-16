# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2021
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
# 2020-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2021-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *



import proggen.D05_SelectMacrosTreeForm as D05

import proggen.M02_Public as M02
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80
import mlpyproggen.Prog_Generator as PG

import ExcelAPI.XLW_Workbook as P01

from ExcelAPI.XLC_Excel_Consts import *

""" ********************************************************************************
 Select macro using the treeView Dialog from JKP Application Development Services

 This Modul is based on the demo from JKP Application Development Services

Build 026.4
***************************************************************************

 Authors:  JKP Application Development Services, info@jkp-ads.com, http://www.jkp-ads.com
           Peter Thornton, pmbthornton@gmail.com

 (c)2013-2015, all rights reserved to the authors

 You are free to use and adapt the code in these modules for
 your own purposes and to distribute as part of your overall project.
 However all headers and copyright notices should remain intact

 You may not publish the code in these modules, for example on a web site,
 without the explicit consent of the authors
***************************************************************************
 Revision History:
 - Filter function
 - Added description to the intermidiate nodes
   - Separate lines must be zsed for the intermidiate nodes
     - Icons must be added also to this lines
   - Short discription is shown in the treeView
   - Detailed discription is shown in the window below
     If not available the Keys help is shown
   - In filter mode the descriptions are not shown because the separate lines are not available
 - Generate result
 - Scroll wheel support
 > Send to Michael
 - DoubleCkick opens/closes child
 - Horizontal scroll bar corrected
 - TreeView settings are keeped when the dialog is closed to get the same view when it's opened again
 - Show HourGlassCursor when building/updating the TreeView
 - New dialog is used in the DCC, ... sheets
 To switch to debug mode and break in error handlers:
   In the VBAProject properties, right-click Treeview_26
   Set the Conditional Compilation Argument -
       DebugMode = 1
   See: https://bettersolutions.com/vba/debugging/conditional-compiling.htm
# VB2PY (CheckDirective) VB directive took path 1 on DebugMode = 1
 PT counters for class Init & Term events
# VB2PY (CheckDirective) VB directive took path 1 on 0
 Geht nicht so richtig
 Es werden zwar irgend welche (zufälligen) Pixel Muster eingebunden, aber nicht das Bild
 https://www.pcreview.co.uk/threads/copy-shape-image-into-image-control.982606/
 21.10.21: Test ToDo Adapt oo 64 Bit

# VB2PY (CheckDirective) VB directive took path 1 on DebugMode = 1

"""


def SelectMacro_TreeView_Test():
    #UT-----------------------------------
    SelectMacro_TreeView('')
    sys.exit(0)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SelectName - ByVal 
def SelectMacro_TreeView(SelectName):
    #----------------------------------------------------------
    SelectMacrosTreeForm = D05.SelectMacrosTreeform()
    SelectMacrosTreeForm.Start()
    if SelectName != '':
        if InStr(SelectName, '(') > 0:
            SelectName = Split(SelectName, '(')(0) + '('
    return SelectMacrosTreeForm.Show_SelectMacros_TreeView(SelectName)

def __ClassCounts():
    # PT, If making any code modifications it's important to ensure all class instances have been properly terminated.
    #     Classes are counted when created and when destroyed in respective Initialize & Terminate events,
    #     when done the totals should be the same.
    if gClsTreeViewInit != gClsTreeViewTerm or gClsNodeInit != gClsNodeTerm or gFormInit != gFormTerm:
        Debug.Print('clsTreeView', gClsTreeViewInit, gClsTreeViewTerm, gClsTreeViewInit - gClsTreeViewTerm)
        Debug.Print('clsNode', gClsNodeInit, gClsNodeTerm, gClsNodeInit - gClsNodeTerm)
        Debug.Print('gFormInit', gFormInit, gFormTerm, gFormInit - gFormTerm)
        P01.MsgBox('NOT all Classes were terminated !' + vbCr + 'see Immediate window')
    gClsTreeViewInit = 0
    gClsTreeViewTerm = 0
    gClsNodeInit = 0
    gClsNodeTerm = 0
    gFormInit = 0
    gFormTerm = 0

def __Update_TextBoxFilter_onTime():
    #----------------------------------------
    if not __ufForm is None:
        __ufForm.Update_TextBoxFilter()

def __Helper_Replace_Empty_Lines_in_Front_of_Cells():
    c = Variant()

    Cnt = int()
    #---------------------------------------------------------
    # Some entries start with an additional empty line. I don't want to change them manualy...
    P01.Sheets(M02.LIBMACROS_SH).Select()
    for c in P01.Range(P01.Cells(4, 1), P01.Cells(M30.LastUsedRow, M30.LastUsedColumn())):
        if c != '':
            while Len(c) > 1 and Left(LTrim(c), 1) == vbLf:
                c.Value = Mid(LTrim(c), 2)
                Cnt = Cnt + 1
    Debug.Print('Replaced ' + Cnt + ' entries')

def Set_Lib_Macros_Test_Language(Test_Language):
    ListDataSh = P01.CWorksheet()
    #----------------------------------------------------------------
    ListDataSh = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
    ListDataSh.Range['Test_Language'] = Test_Language

def __Test_Set_Lib_Macros_Test_Language():
    #UT--------------------------------------------
    Set_Lib_Macros_Test_Language(- 1)

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Private Declare Function OpenClipboard& Lib "user32" (ByVal hwnd&)
# VB2PY (UntranslatedCode) Private Declare Function EmptyClipboard& Lib "user32" ()
# VB2PY (UntranslatedCode) Private Declare Function GetClipboardData& Lib "user32" (ByVal wFormat%)
# VB2PY (UntranslatedCode) Private Declare Function SetClipboardData& Lib "user32" (ByVal wFormat&, ByVal hMem&)
# VB2PY (UntranslatedCode) Private Declare Function CloseClipboard& Lib "user32" ()
# VB2PY (UntranslatedCode) Private Declare Function CopyImage& Lib "user32" (ByVal handle&, ByVal un1&, ByVal n1&, ByVal n2&, ByVal un2&)
# VB2PY (UntranslatedCode) Private Declare Function DestroyIcon& Lib "user32" (ByVal hIcon&)
