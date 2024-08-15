from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M30_Tools as M30
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M08_Load_Sheet_Data
import mlpyproggen.Pattern_Generator as PG

import pgcommon.G00_common as G00

""" Attention: One of the following preprcessor constants have to be defined in
 "Extras / Eigenschafteb VBA Projekt"'
   PATTERN_CONFIG_PROG
   PROG_GENERATOR_PROG

 Other languages could be added in the hidden sheet LANGUAGES_SH = "Languages"
 In addition Get_ExcelLanguage() must be adapted
 Current languages:
  0 = German
  1 = English
  2 = Dutch
  3 = French
  4 = Italian  (Prog_Generator only)
  5 = Spain        "
 Strings which have not been translated could be found with
 The seach expression '[!r]("'  and
 "'   (Without ')
 and enabled "Mit Mustervergleich"
   See also: https://docs.microsoft.com/de-de/office/vba/language/reference/user-interface-help/wildcard-characters-used-in-string-comparisons
 They could be translated by inserting 'Get_Language_Str'


 There are a lot of different locations where text messages are used:
 - In the sheets
 - Error messages in the sheets which are shown on certain condition
 - Hints in the sheets
 - Dialog boxes
   - Some of them are changed from the program code
   - Some messages are located in separate sheets: Special_Mode_Dlg, Par_Description
 - In the program code
 - Buttons
 - The Hotkeys have also to be adapted in the dialogs and single buttons
 - In the configuration files *.MLL_pcf
   - Variable names
   - Text messages
 - ...

 Some messages in the program are only called in case of an error.
 => They are not added automatically to the 'Languages' sheet
 ==> This is done by calling Add_All_VBA_Strings_to_the_Languages_Sheet()

 Location for the translations
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 - The most translations are stored in the hidden "Languages"
 - Some translations are stored in different locations
   - The start page contains one text box for each language.
     This is used because here several colors and fonts are used.
     Normaly only the box which contains the current language
     is visible. The language number is stored in the field
     "Alternativtext" which could be changed using the right mouse
     and the menu "Größe und Eigneschaften".
     The "Alternativtext" must contain the keyword "Language:"
     Example: "Language: 0"
     If a new language is created one text box has to be copied
     and translated and the "Alternativtext" has to be changed to
     the new number.
   - The text messages in the example sheets in the Pattern_Configurator
     have an own text box for each language. Here only the text box
     for the actual language is visible. This method is used to be
     independand from the Excel program. The number after the
     keyword "msoTextBox" defines the language number. Old *.MLL_pcf
     don't have a tailing number they are always shown.
   - The buttons in the "Morsecode" sheet use a button for each
     language fo the same reason as the text boxes.
     (See Activate_Language_in_Example_Sheet(ByVal sh As Worksheet)
     The Language number is stored in the "AlternativeText".
   - Dialog functions which select their data form an Excel sheet
     like the "SelectMacros_Form" or the "UserForm_Other" use
     separate columns in the sheets "Lib_Macros" and "Par_Description



 Language specific messages in the example sheets
 11.02.20:
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Different languages could be used in the "msoTextBox" lines in the example sheets.
 The language number is added to the token:
  "msoTextBox0" = German
  "msoTextBox1" = Englisch
  "msoTextBox2" = Dutch
  "msoTextBox3" = French
 All Lines starting with "msoTextBox" are loaded to the sheet, but only the
 text box with the current language is visible. The Language is stored in
 ShapeRange.AlternativeText = "Language: 0"
 If the line line starts with "msoTextBox" it's an old file without different languages.
 This textbox is always shown.
 If the token has a tailing number it's assumed that there are matching lines for all languages.
 If the current language is missing nothing is displayed ;-( => It's importand to update
 the examples if a new language is added



 Row number 3 in the languages sheet
 This column contains the typ in the languages sheet
 This column contains parameters in the languages sheet
 This is the first column used for the translations in then languages sheet
 Debuging with othwer languages
 -1 = Disable, 0 = German, 1 = Englisch, 2 = Dutch
 If this flag is not set the language could be changed
 temporary with the function "Test_Translations()"
 Is used to simulate a different language for tests Check_Languages = true
 The language number which should be used for the test
 "Rot"
 "Grün"
 "AnAus"
 "Tast"
--------------------------------------------------------------------------------------------------------------
UT-------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
# VB2PY (CheckDirective) VB directive took path 2 on 0
--------------------------------------------------------------------
UT--------------------------------------------
----------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
 04.06.20: Old block in Pattern_config
-----------------------------------
# VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
---------------------------------------------
UT---------------------------------
-------------------------------------------------------------
UT-------------------------------------
-------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on True
 28.01.20:
------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------
-------------------------------------------------
-------------------------------------------
UT---------------------------------
-----------------------------------------------------------
-----------------------------------------------------
UT----------------------------
"""

