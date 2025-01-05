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
# 2021-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

import tkinter as tk
from tkinter import ttk
from mlpyproggen.tooltip import Tooltip
from tkcolorpicker.spinbox import Spinbox
from tkcolorpicker.limitvar import LimitVar

import mlpyproggen.Prog_Generator as PG

import proggen.M02_Public as M02
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_Diverse as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Multiplexer as M80

from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLA_Application as P01

import logging

class UserForm_Other():
    def __init__(self):

        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt = M09.Get_Language_Str("Abbrechen")
        self.button2_txt = M09.Get_Language_Str("Ok")
        self.res = False
        self.UserForm_Res = ""
        
        self.ParList = Variant()
        self.FuncName = String()
        self.NamesA = Variant()
        self.Show_Channel_Type = Long()
        self.CurWidth = Long()
        self.CurHeight = Long()
        self.MinFormHeight = Long()
        self.MinFormWidth = Long()
        self.MAX_PAR_CNT = 14
        self.TypA = vbObjectInitialize((self.MAX_PAR_CNT,), String)
        self.MinA = vbObjectInitialize((self.MAX_PAR_CNT,), Variant)
        self.MaxA = vbObjectInitialize((self.MAX_PAR_CNT,), Variant)
        self.ParName = vbObjectInitialize((self.MAX_PAR_CNT,), String)
        self.Invers = vbObjectInitialize((self.MAX_PAR_CNT,), Boolean)
        self.DEFAULT_PAR_WIDTH = 48
        self.ParamVar = {}
        self.Controls={}
        self.UserForm_Initialize()
        self.default_font = self.controller.defaultfontnormal
        self.default_fontsmall = self.controller.defaultfontsmall
        self.default_fontlarge = self.controller.defaultfontlarge        
 
    def ok(self, event=None):
        self.IsActive = False
        self.OK_Button_Click()
        
        #self.Userform_res = value
        self.top.destroy()
        P01.ActiveSheet.Redraw_table()
        self.res = True
 
    def cancel(self, event=None):
        self.UserForm_Res = '<Abort>'
        self.IsActive = False
        self.top.destroy()
        P01.ActiveSheet.Redraw_table()
        self.res = False

    def show(self):
        
        self.IsActive = True
        self.top.wait_visibility()
        self.top.takefocus = True
        self.top.focus_set()
        self.top.focus_force()
        self.top.grab_set()        
        self.controller.wait_window(self.top)

        return self.res

    
    """ Following parameters exist:
     LED Cx  InCh    Val0    Val1    On_Min  On_Limit    LedCnt  Brightness  DstVar  Mode    Enable  TimeOut DstVar1 DstVarN MinTime MaxTime MinOn   MaxOn   Var SrcLED  EnableCh    Start   End GlobVarNr   FirstInCh   InCh_Cnt    Duration    Period  Pause   Act Off S_InCh  R_InCh  Timeout T_InCh  DstVar0 MinBrightness   MaxBrightness   B_LED_Cx    B_LED   InNr    TmpNr   Rotate  Steps   MaxSoundNr  InReset
    
    
     Maximal 6 named parameter in one macro
    
     ToDo:
     - Alte eingaben speichern und beim nächsten mal wieder verwenden
       - Geht nicht in dem man das Unload Me weglässt
       - Man könnte ein Array anlegen in dem die Parameter Namen und der Letzte Wert enthalten ist
         das sollte aber für jedes Makro spezifisch sein
    # VB2PY (CheckDirective) VB directive took path 1 on VBA7

     Scrollbar:
     ~~~~~~~~~~
     Wir können nicht den Scrollbar der Textboy verwenden weil diese nicht aktiv ist ;-(
     Darum ist ein eigener Balken daneben platziert. Dieser muss aber von Hand angesteuert werden.
    
     - Die Höhe des Scroll handles kann über ScrollBar1.LargeChange gesetzt werden. Diese kann aber
       maximal die halbe Höhe haben
     - Die .LineCount Eigenschaft der Textbox kann nur verwendet werden wenn sie den Fokus hat.
     - Die Position der Textbox wird über SelStart bestimmt. Der Wert wird Buchstabenweise gesetzt.
       Der Wert müsste immer um die Länge einer Zeile erhöht werden.
       Aber das ist kompliziert
    # VB2PY (CheckDirective) VB directive took path 1 on False
    ------------------------------
    -----------------------------------------------
    --------------------------------
    -----------------------------------------------------------------------------------------------------------
     06.11.21: Juergen make form resizeable feature
    -----------------------------------------------------------------------------------------------------------
     06.11.21: Juergen make form resizeable feature
    -----------------------------------------------------------------------------------------------------------
     06.11.21: Juergen make form resizeable feature
    
     Written: August 02, 2010
     Author:  Leith Ross
     Summary: Makes the UserForm resizable by dragging one of the sides. Place a call
             to the macro MakeFormResizable in the UserForm'
     from  https://www.mrexcel.com/board/threads/resize-a-userform.485489/
    -----------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------
    """
    

    def Check_Limit_to_MinMax(self, ParNr, Value):

        fn_return_value = None
        Msg = String()
    
        ValidRangeTxt = String()
        #-------------------------------------------------------------------------------
        # Return true if its within the alowed range
        #With Controls("Par" & ParNr)
        ValidRangeTxt = vbCr + M09.Get_Language_Str('Bitte einen Wert zwischen ') + self.MinA(ParNr - 1) + M09.Get_Language_Str(' und ') + self.MaxA(ParNr - 1) + M09.Get_Language_Str(' eingeben.')
        if Value == '':
            Msg = M09.Get_Language_Str('leer.') + ValidRangeTxt
        elif not IsNumeric(Value):
            Msg = M09.Get_Language_Str('keine gültige Zahl.') + ValidRangeTxt
        elif CStr(Round((int(Value)), 0)) != CStr(Value):
            Msg = M09.Get_Language_Str('nicht Ganzzahlig.') + ValidRangeTxt
        elif self.MinA(ParNr - 1) != '' and int(Value) < P01.val(self.MinA(ParNr - 1)):
            Msg = M09.Get_Language_Str('zu klein!' + vbCr + 'Der Minimal zulässiger Wert ist: ') + self.MinA(ParNr - 1)
        elif self.MaxA(ParNr - 1) != '' and int(Value) > P01.val(self.MaxA(ParNr - 1)):
            Msg = M09.Get_Language_Str('zu groß!' + vbCr + 'Der Maximal zulässige Wert ist: ') + self.MaxA(ParNr - 1)
        if Msg != '':
            #Controls('Par' + ParNr).setFocus()
            P01.MsgBox(M09.Get_Language_Str('Der Parameter \'') + self.Controls.get('LabelPar' + str(ParNr),"key not found") + M09.Get_Language_Str('\' ist ') + Msg, vbInformation, M09.Get_Language_Str('Bereichsüberschreitung'))
        else:
            fn_return_value = True
        #End With
        return fn_return_value
    
    def Check_Txt_Limit_to_MinMax(self, ParNr, Value):
        _fn_return_value = None
        Msg = String()
        # 03.03.23 Juergen
        #-------------------------------------------------------------------------------
        # Return true if its within the alowed range
        Msg = ''
        if self.MinA(ParNr - 1) != '' and Len(Value) < P01.val(self.MinA(ParNr - 1)):
            Msg = M09.Get_Language_Str('zu kurz!' + vbCr + 'Die minimal zulässiger Länge ist: ') + self.MinA(ParNr - 1)
        elif self.MaxA(ParNr - 1) != '' and Len(Value) > P01.val(self.MaxA(ParNr - 1)):
            Msg = M09.Get_Language_Str('zu lang!' + vbCr + 'Die maximal zulässige Länge ist: ') + self.MaxA(ParNr - 1)
        if Msg != '':
            #Controls('Par' + ParNr).setFocus()
            P01.MsgBox(M09.Get_Language_Str('Der Parameter \'') + self.Controls.get('LabelPar' + str(ParNr),"key not found") + M09.Get_Language_Str('\' ist ') + Msg, vbInformation, M09.Get_Language_Str('Bereichsüberschreitung'))
        else:
            _fn_return_value = True
        return _fn_return_value
    
    
    def LimmitActivInput(self, ct, MinVal, MaxVal):
        #--------------------------------------------------------------------------------
        with_0 = ct
        if not IsNumeric(with_0.Value):
            while Len(with_0.Value) > 0 and not IsNumeric(with_0.Value):
                with_0.Value = M30.DelLast(with_0.Value)
        else:
            if P01.val(with_0.Value) < MinVal:
                with_0.Value = MinVal
            if P01.val(with_0.Value) > MaxVal:
                with_0.Value = MaxVal
            #if Round(with_0.Value, 0) != with_0.Value:
            #    with_0.Value = Round(with_0.Value, 0)
    
    def Check_Time_String(self, ParNr):
        
        fn_return_value = None
        ValidRangeTxt = String()
    
        Parts = Variant()
        #-----------------------------------------------------------
        ValidRangeTxt = vbCr + M09.Get_Language_Str('Bitte einen Zeit zwischen ') + self.MinA(ParNr - 1) + M09.Get_Language_Str(' ms und ') + self.MaxA(ParNr - 1) + M09.Get_Language_Str(' ms eingeben.' + vbCr + 'Die Zeitangabe kann auch eine der folgenden Einheit enthalten:' + vbCr + ' Min, Sec, ms ' + vbCr + 'Achtung: Zwischen Zahl und Einheit muss ein Leerzeichen stehen.' + vbCr + 'Beispiel: 3 Sec')
        with_1 = self.Controls['Par' + str(ParNr)]
        if type(with_1) == str:
            Parts = Split(with_1, ' ')
        else:
            Parts = Split(with_1.Value, ' ')
        ValidUnits = " Min Sek sek Sec sec Ms ms "
        Err = UBound(Parts) != 1
        if not Err:
            Err = not IsNumeric(Parts(0))
        if not Err:
            Err = InStr(ValidUnits, ' ' + Parts(1) + ' ') == 0
        if Err:
            P01.MsgBox(M09.Get_Language_Str('Der Parameter \'') + self.ParName(ParNr - 1) + M09.Get_Language_Str('\' ist ungültig') + ValidRangeTxt, vbInformation, M09.Get_Language_Str('Ungültiger Parameter'))
            return fn_return_value
        else:
            select_0 = LCase(Parts(1))
            if (select_0 == 'min'):
                value = P01.val(Parts(0)) * 60 * 1000
            elif (select_0 == 'sec') or (select_0 == 'sek'):
                value = P01.val(Parts(0)) * 1000
            elif (select_0 == 'ms'):
                value = P01.val(Parts(0))
            else:
                P01.MsgBox('Internal error: Unknown unit \'' + Parts(1) + '\' in Check_Time_String()', vbCritical, 'Internal error')
                M30.EndProg()
            if self.Check_Limit_to_MinMax(ParNr, value) == False:
                return fn_return_value
        fn_return_value = True
        return fn_return_value
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Value - ByVal 
    def Check_RGB_List(self, TypStr, Value, ParNr):
        fn_return_value = None
        s = Variant()
    
        Err = Boolean()
    
        ExpCnt = Long()
        #------------------------------------------------------------------------------------------------
        if TypStr == 'RGB':
            ExpCnt = 3
        else:
            ExpCnt = 6
        if UBound(Split(Value, ',')) != ExpCnt - 1:
            P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Es müssen #1# Farbwerte zwischen 0 und 255 angegeben werden'), '#1#', ExpCnt), vbCritical, M09.Get_Language_Str('Anzahl der angegebenen Farbwerte ist falsch'))
            return fn_return_value
        for s in Split(Value, ','):
            if not IsNumeric(Trim(s)):
                Err = True
            if not Err:
                Err = P01.val(s) < 0 or P01.val(s) > 255 or InStr(Value, '.') > 0
            if Err:
                P01.MsgBox(Replace(M09.Get_Language_Str('Fehler der Parameter \'#1#\' ist ungültig.' + vbCr + 'Die Farbwerte müssen im Bereich von 0 bis 255 liegen'), '#1#', Controls('LabelPar' + ParNr)), vbCritical, M09.Get_Language_Str('Ungültiger RGB Parameter'))
                return fn_return_value
        fn_return_value = Value
        return fn_return_value
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: val - ByRef 
    def Check_Par_with_ErrMsg(self, ParNr, value):
        fn_return_value = ""
        VarLabel = String()
    
        ShowErr = Boolean()
        #-------------------------------------------------------------------------------------
        if ParNr > self.MAX_PAR_CNT:
            P01.MsgBox('Internal error in Check_Range', vbCritical,'Internal error in Check_Range')
            M30.EndProg()
        paramName = self.ParName[ParNr-1]
        parVariable = self.ParamVar.get(paramName)
        #with_2 = Controls('Par' + ParNr)
        #with_2.Value = Trim(with_2.Value)
        #Debug.Print "Check_Range " & ParName(ParNr - 1) & ": " & .Value
        value = parVariable.get()
        VarLabel = paramName
        select_1 = self.TypA(ParNr - 1)
        if (select_1 == ''):
            if self.Check_Limit_to_MinMax(ParNr, value) == False:
                return fn_return_value
        elif (select_1 == 'Time'):
            if IsNumeric(value):
                value = Int(value)
                if self.Check_Limit_to_MinMax(ParNr, value) == False:
                    return fn_return_value
            else:
                if self.Check_Time_String(ParNr) == False:
                    return fn_return_value
            #**HLI value = Replace(value, ',', '.') - int cannot be chnaged like a string
        elif (select_1 == 'Var'):
            ShowErr = ( value == '' )
            if not ShowErr:
                if Left(value, Len('#InCh')) != '#InCh':
                    ShowErr = not Like(Left(value, 1), '[_a-zA-Z]')
            if ShowErr:
                P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Der Parameter \'#1#\' muss einen gültigen Variablennamen enthalten'), '#1#', VarLabel), vbCritical, M09.Get_Language_Str('Ungültiger Variablenname'))
                #with_2.setFocus()
                return fn_return_value
        elif (select_1 == 'Txt'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'SheetName'):
            # 03.03.23 Juergen
            if self.Check_Txt_Limit_to_MinMax(ParNr, value) == False:
                return fn_return_value
            if not M30.WorksheetExists(value):
                P01.MsgBox(M09.Get_Language_Str('Der angegebene Blattname existiert nicht: \'') + value + '\'', vbCritical, M09.Get_Language_Str('Fehler beim Einbinden eines Blattes'))
                return fn_return_value            
        elif (select_1 == 'Mode'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'List'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'PinList'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'PinNr'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'Logic'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'OutList'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'InpVar'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'GVarNr'):
            Debug.Print('ToDo: Check parameter typ \'' + self.TypA(ParNr - 1) + '\'')
        elif (select_1 == 'RGB') or (select_1 == 'RGB2'):
            value = self.Check_RGB_List(self.TypA(ParNr - 1), Replace(Trim(M30.Replace_Multi_Space(Replace(value, ',', ' '))), ' ', ', '), ParNr)
            fn_return_value = ( value != '' )
            return fn_return_value
        elif (select_1 == 'CmpMod'):
            if InStr(' ' + M02.L2V_COM_OPERATORS + ' ', ' ' + value + ' ') == 0:
                P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Der Parameter \'#1#\' muss eine der folgenden Vergleichsoperatoren enthalten:' + vbCr + '  #2#'), '#1#', VarLabel), '#2#', M02.L2V_COM_OPERATORS), vbCritical, M09.Get_Language_Str('Ungültiger Vergleichsoperator'))
                return fn_return_value
        elif (select_1 == 'MB_LED'):
            if ( IsNumeric(value) and  ( int(value) < 0 or int(value) > 16 ) )  or  ( not IsNumeric(value) and int(InStr(' ' + M02.MB_LED_NR_STR + ' ', ' ' + value + ' ')) == 0 ) :
                P01.MsgBox(Replace(Replace(M09.Get_Language_Str('Fehler: Der Parameter \'#1#\' muss eine der folgenden Werte enthalten:' + vbCr + '  #2#'), '#1#', VarLabel), '#2#', '0 - 16, D2 - D5, D7 - D13, A0 - A5'), vbCritical, M09.Get_Language_Str('Ungültige LED Bezeichnung'))
                return fn_return_value
        else:
            P01.MsgBox('Internal error: Unknown parameter Typ: \'' + self.TypA(ParNr - 1) + '\'', vbCritical, 'Internal Error')
            M30.EndProg()
        #val = with_2.Value
        fn_return_value = value
        return fn_return_value
    
    def LED_Channel_TextBox_Change(self):
        #---------------------------------------
        if self.Show_Channel_Type == M10.CHAN_TYPE_LED:
            self.LimmitActivInput(LED_Channel_TextBox, 0, M02.LED_CHANNELS - 1)
        elif self.Show_Channel_Type == M10.CHAN_TYPE_SERIAL:
            self.LimmitActivInput(LED_Channel_TextBox, 0, M02.SERIAL_CHANNELS - 1)
    
    def Par10Select_Change():
        Par10.Value = Par10Select.Value
    
    def Par11Select_Change():
        Par11.Value = Par11Select.Value
    
    def Par12Select_Change():
        Par12.Value = Par12Select.Value
    
    def Par13Select_Change():
        Par13.Value = Par13Select.Value
    
    def Par14Select_Change():
        Par14.Value = Par14Select.Value
    
    def Par1Select_Change():
        Par1.Value = Par1Select.Value
    
    def Par2Select_Change():
        Par2.Value = Par2Select.Value
    
    def Par3Select_Change():
        Par3.Value = Par3Select.Value
    
    def Par4Select_Change():
        Par4.Value = Par4Select.Value
    
    def Par5Select_Change():
        Par5.Value = Par5Select.Value
    
    def Par6Select_Change():
        Par6.Value = Par6Select.Value
    
    def Par7Select_Change():
        Par7.Value = Par7Select.Value
    
    def Par8Select_Change():
        Par8.Value = Par8Select.Value
    
    def Par9Select_Change():
        Par9.Value = Par9Select.Value
    
    def ScrollBar1_Change():
        LinesDialog = Long()
        #------------------------------
        # ToDo: Die Steuerung ist noch nicht gut
        # - Slider Size anpassen
        # - Die Description_TextBox sollte nicht editierbar sein
        #
        #Debug.Print ScrollBar1.Value
        LinesDialog = 5
        with_3 = Description_TextBox
        with_3.setFocus()
        ## VB2PY (CheckDirective) VB directive took path 1 on 0
        if with_3.LineCount > LinesDialog:
            ScrollBar1.Min = 0
            ScrollBar1.Max = with_3.LineCount - LinesDialog - 1
            ScrollBar1.LargeChange = with_3.LineCount - LinesDialog - 1
        with_3.SelStart = with_3.TextLength / with_3.LineCount * ScrollBar1.Value
        Debug.Print('Lines:' + with_3.LineCount + ' MaxLength:' + with_3.MaxLength + ' TextLength:' + with_3.TextLength + ' ScrollBar1.Value:' + ScrollBar1.Value + ' SelStart:' + with_3.SelStart)
        ScrollBar1.setFocus()
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lngRotation - ByVal 
    def MouseWheel(lngRotation):
        ctlCurrentControl = Variant()
        #-----------------------------------------------
        # Process the mouse wheel changes
        #Debug.Print "MouseWheel" & lngRotation ' Debug
        ctlCurrentControl = self.ActiveControl
        with_4 = Description_TextBox
        with_4.setFocus()
        ## VB2PY (CheckDirective) VB directive took path 1 on 1
        if lngRotation < 0:
            Application.SendKeys('{HOME}{DOWN}{DOWN}{DOWN}')
        else:
            Application.SendKeys('{HOME}{UP}{UP}{UP}')
        DoEvents()
        ctlCurrentControl.setFocus()
    
    def UserForm_Initialize(self):
        #--------------------------------
        #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
        #*HLChange_Language_in_Dialog(Me)
        self.MinFormHeight = 0
        self.MinFormWidth = 0
        #*M30.Restore_Pos_or_Center_Form(Me, OtherForm_Pos)
    
    def UserForm_Resize(self):
        if self.MinFormHeight != 0 and self.MinFormWidth != 0:
            if self.Height < self.MinFormHeight:
                self.Height = self.MinFormHeight
            if self.Width < self.MinFormWidth:
                self.Width = self.MinFormWidth
            DiffHeight = self.Height - self.CurHeight
            DiffWidth = self.Width - self.CurWidth
            for c in self.Controls:
                if c.Name == Description_TextBox.Name:
                    c.Height = c.Height + DiffHeight
                    c.Width = c.Width + DiffWidth
                elif c.Name == ScrollBar1.Name:
                    c.Height = c.Height + DiffHeight
                    c.Left = c.Left + DiffWidth
                elif c.Name == OK_Button.Name or c.Name == Abort_Button.Name:
                    c.Top = c.Top + DiffHeight
                    c.Left = c.Left + DiffWidth
                elif c.Parent.Name != LED_Kanal_Frame.Name:
                    c.Top = c.Top + DiffHeight
            self.CurWidth = self.Width
            self.CurHeight = self.Height
    
    def Resize_Description(self, heightCorr):
        c = Variant()
        for c in self.Controls:
            if c.Name != Description_TextBox.Name and c.Name != ScrollBar1.Name:
                if c.Parent.Name != LED_Kanal_Frame.Name:
                    c.Top = c.Top + heightCorr
        Description_TextBox.Height = Description_TextBox.Height + heightCorr
        ScrollBar1.Height = ScrollBar1.Height + heightCorr
        self.Height = self.Height + heightCorr
    
    def MakeFormResizable(self, oForm):
        lStyle = Long()
    
        RetVal = Variant()
    
        hwnd = LongPtr()
    
        WS_THICKFRAME = 0x40000
    
        GWL_STYLE = ( - 16 )
        ## VB2PY (CheckDirective) VB directive took path 1 on VBA7
        hwnd = FindWindow('ThunderDFrame', oForm.Caption)
        #Get the basic window style
        lStyle = GetWindowLong(hwnd, GWL_STYLE) or WS_THICKFRAME
        #Set the basic window styles
        RetVal = SetWindowLong(hwnd, GWL_STYLE, lStyle)
        #Clear any previous API error codes
        SetLastError(0)
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: StartNr - ByVal 
    def Get_RGB_from_OldParams(self, OldParams, StartNr, Cnt):
        fn_return_value = None
        Nr = Long()
    
        Res = String()
        #-----------------------------------------------------------------------------------------------------------
        for Nr in vbForRange(StartNr, StartNr + Cnt - 1):
            Res = Res + Trim(OldParams(Nr)) + ' '
        fn_return_value = Res
        return fn_return_value
    
    def _key_return(self,event=None):
        
        param = event.widget
        self._update_value(param.macro,param.key)
    
        
        #tabframe=self.getFramebyName(macro)
        #if tabframe!=None:
        #    tabframe._update_value(paramkey)


    def _update_value(self,macro,paramkey):
        logging.info("update_value: %s - %s",macro,paramkey)
        tabframe=self.getFramebyName(macro)
        if tabframe!=None:
            tabframe._update_value(paramkey)
            
    def create_color_palette(self, parent_frame):
        
        LABELWIDTH = int(16*SIZEFACTOR)
        
        COLOR_PALLETTE_COLUMNS = 4
        
        # --- palette
        self.colorpalette = self.getConfigData("palette")
        self.colorpalette_labels_dict={}
        palette = self.colorpalette
        palette_frame = ttk.Frame(parent_frame)
        palette_frame.grid(row=0, column=1, rowspan=3, sticky="ne")
        for i, key in enumerate(palette):
            keycolor = palette[key]
            color_disp,brightness_text = self.keycolor_to_dispcolor(keycolor)
            fontcolor = "#000000"
            text = key #+ "\n" + brightness_text
            if len(text)>10:
                text = text.replace("_","\n",1)
            l = tk.Label(palette_frame, background=color_disp, width=LABELWIDTH, height=2,text=text,fg=fontcolor)
            l.bind("<Button-1>", self.checkcolor)
            self.ToolTip(l, key=key)
            l.bind("<FocusOut>", lambda e: e.widget.configure(relief="raised"))
            #l.pack()
            l.key = key
            l.grid(row=i % COLOR_PALLETTE_COLUMNS, column=i // COLOR_PALLETTE_COLUMNS, padx=2, pady=2)
            
            self.colorpalette_labels_dict[key]=l
            
    def ToolTip(self, widget,text="", key="",button_1=False):
        if text:
            tooltiptext = text
        else:
            tooltiptext = ""
        tooltip_var = None
        try:
            tooltip_var = widget.tooltip
        except:
            tooltip_var = None
            
        if tooltip_var==None:
            tooltip_var=Tooltip(widget, text=tooltiptext,button_1=button_1)
            widget.tooltip = tooltip_var
        else:
            tooltip_var.unschedule()
            tooltip_var.hide()
            tooltip_var.update_text(text)            
        return    
    
    def create_widget(self,parent_frame,row,column,paramkey, param_title,param_type,param_min,param_max,param_default,titlerow,titlecolumn,param_tooltip,combo_value_list=[],combo_text_list=[]):
        
        MACROLABELWIDTH = 40*2
        MACRODESCWIDTH = 20*2
        MACRODESCWRAPL = 120*2
        
        PARAMFRAMEWIDTH = 105
        
        PARAMLABELWIDTH = 40
        PARAMLABELWRAPL = 1000
        
        PARAMSPINBOXWIDTH = 6
        PARAMENTRWIDTH = 16
        PARAMCOMBOWIDTH = 16
     
        STICKY = "w"
        ANCHOR = "w"
        
        titlerow = 0
        valuerow = 0
        titlecolumn = 1
        valuecolumn = 0
        deltarow = 1
        deltacolumn = 2
        
        param_hide = False
        param_value_scrollable = False
        param_readonly = False
        param_allow_value_entry = False
        
        self.fontlabel = self.default_font
        self.fontspinbox = self.default_font
        self.fonttext = self.default_font
        self.fontentry = self.default_font
        
        if param_type == "": # number value param
            
            label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
            label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
            self.ToolTip(label, text=param_tooltip)
            if param_max == "":
                param_max = 255
            if param_min == "":
                param_min = 0
            paramvar = LimitVar(param_min, param_max, parent_frame)
            paramvar.set(param_default)
            paramvar.key = paramkey
            
            #if param_value_change_event:
            #    s_paramvar = Spinbox(parent_frame, from_=param_min, to=param_max, width=PARAMSPINBOXWIDTH, name='spinbox', textvariable=paramvar,font=self.fontspinbox,command=lambda:self._update_value(macro,paramkey))
            #else:
            s_paramvar = Spinbox(parent_frame, from_=param_min, to=param_max, width=PARAMSPINBOXWIDTH, name='spinbox', textvariable=paramvar,font=self.fontspinbox)

            s_paramvar.delete(0, 'end')
            s_paramvar.insert(0, param_default)
            s_paramvar.grid(row=row+valuerow, column=column+valuecolumn, padx=2, pady=2, sticky=STICKY)
            s_paramvar.key = paramkey
            
            return paramvar
            
        elif param_type == "Time": # Time value param
            
            label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
            label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
            self.ToolTip(label, text=param_tooltip)
            
            
            paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH,font=self.fontentry)
            paramvar.delete(0, 'end')
            paramvar.insert(0, param_default)
            paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
            paramvar.key = paramkey
            
            return paramvar
                
        elif param_type == "String" or param_type=="Var": # String value param
            
            label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
            label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
            self.ToolTip(label, text=param_tooltip)
            
            
            paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH,font=self.fontentry)
                 
            #if param_value_change_event:
            #    paramvar.bind("<Return>",self._key_return)                

            paramvar.delete(0, 'end')
            paramvar.insert(0, param_default)
            paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
            paramvar.key = paramkey
            #paramvar.macro = macro
            
            return paramvar
        
        elif param_type == "BigEntry": # Text value param
            
            label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,font=self.fontlabel)
            label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
            self.ToolTip(label, text=param_tooltip)
            paramvar = tk.Entry(parent_frame,width=PARAMENTRWIDTH*3,font=self.fontentry)
            
            #if param_value_change_event:
            #    paramvar.bind("<Return>",self._key_return)
                                
            paramvar.delete(0, 'end')
            paramvar.insert(0, param_default)
            paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
            paramvar.key = paramkey
            #paramvar.macro = macro
            
            return paramvar
        
        elif param_type == "Text": # Text value param
            if not param_hide:
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.ToolTip(label, text=param_tooltip)
            
            number_of_lines = "" #paramconfig_dict.get("Lines","")
            if number_of_lines == "":
                number_of_lines = "2"
                
            if param_value_scrollable:
                paramvar = tk.scrolledtext.ScrolledText(parent_frame,bg=self.cget('bg'),width=PARAMENTRWIDTH*5,height=int(number_of_lines),font=self.fonttext)
            else:
                paramvar = tk.Text(parent_frame,width=PARAMENTRWIDTH*5,bg=self.cget('bg'),height=int(number_of_lines),font=self.fonttext)
            
            paramvar.delete("1.0", "end")
            paramvar.insert("end",param_default)
            if not param_hide:
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
            paramvar.key = paramkey
            
            if param_readonly:
                paramvar.state = "disabled"
                
            return paramvar
                
        elif param_type == "Checkbutton": # Checkbutton param
            paramvar = tk.IntVar(value=0)
            paramvar.key = paramkey
             
            label=tk.Checkbutton(parent_frame, text=param_title,width=PARAMLABELWIDTH*2,wraplength = PARAMLABELWRAPL*2,variable=paramvar,font=self.fontlabel,onvalue = 1, offvalue = 0)
            label.grid(row=row+valuerow, column=column, columnspan=2,sticky=STICKY, padx=2, pady=2)
            self.ToolTip(label, text=param_tooltip)
            
            return paramvar
                            
        elif param_type == "Combo" or param_type == "List": # Combolist param
            
            if not param_hide:
                label=tk.Label(parent_frame, text=param_title,width=PARAMLABELWIDTH,height=2,wraplength = PARAMLABELWRAPL,anchor=ANCHOR,font=self.fontlabel)
                label.grid(row=row+titlerow, column=column+titlecolumn, sticky=STICKY, padx=2, pady=2)
                self.ToolTip(label, text=param_tooltip)
            
            if param_allow_value_entry:
                paramvar = ttk.Combobox(parent_frame, value=combo_value_list,width=PARAMCOMBOWIDTH,font=self.fontlabel)
            else:                
                paramvar = ttk.Combobox(parent_frame, value=combo_value_list, state="readonly", width=PARAMCOMBOWIDTH,font=self.fontlabel)
            #combo_value_list = paramconfig_dict.get("KeyValues",paramconfig_dict.get("Values",[]))
            #combo_text_list = paramconfig_dict.get("ValuesText",[])
            
            if combo_text_list == []:
                paramvar["values"] = combo_value_list
            else:
                paramvar["values"] = combo_text_list
            found = False
            index = 0
            for select_value in combo_value_list:
                if select_value == param_default:
                    paramvar.current(index)
                    found = True
                    break
                index = index +1
            if not found:
                paramvar.current(0) #set the selected view                    
            
            if not param_hide:
                paramvar.grid(row=row+valuerow, column=column+valuecolumn, sticky=STICKY, padx=2, pady=2)
            paramvar.key = paramkey
            paramvar.keyvalues = combo_value_list
            paramvar.textvalues = combo_text_list
            
            return paramvar
        
        else:
            return None
                

    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Par - ByVal 
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
    def Show_UserForm_Other(self, Par, Name, Description, LedChannels, Show_Channel, LED_Channel, Def_Channel):
        
        MLLtype2widgettype = {"Mode" : "String",
                              "SheetName" : "String",
                              "Var" : "String",
                              "CmpMod" : "String",
                              "MB_LED" : "String",
                              "List" : "List",
                              "Time" : "Time",
                              "RGB" : "String",
                              "RGB2" : "String",
                              "PinNr" : "String",
                              "PinLst": "String",
                              "InpVar": "String", 
                              "GVarNr": "String",
                              "OutList": "String",
                              "Logic": "BigEntry",
                              "Cx": "String",
                              "#" : "String",
                              }        
        
        OldCmdLine = String()
    
        UseOldParams = Boolean()
    
        OldParams = vbObjectInitialize(objtype=String)
    
        #p = Variant()
    
        UsedParNr = 0 #Long()
    
        Nr = 0 #Long()
    
        UsedArgNr = 0 #Long()
    
        SelectValues = [] #Variant()
    
        #c1 = Variant()
    
        minIndex = Integer()
    
        minControl = Variant()
        
        self.title = M09.Get_Language_Str('Parametereingabe der \'') + Name + M09.Get_Language_Str('\' Funktion')
        
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)

        self.top.grab_set()
        
        self.top.resizable(True, True)  # This code helps to disable windows from resizing
        
        window_height = 700
        window_width = 500
        
        winfo_x = PG.global_controller.winfo_x()
        winfo_y = PG.global_controller.winfo_y()
        
        screen_width = PG.global_controller.winfo_width()
        screen_height = PG.global_controller.winfo_height()
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
        
        #self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))                 
        self.top.geometry("+{}+{}".format(x_cordinate, y_cordinate))                 
               
        if len(self.title) > 0: 
            self.top.title(self.title)
            
        self.FuncName = Name
        self.Show_Channel_Type = Show_Channel
        #Const CNames = "Val0 Val1 Period Duration Timeout DstVar MinTime MaxTime Par1"
        
        if Description == '':
            Description = M09.Get_Language_Str('Noch keine Beschreibung zur Funktion \'') + Name + M09.Get_Language_Str('\' vorhanden ;-(')
        
        self.Description_TextBox = ttk.Label(self.top, text=Description,font=self.default_font,wraplength=window_width-20,relief=tk.SUNKEN, borderwidth=1)
              
        self.Description_TextBox.focus_set()

        self.Description_TextBox.grid(row=0,column=0,columnspan=3,sticky="nesw",padx=10,pady=10)

        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.FuncName = Name
        self.Show_Channel_Type = Show_Channel
        #Const CNames = "Val0 Val1 Period Duration Timeout DstVar MinTime MaxTime Par1"

        #self.Caption = M09.Get_Language_Str('Parametereingabe der \'') + Name + M09.Get_Language_Str('\' Funktion')
        #Debug.Print                         ' Debug
        #Debug.Print Name & " (" & Par & ")" ' Debug
        #*** Hide all entrys in the dialog which are not needed ***
        self.ParList = Split(Par, ',')
        # Hide CX selection if it's not used
        if not M30.Is_Contained_in_Array('Cx', self.ParList) and not M30.Is_Contained_in_Array('B_LED_Cx', self.ParList):
            pass
            #Hide_and_Move_up(Me, 'LED_Kanal_Frame', 'Par1')
        else:
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    # On the other hand it's o.K. if the PushButton function could use more than one LED,
    # => It's enabled again

            OptionButton_12 = OptionButton_23 = OptionButton_All = OptionButton_C1 = True
            if (LedChannels == - 1):
                OptionButton_All = False
                OptionButton_12 = False
                OptionButton_23 = False
                OptionButton_C1 = True
            elif (LedChannels == - 2):
                OptionButton_All = False
                OptionButton_C1 = True
            elif (LedChannels == 2):
                OptionButton_All = False
                if True: #OptionButton_All:
                    OptionButton_23 = True
           
            self.LED_Kanal_Frame = ttk.Frame(self.top,relief=tk.RIDGE, borderwidth=1)
            self.LED_Kanal_Frame_Caption = ttk.Label(self.top, text=M09.Get_Language_Str("LED Kanal Auswahl"),font=self.default_font)
            self.LED_Kanal_Frame_Caption.grid(row=1,column=0)
            
            self.RB_Option_Button_var = tk.StringVar()
            self.RB_Option_Button_var.set(1)
            
            if OptionButton_All:
                self.radiobtn1_txt = "Alle"
                self.RB_OptionButton_All = tk.Radiobutton(self.LED_Kanal_Frame, text=self.radiobtn1_txt, variable=self.RB_Option_Button_var, value=1)
                self.RB_OptionButton_All.grid(row=1,column=0,sticky="w",padx=10,pady=10)
            if OptionButton_12:
                self.radiobtn2_txt = "1&2 / Gelb"
                self.RB_OptionButton_12 = tk.Radiobutton(self.LED_Kanal_Frame, text=self.radiobtn2_txt, variable=self.RB_Option_Button_var, value=2)
                self.RB_OptionButton_12.grid(row=2,column=0,sticky="w",padx=10,pady=10)
            if OptionButton_23:
                self.radiobtn3_txt = "2&3/ Zyan"
                self.RB_OptionButton_23 = tk.Radiobutton(self.LED_Kanal_Frame, text=self.radiobtn3_txt, variable=self.RB_Option_Button_var, value=3) 
                self.RB_OptionButton_23.grid(row=3,column=0,sticky="w",padx=10,pady=10)
            if OptionButton_C1:
                self.radiobtn4_txt = "1 / Rot"
                self.radiobtn5_txt = "2 / Grün"
                self.radiobtn6_txt = "3 / Blau"        
                self.RB_OptionButton_1 = tk.Radiobutton(self.LED_Kanal_Frame, text=self.radiobtn4_txt, variable=self.RB_Option_Button_var, value=4)
                self.RB_OptionButton_2 = tk.Radiobutton(self.LED_Kanal_Frame, text=self.radiobtn5_txt, variable=self.RB_Option_Button_var, value=5)
                self.RB_OptionButton_3 = tk.Radiobutton(self.LED_Kanal_Frame, text=self.radiobtn6_txt, variable=self.RB_Option_Button_var, value=6) 
                self.RB_OptionButton_1.grid(row=1,column=1,sticky="w",padx=10,pady=10)
                self.RB_OptionButton_2.grid(row=2,column=1,sticky="w",padx=10,pady=10)
                self.RB_OptionButton_3.grid(row=3,column=1,sticky="w",padx=10,pady=10)
                
            self.LED_Kanal_Frame.grid(row=2,column=0,columnspan=2,sticky="w",padx=10,pady=10)
                
            
        OldCmdLine = P01.Cells(P01.ActiveCell().Row, M25.Config__Col)
        
        if Len(OldCmdLine) > Len(Name) and Left(OldCmdLine, Len(Name) + 1) == Name + '(':
            UseOldParams = True
            OldParams = Split(Trim(Replace(Mid(OldCmdLine, Len(Name) + 2), ')', '')), ',')
            
        # show LED Channel textbox    
        #LED_Channel_TextBox.Visible = Show_Channel != M10.CHAN_TYPE_NONE
        LED_Channel_TextBox_Visible = Show_Channel != M10.CHAN_TYPE_NONE
        LED_Channel_Label_Visible = LED_Channel_TextBox_Visible
        
        if LED_Channel_TextBox_Visible:
        
            self.LED_Channel_Label_txt = "LED Channel"
            self.LED_Channel_TextBox_svar = tk.StringVar(self.controller)
            self.LED_Channel_TextBox_svar.set("1")
            self.LED_Channel_TextBox = tk.Entry(self.top,width=4,textvariable=self.LED_Channel_TextBox_svar)
            self.LED_Channel_Label = ttk.Label(self.top, text=self.LED_Channel_Label_txt,wraplength=window_width,font=self.default_font)
            self.LED_Channel_TextBox.grid(row=5,column=0,sticky="w",padx=10,pady=10)
            self.LED_Channel_Label.grid(row=5,column=1,sticky="w",padx=10,pady=10)
            
            if Show_Channel == M10.CHAN_TYPE_SERIAL:
                self.LED_Channel_TextBox_svar.set(str(LED_Channel))
                self.LED_Channel_Label.configure(text= M09.Get_Language_Str('Sound Kanal'))
            elif Show_Channel == M10.CHAN_TYPE_LED:
                if UseOldParams:
                    self.LED_Channel_TextBox_svar.set(str(LED_Channel))
                else:
                    self.LED_Channel_TextBox_svar.set(str(Def_Channel))
                
        # Add parameters
        else:
            self.LED_Channel_TextBox_svar = None
        
        self.Param_Frame = ttk.Frame(self.top)

        for p in self.ParList:
            p = Trim(p)
            if Left(p, 1) != '#' and InStr(' Cx B_LED_Cx ', ' ' + p + ' ') == 0:
                if UsedParNr >= self.MAX_PAR_CNT:
                    P01.MsgBox('Internal error: The number of parameters is to large in Show_UserForm_Other()',vbCritical,"Internal Error")
                    M30.EndProg()
                ParVal = ''
                Typ, Min, Max, Def, Opt, InpTxt, Hint = M10.Get_Par_Data(p)
                if UseOldParams:
                    if (Typ == 'RGB'):
                        ParVal = self.Get_RGB_from_OldParams(OldParams, Nr, 3)
                        Nr = Nr + 2
                    elif (Typ == 'RGB2'):
                        ParVal = self.Get_RGB_from_OldParams(OldParams, Nr, 3) + '  ' + self.Get_RGB_from_OldParams(OldParams, Nr + 3, 3)
                        Nr = Nr + 5
                    else:
                        if Nr <= UBound(OldParams):
                            ParVal = OldParams(Nr)
                            # 20.05.20: Added if()... to prevent crash if the number of parameters have been changed in a new version of the library  ' 07.06.20: Old "<" => "<="
                ParVal = Trim(ParVal)
                self.TypA[UsedParNr] = Typ
                self.MinA[UsedParNr] = Min
                self.MaxA[UsedParNr] = Max
                self.ParName[UsedParNr] = p
                UsedParNr = UsedParNr + 1
                #if OK_Button is self.ActiveControl:
                #    self.Controls('Par' + UsedParNr).setFocus()
                SelectValues = None
                
                self.Controls['Par' + str(UsedParNr)] = ParVal
                w = self.DEFAULT_PAR_WIDTH
                if Opt != '':
                    for OptionValue in Split(Opt, ';'):
                        OptionValue = Trim(OptionValue)
                        if ( LCase(Left(OptionValue, 7)) == 'values:' ) :
                            SelectValues = Trim(Mid(OptionValue, 8)).split(',')
                        else:
                            Opt = OptionValue
                            for o in Split(Opt, ' '):
                                Parts = Split(o, '=')
                                select_4 = Parts(0)
                                if (select_4 == 'w'):
                                    w = P01.val(Parts(1))
                                    #self.Controls['Par' + str(UsedParNr)].Width = w
                                    #with_5 = self.Controls('LabelPar' + str(UsedParNr))
                                    #with_5.Left = with_5.Left + w - self.DEFAULT_PAR_WIDTH
                                elif (select_4 == 'wn'):
                                    w = P01.val(Parts(1))
                                    #self.Controls['Par' + str(UsedParNr)].Width = w
                                elif (select_4 == 'Inv'):
                                    self.Invers[UsedParNr - 1] = True
                                    if ParVal == 0:
                                        ParVal = 1
                                    else:
                                        ParVal = 0
                                    self.Controls['Par' + str(UsedParNr)] = ParVal
                                elif (select_4 == '...') or (select_4 == '…'):
                                    if UseOldParams:
                                        for i in vbForRange(UsedParNr + 1, UBound(OldParams)):
                                            ParVal = ParVal + ', ' + Trim(OldParams(i))
                                        self.Controls['Par' + str(UsedParNr)] = ParVal
                                else:
                                    P01.MsgBox('Internal Error: Unknown option \'' + o + '\' in parameter \'' + InpTxt + '\' in sheet \'' + M02.PAR_DESCR_SH + '\'', vbCritical, 'Internal Error')
                                    M30.EndProg()
                #self.Controls['LabelPar' + str(UsedParNr)] = InpTxt
                #self.Controls['LabelPar' + str(UsedParNr)].ControlTipText = Hint
                #self.Controls['Par' + str(UsedParNr)].ControlTipText = Hint
                #self.Controls['Par' + UsedParNr + 'Select'].ControlTipText = Hint
                validListEntry = False
                if ( SelectValues ) :
                    pass
                    for SelectValue in SelectValues:
                        SelectValue = Trim(SelectValue)
                        if ( SelectValue != '' ) :
                            # Debug.Print (SelectValue)
                            if SelectValue == ParVal:
                                validListEntry = True
                            #with_6 = self.Controls['Par' + str(UsedParNr) + 'Select']
                            #with_6.AddItem(SelectValue)
                    #self.Controls['Par' + UsedParNr + 'Select'].Visible = True
                    #self.Controls['Par' + UsedParNr].Width = w
                    #self.Controls['Par' + UsedParNr].Left = 12
                    #self.Controls['Par' + UsedParNr + 'Select'].Left = 12 + w + 4
                    #self.Controls['Par' + UsedParNr + 'Select'].Width = w
                    #with_7 = self.Controls('LabelPar' + str(UsedParNr))
                    #with_7.Left = 12 + 2 * w + 8
                    #with_7.Width = 410 -  ( 12 + 2 * w + 8 )
                else:
                    #self.Controls['Par' + str(UsedParNr) + 'Select'].Visible = False
                    pass
                if ParVal == '':
                    ParVal = Def
                    validListEntry = True
                if (Typ == 'List'):
                    #self.Controls['Par' + UsedParNr + 'Select'].Style = 2
                    #self.Controls['Par' + UsedParNr].Enabled = False
                    if not validListEntry:
                        P01.MsgBox(Replace(Replace(Replace(M09.Get_Language_Str('Fehler: Der Parameter \'#1#\' hat einen ungültigen Wert #2#. Der Parameter wird auf den Standardwert #3# zurückgesetzt.'), '#1#', p), '#2#', ParVal), '#3#', Def), vbCritical, M09.Get_Language_Str('Parameter Fehler'))
                        ParVal = Def
                #if (Typ == "Logic"):
                #    Typ = "BigEntry"
                self.Controls['Par' + str(UsedParNr) + 'Select'] = ParVal
                self.Controls['Par' + str(UsedParNr)] = ParVal
                
                #*HL create widget
                row = UsedParNr
                column = 0
                paramkey = p
                param_title = InpTxt
                param_type = Typ
                param_min = Min
                param_max = Max
                param_default = ParVal
                titlerow = row
                titlecolumn = 1
                param_tooltip = Hint
                combo_value_list = SelectValues
                w_param_type = MLLtype2widgettype.get(param_type.Value, "String")
                #if param_type in ("Mode","Var","CmpMod","SheetName", "MB_LED"):
                #    param_type = "String"
                self.ParamVar[paramkey] = self.create_widget(self.Param_Frame, row, column, paramkey, param_title, w_param_type, param_min, param_max, param_default, titlerow, titlecolumn, param_tooltip,combo_value_list=combo_value_list)
                
            if ( p == 'Cx' or p == 'B_LED_Cx' ) :
                if UseOldParams:
                    self.Set_OptionButton(Trim(OldParams(Nr)), p == 'B_LED_Cx')
                else:
                    #OptionButton_C1.focus_set()
                    pass
            Nr = Nr + 1
            #Debug.Print "UsedParNr=" & UsedParNr ' Debug
            

        
        #Hide_and_Move_up(Me, 'Par' + UsedParNr + 1, 'Abort_Button')
        # set focus to first visible and enabeld control                          ' 09.10.21 Jürgen
        # VB2PY (UntranslatedCode) On Error Resume Next
        minIndex = 9999
        #OK_Button.setFocus()
        """
        for c1 in self.Controls:
            if c1.Visible and c1.TabIndex > 0 and not Left(c1.Name, 13) == 'OptionButton_':
                isTabStop = False
                isTabStop = c1.TabStop
                #If isTabStop And c1.TabIndex > 2 And c1.TabIndex < minIndex Then     ' 06.11.21 Jürgen  First par not selected
                if isTabStop and c1.TabIndex >= 2 and c1.TabIndex < minIndex:
                    minIndex = c1.TabIndex
                    minControl = c1
        if minIndex != 9999:
            minControl.setFocus()
        """
        # VB2PY (UntranslatedCode) On Error GoTo 0
        #Center_Form(Me)
        #hook at end of initialisation code, because if an error and exception thrown AFTER HookFormScroll Excel will crash soon      ' 09.10.21 Juergen
        #HookFormScroll(Me, 'Description_TextBox')
        #self.CurWidth = self.Width
        #self.CurHeight = self.Height
        #self.MinFormHeight = self.Height
        #self.MinFormWidth = self.Width
        #self.MakeFormResizable(Me)
        
        self.Param_Frame.grid(row=4,column=0,columnspan=3,padx=10,pady=10,sticky="w")
        
        self.button_frame = ttk.Frame(self.top)
        
        self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=self.default_font)
        self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=self.default_font)

        self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
        
        self.button_frame.grid(row=5,column=2,sticky="e",padx=10,pady=10)
        
        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)                   
        self.show()

   
    def Get_OptionButton_Res(self):
        fn_return_value = None
        val = String()
        
        res = self.RB_Option_Button_var.get()
        #------------------------------------------------
        if res == "1": #OptionButton_All:
            val = 'C_ALL'
        elif res == "4": #OptionButton_C1:
            val = 'C1'
        elif res == "5": #OptionButton_C2:
            val = 'C2'
        elif res == "6": #OptionButton_C3:
            val = 'C3'
        elif res == "2": #OptionButton_12:
            val = 'C12'
        elif res == "3": #OptionButton_23:
            val = 'C23'
        else:
            P01.MsgBox(M09.Get_Language_Str('LED Auswahl Fehler'), vbCritical,"Error")
        fn_return_value = val
        return fn_return_value
    
    def Set_OptionButton(self, val, Only_Single):
        #------------------------------------------------------------------
        if (val == 'C_ALL'):
            if Only_Single:
                #OptionButton_C1 = True
                self.RB_Option_Button_var.set(4)
                self.RB_OptionButton_1.focus_set()
            else:
                #OptionButton_All = True
                self.RB_Option_Button_var.set(1)
                self.RB_OptionButton_All.focus_set()
        elif (val == 'C1'):
            #OptionButton_C1 = True
            self.RB_Option_Button_var.set(4)
            self.RB_OptionButton_1.focus_set()            
        elif (val == 'C2'):
            #OptionButton_C2 = True
            self.RB_Option_Button_var.set(5)
            self.RB_OptionButton_2.focus_set()            
            #OptionButton_C2.setFocus()
        elif (val == 'C3'):
            #OptionButton_C3 = True
            self.RB_Option_Button_var.set(6)
            self.RB_OptionButton_3.focus_set()            
            #OptionButton_C3.setFocus()
        elif (val == 'C12'):
            if Only_Single:
                # OptionButton_C1 = True
                # OptionButton_C1.setFocus()
                self.RB_Option_Button_var.set(4)
                self.RB_OptionButton_1.focus_set()                    
            else:
                #OptionButton_12 = True
                #OptionButton_12.setFocus()
                self.RB_Option_Button_var.set(2)
                self.RB_OptionButton_12.focus_set()                    
        elif (val == 'C23'):
            if Only_Single:
                #OptionButton_C2 = True
                #OptionButton_C2.setFocus()
                self.RB_Option_Button_var.set(5)
                self.RB_OptionButton_2.focus_set()                   
            else:
                #OptionButton_23 = True
                #OptionButton_23.setFocus()
                self.RB_Option_Button_var.set(3)
                self.RB_OptionButton_23.focus_set()                       
        else:
            #OptionButton_All = True
            #OptionButton_All.setFocus()
            self.RB_Option_Button_var.set(1)
            self.RB_OptionButton_All.focus_set()            
            P01.MsgBox(M09.Get_Language_Str('Fehler beim Lesen der bestehenden Kanalbezeichnung \'') + val + '\'', vbCritical, M09.Get_Language_Str('Unbekannte Kanalbezeichnung'))
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Res - ByRef 
    def Create_Result(self):
        fn_return_value = ""
        p = Variant()
        #-------------------------------------------------------------
        # Return True if sucessfully checked all inputs
        Res = ''
        for p in self.ParList:
            val = 'Not Found'
            p = Trim(p)
            if Left(p, 1) == '#':
                val = p
            else:
                if p == 'Cx' or p == 'B_LED_Cx':
                    val = self.Get_OptionButton_Res()
                else:
                    for Nr in vbForRange(1, self.MAX_PAR_CNT):
                        if self.ParName(Nr - 1) == p:
                            val = self.Check_Par_with_ErrMsg(Nr, val)
                            if val == None:
                                #Controls('Par' + Nr).setFocus()
                                return fn_return_value
                            if self.Invers(Nr - 1):
                                if val == 0:
                                    val = 1
                                else:
                                    val = 0
                            break
            if val == 'Not Found':
                P01.MsgBox(M09.Get_Language_Str('Fehler der Parameter \'') + p + M09.Get_Language_Str('\' wurde nicht gefunden'), vbCritical, M09.Get_Language_Str('Programm Fehler'))
            Res = Res + str(val) + ', '
        Res = self.FuncName + '(' + M30.DelLast(Res, 2) + ')'
        if self.LED_Channel_TextBox_svar:
            if self.LED_Channel_TextBox_svar.get():
                Res = Res + '$' + self.LED_Channel_TextBox_svar.get()
        fn_return_value = Res
        return fn_return_value
    
    def Abort_Button_Click(self):
        #-------------------------------
        #self.UnhookFormScroll()
        self.UserForm_Res = ''
        #self.Store_Pos(Me, OtherForm_Pos)
        #Unload(Me)
    
    def OK_Button_Click(self):
        #----------------------------
        self.UserForm_Res = self.Create_Result()
        
        if self.UserForm_Res:
            #self.UnhookFormScroll()
            #self.Store_Pos(Me, OtherForm_Pos)
           # Unload(Me)
            return

