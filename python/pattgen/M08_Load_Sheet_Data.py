from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M09_Language as M09
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M03_Analog_Trend
import pattgen.M80_Multiplexer_INI_Handling
import pattgen.M30_Tools as M30
import pattgen.M07_Save_Sheet_Data
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M02_Main as M02a
import pattgen.M06_Goto_Graph
import pattgen.D00_Forms as D00
import mlpyproggen.Pattern_Generator as PG

import pgcommon.G00_common as G00

"""--------------------------------------------------
-------------------------------------------------------------------------------------------
UT------------------------
-------------------------
-----------------------------
---------------------------------------------------------------------------------------------------------------------------------------
------------------------
---------------------
---------------------------------------
---------------------------------------------------------------------
-----------------------------------------
----------------------------------------
-------------------------------------------------------------
-------------------------------------------------------
-------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------
---------------------------------------------------------------------------------
-----------------------------------------------------
-----------------------------------------------------------
-----------------------------------
------------------------------------------------
-------------------------------------------------------------------------------------------------------------
UT---------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on 1
 09.06.20:
---------------------------------------------------
-----------------------------------------------------------------------------
-------------------------------------
-----------------------------------------------------------
UT------------------------------
"""

MLL_pcf_Version = Long()

def Set_Cell(Desc, Val):
    c = Variant()

    RngStr = String()
    #--------------------------------------------------
    # Write val to the cell which matches the given Desc in the language sheet.
    for c in X02.Range(M01.PARAMETER_RANGE):
        if Trim(c) == Desc:
            c.offset(0, 1).Value = Val
            return
    RngStr = M09.Find_Cell_Pos_by_Name(Desc)
    if RngStr != '':
        X02.Range(RngStr).offset(0,1).Value = Val
        return
    X02.MsgBox(Replace(pattgen.M09_Language.Get_Language_Str('Fehler beim laden der Konfiguration: Die Zelle \'#1#\' existiert nicht. Der Eintrag wird ignoriert.'), '#1#', Desc), vbCritical, pattgen.M09_Language.Get_Language_Str('Unbekannter Eintrag in Konfigrationsdatei'))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DescArray - ByVal 
def Get_Cell(DescArray, GenError=True):
    _fn_return_value = None
    c = Variant()

    Desc = Variant()

    DescStr = String()
    #-------------------------------------------------------------------------------------------
    if not IsArray(DescArray):
        DescArray = Array(DescArray)
    for Desc in DescArray:
        for c in X02.Range(M01.PARAMETER_RANGE):
            if Trim(c) == Desc:
                _fn_return_value = c.offset(0, 1)
                return _fn_return_value
        RngStr = M09.Find_Cell_Pos_by_Name(Desc)
        if RngStr != '':
            _fn_return_value = X02.Range(RngStr).offset(0, 1)
            return _fn_return_value
        DescStr = DescStr + ' \'' + Desc + '\' &'
    if GenError:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Error: \'') + Left(DescStr, Len(DescStr) - 1) + '\' ' + '\' ' + pattgen.M09_Language.Get_Language_Str('not found in') + '\'Get_Cell()\'')
    return _fn_return_value

def Test_Get_Cell():
    #UT------------------------
    Debug.Print(Get_Cell(Array('Analoges Überblend', 'Test')))

def Del_Text_Box():
    o = Variant()
    #-------------------------
    for o in X02.ActiveSheet.Shapes:
        _select7 = o.Type
        #*HL if (_select7 == X01.msoTextBox):
        if (_select7 == X01.msoOLEControlObject and o.Name=="TextBox1"):
            # 17: TextBox
            #o.Select
            # Debug
            o.Delete()