FirstLangRow = 3
LangType_Col = 1
LangParamCol = 2
FirstLangCol = 3
Simulate_Language = - 1
Check_Languages = Boolean()
Test_Language = Integer()
Red_T = String()
Green_T = String()
OnOff_T = String()
Tast_T = String()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def Update_Language_in_Sheet(Sh, DestLang):
    _fn_return_value = None
    LSh = X02.Worksheet()
    # Old Name: Update_Language_in_Pattern_Config_Sheet
    #--------------------------------------------------------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
    #Set OldSel = Selection
    LSh = PG.ThisWorkbook.Sheets(M01.LANGUAGES_SH)
    _with39 = Sh
    # Check if the language has to be changed by comparing the first string
    # Check the actual used language in the sheet
    ActLang = - 1
    FirstMsg = _with39.Range(LSh.Cells(FirstLangRow, LangParamCol))
    for c in vbForRange(FirstLangCol, M30.LastUsedColumnInRow(LSh, FirstLangRow)):
        if FirstMsg == LSh.Cells(FirstLangRow, c):
            ActLang = c - FirstLangCol
            break
    if ActLang == - 1:
        X02.MsgBox('Error: \'' + FirstMsg + '\' not found in the \'Languages\' sheet', vbCritical, 'Language Error')
        return _fn_return_value
    if ( ActLang == DestLang ) :
        return _fn_return_value
    # Language is correct
    # Unprotect the sheet
    WasProtected = Sh.ProtectContents
    # 04.06.20: In Prog_Gen ActiveSheet... was used
    if WasProtected:
        Sh.Unprotect()
    # Debug
    MaxLang = M30.LastUsedColumnInRow(LSh, FirstLangRow) - FirstLangCol
    if DestLang == - 1:
        # -1 could be used for debugging
        DestLang = ActLang + 1
        if ActLang >= MaxLang:
            DestLang = 0
    # Replace the texts
    LangCol = FirstLangCol + DestLang
    for r in vbForRange(FirstLangRow, M30.LastUsedRowIn(LSh)):
        Param = LSh.Cells(r, LangParamCol)
        if Param != '':
            tmp = LSh.Cells(r, LangCol)
            _select25 = LSh.Cells(r, LangType_Col)
            if (_select25 == ''):
                # Nothing
                pass
            elif (_select25 == 'Cell'):
                _with39.Range[Param].FormulaR1C1 = tmp
                # Cell values and formulas
                ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
            elif (_select25 == 'NumberFormat'):
                _with39.Range[Param].NumberFormat = tmp
            elif (_select25 == 'Button'):
                ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
                _with39.Shapes.Range[Array(Param)].Item[1].DrawingObject.Caption = tmp
            elif (_select25 == 'Comment'):
                # Comments
                _with40 = _with39.Range(Param).Comment
                _with40.Text(Text=Replace(tmp, vbLf, Chr(10)))
                _with40.Shape.TextFrame.Characters[1, Len(tmp)].Font.Bold = False
                # ToDo: Bolt aus Sheet lesen
                ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
            elif (_select25 == 'ErrorMessage'):
                _with39.Range[Param].Validation.ErrorMessage = tmp
            elif (_select25 == 'ErrorTitle'):
                _with39.Range[Param].Validation.ErrorTitle = tmp
                # ToDo Warnungen
    if WasProtected:
        M30.Protect_Active_Sheet()
    #OldSel.Select
    _fn_return_value = True
    #Debug.Print "Updated Language in " & Sh.Name
    # Debug
    return _fn_return_value

