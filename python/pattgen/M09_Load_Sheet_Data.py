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


import proggen.Prog_Generator as PG

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

"""--------------------------------------------------

"""

__MLL_pcf_Version = Long()

def __Set_Cell(Desc, Val):
    c = Variant()

    RngStr = String()
    #--------------------------------------------------
    # Write val to the cell which matches the given Desc in the language sheet.
    for c in Range(PARAMETER_RANGE):
        if Trim(c) == Desc:
            c.offset[0, 1] = Val
            return
    RngStr = Find_Cell_Pos_by_Name(Desc)
    if RngStr != '':
        Range[RngStr].offset[0, 1] = Val
        return
    MsgBox(Replace(Get_Language_Str('Fehler beim laden der Konfiguration: Die Zelle \'#1#\' existiert nicht. Der Eintrag wird ignoriert.'), '#1#', Desc), vbCritical, Get_Language_Str('Unbekannter Eintrag in Konfigrationsdatei'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DescArray - ByVal 
def __Get_Cell(DescArray, GenError=True):
    fn_return_value = None
    c = Variant()

    Desc = Variant()

    DescStr = String()
    #-------------------------------------------------------------------------------------------
    if not IsArray(DescArray):
        DescArray = Array(DescArray)
    for Desc in DescArray:
        for c in Range(PARAMETER_RANGE):
            if Trim(c) == Desc:
                fn_return_value = c.offset(0, 1)
                return fn_return_value
            RngStr = Find_Cell_Pos_by_Name(Desc)
            if RngStr != '':
                fn_return_value = Range(RngStr).offset(0, 1)
                return fn_return_value
        DescStr = DescStr + ' \'' + Desc + '\' &'
    if GenError:
        MsgBox(Get_Language_Str('Error: \'') + Left(DescStr, Len(DescStr) - 1) + '\' ' + '\' ' + Get_Language_Str('not found in') + '\'Get_Cell()\'')
    return fn_return_value

def __Test_Get_Cell():
    #UT------------------------
    Debug.Print(__Get_Cell(Array('Analoges Überblend', 'Test')))

def __Del_Text_Box():
    o = Variant()
    #-------------------------
    for o in ActiveSheet.Shapes:
        if (o.Type == msoTextBox):
            #o.Select ' Debug
            o.Delete()

def __Clear_Sheet_Data():
    #-----------------------------
    with_0 = ActiveSheet
    with_0.Unprotect()
    # Set deault values
    __Set_Cell('Erste RGB LED:', '1')
    __Set_Cell('Startkanal der RGB LED:', 0)
    __Set_Cell('Schalter Nummer:', 'SI_1')
    __Set_Cell('Anzahl der Ausgabe Kanäle:', 2)
    __Set_Cell('Bits pro Wert:', 1)
    __Set_Cell('Wert Min:', 0)
    __Set_Cell('Wert Max:', 255)
    __Set_Cell('Wert ausgeschaltet:', 0)
    __Set_Cell('Mode:', 0)
    __Set_Cell('Analoges Überblenden:', 0)
    __Set_Cell('Goto Mode:', 0)
    __Set_Cell('Grafische Anzeige:', '')
    __Set_Cell('Spezial Mode:', '')
    __Set_Cell('RGB Modul Nummer:', '')
    __Set_Cell('Charlieplexing LED Zuordnung:', '')
    __Set_Cell('Analoge Eingänge: ', '')
    Set_RGB_LED_CheckBox(0)
    # Clear the LEDs table
    with_1 = with_0.Range(LEDsRANGE)
    with_1.ClearContents()
    with_2 = with_1.Interior
    with_2.Pattern = xlNone
    with_2.TintAndShade = 0
    with_2.PatternTintAndShade = 0
    with_3 = with_1.Font
    with_3.ColorIndex = xlAutomatic
    with_3.TintAndShade = 0
    __Del_Text_Box()
    Del_Analog_Trend_Objects()
    Delete_Shapes('M99O01')

def Create_New_Sheet(SheetName, Add_to_Duplicate_Name='_Copy_', AfterSheetName=VBMissingArgument):
    OrgName = String()

    AfterSheet = Worksheet()
    #---------------------------------------------------------------------------------------------------------------------------------------
    OrgName = SheetName
    SheetName = Unic_SheetName(SheetName, Add_to_Duplicate_Name)
    #ThisWorkbook.Activate                                                     ' 12.06.20: Prevent crash if prog. is started an other excel is open
    AfterSheet = Sheets(Sheets.Count)
    if SheetEx(OrgName):
        AfterSheet = Sheets(OrgName)
    if AfterSheetName != '':
        AfterSheet = Sheets(AfterSheetName)
    Sheets(MAIN_SH).Copy(After=AfterSheet)
    ThisWorkbook.Activate()
    ActiveSheet.Name = SheetName
    Sheets(MAIN_SH).Select()
    Range(FirstLEDTabRANGE).Select()
    Sheets(SheetName).Select()
    __Clear_Sheet_Data()
    Range[MacEnab_Rng] = ''

def Add_by_Hardi():
    #------------------------
    ActiveSheet.Shapes.AddLabel(msoTextOrientationHorizontal, 443, 0, 55, 5).Select()
    Selection.ShapeRange[1].TextFrame2.TextRange.Characters.Text = 'by Hardi'
    Selection.ShapeRange.TextFrame2.TextRange.Font.Fill.ForeColor.rgb = rgb(0, 0, 255)
    Selection.ShapeRange.Name = 'InternalTextBox'
    Selection.Placement = xlFreeFloating

def New_Sheet():
    CopyFormSheet = String()

    Name = String()
    #---------------------
    # Is called if the "Neues Blatt" Button is pressed
    select_1 = MsgBox(Get_Language_Str('Sollen die Einstellungen des aktuellen Blatts übernommen werden?'), vbYesNoCancel + vbQuestion, Get_Language_Str('Neues Blatt anlegen'))
    if (select_1 == vbCancel):
        return
    elif (select_1 == vbYes):
        CopyFormSheet = ActiveSheet.Name
    Name = InputBox(Get_Language_Str('Name des neuen Blattes?'), Get_Language_Str('Neues Blatt anlegen'), Unic_SheetName(CopyFormSheet, '_'))
    if Name != '':
        if CopyFormSheet != '':
            TempName = ThisWorkbook.Path + '/' + ExampleDir + '/TempExample.MLL_pcf'
            Save_One_Sheet(Sheets(CopyFormSheet), TempName, False, Unic_SheetName(Name, '_'))
            Load_Sheets(TempName, '', AfterSheetName=CopyFormSheet)
            __Translate_Standard_Description_Box()
            #           It should be "Description Message" to be translated
        else:
            Create_New_Sheet(Name, Add_to_Duplicate_Name='_', AfterSheetName=MAIN_SH)
            __Load_Textbox(StdDescEdges + Chr(pcfSep) + Get_Language_Str(StdDescStart), 'Description Message')
            Range[Macro_N_Rng] = Replace_Illegal_Char(ActiveSheet.Name)
            Add_by_Hardi()
        Range(FirstLEDTabRANGE).Select()
        Protect_Active_Sheet()

def __Translate_Standard_Description_Box():
    o = Variant()
    #---------------------------------------
    for o in ActiveSheet.Shapes:
        if (o.Type == msoTextBox):
            if o.Name == 'Description Message':
                # 21.01.20: Disabled If Get_ExcelLanguage() <> 0 Then ' Left(o.TextFrame.Characters.Text, Len(StdDescStart)) = StdDescStart Then
                WasProtected = ActiveSheet.ProtectContents
                if WasProtected:
                    ActiveSheet.Unprotect()
                o.Delete()
                __Load_Textbox(StdDescEdges + Chr(pcfSep) + Get_Language_Str(StdDescStart), 'Description Message')
                if WasProtected:
                    Protect_Active_Sheet()
                break
                #End If

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def __Translate_Standard_Description_Box_in_Sheet(Sh):
    o = Variant()
    #---------------------------------------------------------------------
    for o in Sh.Shapes:
        if (o.Type == msoTextBox):
            if o.Name == 'Description Message':
                # 21.01.20: Disabled If Get_ExcelLanguage() <> 0 Then ' Left(o.TextFrame.Characters.Text, Len(StdDescStart)) = StdDescStart Then
                WasProtected = Sh.ProtectContents
                if WasProtected:
                    Sh.Unprotect()
                o.Delete()
                OldSh = ActiveSheet.Name
                Sh.Select()
                __Load_Textbox(StdDescEdges + Chr(pcfSep) + Get_Language_Str(StdDescStart), 'Description Message')
                Sheets(OldSh).Select()
                if WasProtected:
                    Protect_Active_Sheet()
                break
                #End If

def __Test_Translate_Standard_Description_Box_in_Sheet():
    __Translate_Standard_Description_Box_in_Sheet(Sheets('Main'))

def __Load_Dauer_Tab(Line):
    c = Variant()

    i = Long()
    #-----------------------------------------
    for c in Split(Line, Chr(pcfSep)):
        Cells[Dauer_Row, Dauer_Col1 + i] = Replace(c, '~', Dauer_Row)
        i = i + 1

def __Load_GoTo_Tab(Line):
    c = Variant()

    i = Long()
    #----------------------------------------
    for c in Split(Line, Chr(pcfSep)):
        Cells[GoTo_Row, GoTo_Col1 + i] = c
        i = i + 1

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LTabNr - ByRef 
def __Load_LED_Tab(Line, LTabNr):
    #-------------------------------------------------------------
    with_4 = Range(FirstLEDTabRANGE)
    i = - 1
    for c in Split(Line, Chr(pcfSep)):
        if i != - 1 and c != '':
            with_4.offset[LTabNr, i] = c
        i = i + 1
    LTabNr = LTabNr + 1

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: attr - ByVal 
def __Set_Attrib(r, attr):
    a = Variant()
    #-------------------------------------------------------
    with_5 = r
    for a in Split(attr, ','):
        select_4 = Left(a, 1)
        if (select_4 == 'c'):
            with_5.Font.Color = Mid(a, 2)
        elif (select_4 == 'i'):
            with_5.Interior.Color = Mid(a, 2)
        elif (select_4 == 'B'):
            with_5.Font.Bold = True
        elif (select_4 == 'I'):
            with_5.Font.Italic = True
        elif (select_4 == 'U'):
            with_5.Font.Underline = Mid(a, 2)
        elif (select_4 == 'W'):
            with_5.WrapText = True
        elif (select_4 == 'O'):
            with_5.Orientation = Val(Mid(a, 2))
        else:
            MsgBox('Error: Unknown attribut: \'' + a + '\'')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LAttNr - ByRef 
def __Load_LED_Att(Line, LAttNr):
    #-------------------------------------------------------------
    with_6 = Range(FirstLEDTabRANGE)
    i = - 2
    for c in Split(Line, Chr(pcfSep)):
        if i == - 1:
            with_6.offset[LAttNr, 0].EntireRow.RowHeight = NrStr2d(c)
        if i >= 0 and c != '':
            __Set_Attrib(with_6.offset(LAttNr, i), c)
        i = i + 1
    LAttNr = LAttNr + 1

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def __Load_Textbox(Line, Name='', LanguageNr=- 2):
    Params = vbObjectInitialize(objtype=String)

    Edges = vbObjectInitialize(objtype=String)

    Line2 = String()

    Parts = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------------------------------------------------
    # Special values for "LanguageNr"
    # -1 = Old file without language number
    # -2 = Todo
    Params = Split(Line, Chr(pcfSep))
    Edges = Split(CorrectKomma(Params(0)), ';')
    Line2 = Mid(Line, Len(Params(0)) + 2)
    Line2 = Replace(Line2, '{Attrib}', Chr(1))
    Parts = Split(Line2, Chr(1))
    ActiveSheet.Shapes.AddLabel(msoTextOrientationHorizontal, Val(Edges(0)), __Correct_Top_Pos_by_Version(Val(Edges(1))), Val(Edges(2)), Val(Edges(3))).Select()
    Selection.Placement = xlFreeFloating
    Selection.ShapeRange[1].TextFrame2.TextRange.Characters.Text = Replace(Replace(Parts(0), '| ', '|'), '|', vbLf)
    if Name != '':
        Selection.ShapeRange[1].Name = Name
    if UBound(Parts) == 1:
        for c in Split(Parts(1), ' '):
            select_5 = Left(c, 1)
            if (select_5 == 'B') or (select_5 == 'F'):
                Par = Split(Mid(c, 2), ',')
                Start = Val(Par(0))
                Lenghth = Val(Par(1)) - Val(Par(0)) + 1
                select_6 = Left(c, 1)
                if (select_6 == 'B'):
                    Selection.ShapeRange[1].TextFrame2.TextRange.Characters[Start, Lenghth].Font.Bold = msoTrue
                elif (select_6 == 'F'):
                    Selection.ShapeRange[1].TextFrame2.TextRange.Characters[Start, Lenghth].Font.Fill.ForeColor.rgb = Par(2)
    if LanguageNr >= 0:
        Selection.ShapeRange[1].AlternativeText = 'Language: ' + LanguageNr
        if Get_ExcelLanguage() != LanguageNr:
            Selection.ShapeRange[1].Visible = False

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: RotPos - ByRef 
def __Show_Rotating_Status(message, RotPos):
    RotatingChr = '-\\|/'
    #-------------------------------------------------------------------
    if RotPos > 4 or RotPos < 1:
        RotPos = 1
    Application.StatusBar = message + Mid(RotatingChr, RotPos, 1)
    RotPos = RotPos + 1
    Sleep(100)
    DoEvents()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def __Load_msoFormControl(Line, LanguageNr=- 2):
    Params = vbObjectInitialize(objtype=String)

    Edges = vbObjectInitialize(objtype=String)

    Init_Proc = String()
    #---------------------------------------------------------------------------------
    # Load Button
    Params = Split(Line, Chr(pcfSep))
    if InStr(Params(2), 'Update_Grafik') > 0 or InStr(Params(2), 'New_Sheet') > 0:
        return
        # Skip buttons which have been added by a wrong program  13.02.20:
    Edges = Split(CorrectKomma(Params(0)), ';')
    ActiveSheet.Buttons.Add(Val(Edges(0)), __Correct_Top_Pos_by_Version(Val(Edges(1))), Val(Edges(2)), Val(Edges(3))).Select()
    Selection.Characters.Text = Params(1)
    Selection.OnAction = Params(2)
    Init_Proc = Params(2) + '_Init'
    if LanguageNr >= 0:
        Selection.ShapeRange[1].AlternativeText = 'Language: ' + LanguageNr
        if Get_ExcelLanguage() != LanguageNr:
            Selection.Visible = False
    #Button_Init_Proc_Finished = False
    #Dim OldStatus As String, OldEvents As Boolean
    #OldStatus = Application.StatusBar
    #OldEvents = Application.EnableEvents
    #Application.OnTime Now, Init_Proc
    #Application.EnableEvents = True
    #Dim message As String, RotPos As Integer
    #message = Get_Language_Str("Warte auf '") & Init_Proc & "'"
    #While Not Button_Init_Proc_Finished
    #   Show_Rotating_Status message, RotPos
    #Wend
    #Application.StatusBar = OldStatus
    #Application.EnableEvents = OldEvents
    Application.Run(Init_Proc)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Top - ByVal 
def __Correct_Top_Pos_by_Version(Top):
    fn_return_value = None
    #-----------------------------------------------------
    # Correct the position of elemets which are stored with an old version
    fn_return_value = Top
    if __MLL_pcf_Version == 0:
        if Top > 160:
            fn_return_value = Top + 31.2
    return fn_return_value

def Load_Picture(Line, SourceDir):
    Params = vbObjectInitialize(objtype=String)

    Edges = vbObjectInitialize(objtype=String)

    PicName = String()
    #-----------------------------------------------------------
    Params = Split(Line, Chr(pcfSep))
    Edges = Split(CorrectKomma(Params(0)), ';')
    PicName = SourceDir + Params(1)
    if Dir(PicName) == '':
        SecondDir = ThisWorkbook.Path + '/' + ExampleDir + '/'
        PicName = SecondDir + Params(1)
        if UCase(SecondDir) != UCase(SourceDir):
            SecondDir = vbCr + '  ' + SecondDir
        else:
            SecondDir = ''
        if Dir(PicName) == '':
            MsgBox(Get_Language_Str('Fehler: Das Bild \'') + Params(1) + Get_Language_Str('\' existiert nicht in folgenen Verzeichnissen:') + vbCr + '  ' + SourceDir + SecondDir, vbCritical, Get_Language_Str('Bild nicht gefunden'))
            return
    Global_Worksheet_Change(Cells(1, 1))
    # VB2PY (UntranslatedCode) On Error GoTo LoadError
    ActiveSheet.Shapes.AddPicture(PicName, linktofile= msoFalse, savewithdocument= msoCTrue, Left= Val(Edges(0)), Top= __Correct_Top_Pos_by_Version(Val(Edges(1))), Width= Val(Edges(2)), Height= Val(Edges(3))).Select()
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Selection.Name = NoExt(Params(1))
    Selection.Placement = xlMove
    #  Selection.ShapeRange.PictureFormat.TransparentBackground = msoTrue        ' Added by Misha 29-6-2020.
    #  Selection.ShapeRange.PictureFormat.TransparencyColor = rgb(255, 0, 0)     ' Added by Misha 29-6-2020. RED is Transparant Color
    #  Selection.ShapeRange.Fill.Visible = msoFalse                              ' Added by Misha 29-6-2020.
    return
    MsgBox(Get_Language_Str('Fehler beim laden des Bildes: ') + '\'' + PicName + '\'', vbCritical, Get_Language_Str('Fehler'))

def __Set_Defaults_for_Sheet():
    #-----------------------------------
    # The Cell positions are searched the Language sheet => It's independant from the current language
    if __Get_Cell('Grafische Anzeige:') == '' and __Get_Cell(Array('Analoges Überblenden:', 'Analoges Überblenden'), False) != '':
        __Set_Cell('Grafische Anzeige:', 1)
    Range('RGB_Modul_Nr').ClearContents()
    Hide_Show_GotoLines_If_Enabled()
    Hide_Show_Special_ModeLines_If_Enabled()
    Add_by_Hardi()
    ActiveWindow.DisplayHeadings = False
    if __Get_Cell('Grafische Anzeige:') != '':
        ## VB2PY (CheckDirective) VB directive took path 1 on True
        Update_Grafik_from_Str(__Get_Cell('Grafische Anzeige:'))
    Hide_Show_Check_Goto_Activation()

def Set_RGB_LED_CheckBox(Value):
    OldEvents = Boolean()

    Oldupdating = Boolean()
    #------------------------------------------------
    OldEvents = Application.EnableEvents
    Application.EnableEvents = False
    #OldUpdating = Application.ScreenUpdating
    ActiveSheet.RGB_LED_CheckBox.Enabled = False
    ActiveSheet.RGB_LED_CheckBox.Value = ( Value > 0 )
    ActiveSheet.RGB_LED_CheckBox.Enabled = True
    Application.EnableEvents = OldEvents
    #Application.ScreenUpdating = OldUpdating ' Is enabled when the CheckBox is changed

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Loaded_Sheets - ByRef 
def Load_Sheets(SourceName, Loaded_Sheets, AfterSheetName=VBMissingArgument):
    FileNr = Integer()

    OldSheet = Worksheet()

    AddedSheets = Long()

    SrcPath = String()

    SourceDir = String()

    Line = String()

    LNr = Long()

    LTabNr = Long()

    LAttNr = Long()

    ScrUpd = Boolean()

    FinishPrevious = Boolean()

    SkipSheet = Boolean()
    #-------------------------------------------------------------------------------------------------------------
    OldSheet = ActiveSheet
    Application.EnableEvents = False
    FileNr = FreeFile()
    if Dir(SourceName) == '':
        MsgBox(Get_Language_Str('Fehler: Die Datei \'') + SourceName + '\' ' + Get_Language_Str('existiert nicht.'), vbCritical, Get_Language_Str('Fehler'))
        return
    SourceDir = FilePath(SourceName)
    VBFiles.openFile(FileNr, SourceName, 'r') 
    #FirstSheet = True
    LNr = 0
    ScrUpd = Application.ScreenUpdating
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    while not EOF(FileNr):
        LNr = LNr + 1
        Line = VBFiles.getLineInput(FileNr, 1)
        Line = Replace(Line, vbTab, Chr(pcfSep))
        if Line != '':
            Tokens = Split(Line, Chr(pcfSep))
            if SkipSheet == False or Tokens(0) == 'SheetName':
                select_7 = Tokens(0)
                if (select_7 == ''):
                    pass
                elif (select_7 == 'SheetName'):
                    if FinishPrevious and not SkipSheet:
                        __Set_Defaults_for_Sheet()
                        Protect_Active_Sheet()
                        FinishPrevious = False
                    StatusMsg_UserForm.Set_ActSheet_Label(Get_Language_Str('Lade ') + ': ' + Tokens(1))
                    if InStr(vbTab + Loaded_Sheets, vbTab + Tokens(1) + vbTab) > 0:
                        SkipSheet = True
                    else:
                        Loaded_Sheets = Loaded_Sheets + Tokens(1) + vbTab
                        SkipSheet = False
                        if AfterSheetName == '<<LASTSHEET>>':
                            AfterSheetName = Sheets(Sheets.Count).Name
                            # 14.06.20:
                        Create_New_Sheet(Tokens(1), AfterSheetName=AfterSheetName)
                        LTabNr = 0
                        LAttNr = 0
                        AddedSheets = AddedSheets + 1
                        FinishPrevious = True
                elif (select_7 == 'Dauer'):
                    __Load_Dauer_Tab(Mid(Line, Len(Tokens(0)) + 2))
                elif (select_7 == 'Version'):
                    __MLL_pcf_Version = Val(Tokens(1))
                elif (select_7 == 'Goto Tabelle'):
                    __Load_GoTo_Tab(Mid(Line, Len(Tokens(0)) + 2))
                elif (select_7 == 'LED_Tab'):
                    __Load_LED_Tab(Line, LTabNr)
                elif (select_7 == 'LED_Attr'):
                    __Load_LED_Att(Line, LAttNr)
                elif (select_7 == 'Analoges Überblenden'):
                    __Set_Cell('Analoges Überblenden:', Tokens(1))
                elif (select_7 == 'msoTextBox'):
                    __Load_Textbox(Mid(Line, Len(Tokens(0)) + 2), LanguageNr=- 1)
                elif (select_7 == 'msoFormControl'):
                    __Load_msoFormControl(Mid(Line, Len(Tokens(0)) + 2), LanguageNr=- 1)
                elif (select_7 == 'msoPicture'):
                    Load_Picture(Mid(Line, Len(Tokens(0)) + 2), SourceDir)
                elif (select_7 == 'msoShapeOval'):
                    Load_msoShapeOval(Tokens(1), Tokens(2))
                elif (select_7 == 'RGB_LED_CheckBox'):
                    Set_RGB_LED_CheckBox(Val(Tokens(1)))
                else:
                    if Left(Tokens(0), Len('msoTextBox')) == 'msoTextBox':
                        LanguageNr = Val(Mid(Tokens(0), Len('msoTextBox') + 1))
                        __Load_Textbox(Mid(Line, Len(Tokens(0)) + 2), LanguageNr=LanguageNr)
                    elif Left(Tokens(0), Len('msoFormControl')) == 'msoFormControl':
                        LanguageNr = Val(Mid(Tokens(0), Len('msoFormControl') + 1))
                        __Load_msoFormControl(Mid(Line, Len(Tokens(0)) + 2), LanguageNr=LanguageNr)
                    else:
                        __Set_Cell(Trim(Tokens(0)), Tokens(1))
    # All sheets loade
    if FinishPrevious:
        __Set_Defaults_for_Sheet()
        Protect_Active_Sheet()
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
    Calculate()
    Application.ScreenUpdating = ScrUpd
    VBFiles.closeFile(FileNr)
    if AddedSheets > 1:
        OldSheet.Activate()

def __Test_Examples_UserForm():
    #UT---------------------------------
    Debug.Print('Result=' + Examples_UserForm.Show_Dialog)

def Load_AllExamples_Sheets():
    fn_return_value = None
    ExampleList = String()
    #---------------------------------------------------
    Application.Calculation = xlCalculationAutomatic
    ExampleList = Examples_UserForm.Show_Dialog()
    ThisWorkbook.Activate()
    if ExampleList != '':
        StatusMsg_UserForm.Show()
        Application.StatusBar = Get_Language_Str('Lade Beispielseiten...')
        for Example in Split(ExampleList, vbTab):
            Load_Sheets(ThisWorkbook.Path + '/' + ExampleDir + '/' + Example + '.MLL_pcf', Loaded_Sheets, '<<LASTSHEET>>')
        if Left(Application.StatusBar, Len(Get_Language_Str('Lade Beispielseiten...'))) == Get_Language_Str('Lade Beispielseiten...'):
            Application.StatusBar = Get_Language_Str('Beispiele geladen')
        fn_return_value = True
        Unload(StatusMsg_UserForm)
    Application.Calculation = xlCalculationAutomatic
    return fn_return_value

def Is_Normal_Data_Sheet(Name, Txt):
    fn_return_value = None
    #-----------------------------------------------------------------------------
    if ThisWorkbook.Sheets(Name).Visible == False:
        return fn_return_value
        # 11.01.20:
    if Name != MAIN_SH and Name != LANGUAGES_SH and Name != GOTO_ACTIVATION_SH and Name != PAR_DESCRIPTION_SH and Name != SPECIAL_MODEDLG_SH:
        fn_return_value = True
        # Additional savety check in case a new sheet has been added which is not listed above
        ## VB2PY (CheckDirective) VB directive took path 1 on True
        CheckCell = 'A1'
        if ThisWorkbook.Sheets(Name).Range(CheckCell) != CheckStr:
            select_8 = MsgBox(Get_Language_Str('Achtung: Soll die Seite \'') + Name + '\' ' + Txt + Get_Language_Str(' werden?'), vbQuestion + vbYesNoCancel, Get_Language_Str('Unbekannte Seite entdeckt'))
            if (select_8 == vbNo):
                fn_return_value = False
            elif (select_8 == vbCancel):
                EndProg()
    return fn_return_value

def Del_All_Sheets_Excep_Main():
    Sh = Variant()
    #-------------------------------------
    Application.Calculation = xlCalculationManual
    for Sh in ThisWorkbook.Sheets:
        if Is_Normal_Data_Sheet(Sh.Name, Get_Language_Str('gelöscht')):
            Application.DisplayAlerts = False
            Sheets(Sh.Name).Delete()
            Application.DisplayAlerts = True
    Application.Calculation = xlCalculationAutomatic

def Del_All_Sheets_which_contain_Copy_in_their_Name():
    Sh = Variant()

    OldSheet = Worksheet()
    #-----------------------------------------------------------
    OldSheet = ActiveSheet
    Application.Calculation = xlCalculationManual
    for Sh in ThisWorkbook.Sheets:
        if InStr(Sh.Name, '_Copy_'):
            Application.DisplayAlerts = False
            Sheets(Sh.Name).Delete()
            Application.DisplayAlerts = True
    Application.Calculation = xlCalculationAutomatic
    # VB2PY (UntranslatedCode) On Error Resume Next
    OldSheet.Activate()
    # VB2PY (UntranslatedCode) On Error GoTo 0

def __Test_Load_One_Sheet():
    #UT------------------------------
    Application.Calculation = xlCalculationAutomatic
    Load_Sheets(ThisWorkbook.Path + '/' + ExampleDir + '/TestExample.MLL_pcf', '', AfterSheetName=MAIN_SH)
    Application.Calculation = xlCalculationAutomatic

# VB2PY (UntranslatedCode) Option Explicit