def Clear_Sheet_Data():
    #-----------------------------
    _with19 = X02.ActiveSheet
    _with19.Unprotect()
    # Set deault values
    Set_Cell('Erste RGB LED:', '1')
    # The Cell position is searched the Language sheet => It's independant from the current language
    Set_Cell('Startkanal der RGB LED:', 0)
    Set_Cell('Schalter Nummer:', 'SI_1')
    Set_Cell('Anzahl der Ausgabe Kanäle:', 2)
    Set_Cell('Bits pro Wert:', 1)
    Set_Cell('Wert Min:', 0)
    Set_Cell('Wert Max:', 255)
    Set_Cell('Wert ausgeschaltet:', 0)
    Set_Cell('Mode:', 0)
    Set_Cell('Analoges Überblenden:', 0)
    Set_Cell('Goto Mode:', 0)
    Set_Cell('Grafische Anzeige:', '')
    Set_Cell('Spezial Mode:', '')
    Set_Cell('RGB Modul Nummer:', '')
    Set_Cell('Charlieplexing LED Zuordnung:', '')
    Set_Cell('Analoge Eingänge: ', '')
    Set_RGB_LED_CheckBox(0)
    # 13.06.20:
    # Clear the LEDs table
    _with20 = _with19.Range(M01.LEDsRANGE)
    _with20.ClearContents()
    _with21 = _with20.Interior
    _with21.Pattern = X01.xlNone
    _with21.TintAndShade = 0
    _with21.PatternTintAndShade = 0
    _with22 = _with20.Font
    _with22.ColorIndex = X01.xlAutomatic
    _with22.TintAndShade = 0
    Del_Text_Box()
    pattgen.M03_Analog_Trend.Del_Analog_Trend_Objects()
    pattgen.M80_Multiplexer_INI_Handling.Delete_Shapes('M99O01')
    # Delete the existing LEDs
    # 09.07.20:

def Create_New_Sheet(SheetName, Add_to_Duplicate_Name='_Copy_', AfterSheetName=VBMissingArgument):
    OrgName = String()

    AfterSheet = X02.Worksheet()
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
    AfterSheet="Main" #*HL
    X02.Sheets(M01.MAIN_SH).Copy(SheetName=SheetName,After=AfterSheet)
    PG.ThisWorkbook.Activate()
    #X02.ActiveSheet.Name = SheetName
    X02.Sheets(M01.MAIN_SH).Select()
    # For some reasons the "Akualisieren" Button gets selected after the "Sheets(MAIN_SH).Copy" command above.
    X02.Range(M01.FirstLEDTabRANGE).Select()
    # This generates later problems because the sheet is protected and the Button shouldent be selected. ?!?
    X02.Sheets(SheetName).Select()
    # I love Excel ...
    Clear_Sheet_Data()
    X02.Range(M01.MacEnab_Rng).Value = ''

def Add_by_Hardi():
   
    #------------------------
    X02.ActiveSheet.Shapes.AddLabel(X01.msoTextOrientationHorizontal, 443*X02.guifactor, 0, 55*X02.guifactor, 5*X02.guifactor).Select()
    X02.Selection.ShapeRange[1].TextFrame2.TextRange.Characters.Text = 'by Hardi'
    X02.Selection.ShapeRange[1].TextFrame2.TextRange.Font.Fill.ForeColor.rgb = rgb(0, 0, 255)
    X02.Selection.ShapeRange[1].Name = 'InternalTextBox'
    X02.Selection.Placement = X01.xlFreeFloating

def New_Sheet():
    CopyFormSheet = String()

    Name = String()
    #---------------------
    # Is called if the "Neues Blatt" Button is pressed
    _select8 = X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Sollen die Einstellungen des aktuellen Blatts übernommen werden?'), vbYesNoCancel + vbQuestion, pattgen.M09_Language.Get_Language_Str('Neues Blatt anlegen'))
    if (_select8 == vbCancel):
        return
    elif (_select8 == vbYes):
        CopyFormSheet = X02.ActiveSheet.Name
    Name = G00.InputBox(pattgen.M09_Language.Get_Language_Str('Name des neuen Blattes?'), pattgen.M09_Language.Get_Language_Str('Neues Blatt anlegen'), M30.Unic_SheetName(CopyFormSheet, '_'))
    if Name != '':
        if CopyFormSheet != '':
            TempName = PG.ThisWorkbook.Path + '\\' + M01.ExampleDir + '\\TempExample.MLL_pcf'
            pattgen.M07_Save_Sheet_Data.Save_One_Sheet(X02.Sheets(CopyFormSheet), TempName, False, M30.Unic_SheetName(Name, '_'))
            Load_Sheets(TempName, '', AfterSheetName=CopyFormSheet)
            Translate_Standard_Description_Box()
            # 24.06.20: This is not working because the name of the Textbox is not copied ;-(
            #           It should be "Description Message" to be translated
        else:
            Create_New_Sheet(Name, Add_to_Duplicate_Name='_', AfterSheetName=M01.MAIN_SH)
            Load_Textbox(M01.StdDescEdges + Chr(M01.pcfSep) + pattgen.M09_Language.Get_Language_Str(M01.StdDescStart), 'Description Message')
            # 24.06.20: Added: "Description Message" to make sure that the description is translated
            X02.RangeDict[M01.Macro_N_Rng] = M30.Replace_Illegal_Char(X02.ActiveSheet.Name)
            Add_by_Hardi()
        X02.Range(M01.FirstLEDTabRANGE).Select()
        M30.Protect_Active_Sheet()