def Test_Update_Language_in_Sheet():
    OldEvents = Boolean()

    OldUpdate = Boolean()
    #UT-------------------------------------------------------
    # Switches to the next language
    OldEvents = X02.Application.EnableEvents
    OldUpdate = X02.Application.ScreenUpdating
    X02.Application.EnableEvents = False
    X02.Application.ScreenUpdating = False
    Update_Language_in_Sheet(X02.ActiveSheet, - 1)
    X02.Application.EnableEvents = OldEvents
    X02.Application.ScreenUpdating = OldUpdate

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def Activate_Language_in_Example_Sheet(Sh):
    o = Variant()

    ActLanguage = Integer()

    LanguageNr = Integer()
    # 11.02.20:
    #--------------------------------------------------------------------
    ActLanguage = Get_ExcelLanguage()
    for o in Sh.Shapes:
        _select26 = o.Type
        if (_select26 == X01.msoTextBox):
            # 17: TextBox
            if Left(o.Name, Len('Goto_Graph')) != 'Goto_Graph' and o.Name != 'InternalTextBox':
                # "InternalTextBox" = "by Hardi"
                if Left(o.AlternativeText, Len('Language: ')) == 'Language: ':
                    #  11.02.20:
                    LanguageNr = Val(Mid(o.AlternativeText, Len('Language: ') + 1))
                    o.Visible = ( LanguageNr == ActLanguage )
        elif (_select26 == msoFormControl):
            # 8: Button
            # 19.10.19:
            if o.AlternativeText != '_Internal_Button_' and o.AlternativeText != 'Add_Del_Button':
                if Left(o.AlternativeText, Len('Language: ')) == 'Language: ':
                    LanguageNr = Val(Mid(o.AlternativeText, Len('Language: ') + 1))
                    o.Visible = ( LanguageNr == ActLanguage )
                #ToDo     Print_Typ_and_Pos FileNr, "msoFormControl", o, o.AlternativeText & Chr(pcfSep) & Replace(o.OnAction, ThisWorkbook.Name & "!", "")
            ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG

def Activate_Language_in_Active_Sheet():
    #UT--------------------------------------------
    Activate_Language_in_Example_Sheet(X02.ActiveSheet)

