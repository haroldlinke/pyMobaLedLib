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
import tkinter as tk
import mlpyproggen.Prog_Generator as PG
import ExcelAPI.XLF_FormGenerator as XLF
import ExcelAPI.XLW_Workbook as X02

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

import ExcelAPI.XLW_Workbook as X02
import pattgen.M30_Tools as M30
import pattgen.M01_Public_Constants_a_Var as M01
import mlpyproggen.Pattern_Generator as PG
import proggen.M09_Language as M09
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M50_Exchange as M50
import proggen.F00_mainbuttons as F00

# VB2PY (UntranslatedCode) Option Explicit




#################################################################################################

class CSelect_from_Sheet_Form:

    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.UserForm_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
                
        self.Enable_Listbox_Changed = Boolean()
        self.SrcSh = X02.Worksheet()
        self.ListDataSh = String()
        self.Result = String()
        self.Exp_Mode_COL = Long()
        self.LowerWin_COL = Long()
        self.Name_Dat_COL = Long()
        self.ShortDescCOL = Long()
        self.MiddleWinCOL = Long()
        self.Dialog_Dat_ROW1 = Long()
        self.Check_Param_Func = String()
        #*HL Center_Form(Me)

        self.Select_from_Sheet_Form_RSC = {"UserForm":{
            "Name"          : "Select_from_Sheet_Form",
                                "BackColor"     : "#000008",
                                "BorderColor"   : "#000012",
                                "Caption"       : "Dialog_Titel",
                                "Height"        : 472.5,
                                "Left"          : 0,
                                "Top"           : 0,
                                "Type"          : "MainWindow",
                                "Visible"       : True,
                                "Width"         : 574.5,
                                "Components"    : [{"Name":"Description_Frame","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":72,"Left":12,"SpecialEffect":"fmSpecialEffectEtched","Top":240,"Type":"Frame","Visible":True,"Width":540,
                                                    "Components":[{"Name":"Description","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                   "Caption":"",
                                                                   "ControlTipText":"","ForeColor":"#000012","Height":66,"Left":6,"TextAlign":"fmTextAlignLeft","Top":3,"Type":"Label","Visible":True,"Width":528},
                                                                  ]},
                                                   {"Name":"Detail_Frame","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                        "Caption":"",
                                                        "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":12,"SpecialEffect":"fmSpecialEffectEtched","Top":318,"Type":"Frame","Visible":True,"Width":540,
                                                        "Components":[{"Name":"Detail","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                       "Caption":"",
                                                                       "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":6,"TextAlign":"fmTextAlignLeft","Top":3,"Type":"Label","Visible":True,"Width":528},
                                                                      ]},                                                   
                                                   {"Name":"Description_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Description_Label",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":42,"Left":18,"TextAlign":"fmTextAlignLeft","Top":30,"Type":"Label","Visible":True,"Width":528},
                                                   
                                                   {"Name":"Head_Label","BackColor":"#FF0000","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Head_Label",
                                                    "ControlTipText":"","ForeColor":"#FF0000","Height":18,"Left":18,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":228},
                                                   
                                                   {"Name":"Label3","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Name",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":15,"Left":18,"TextAlign":"fmTextAlignLeft","Top":92,"Type":"Label","Visible":True,"Width":222},
                                                   
                                                   {"Name":"Label4","BackColor":"#FF0000","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"",
                                                    "ControlTipText":"","ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","Top":90,"Type":"Label","Visible":True,"Width":540},
                                                   
                                                   {"Name":"Label5","BackColor":"#FF0000","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Beschreibung",
                                                    "ControlTipText":"","ForeColor":"#FF0000","Height":15,"Left":120,"TextAlign":"fmTextAlignLeft","Top":92,"Type":"Label","Visible":True,"Width":420},                                                   
                                                   
                                                   {"Name":"SelectedCnt_Label","BackColor":"#FF0000","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Ausgewählt:     0",
                                                    "ControlTipText":"","ForeColor":"#FF0000","Height":12,"Left":480,"TextAlign":"fmTextAlignLeft","Top":78,"Type":"Label","Visible":True,"Width":66},        
                                                   
                                                   {"Name":"Abort_Button","Accelerator":"A","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Abbrechen",
                                                    "Command": self.Abort_Button_Click ,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":384,"Top":366,"Type":"CommandButton","Visible":True,"Width":72},
                                                   
                                                   {"Name":"Del_Button","Accelerator":"L","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Löschen",
                                                    "Command": self.Del_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":294,"Top":366,"Type":"CommandButton","Visible":True,"Width":72},
                                                   
                                                   {"Name":"Select_Button","Accelerator":"O","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Auswahl",
                                                    "Command": self.Select_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":474,"Top":366,"Type":"CommandButton","Visible":True,"Width":72},
                                                   
                                                   {"Name":"Expert_CheckBox","Accelerator":"E","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Expertenmodus",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":18,"Left":12,"Top":372,"Type":"CheckBox","Visible":True,"Width":142},
                                                   
                                                   {"Name":"ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"",
                                                    "ControlTipText":"","ForeColor":"#000012","Height":126,"Left":12,"Top":106,"Type":"ListBox","Visible":True,"Width":540},                                                   
                                                   ]}
                                             }
        
    def ControlsFind(self,searchname):
        #return control with searchname
        for control in self.Controls:
            if control.Name==searchname:
                return control
        return None
    
    def destroy(self):
        Debug.Print("Destroy Form")
        self.Form.destroy()


    def Calc_Result(self):
        global Result
        Nr = Long()
    
        Res = String()
        #------------------------
        # Return the name and the row number in the Data Sheet
        # If MultiSelect is enabled a space separated list is returned
        for Nr in vbForRange(0, self.ListBox.ListCount - 1):
            if self.ListBox.Selected(Nr):
                Res = Res + self.ListBox.List(Nr, 0) + ',' + str(self.Get_Row_with_Mode_Filter(Nr)) + ' '
                # Return "Name,Nr"  Nr: row nr in the data sheet
        self.Result = M30.DelLast(Res)
        # Delete the tailing space
        
    def Get_Row_with_Mode_Filter(self, ListNr):
        _fn_return_value = None
        Nr = Long()
    
        r = Long()
        #--------------------------------------------------------
        r = self.Dialog_Dat_ROW1
        Nr = - 1
        _with74 = X02.Sheets(self.ListDataSh)
        while True:
            if self.Exp_Mode_COL > 0:
                Is_Valid = _with74.Cells(r, self.Exp_Mode_COL) == '' or self.Expert_CheckBox
            else:
                Is_Valid = True
            if Is_Valid:
                Nr = Nr + 1
            if Nr < ListNr:
                r = r + 1
            else:
                _fn_return_value = r
                return _fn_return_value
        return _fn_return_value
    
    def ListBox_Change(self):
        #---------------------------
        Description = ''
        Detail = ''
        if self.Enable_Listbox_Changed:
            for Nr in vbForRange(0, self.ListBox.ListCount - 1):
                if self.ListBox.Selected(Nr):
                    Cnt = Cnt + 1
                    Row = self.Get_Row_with_Mode_Filter(Nr)
                    if self.MiddleWinCOL > 0:
                        Txt = Replace(self.SrcSh.Cells(Row, self.MiddleWinCOL), '|', vbLf)
                    if Txt != '':
                        Description = Description + Txt + vbCr
                    else:
                        Description = Description + self.SrcSh.Cells(Row, self.ShortDescCOL) + vbCr
                    if self.LowerWin_COL > 0:
                        Detail = Detail + M30.Replace_Double_Space(self.SrcSh.Cells(Row, self.LowerWin_COL)) + vbCr
                        # Show one or more selected details
            self.SelectedCnt_Label = 'Selected: ' + Cnt
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByVal 
    def ListBox_DblClick(self,Cancel):
        #------------------------------------------------------------------
        self.Select_Button_Click()
    
    def Add_Filtered(self):
        r = X02.Range()
    
        c = X02.Range()
        #-------------------------
        # If 3 empty names are found the function is aborted
        _with75 = X02.Sheets(self.ListDataSh)
        r = _with75.Range(_with75.Cells(self.Dialog_Dat_ROW1, self.Name_Dat_COL), _with75.Cells(M30.LastUsedRowIn(PG.ThisWorkbook.Sheets(self.ListDataSh)), self.Name_Dat_COL))
        for c in r:
            if c.Value == '' and _with75.Cells(c.Row + 1, self.Name_Dat_COL) == '' and _with75.Cells(c.Row + 2, self.Name_Dat_COL) == '':
                return
            if self.Exp_Mode_COL > 0:
                Is_Valid = ( _with75.Cells(c.Row, self.Exp_Mode_COL) == '' or self.Expert_CheckBox )  and self.Check_Param(c.Row)
            else:
                Is_Valid = True
            if Is_Valid:
                #self.ListBox.AddItem(c.Value)
                #self.ListBox.List[self.ListBox.ListCount - 1, 1] = _with75.Cells(c.Row, self.ShortDescCOL).Value
                
                value = c.Value + " : " + _with75.Cells(c.Row, self.ShortDescCOL).Value
                self.ListBox.AddItem(value)
    
    def Expert_CheckBox_Click(self):
        #----------------------------------
        if self.Enable_Listbox_Changed:
            self.Load_Data_to_Listbox(self.ListDataSh)
    
    def Load_Data_to_Listbox(self,ListDataSh_par):
        global ListDataSh, SrcSh
        #---------------------------------------------------------
        # Defines the sheet which contains the data and loads the data into the form.
        self.ListDataSh = ListDataSh_par
        # VB2PY (UntranslatedCode) On Error Resume Next
        # For some reasons this function is called two times and the second call generates a crash
        self.SrcSh = PG.ThisWorkbook.Sheets(self.ListDataSh)
        self.ListBox.Clear()
        # VB2PY (UntranslatedCode) On Error GoTo 0
        _with76 = self.ListBox
        _with76.ColumnCount = 2
        _with76.ColumnWidths = '100 Pt'
        self.Add_Filtered()

    def UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialice the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.Form=XLF.generate_form(self.Select_from_Sheet_Form_RSC,self.controller,dlg=self,modal=False)

    def UserForm_Activate(self):
        #------------------------------
        # Is called every time when the form is shown
        #M25.Make_sure_that_Col_Variables_match()
        pass

    def Hide(self):
        self.IsActive=False
        self.Form.destroy()

    def AddControl(self,control):
        self.Controls.append(control)
        self.Controls_Dict[control.Name]=control

    def Show_Dialog(self):
        self.Show()
        
    def Show_Form(self, ListDataSh, Dialog_Titel, Head_Label_Txt, Description_Label_Txt, oCheck_Param_Func=VBMissingArgument, oExpert_CheckBox=VBMissingArgument, oExpert_CheckBox_Checked=VBMissingArgument, oDelete_Button=VBMissingArgument, oExp_Mode_COL=0, oLowerWin_COL=0, oName_Dat_COL=4, oShortDescCOL=5, oMiddleWinCOL=0, oDialog_Dat_ROW1=4):
        #global Check_Param_Func, Exp_Mode_COL, LowerWin_COL, Name_Dat_COL, ShortDescCOL, MiddleWinCOL, Dialog_Dat_ROW1, Enable_Listbox_Changed
        _fn_return_value = None
        #-------------------------------------------------------------------------------
        # Use this function to show the dialog.
        self.UserForm_Initialize()
        self.Caption = Dialog_Titel
        self.Head_Label = Head_Label_Txt
        self.Description_Label = Description_Label_Txt
        self.Check_Param_Func = oCheck_Param_Func
        #if oExpert_CheckBox != '':
        #    self.Expert_CheckBox.Visible = True
        #    self.Expert_CheckBox.Caption = oExpert_CheckBox
        #    self.Expert_CheckBox.Value = oExpert_CheckBox_Checked
        self.Exp_Mode_COL = oExp_Mode_COL
        self.LowerWin_COL = oLowerWin_COL
        self.Name_Dat_COL = oName_Dat_COL
        self.ShortDescCOL = oShortDescCOL
        self.MiddleWinCOL = oMiddleWinCOL
        self.Dialog_Dat_ROW1 = oDialog_Dat_ROW1
        if oDelete_Button == False:
            self.Del_Button.Visible = False
        _with78 = self
        if self.MiddleWinCOL <= 0:
            if self.LowerWin_COL <= 0:
                pass # M30.Hide_and_Move_up(self, self.Description_Frame.Name, self.Del_Button.Name)
                # Both windows hidden
            else:
                # LowerWin_COL > 0 and MiddleWinCOL <= 0
                pass #M30.Hide_and_Move_up(self, self.Description_Frame.Name, self.Detail_Frame.Name)
                # Middle window hidden
        else:
            if self.LowerWin_COL <= 0:
                # MiddleWinCOL > 0
                pass #M30.Hide_and_Move_up(self, self.Detail_Frame.Name, self.Del_Button.Name)
                # Lower window hidden
        self.Load_Data_to_Listbox(ListDataSh)
        self.Enable_Listbox_Changed = True
        self.SelectedCnt_Label = 'Selected: 0'
        self.ControlsFind('ListBox').setFocus()
        #HookFormScroll(Me, 'ListBox')
        # Initialize the mouse wheel scroll function
        self.Show()
        _fn_return_value = self.Result
        #UnhookFormScroll()
        # Deactivate the mouse weel scrol function
        X02.Unload(self)
        # don't keep the data because the form may be used with several data sources
        return _fn_return_value    

    def Show(self):
        self.IsActive = True
        self.UserForm_Activate()
        self.Form.update()
        self.Form.deiconify()
        self.controller.wait_window(self.Form)

    def __UserForm_Initialize():
        #--------------------------------
        # Center the dialog if it's called the first time.
        # On a second call without me.close this function is not called
        # => The last position ist used
        # Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        pass

    def Abort_Button_Click(self):
        #-------------------------------
        global Result, Enable_Listbox_Changed
        #-------------------------------
        self.Hide()
        self.Result = ''
        self.Enable_Listbox_Changed = False
        
    def Del_Button_Click(self):
        global Result, Enable_Listbox_Changed
        #-----------------------------
        self.Hide()
        self.Result = 'DELETE'
        self.Enable_Listbox_Changed = False
    
    def Select_Button_Click(self):
        global Enable_Listbox_Changed
        #--------------------------------
        self.Enable_Listbox_Changed = False
        self.Calc_Result()
        self.Hide()