def Translate_Standard_Description_Box():
    o = Variant()
    #---------------------------------------
    for o in X02.ActiveSheet.Shapes:
        _select9 = o.Type
        if (_select9 == X01.msoTextBox):
            # 17: TextBox
            if o.Name == 'Description Message':
                # 21.01.20: Disabled If Get_ExcelLanguage() <> 0 Then
                # Left(o.TextFrame.Characters.Text, Len(StdDescStart)) = StdDescStart Then
                WasProtected = X02.ActiveSheet.ProtectContents
                if WasProtected:
                    X02.ActiveSheet.Unprotect()
                o.Delete()
                Load_Textbox(M01.StdDescEdges + Chr(M01.pcfSep) + pattgen.M09_Language.Get_Language_Str(M01.StdDescStart), 'Description Message')
                if WasProtected:
                    M30.Protect_Active_Sheet()
                break
                #End If

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def Translate_Standard_Description_Box_in_Sheet(Sh):
    o = Variant()
    #---------------------------------------------------------------------
    for o in Sh.Shapes:
        _select10 = o.Type
        if (_select10 == X01.msoTextBox):
            # 17: TextBox
            if o.Name == 'Description Message':
                # 21.01.20: Disabled If Get_ExcelLanguage() <> 0 Then
                # Left(o.TextFrame.Characters.Text, Len(StdDescStart)) = StdDescStart Then
                WasProtected = Sh.ProtectContents
                if WasProtected:
                    Sh.Unprotect()
                o.Delete()
                OldSh = X02.ActiveSheet.Name
                # 23.06.20: Otherwise the description is moved to the active sheet
                Sh.Select()
                Load_Textbox(M01.StdDescEdges + Chr(M01.pcfSep) + pattgen.M09_Language.Get_Language_Str(M01.StdDescStart), 'Description Message')
                X02.Sheets(OldSh).Select()
                # 23.06.20:
                if WasProtected:
                    M30.Protect_Active_Sheet()
                break
                #End If

def Test_Translate_Standard_Description_Box_in_Sheet():
    Translate_Standard_Description_Box_in_Sheet(X02.Sheets('Main'))

def Load_Dauer_Tab(Line):
    c = Variant()

    i = Long()
    #-----------------------------------------
    for c in Split(Line, Chr(M01.pcfSep)):
        if c[0]!="=": #*HL no formulas allowed
            X02.CellDict[M01.Dauer_Row, M01.Dauer_Col1 + i] = Replace(c, '~', str(M01.Dauer_Row))
        i = i + 1

def Load_GoTo_Tab(Line):
    c = Variant()

    i = Long()
    #----------------------------------------
    for c in Split(Line, Chr(M01.pcfSep)):
        X02.CellDict[M01.GoTo_Row, M01.GoTo_Col1 + i] = c
        i = i + 1

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LTabNr - ByRef 
def Load_LED_Tab(Line, LTabNr):
    #-------------------------------------------------------------
    _with23 = X02.Range(M01.FirstLEDTabRANGE)
    i = - 1
    for c in Split(Line, Chr(M01.pcfSep)):
        if i != - 1 and c != '':
            _with23.offset(LTabNr, i).Value = c
        i = i + 1
    LTabNr = LTabNr + 1
    return LTabNr #*HL ByRef

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: attr - ByVal 
def Set_Attrib(r, attr):
    a = Variant()
    #-------------------------------------------------------
    _with24 = r
    for a in Split(attr, ','):
        _select11 = Left(a, 1)
        if (_select11 == 'c'):
            _with24.Font.Color = Mid(a, 2)
        elif (_select11 == 'i'):
            _with24.Interior.Color = Mid(a, 2)
        elif (_select11 == 'B'):
            _with24.Font.Bold = True
        elif (_select11 == 'I'):
            _with24.Font.Italic = True
        elif (_select11 == 'U'):
            _with24.Font.Underline = Mid(a, 2)
        elif (_select11 == 'W'):
            _with24.WrapText = True
        elif (_select11 == 'O'):
            _with24.Orientation = Val(Mid(a, 2))
        else:
            X02.MsgBox('Error: Unknown attribut: \'' + a + '\'')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: LAttNr - ByRef 