def Update_Language_in_All_Sheets():
    return #*HL
    OldEvents = Boolean()

    OldUpdate = Boolean()

    OldSheet = X02.Worksheet()

    Sh = Variant()

    DestLang = Integer()

    Initialized = Boolean()
    # 25.02.20: Old name: Update_Language_in_All_Pattern_Config_Sheets
    #----------------------------------
    # Set the language of all sheets to the active display language in excel
    OldSheet = X02.ActiveSheet
    OldEvents = X02.Application.EnableEvents
    OldUpdate = X02.Application.ScreenUpdating
    X02.Application.EnableEvents = False
    X02.Application.ScreenUpdating = False
    DestLang = Get_ExcelLanguage()
    #DestLang = 1
    # debug
    for Sh in PG.ThisWorkbook.sheets:
        #If sh.Name <> LANGUAGES_SH And sh.Name <> GOTO_ACTIVATION_SH And sh.Name <> PAR_DESCRIPTION_SH Then
        # 20.01.20: Old
        ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
        if Sh.Name == M01.MAIN_SH or pattgen.M08_Load_Sheet_Data.Is_Normal_Data_Sheet(Sh.Name, Get_Language_Str('übersetzt')):
            if not Initialized:
                D00.StatusMsg_UserForm.Set_Label(Get_Language_Str('Umstellung der Sprache'))
                #12.02.20:
            D00.StatusMsg_UserForm.Set_ActSheet_Label(Sh.Name)
            if not Initialized:
                D00.StatusMsg_UserForm.Show()
            Initialized = True
            # 07.03.20: sh.Activate
            # Necessary for the button names ;-(
            ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
            if Sh.Name != 'Multiplexer':
                # 23.06.20:
                Translate_Standard_Description_Box_in_Sheet(Sh)
                # 07.03.20: Using new function which doesn't need the active sheet
                if Update_Language_in_Sheet(Sh, DestLang) == False and Sh.Name == M01.MAIN_SH:
                    break
            ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
            Activate_Language_in_Example_Sheet(Sh)
    ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
    X02.Unload(StatusMsg_UserForm)
    if not OldSheet is None:
        # 01.05.20: Prevent crash if downloaded from the internet when the Savety messages is shown
        OldSheet.Activate()
    X02.Application.EnableEvents = OldEvents
    X02.Application.ScreenUpdating = OldUpdate

def Check_SIMULATE_LANGUAGE():
    #-----------------------------------
    if Simulate_Language >= 0:
        X02.MsgBox('Attention the compiler switch \'SIMULATE_LANGUAGE\' is set to ' + Simulate_Language + vbCr + 'This is used to test the languages. It must be disabled in the release version!', vbInformation)

def Get_ExcelLanguage():
    _fn_return_value = None
    #---------------------------------------------
    # Return a number corrosponding to the actual language used in excel
    #  0 = German
    #  1 = English and all other languages
    #  2 = Dutch
    #  3 = French�
    #  4 = Italian    (Only in the Prog_Generator)
    #  5 = Spain        "
    # The number must match to the position in the language strings in M6_Language_Constants
    #
    # Is working if the office language is changed or the Window language
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    if Simulate_Language >= 0:
        _fn_return_value = Simulate_Language
        return _fn_return_value
    if Check_Languages:
        # 20.01.20:
        _fn_return_value = Test_Language
        return _fn_return_value
    _fn_return_value = 1
    ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
    #Debug.Print "Achtung: Get_ExcelLanguage() liefert immer 1"
    #Exit Function
    _select27 = X02.Application.LanguageSettings.LanguageID(X01.msoLanguageIDUI)