def Load_LED_Att(Line, LAttNr):
    #-------------------------------------------------------------
    _with25 = X02.Range(M01.FirstLEDTabRANGE)
    i = - 2
    for c in Split(Line, Chr(M01.pcfSep)):
        if i == - 1:
            _with25.offset(LAttNr, 0).EntireRow.RowHeight = M30.NrStr2d(c)
        if i >= 0 and c != '':
            Set_Attrib(_with25.offset(LAttNr, i), c)
        i = i + 1
    LAttNr = LAttNr + 1
    return LAttNr #*HL ByRef

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def Load_Textbox(Line, Name='', LanguageNr=- 2):
    Params = vbObjectInitialize(objtype=String)

    Edges = vbObjectInitialize(objtype=String)

    Line2 = String()

    Parts = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------------------------------------------------
    # Special values for "LanguageNr"
    # -1 = Old file without language number
    # -2 = Todo
    Params = Split(Line, Chr(M01.pcfSep))
    Edges = Split(M30.CorrectKomma(Params(0)), ';')
    Line2 = Mid(Line, Len(Params(0)) + 2)
    Line2 = Replace(Line2, '{Attrib}', Chr(1))
    Parts = Split(Line2, Chr(1))
    #*HLX02.ActiveSheet.Shapes.AddLabel(X01.msoTextOrientationHorizontal, Val(Edges(0))*X02.guifactor, Correct_Top_Pos_by_Version(Val(Edges(1)))*X02.guifactor, Val(Edges(2))*X02.guifactor, Val(Edges(3))*X02.guifactor).Select()
    # 21.10.19: Added Val()  17.11.19: Added: Correct_Top_Pos_by_Version
    #*HL X02.Selection.Placement = X01.xlFreeFloating
    #*HL X02.Selection.ShapeRange[1].TextFrame2.TextRange.Characters.Text = Replace(Replace(Parts(0), '| ', '|'), '|', vbLf)
    # 13.02.20: Added: Replace(...)
    Text = Replace(Replace(Parts(0), '| ', '|'), '|', vbLf)
    X02.ActiveSheet.Shapes.AddTextBox(Name, X01.msoTextOrientationHorizontal, Val(Edges(0))*X02.guifactor, Correct_Top_Pos_by_Version(Val(Edges(1)))*X02.guifactor, Val(Edges(2))*X02.guifactor, Val(Edges(3))*X02.guifactor,Text=Text).Select()
    if Name != '':
        X02.Selection.ShapeRange[1].Name = Name
    if UBound(Parts) == 1:
        for c in Split(Parts(1), ' '):
            _select12 = Left(c, 1)
            if (_select12 == 'B') or (_select12 == 'F'):
                # Bold / ForeColor
                Par = Split(Mid(c, 2), ',')
                # 19.10.19: Old:
                Start = Val(Par(0))
                Lenghth = Val(Par(1)) - Val(Par(0)) + 1
                # 19.10.19: Second parameter is the lenght and not the end position
                _select13 = Left(c, 1)
                if (_select13 == 'B'):
                    X02.Selection.ShapeRange[1].TextFrame2.TextRange.Characters.charformat(Start, Lenghth,Bold=True)  #*HL
                elif (_select13 == 'F'):
                    X02.Selection.ShapeRange[1].TextFrame2.TextRange.Characters.charformat(Start, Lenghth,ForeColor=Par(2))   #*HL
                    # 19.10.19:
    if LanguageNr >= 0:
        # 11.02.20:
        X02.Selection.ShapeRange[1].AlternativeText = 'Language: ' + str(LanguageNr)
        if pattgen.M09_Language.Get_ExcelLanguage() != LanguageNr:
            X02.Selection.ShapeRange[1].Visible = False

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: RotPos - ByRef 
def Show_Rotating_Status(message, RotPos):
    RotatingChr = '-\\|/'
    # 27.10.19:
    #-------------------------------------------------------------------
    if RotPos > 4 or RotPos < 1:
        RotPos = 1
    X02.Application.StatusBar = message + Mid(RotatingChr, RotPos, 1)
    RotPos = RotPos + 1
    X03.Sleep(100)
    X02.DoEvents()
    return RotPos #*HL ByRef

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Line - ByVal 
def Load_msoFormControl(Line, LanguageNr=- 2):
    
    logging.debug("Load_msoFormControl- ERROR: %s",Line)
    
    Params = vbObjectInitialize(objtype=String)

    Edges = vbObjectInitialize(objtype=String)

    Init_Proc = String()
    # 19.10.19:
    #---------------------------------------------------------------------------------
    # Load Button
    Params = Split(Line, Chr(M01.pcfSep))
    if InStr(Params(2), 'Update_Grafik') > 0 or InStr(Params(2), 'New_Sheet') > 0:
        return
    # Skip buttons which have been added by a wrong program  13.02.20:
    Edges = Split(M30.CorrectKomma(Params(0)), ';')
    shape= X02.ActiveSheet.Buttons.Add(Val(Edges(0)), Correct_Top_Pos_by_Version(Val(Edges(1))), Val(Edges(2)), Val(Edges(3))) #*HL
    # 21.10.19: Added Val() 17.11.19: Added: Correct_Top_Pos_by_Version
    shape.TextFrame2.TextRange.Characters.Text = Params(1)
    shape.OnAction = Params(2)
    Init_Proc = Params(2) + '_Init'
    if LanguageNr >= 0:
        # 12.02.20:
        shape.AlternativeText = 'Language: ' + str(LanguageNr)
        if pattgen.M09_Language.Get_ExcelLanguage() != LanguageNr:
            shape.Visible = False
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
    X02.Application.Run(Init_Proc)
    # 05.01.22: Juergen call init function synchronous

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Top - ByVal 
def Correct_Top_Pos_by_Version(Top):
    _fn_return_value = None
    # 17.09.19:
    #-----------------------------------------------------
    # Correct the position of elemets which are stored with an old version
    _fn_return_value = Top
    if MLL_pcf_Version == 0:
        # Line "Goto Aktivierung" has been added in version 1     17.09.19:
        if Top > 160:
            _fn_return_value = Top + 31.2
    return _fn_return_value