# Language ID's: https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2007/aa432635(v=office.12)
    if (_select27 == X01.msoLanguageIDGerman) or (_select27 == X01.msoLanguageIDGermanAustria) or (_select27 == X01.msoLanguageIDGermanLiechtenstein) or (_select27 == X01.msoLanguageIDGermanLuxembourg) or (_select27 == X01.msoLanguageIDSwissGerman):
        _fn_return_value = 0
    elif (_select27 == X01.msoLanguageIDDutch) or (_select27 == X01.msoLanguageIDBelgianDutch):
        #   Added by Misha 24-2-2020
        _fn_return_value = 2
    elif (_select27 == X01.msoLanguageIDFrench) or (_select27 == X01.msoLanguageIDBelgianFrench) or (_select27 == X01.msoLanguageIDFrenchCameroon) or (_select27 == X01.msoLanguageIDFrenchCanadian) or (_select27 == X01.msoLanguageIDFrenchCotedIvoire) or (_select27 == X01.msoLanguageIDFrenchHaiti) or (_select27 == X01.msoLanguageIDFrenchLuxembourg) or (_select27 == X01.msoLanguageIDFrenchMali) or (_select27 == X01.msoLanguageIDFrenchMonaco) or (_select27 == X01.msoLanguageIDFrenchMorocco) or (_select27 == X01.msoLanguageIDFrenchReunion) or (_select27 == X01.msoLanguageIDFrenchSenegal) or (_select27 == X01.msoLanguageIDFrenchWestIndies) or (_select27 == X01.msoLanguageIDSwissFrench):
        # Not defined at Exel 2016? msoLanguageIDFranchCongoDRC
        _fn_return_value = 3
        # ' Added by Misha 24-2-2020
    elif (_select27 == X01.msoLanguageIDItalian) or (_select27 == X01.msoLanguageIDSwissItalian):
        _fn_return_value = 4
    elif (_select27 == X01.msoLanguageIDSpanish) or (_select27 == X01.msoLanguageIDSpanishArgentina) or (_select27 == X01.msoLanguageIDSpanishBolivia) or (_select27 == X01.msoLanguageIDSpanishChile) or (_select27 == X01.msoLanguageIDSpanishColombia) or (_select27 == X01.msoLanguageIDSpanishCostaRica) or (_select27 == X01.msoLanguageIDSpanishDominicanRepublic) or (_select27 == X01.msoLanguageIDSpanishEcuador) or (_select27 == X01.msoLanguageIDSpanishElSalvador) or (_select27 == X01.msoLanguageIDSpanishGuatemala) or (_select27 == X01.msoLanguageIDSpanishHonduras) or (_select27 == X01.msoLanguageIDSpanishModernSort) or (_select27 == X01.msoLanguageIDSpanishNicaragua) or (_select27 == X01.msoLanguageIDSpanishPanama) or (_select27 == X01.msoLanguageIDSpanishParaguay) or (_select27 == X01.msoLanguageIDSpanishPeru) or (_select27 == X01.msoLanguageIDSpanishPuertoRico) or (_select27 == X01.msoLanguageIDSpanishUruguay) or (_select27 == X01.msoLanguageIDSpanishVenezuela) or (_select27 == X01.msoLanguageIDMexicanSpanish):
        _fn_return_value = 5
    #05.07.20: Get_ExcelLanguage = 1
    #  For testing by Misha 2-7-2020.
    return _fn_return_value

def Test_Get_ExcelLanguage():
    #UT---------------------------------
    Debug.Print('Get_ExcelLanguage()=' + Get_ExcelLanguage())

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
def Find_Cell_Pos_by_Name(Desc):
    _fn_return_value = ""
    LSh = X02.Worksheet()

    Res = Variant()
    #-------------------------------------------------------------
    # Find the given Desc in the language sheet and return the
    # destination position as string.
    #
    # If Desc is not found "" is returned
    LSh = PG.ThisWorkbook.Sheets(M01.LANGUAGES_SH)
    _with41 = LSh
    #Res = LSh.CellsFind.Find(What= Desc, After= _with41.Range('A1'), LookIn= X01.xlFormulas, LookAt= X01.xlPart, SearchOrder= X01.xlByRows, SearchDirection= X01.xlNext, MatchCase= True, SearchFormat= False) #*HL
    Row = LSh.find_in_col_ret_row(Desc, FirstLangCol)
    if not Row is None:
        _fn_return_value = _with41.Cells(Row, LangParamCol).Value
    return _fn_return_value

def Test_Find_Cell_Pos_by_Name():
    #UT-------------------------------------
    Debug.Print('Find_Cell_Pos_by_Name("Bits pro Wert:")=\'' + Find_Cell_Pos_by_Name('Bits pro Wert:') + '\'')
    Debug.Print('Find_Cell_Pos_by_Name("Bits per value:")=\'' + Find_Cell_Pos_by_Name('Bits per value:') + '\'')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