def Load_Picture(Line, SourceDir):
    Params = vbObjectInitialize(objtype=String)

    Edges = vbObjectInitialize(objtype=String)

    PicName = String()
    # Changed to public by Misha 29-6-2020.
    #-----------------------------------------------------------
    Params = Split(Line, Chr(M01.pcfSep))
    Edges = Split(M30.CorrectKomma(Params(0)), ';')
    # 02.07.19: Added: CorrectKomma()
    PicName = SourceDir + Params(1)
    PicName=PicName.replace(".jpg",".png")
    # 25.11.19: First look in the source dir
    if Dir(PicName) == '':
        SecondDir = PG.ThisWorkbook.Path + '\\' + M01.ExampleDir + '\\'
        PicName = SecondDir + Params(1)
        if UCase(SecondDir) != UCase(SourceDir):
            SecondDir = vbCr + '  ' + SecondDir
        else:
            SecondDir = ''
        if Dir(PicName) == '':
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Das Bild \'') + Params(1) + pattgen.M09_Language.Get_Language_Str('\' existiert nicht in folgenen Verzeichnissen:') + vbCr + '  ' + SourceDir + SecondDir, vbCritical, pattgen.M09_Language.Get_Language_Str('Bild nicht gefunden'))
            return
    M02a.Global_Worksheet_Change(X02.Cells(1, 1))
    # Redraw everything to make sure that the picture is placed correctly
    # 12.01.20:
    # VB2PY (UntranslatedCode) On Error GoTo LoadError
    
    X02.ActiveSheet.Shapes.AddPicture(PicName, linktofile= X01.msoFalse, savewithdocument= X01.msoCTrue, Left= Val(Edges(0))*X02.guifactor, Top= Correct_Top_Pos_by_Version(Val(Edges(1)))*X02.guifactor, Width= Val(Edges(2))*X02.guifactor, Height= Val(Edges(3))*X02.guifactor).Select()
    # 12.07.20: Old: Width:=-1, Height:=-1
    # VB2PY (UntranslatedCode) On Error GoTo 0
    X02.Selection.Name = M30.NoExt(Params(1))
    X02.Selection.Placement = X01.xlMove
    # 30.12.19: Old: Selection.Placement = xlFreeFloating
    #  Selection.ShapeRange.PictureFormat.TransparentBackground = msoTrue
    # Added by Misha 29-6-2020.
    #  Selection.ShapeRange.PictureFormat.TransparencyColor = rgb(255, 0, 0)
    # Added by Misha 29-6-2020. RED is Transparant Color
    #  Selection.ShapeRange.Fill.Visible = msoFalse
    # Added by Misha 29-6-2020.
    return
    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler beim laden des Bildes: ') + '\'' + PicName + '\'', vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler'))