def Get_German_Name(Desc):
    _fn_return_value = ""
    LSh = X02.Worksheet()
    Desc_split = Desc.split("§")
    Desc = Desc_split[0]

    Res = Variant()
    #-------------------------------------------------------
    LSh = PG.ThisWorkbook.Sheets(M01.LANGUAGES_SH)
    _with42 = LSh
    #Res = LSh.CellsFind.Find(What= Desc, After= _with42.Range('A1'), LookIn= X01.xlFormulas, LookAt= X01.xlPart, SearchOrder= X01.xlByRows, SearchDirection= X01.xlNext, MatchCase= True, SearchFormat= False)
    Row = LSh.find_in_col_ret_row(Desc, FirstLangCol)
    #if not Res is None:
    if not Row is None:
        _fn_return_value = _with42.Cells(Row, FirstLangCol).Value
    else:
        #X02.MsgBox('Error \'' + Desc + '\' not found in \'Get_German_Name\'', vbCritical, 'Error')
        logging.debug('Error \'' + Desc + '\' not found in \'Get_German_Name\'')
        _fn_return_value = Desc
    return _fn_return_value

def Add_Entry_to_Languages_Sheet(GermanTxt):
    #------------------------------------------------------------
    return #*HL
    if Get_ExcelLanguage() == 0:
        LSh = PG.ThisWorkbook.Sheets(M01.LANGUAGES_SH)
        if LSh!=None:
            _with43 = LSh
            Row = M30.LastUsedRowIn(LSh) + 1
            _with43.CellDict[Row, FirstLangCol] = GermanTxt

def Debug_Find_Diff(S1, s2):
    i = Long()
    #------------------------------------------------------
    Debug.Print('Len:' + Len(S1) + '  ' + Len(s2))
    for i in vbForRange(1, Len(S1)):
        if Mid(S1, i, 1) != Mid(s2, i, 1):
            Debug.Print('Different pos: ' + i)
            i = i - 3
            if i < 1:
                i = 1
            Debug.Print(Mid(S1, i - 3, 7))
            Debug.Print(Mid(s2, i - 3, 7))
            Debug.Print(Space(i - 1) + '^')
            return
    Debug.Print('Strings are equal')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At=X01.xlPart - ByVal 
def Find_Language_Str_Row(Desc, Look_At=X01.xlPart):
    _fn_return_value = None
    LSh = X02.Worksheet()

    Res = Variant()
    #--------------------------------------------------------------------------------------------------------------
    LSh = PG.ThisWorkbook.Sheets(M01.LANGUAGES_SH)
    if LSh==None:
        return 0
    _with44 = LSh
    # VB2PY (UntranslatedCode) On Error Resume Next
    # In case the Description is missing
    # Maximal length for the find command: 255
    Start = _with44.Range('A1')
    Desc = RTrim(Desc)
    ## VB2PY (CheckDirective) VB2PY Python directive
    Res = LSh.find_in_col_ret_row(Desc, FirstLangCol)
    if not Res is None:
        _fn_return_value = Int(Res)
    else:
        _fn_return_value = 0
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At=X01.xlPart - ByVal 
def Get_Language_Str(Desc, GenError=False, Look_At=X01.xlPart):
    _fn_return_value = None
    Use_CrLf = Boolean()

    Res = String()
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Replace the vbCr in the input string to be able to find in in the "Languages" sheet
    # 30.01.20:
    # Problem:
    # vbCr cant be used in an excel table (Languages sheet)
    # => It is replaced by '|' in the sheet
    # To identify the structure of the message an vbLf is also used.
    # - If the original string is stored in a dialog it contains cvCr & vbLf
    #   only the vbCr has to be replaced
    # - If the original string is stored in the VB code only vbCr is used
    #   therefore the cvLf is added in "Add_All_VBA_Strings_to_the_Languages_Sheet()"
    #   to get the visual line breaks.
    #   In this case the cvLf must also be added in this function
    if Desc == '':
        return _fn_return_value
    # 23.01.20:
    Desc = Replace(Desc, '| ', '|')
    # 24.02.20: Added because of Misha's improvement
    if InStr(Desc, vbCr + vbLf) > 0:
        Use_CrLf = True
        Desc = Replace(Desc, vbCr, '|')
    else:
        # no combination of vbCr & vbLf used => Add vbLf for the check
        Desc = Replace(Desc, vbCr, '|' + vbLf)
    Res = Get_Language_Str_Sub(Desc, GenError, Look_At)
    if Use_CrLf:
        _fn_return_value = Replace(Res, '|', vbCr)
    else:
        _fn_return_value = Replace(Res, '|' + vbLf, vbCr)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At - ByVal 
def Get_Language_Str_Sub(Desc, GenError, Look_At):
    _fn_return_value = None
    Row = Long()

    return_value = String()

    LSh = X02.Worksheet()
    #-------------------------------------------------------------------------------------------------------------------
    # Find the given Desc in the language sheet and return the
    # string in the actual language
    #
    if IsNumeric(Desc):
        _fn_return_value = Desc
        return _fn_return_value
    _fn_return_value = ''
    Row = Find_Language_Str_Row(Desc, Look_At)
    LSh = PG.ThisWorkbook.Sheets(M01.LANGUAGES_SH)
    _with45 = LSh
    if Row > 0:
        return_value = _with45.Cells(Row, FirstLangCol + Get_ExcelLanguage()).Value
        if return_value != '':
            # 25.01.20: Prior the function was left with an empty result ;-( Now a message is generated an the Germal text is used
            _fn_return_value = return_value
            return _fn_return_value
    # The language string was not found
    if GenError:
        X02.MsgBox('Error translation missing in sheet \'Languages\' for:' + vbCr + '  \'' + Desc + '\'', vbCritical, 'Error: Translation missing')
    else:
        #Debug.Print('*** Translation not found for:' + vbCr + Desc)
        pass
    if Row > 0:
        return_value = _with45.Cells(Row, FirstLangCol + 1).Value
    # Use the Enlish text if available
    # 26.01.20:
    if return_value == '':
        _fn_return_value = Desc
    else:
        _fn_return_value = return_value
    Add_Entry_to_Languages_Sheet(Desc)
    # Add the german text to the 'Languages' sheet
    # 24.01.20:
    return _fn_return_value

def Change_Lang_in_MultiPage(o):
    Pg = Variant()
    # 25.01.20:
    #-------------------------------------------------
    for Pg in o.Pages:
        #Pg.Caption = Replace(Get_Language_Str(Replace(Pg.Caption, vbCr, "|"), False, xlWhole), "|", vbCr)
        # Old 30.01.20:
        Pg.Caption = Get_Language_Str(Pg.Caption, False, X01.xlWhole)

def Change_Language_in_Dialog(dlg):
    o = Variant()
    #-------------------------------------------
    dlg.Caption = Get_Language_Str(dlg.Caption)
    # 25.01.20:
    for o in dlg.Controls:
        if o.ControlTipText != '':
            o.ControlTipText = Get_Language_Str(o.ControlTipText)
        #Debug.Print o.Name
        #If o.Name = "Label12" Then
        #   Debug.Print "Debug"
        #End If
        # VB2PY (UntranslatedCode) On Error Resume Next
        # Problem: if o.Caption doesn't exist "<Objekt unterstützt diese Eigenschaft oder Methode nicht>"
        if Left(o.Name, Len('MultiPage')) == 'MultiPage':
            Change_Lang_in_MultiPage(o)
        elif Left(o.Name, Len('ListBox')) == 'ListBox':
            # There is no constant text in the ListBox dialog. It is loaded dymanicaly
            pass
        elif o.Caption != 'by Hardi' and Left(o.Caption, 4) != 'http' and o.Caption != '*' and o.Caption != 'J':
            # "J" = Smilly in "Wait_CheckColors_Form"
            #o.Caption = Replace(Get_Language_Str(Replace(o.Caption, vbCr, "|"), False, xlWhole), "|", vbCr)
            # 30.01.20: Old:
            o.Caption = Get_Language_Str(o.Caption, False, X01.xlWhole)
        # VB2PY (UntranslatedCode) On Error GoTo 0