def Set_Defaults_for_Sheet():
    #-----------------------------------
    # The Cell positions are searched the Language sheet => It's independant from the current language
    if Get_Cell('Grafische Anzeige:') == '' and Get_Cell(Array('Analoges Überblenden:', 'Analoges Überblenden'), False) != '':
        Set_Cell('Grafische Anzeige:', 1)
    X02.Range('RGB_Modul_Nr').ClearContents()
    # 30.12.19:
    pattgen.M06_Goto_Graph.Hide_Show_GotoLines_If_Enabled()
    pattgen.M06_Goto_Graph.Hide_Show_Special_ModeLines_If_Enabled()
    # 29.12.19:
    Add_by_Hardi()
    X02.ActiveWindow.DisplayHeadings = False
    
    X02.ActiveSheet.EventWScalculate(X02.Cells(5,5))  #*HL
    X02.ActiveSheet.EventWScalculate(X02.Cells(5,5))  #*HL
    X02.Application.Caller="Update" #*HL
    X02.ActiveSheet.EventWSchanged(X02.Cells(5,5)) #*HL
    
    #X02.ActiveSheet.EventWSchanged(X02.Cells(5,5)) #*HL  

    if Get_Cell('Grafische Anzeige:') != '':
        ## VB2PY (CheckDirective) VB directive took path 1 on True
        # 25.11.19:
        M02a.Update_Grafik_from_Str(Get_Cell('Grafische Anzeige:'))
    M02a.Hide_Show_Check_Goto_Activation()
    # 19.11.19:

def Set_RGB_LED_CheckBox(Value):
    
    OldEvents = Boolean()

    Oldupdating = Boolean()
    # 13.06.20:
    #------------------------------------------------
    OldEvents = X02.Application.EnableEvents
    X02.Application.EnableEvents = False
    #OldUpdating = Application.ScreenUpdating
    X02.ActiveSheet.RGB_LED_CheckBox.Enabled = False
    X02.ActiveSheet.RGB_LED_CheckBox.Value = ( Value > 0 )
    X02.ActiveSheet.RGB_LED_CheckBox.Enabled = True
    X02.Application.EnableEvents = OldEvents
    #Application.ScreenUpdating = OldUpdating
    # Is enabled when the CheckBox is changed

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Loaded_Sheets - ByRef 
def Load_Sheets(SourceName, Loaded_Sheets, AfterSheetName=VBMissingArgument):
    global MLL_pcf_Version
    FileNr = Integer()

    OldSheet = X02.Worksheet()

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
    OldSheet = X02.ActiveSheet
    X02.Application.EnableEvents = False
    FileNr = FreeFile()
    if Dir(SourceName) == '':
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Die Datei \'') + SourceName + '\' ' + pattgen.M09_Language.Get_Language_Str('existiert nicht.'), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler'))
        return
    SourceDir = M30.FilePath(SourceName)
    VBFiles.openFile(FileNr, SourceName, 'r') #*HL
    #FirstSheet = True
    LNr = 0
    ScrUpd = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = False
    X02.Application.Calculation = X01.xlCalculationManual
    while not EOF(FileNr):
        # Loop over all lines in the file
        LNr = LNr + 1
        Line = VBFiles.getLineInput(FileNr, 1)
        Line = Replace(Line, vbTab, Chr(M01.pcfSep))
        # To be able to read old files which have been separeted by tab
        if Line != '':
            Tokens = Split(Line, Chr(M01.pcfSep))
            if SkipSheet == False or Tokens(0) == 'SheetName':
                _select14 = Tokens(0)
                if (_select14 == ''):
                    # Nothing
                    pass
                elif (_select14 == 'SheetName'):
                    # Start of a new sheet
                    if FinishPrevious and not SkipSheet:
                        # Do we have to finish the previous sheet
                        Set_Defaults_for_Sheet()
                        M30.Protect_Active_Sheet()
                        # Protect the previos sheet
                        FinishPrevious = False
                        # 14.06.20:
                    D00.StatusMsg_UserForm.Set_ActSheet_Label(pattgen.M09_Language.Get_Language_Str('Lade ') + ': ' + Tokens(1))
                    #  ( & ": ") Added by Misha 7-2-2020 for readability.
                    if InStr(vbTab + Loaded_Sheets, vbTab + Tokens(1) + vbTab) > 0:
                        SkipSheet = True
                    else:
                        Loaded_Sheets = Loaded_Sheets + Tokens(1) + vbTab
                        SkipSheet = False
                        if AfterSheetName == '<<LASTSHEET>>':
                            #AfterSheetName = X02.Sheets(X02.Sheets.Count).Name #*HL
                            AfterSheetName = X02.Sheets('<<LASTSHEET>>').Name  #*HL
                        # 14.06.20:
                        Create_New_Sheet(Tokens(1), AfterSheetName=AfterSheetName)
                        LTabNr = 0
                        LAttNr = 0
                        AddedSheets = AddedSheets + 1
                        FinishPrevious = True
                        # 14.06.20:
                elif (_select14 == 'Dauer'):
                    Load_Dauer_Tab(Mid(Line, Len(Tokens(0)) + 2))
                elif (_select14 == 'Version'):
                    MLL_pcf_Version = Val(Tokens(1))
                    # 17.11.19:
                elif (_select14 == 'Goto Tabelle'):
                    Load_GoTo_Tab(Mid(Line, Len(Tokens(0)) + 2))
                elif (_select14 == 'LED_Tab'):
                    LTabNr=Load_LED_Tab(Line, LTabNr) #*HL
                elif (_select14 == 'LED_Attr'):
                    LAttNr=Load_LED_Att(Line, LAttNr)
                elif (_select14 == 'Analoges Überblenden'):
                    Set_Cell('Analoges Überblenden:', Tokens(1))
                    # Two different spellings used ;-(
                elif (_select14 == 'msoTextBox'):
                    Load_Textbox(Mid(Line, Len(Tokens(0)) + 2), LanguageNr=- 1)
                    # Old line without language number
                elif (_select14 == 'msoFormControl'):
                    Load_msoFormControl(Mid(Line, Len(Tokens(0)) + 2), LanguageNr=- 1)
                    # Old line without language number
                elif (_select14 == 'msoPicture'):
                    Load_Picture(Mid(Line, Len(Tokens(0)) + 2), SourceDir)
                elif (_select14 == 'msoShapeOval'):
                    pattgen.M80_Multiplexer_INI_Handling.Load_msoShapeOval(Tokens(1), Tokens(2))
                    # Added by Misha 26-6-2020
                elif (_select14 == 'RGB_LED_CheckBox'):
                    Set_RGB_LED_CheckBox(Val(Tokens(1)))
                    # 13.06.20:
                else:
                    if Left(Tokens(0), Len('msoTextBox')) == 'msoTextBox':
                        # 11.02.20:
                        LanguageNr = Val(Mid(Tokens(0), Len('msoTextBox') + 1))
                        Load_Textbox(Mid(Line, Len(Tokens(0)) + 2), LanguageNr=LanguageNr)
                    elif Left(Tokens(0), Len('msoFormControl')) == 'msoFormControl':
                        LanguageNr = Val(Mid(Tokens(0), Len('msoFormControl') + 1))
                        Load_msoFormControl(Mid(Line, Len(Tokens(0)) + 2), LanguageNr=LanguageNr)
                    else:
                        if len(Tokens)==2: #*HL correction /n problem
                            Set_Cell(Trim(Tokens(0)), Tokens(1))
                        elif len(Tokens)==1: #*HL correction /n problem
                            pass
                            
    # All sheets loade
    if FinishPrevious:
        # Do we have to finish the previous sheet (In case there was no sheet in the configuration file)
        # 14.06.20: Old: Not FirstSheet
        Set_Defaults_for_Sheet()
        M30.Protect_Active_Sheet()
        # Protect the previos sheet
    X02.Application.Calculation = X01.xlCalculationAutomatic
    X02.Application.EnableEvents = True
    X02.Application.ScreenUpdating = ScrUpd
    VBFiles.closeFile(FileNr)
    if AddedSheets > 1:
        OldSheet.Activate()

def Test_Examples_UserForm():
    #UT---------------------------------
    Debug.Print('Result=' + Examples_UserForm.Show_Dialog)