def Test_Change_Language_in_Dialog():
    #UT---------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    Copy_Select_GotoAct_Form.Show()

def Set_Tast_Txt_Var(ForceUpdate=VBMissingArgument):
    global Red_T, Green_T, OnOff_T, Tast_T
    # 06.03.20:
    #-----------------------------------------------------------
    if ForceUpdate or Red_T == '':
        Red_T = Get_Language_Str('Rot')
        Green_T = Get_Language_Str('Grün')
        OnOff_T = Get_Language_Str('AnAus')
        Tast_T = Get_Language_Str('Tast')

def Get_Dialog_Nr(Name):
    _fn_return_value = None
    o = Variant()

    Nr = Long()
    # 23.06.20:
    #-----------------------------------------------------
    # Get the number of a loaded dialog
    # Generate an error message and abort the progra if the dialog is not available
    for o in UserForms:
        if o.Name == Name:
            _fn_return_value = Nr
            return _fn_return_value
        Nr = Nr + 1
    X02.MsgBox('Internal Error: The Dialog \'' + Name + '\' is not loaded for some reasons', vbCritical, 'Internal Error')
    M30.EndProg()
    return _fn_return_value

def Test_Translations():
    global Check_Languages, Test_Language
    Res = String()

    c = Object()
    #UT----------------------------
    # Check it the translation works correct
    Check_Languages = True
    Debug.Print(vbCr + '-------------------------------------------')
    Res = G00.InputBox('Input the Language number' + vbCr + ' 0 = German' + vbCr + ' 1 = English' + vbCr + ' 2 = Dutch' + vbCr + ' 3 = French' + vbCr + ' 4 = Italian' + vbCr + ' 5 = Spain')
    if not IsNumeric(Res):
        return
    Test_Language = Val(Res)
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    # 23.06.20:
    if X02.ActiveSheet.Name == 'Multiplexer':
        X02.Sheets(M01.MAIN_SH).Select()
    # Otherwise the standard sheet description is moved to the Multiplexewr sheet for some reasons
    Update_Language_in_All_Sheets()
    # Is also used in the Prog_Generator
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    # Loop over all userforms
    # 11.06.20:
    for c in PG.ThisWorkbook.VBProject.VBComponents:
        # Enable: Excel Options > Trust Centre > Macro Settings > Trust access to the VBA Project object model
        if c.Type == 3:
            # VB2PY (UntranslatedCode) On Error GoTo Err_Change_Language_in_Dialog
            if c.Designer is None:
                # Dialog is already loaded
                # 23.06.20: Prevent crash if teh dialog was already open
                Change_Language_in_Dialog(UserForms(Get_Dialog_Nr(c.Name)))
            else:
                Change_Language_in_Dialog(c.Designer)
            # VB2PY (UntranslatedCode) On Error GoTo 0
    return
    X02.MsgBox('Internal error: Error changing the language in the dialog \'' + c.Name + '\'' + vbCr + 'For some reasons \'c.Designer\' is nothing when the dialog was called before.' + 'All variables are cleared now. Please try it again.')
    M30.EndProg()
    # Clear all variables
    #'# VB2PY (CheckDirective) VB2PY directive Ignore Text
    Set_Tast_Txt_Var(ForceUpdate=True)
    # 06.03.20:
    #UserForm_DialogGuide1.Show
    # Debug

def Test_Userform():
    c = Object()
    for c in PG.ThisWorkbook.VBProject.VBComponents:
        # Enable: Excel Options > Trust Centre > Macro Settings > Trust access to the VBA Project object model
        if c.Name == 'MainMenu_Form':
            if c.Type == 3:
                X02.MsgBox(c.Name)

# VB2PY (UntranslatedCode) Option Explicit