def Load_AllExamples_Sheets():
    _fn_return_value = None
    ExampleList = String()
    #---------------------------------------------------
    X02.Application.Calculation = X01.xlCalculationAutomatic
    # In case the previous macro was aborted
    ExampleList = D00.Examples_UserForm.Show_Dialog()
    PG.ThisWorkbook.Activate()
    # 13.06.20:
    if ExampleList != '':
        D00.StatusMsg_UserForm.Show()
        X02.Application.StatusBar = pattgen.M09_Language.Get_Language_Str('Lade Beispielseiten...')
        # Prevent loading duplicate sheets
        Loaded_Sheets=""
        for Example in Split(ExampleList, vbTab):
            Load_Sheets(PG.ThisWorkbook.Path + '/' + M01.ExampleDir + '/' + Example + '.MLL_pcf', Loaded_Sheets, '<<LASTSHEET>>')
        if Left(X02.Application.StatusBar, Len(pattgen.M09_Language.Get_Language_Str('Lade Beispielseiten...'))) == pattgen.M09_Language.Get_Language_Str('Lade Beispielseiten...'):
            # Still the same status line and no error message
            X02.Application.StatusBar = pattgen.M09_Language.Get_Language_Str('Beispiele geladen')
        _fn_return_value = True
        X02.Unload(D00.StatusMsg_UserForm)
    X02.Application.Calculation = X01.xlCalculationAutomatic
    return _fn_return_value

def Is_Normal_Data_Sheet(Name, Txt):
    _fn_return_value = False
    #-----------------------------------------------------------------------------
    if PG.ThisWorkbook.Sheets(Name).Visible == False:
        return _fn_return_value
    # 11.01.20:
    if Name != M01.MAIN_SH and Name != M01.LANGUAGES_SH and Name != M01.GOTO_ACTIVATION_SH and Name != M01.PAR_DESCRIPTION_SH and Name != M01.SPECIAL_MODEDLG_SH and Name != "Named_Ranges":
        _fn_return_value = True
        # Additional savety check in case a new sheet has been added which is not listed above
        ## VB2PY (CheckDirective) VB directive took path 1 on True
        # 25.01.20:
        # Invisible string at "A1"
        # 25.01.20:
        CheckCell = 'A1'
        CheckStr = "Normal Data Sheet" # Invisible string at "A1" 
        if PG.ThisWorkbook.Sheets(Name).Range(CheckCell) != CheckStr:
            _select15 = X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Achtung: Soll die Seite \'') + Name + '\' ' + Txt + pattgen.M09_Language.Get_Language_Str(' werden?'), vbQuestion + vbYesNoCancel, pattgen.M09_Language.Get_Language_Str('Unbekannte Seite entdeckt'))
            if (_select15 == vbNo):
                _fn_return_value = False
            elif (_select15 == vbCancel):
                M30.EndProg()
    return _fn_return_value

def Del_All_Sheets_Excep_Main():
    Sh = Variant()
    #-------------------------------------
    X02.Application.Calculation = X01.xlCalculationManual
    # Otherwise the "CalculatePattern()" functionis called for every sheet
    for Sh in PG.ThisWorkbook.sheets: #*HL
        if Is_Normal_Data_Sheet(Sh.Name, pattgen.M09_Language.Get_Language_Str('gelöscht')):
            X02.Application.DisplayAlerts = False
            X02.Sheets(Sh.Name).Delete()
            X02.Application.DisplayAlerts = True
    X02.Application.Calculation = X01.xlCalculationAutomatic

def Del_All_Sheets_which_contain_Copy_in_their_Name():
    Sh = Variant()

    OldSheet = X02.Worksheet()
    #-----------------------------------------------------------
    OldSheet = X02.ActiveSheet
    X02.Application.Calculation = X01.xlCalculationManual
    # Otherwise the "CalculatePattern()" functionis called
    for Sh in PG.ThisWorkbook.sheets:
        if InStr(Sh.Name, '_Copy_'):
            X02.Application.DisplayAlerts = False
            X02.Sheets(Sh.Name).Delete()
            X02.Application.DisplayAlerts = True
    X02.Application.Calculation = X01.xlCalculationAutomatic
    # VB2PY (UntranslatedCode) On Error Resume Next
    # In case the sheet was deleted
    OldSheet.Activate()
    # VB2PY (UntranslatedCode) On Error GoTo 0

def Test_Load_One_Sheet():
    #UT------------------------------
    X02.Application.Calculation = X01.xlCalculationAutomatic
    # In case the previous macro was aborted
    Load_Sheets(PG.ThisWorkbook.Path + '\\' + M01.ExampleDir + '\\TestExample.MLL_pcf', '', AfterSheetName=M01.MAIN_SH)
    X02.Application.Calculation = X01.xlCalculationAutomatic

# VB2PY (UntranslatedCode) Option Explicit
