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
 The seach expression '[!r]("'  and ' "'   (Without ')
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



 Language specific messages in the example sheets                          ' 11.02.20:
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



 Debuging with othwer languages
 If this flag is not set the language could be changed
 temporary with the function "Test_Translations()"
--------------------------------------------------------------------------------------------------------------
UT-------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
-------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on 0
-------------------------------------------------
--------------------------------------------------------------------
UT--------------------------------------------
----------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
-----------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
------------------------------------------
----------------------------------------------
---------------------------------------------
UT---------------------------------
-------------------------------------------------------------
UT-------------------------------------
-------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on True
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
__Simulate_Language = - 1
__Check_Languages = Boolean()
__Test_Language = Integer()
Red_T = String()
Green_T = String()
OnOff_T = String()
Tast_T = String()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def __Update_Language_in_Sheet(Sh, DestLang):
    fn_return_value = None
    LSh = Worksheet()
    #--------------------------------------------------------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    Make_sure_that_Col_Variables_match(Sh)
    #Set OldSel = Selection
    LSh = ThisWorkbook.Sheets(LANGUAGES_SH)
    with_0 = Sh
    # Check if the language has to be changed by comparing the first string
    # Check the actual used language in the sheet
    ActLang = - 1
    FirstMsg = with_0.Range(LSh.Cells(FirstLangRow, LangParamCol))
    for c in vbForRange(FirstLangCol, LastUsedColumnInRow(LSh, FirstLangRow)):
        if FirstMsg == LSh.Cells(FirstLangRow, c):
            ActLang = c - FirstLangCol
            break
    if ActLang == - 1:
        MsgBox('Error: \'' + FirstMsg + '\' not found in the \'Languages\' sheet', vbCritical, 'Language Error')
        return fn_return_value
    if ( ActLang == DestLang ) :
        return fn_return_value
        # Language is correct
    # Unprotect the sheet
    WasProtected = Sh.ProtectContents
    if WasProtected:
        Sh.Unprotect()
    # Debug
    MaxLang = LastUsedColumnInRow(LSh, FirstLangRow) - FirstLangCol
    if DestLang == - 1:
        DestLang = ActLang + 1
        if ActLang >= MaxLang:
            DestLang = 0
    # Replace the texts
    LangCol = FirstLangCol + DestLang
    for r in vbForRange(FirstLangRow, LastUsedRowIn(LSh)):
        Param = LSh.Cells(r, LangParamCol)
        if Param != '':
            tmp = LSh.Cells(r, LangCol)
            select_0 = LSh.Cells(r, LangType_Col)
            if (select_0 == ''):
                pass
            elif (select_0 == 'Cell'):
                with_0.Range[Param].FormulaR1C1 = tmp
                ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
            elif (select_0 == 'Cell_DCC'):
                if Page_ID == 'DCC':
                    with_0.Range[Param].FormulaR1C1 = tmp
                    # Cell values and formulas
            elif (select_0 == 'Cell_SX'):
                if Page_ID == 'Selectrix':
                    with_0.Range[Param].FormulaR1C1 = tmp
                    # Cell values and formulas
            elif (select_0 == 'Cell_CAN'):
                if Page_ID == 'CAN':
                    with_0.Range[Param].FormulaR1C1 = tmp
                    # Cell values and formulas
            elif (select_0 == 'NumberFormat'):
                with_0.Range[Param].NumberFormat = tmp
            elif (select_0 == 'Button'):
                ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
                with_0.Shapes.Range(Array(Param)).Select()
                Selection.Characters.Text = tmp
            elif (select_0 == 'Comment'):
                with_1 = with_0.Range(Param).Comment
                with_1.Text(Text=Replace(tmp, vbLf, Chr(10)))
                with_1.Shape.TextFrame.Characters[1, Len(tmp)].Font.Bold = False
                ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
            elif (select_0 == 'Comment_DCC'):
                if Page_ID == 'DCC':
                    with_2 = with_0.Range(Param).Comment
                    with_2.Text(Text=Replace(tmp, vbLf, Chr(10)))
                    with_2.Shape.TextFrame.Characters[1, Len(tmp)].Font.Bold = False
            elif (select_0 == 'Comment_SX'):
                if Page_ID == 'Selectrix':
                    with_3 = with_0.Range(Param).Comment
                    with_3.Text(Text=Replace(tmp, vbLf, Chr(10)))
                    with_3.Shape.TextFrame.Characters[1, Len(tmp)].Font.Bold = False
            elif (select_0 == 'Comment_CAN'):
                if Page_ID == 'CAN':
                    with_4 = with_0.Range(Param).Comment
                    with_4.Text(Text=Replace(tmp, vbLf, Chr(10)))
                    with_4.Shape.TextFrame.Characters[1, Len(tmp)].Font.Bold = False
            elif (select_0 == 'ErrorMessage'):
                with_0.Range[Param].Validation.ErrorMessage = tmp
            elif (select_0 == 'ErrorTitle'):
                with_0.Range[Param].Validation.ErrorTitle = tmp
                # ToDo Warnungen
    if WasProtected:
        Protect_Active_Sheet()
    #OldSel.Select
    fn_return_value = True
    #Debug.Print "Updated Language in " & Sh.Name ' Debug
    return fn_return_value

def __Test_Update_Language_in_Sheet():
    OldEvents = Boolean()

    OldUpdate = Boolean()
    #UT-------------------------------------------------------
    # Switches to the next language
    OldEvents = Application.EnableEvents
    OldUpdate = Application.ScreenUpdating
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    __Update_Language_in_Sheet()(ActiveSheet, - 1)
    Application.EnableEvents = OldEvents
    Application.ScreenUpdating = OldUpdate

def __Update_Language_in_Config_Sheet(DestLang):
    fn_return_value = None
    Row = Long()

    Col = Long()

    Sh = Worksheet()
    #-------------------------------------------------------------------------------
    Col = 2
    Sh = ThisWorkbook.Sheets(ConfigSheet)
    with_5 = Sh
    if with_5.Range('A1') == DestLang:
        return fn_return_value
        # Pos A1 contains the actual language number (White text on white ground)
    for Row in vbForRange(1, LastUsedRowIn(Sh)):
        with_6 = with_5.Cells(Row, Col)
        if with_6.Value != '':
            with_6.Value = Get_Language_Str(with_6.Value)
        if not with_6.Comment is None:
            with_6.Comment.Text(Text=Get_Language_Str(with_6.Comment.Text))
    # Special cells
    with_7 = with_5.Range('Lib_Installed_other')
    if with_7.Value != '':
        with_7.Value = Get_Language_Str(with_7.Value)
    with_5.Range['A1'] = DestLang
    fn_return_value = True
    return fn_return_value

def __Test_Update_Language_in_Config_Sheet():
    #-------------------------------------------------
    __Test_Language = 0
    __Check_Languages = 1
    Debug.Print(__Update_Language_in_Config_Sheet(__Test_Language))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def __Activate_Language_in_Example_Sheet(Sh):
    o = Variant()

    ActLanguage = Integer()

    LanguageNr = Integer()
    #--------------------------------------------------------------------
    ActLanguage = Get_ExcelLanguage()
    for o in Sh.Shapes:
        if (o.Type == msoTextBox):
            if Left(o.Name, Len('Goto_Graph')) != 'Goto_Graph' and o.Name != 'InternalTextBox':
                if Left(o.AlternativeText, Len('Language: ')) == 'Language: ':
                    LanguageNr = Val(Mid(o.AlternativeText, Len('Language: ') + 1))
                    o.Visible = ( LanguageNr == ActLanguage )
        elif (o.Type == msoFormControl):
            if o.AlternativeText != '_Internal_Button_' and o.AlternativeText != 'Add_Del_Button':
                if Left(o.AlternativeText, Len('Language: ')) == 'Language: ':
                    LanguageNr = Val(Mid(o.AlternativeText, Len('Language: ') + 1))
                    o.Visible = ( LanguageNr == ActLanguage )
                #ToDo     Print_Typ_and_Pos FileNr, "msoFormControl", o, o.AlternativeText & Chr(pcfSep) & Replace(o.OnAction, ThisWorkbook.Name & "!", "")
            ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
            # Translate the buttons.
            # Attention: This part is not working in the Pattern_Configurator.
            #            ==> It overwrites the Button texts ;-(
            #            The problem is, that the buttons already had an alternative text. (05.06.20: Deleted the text)
            #            => At the moment (05.06.20) the Buttons "Import vom Prog. Gen.",
            #               "Programm Genarator" and "Zum Modul schicken" are not translated
        elif (o.Type == msoOLEControlObject):
            if o.AlternativeText == '':
                o.AlternativeText = o.DrawingObject.Object.Caption
                # Store the original text
            o.DrawingObject.Object.Caption = Get_Language_Str(o.AlternativeText)
            # Todo: Change also the activation key

def __Activate_Language_in_Active_Sheet():
    #UT--------------------------------------------
    __Activate_Language_in_Example_Sheet(ActiveSheet)

def __Update_Language_in_All_Sheets():
    OldEvents = Boolean()

    OldUpdate = Boolean()

    OldSheet = Worksheet()

    Sh = Variant()

    DestLang = Integer()

    Initialized = Boolean()
    #----------------------------------
    # Set the language of all sheets to the active display language in excel
    OldSheet = ActiveSheet
    OldEvents = Application.EnableEvents
    OldUpdate = Application.ScreenUpdating
    Application.EnableEvents = False
    Application.ScreenUpdating = False
    DestLang = Get_ExcelLanguage()
    #DestLang = 1 ' debug
    for Sh in ThisWorkbook.Sheets:
        #If sh.Name <> LANGUAGES_SH And sh.Name <> GOTO_ACTIVATION_SH And sh.Name <> PAR_DESCRIPTION_SH Then ' 20.01.20: Old
        ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
        if Sh.Name == MAIN_SH or Is_Normal_Data_Sheet(Sh.Name, Get_Language_Str('übersetzt')):
            if not Initialized:
                StatusMsg_UserForm.Set_Label(Get_Language_Str('Umstellung der Sprache'))
                #12.02.20:
            StatusMsg_UserForm.Set_ActSheet_Label(Sh.Name)
            if not Initialized:
                StatusMsg_UserForm.Show()
            Initialized = True
            # 07.03.20: sh.Activate ' Necessary for the button names ;-(
            ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
            if Sh.Name != 'Multiplexer':
                Translate_Standard_Description_Box_in_Sheet(Sh)
                if __Update_Language_in_Sheet(Sh, DestLang) == False and Sh.Name == MAIN_SH:
                    break
            ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
            if Is_Data_Sheet(Sh):
                if __Update_Language_in_Sheet(Sh, DestLang):
                    Translate_Example_Texts_in_Sheet(Sh)
            __Activate_Language_in_Example_Sheet(Sh)
    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    __Update_Language_in_Config_Sheet()(DestLang)
    Unload(StatusMsg_UserForm)
    if not OldSheet is None:
        OldSheet.Activate()
    Application.EnableEvents = OldEvents
    Application.ScreenUpdating = OldUpdate

def Check_SIMULATE_LANGUAGE():
    #-----------------------------------
    if __Simulate_Language >= 0:
        MsgBox('Attention the compiler switch \'SIMULATE_LANGUAGE\' is set to ' + __Simulate_Language + vbCr + 'This is used to test the languages. It must be disabled in the release version!', vbInformation)

def __Get_Language_Def():
    fn_return_value = None
    LangStr = String()
    #------------------------------------------
    LangStr = ThisWorkbook.Sheets(ConfigSheet).Range('Language_Def')
    if IsNumeric(LangStr):
        fn_return_value = Val(LangStr)
    else:
        fn_return_value = - 1
    return fn_return_value

def Set_Language_Def(LanguageNr):
    #----------------------------------------------
    ThisWorkbook.Sheets[ConfigSheet].Range['Language_Def'] = LanguageNr

def Get_ExcelLanguage():
    fn_return_value = None
    Simulate_Language = Long()
    #---------------------------------------------
    # Return a number corrosponding to the actual language used in excel
    #  0 = German
    #  1 = English and all other languages
    #  2 = Dutch
    #  3 = French
    #  4 = Italian    (Only in the Prog_Generator)
    #  5 = Spain        "
    # The number must match to the position in the language strings in M6_Language_Constants
    #
    # Is working if the office language is changed or the Window language
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    if Simulate_Language >= 0:
        fn_return_value = Simulate_Language
        return fn_return_value
    if __Check_Languages:
        fn_return_value = __Test_Language
        return fn_return_value
    fn_return_value = 1
    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    Simulate_Language = __Get_Language_Def()
    if Simulate_Language >= 0:
        fn_return_value = Simulate_Language
        return fn_return_value
    #Debug.Print "Achtung: Get_ExcelLanguage() liefert immer 1"
    #Exit Function
    select_2 = Application.LanguageSettings.LanguageID(msoLanguageIDUI)
# Language ID's: https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2007/aa432635(v=office.12)
    if (select_2 == msoLanguageIDGerman) or (select_2 == msoLanguageIDGermanAustria) or (select_2 == msoLanguageIDGermanLiechtenstein) or (select_2 == msoLanguageIDGermanLuxembourg) or (select_2 == msoLanguageIDSwissGerman):
        fn_return_value = 0
    elif (select_2 == msoLanguageIDDutch) or (select_2 == msoLanguageIDBelgianDutch):
        fn_return_value = 2
    elif (select_2 == msoLanguageIDFrench) or (select_2 == msoLanguageIDBelgianFrench) or (select_2 == msoLanguageIDFrenchCameroon) or (select_2 == msoLanguageIDFrenchCanadian) or (select_2 == msoLanguageIDFrenchCotedIvoire) or (select_2 == msoLanguageIDFrenchHaiti) or (select_2 == msoLanguageIDFrenchLuxembourg) or (select_2 == msoLanguageIDFrenchMali) or (select_2 == msoLanguageIDFrenchMonaco) or (select_2 == msoLanguageIDFrenchMorocco) or (select_2 == msoLanguageIDFrenchReunion) or (select_2 == msoLanguageIDFrenchSenegal) or (select_2 == msoLanguageIDFrenchWestIndies) or (select_2 == msoLanguageIDSwissFrench):
        fn_return_value = 3
    elif (select_2 == msoLanguageIDItalian) or (select_2 == msoLanguageIDSwissItalian):
        fn_return_value = 4
    elif (select_2 == msoLanguageIDSpanish) or (select_2 == msoLanguageIDSpanishArgentina) or (select_2 == msoLanguageIDSpanishBolivia) or (select_2 == msoLanguageIDSpanishChile) or (select_2 == msoLanguageIDSpanishColombia) or (select_2 == msoLanguageIDSpanishCostaRica) or (select_2 == msoLanguageIDSpanishDominicanRepublic) or (select_2 == msoLanguageIDSpanishEcuador) or (select_2 == msoLanguageIDSpanishElSalvador) or (select_2 == msoLanguageIDSpanishGuatemala) or (select_2 == msoLanguageIDSpanishHonduras) or (select_2 == msoLanguageIDSpanishModernSort) or (select_2 == msoLanguageIDSpanishNicaragua) or (select_2 == msoLanguageIDSpanishPanama) or (select_2 == msoLanguageIDSpanishParaguay) or (select_2 == msoLanguageIDSpanishPeru) or (select_2 == msoLanguageIDSpanishPuertoRico) or (select_2 == msoLanguageIDSpanishUruguay) or (select_2 == msoLanguageIDSpanishVenezuela) or (select_2 == msoLanguageIDMexicanSpanish):
        fn_return_value = 5
    #05.07.20: Get_ExcelLanguage = 1     '  For testing by Misha 2-7-2020.
    return fn_return_value

def __Test_Get_ExcelLanguage():
    #UT---------------------------------
    Debug.Print('Get_ExcelLanguage()=' + Get_ExcelLanguage())

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
def __Find_Cell_Pos_by_Name(Desc):
    fn_return_value = None
    LSh = Worksheet()

    Res = Variant()
    #-------------------------------------------------------------
    # Find the given Desc in the language sheet and return the
    # destination position as string.
    #
    # If Desc is not found "" is returned
    LSh = ThisWorkbook.Sheets(LANGUAGES_SH)
    with_8 = LSh
    Res = LSh.Cells.Find(What= Desc, After= with_8.Range('A1'), LookIn= xlFormulas, LookAt= xlPart, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False)
    if not Res is None:
        fn_return_value = with_8.Cells(Res.Row, LangParamCol).Value
    return fn_return_value

def __Test_Find_Cell_Pos_by_Name():
    #UT-------------------------------------
    Debug.Print('Find_Cell_Pos_by_Name("Bits pro Wert:")=\'' + __Find_Cell_Pos_by_Name('Bits pro Wert:') + '\'')
    Debug.Print('Find_Cell_Pos_by_Name("Bits per value:")=\'' + __Find_Cell_Pos_by_Name('Bits per value:') + '\'')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
def __Get_German_Name(Desc):
    fn_return_value = None
    LSh = Worksheet()

    Res = Variant()
    #-------------------------------------------------------
    LSh = ThisWorkbook.Sheets(LANGUAGES_SH)
    with_9 = LSh
    Res = LSh.Cells.Find(What= Desc, After= with_9.Range('A1'), LookIn= xlFormulas, LookAt= xlPart, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False)
    if not Res is None:
        fn_return_value = with_9.Cells(Res.Row, FirstLangCol).Value
    else:
        MsgBox('Error \'' + Desc + '\' not found in \'Get_German_Name\'', vbCritical, 'Error')
    return fn_return_value

def __Add_Entry_to_Languages_Sheet(GermanTxt):
    #------------------------------------------------------------
    if Get_ExcelLanguage() == 0:
        LSh = ThisWorkbook.Sheets(LANGUAGES_SH)
        with_10 = LSh
        Row = LastUsedRowIn(LSh) + 1
        with_10.Cells[Row, FirstLangCol] = GermanTxt

def __Debug_Find_Diff(S1, s2):
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
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At=xlPart - ByVal 
def Find_Language_Str_Row(Desc, Look_At=xlPart):
    fn_return_value = None
    LSh = Worksheet()

    Res = Variant()
    #--------------------------------------------------------------------------------------------------------------
    LSh = ThisWorkbook.Sheets(LANGUAGES_SH)
    with_11 = LSh
    # VB2PY (UntranslatedCode) On Error Resume Next
    # Maximal length for the find command: 255
    Start = with_11.Range('A1')
    Desc = RTrim(Desc)
    while 1:
        if Len(Desc) > 90:
            Look_At = xlPart
        Res = LSh.Cells.Find(What= Left(Desc, 90), After= Start, LookIn= xlFormulas, LookAt= Look_At, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= True)
        if Look_At == xlPart and not IsEmpty(Res):
            Retry = ( RTrim(Res.Value) != RTrim(Desc) )  
            #Debug_Find_Diff Res.Value, Desc ' Debug
            if Retry:
                #If Len(Desc) >= 255 Then
                #   Debug.Print "Debug long string in Get_Language_Str"
                #End If
                Start = Res
                if FirstPos is None:
                    FirstPos = Res
                else:
                    if Res.Address == FirstPos.Address:
                        Retry = False
                        Res = None
        if not (Retry):
            break
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if not IsEmpty(Res):
        if not Res is None:
            fn_return_value = Res.Row
            ## VB2PY (CheckDirective) VB directive took path 1 on 0
            with_12 = Res.Interior
            with_12.PatternColorIndex = xlAutomatic
            with_12.Color = 5296274
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At=xlPart - ByVal 
def Get_Language_Str(Desc, GenError=False, Look_At=xlPart):
    fn_return_value = None
    Use_CrLf = Boolean()

    Res = String()
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # Replace the vbCr in the input string to be able to find in in the "Languages" sheet      ' 30.01.20:
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
        return fn_return_value
        # 23.01.20:
    Desc = Replace(Desc, '| ', '|')
    if InStr(Desc, vbCr + vbLf) > 0:
        Use_CrLf = True
        Desc = Replace(Desc, vbCr, '|')
    else:
        Desc = Replace(Desc, vbCr, '|' + vbLf)
    Res = __Get_Language_Str_Sub(Desc, GenError, Look_At)
    if Use_CrLf:
        fn_return_value = Replace(Res, '|', vbCr)
    else:
        fn_return_value = Replace(Res, '|' + vbLf, vbCr)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At - ByVal 
def __Get_Language_Str_Sub(Desc, GenError, Look_At):
    fn_return_value = None
    Row = Long()

    LSh = Worksheet()
    #-------------------------------------------------------------------------------------------------------------------
    # Find the given Desc in the language sheet and return the
    # string in the actual language
    #
    if IsNumeric(Desc):
        fn_return_value = Desc
        return fn_return_value
    Row = Find_Language_Str_Row(Desc, Look_At)
    LSh = ThisWorkbook.Sheets(LANGUAGES_SH)
    with_13 = LSh
    if Row > 0:
        fn_return_value = with_13.Cells(Row, FirstLangCol + Get_ExcelLanguage()).Value
        if __Get_Language_Str_Sub() != '':
            return fn_return_value
    # The language string was not found
    if GenError:
        MsgBox('Error translation missing in sheet \'Languages\' for:' + vbCr + '  \'' + Desc + '\'', vbCritical, 'Error: Translation missing')
    else:
        Debug.Print('*** Translation not found for:' + vbCr + Desc)
    if Row > 0:
        fn_return_value = with_13.Cells(Row, FirstLangCol + 1).Value
        # Use the Enlish text if available  ' 26.01.20:
    if __Get_Language_Str_Sub() == '':
        fn_return_value = Desc
    __Add_Entry_to_Languages_Sheet(Desc)
    return fn_return_value

def __Change_Lang_in_MultiPage(o):
    Pg = Variant()
    #-------------------------------------------------
    for Pg in o.Pages:
        #Pg.Caption = Replace(Get_Language_Str(Replace(Pg.Caption, vbCr, "|"), False, xlWhole), "|", vbCr)   ' Old 30.01.20:
        Pg.Caption = Get_Language_Str(Pg.Caption, False, xlWhole)

def __Change_Language_in_Dialog(dlg):
    o = Variant()
    #-------------------------------------------
    dlg.Caption = Get_Language_Str(dlg.Caption)
    for o in dlg.Controls:
        if o.ControlTipText != '':
            o.ControlTipText = Get_Language_Str(o.ControlTipText)
        #Debug.Print o.Name
        #If o.Name = "Label12" Then
        #   Debug.Print "Debug"
        #End If
        # VB2PY (UntranslatedCode) On Error Resume Next
        if Left(o.Name, Len('MultiPage')) == 'MultiPage':
            __Change_Lang_in_MultiPage(o)
        elif Left(o.Name, Len('ListBox')) == 'ListBox':
            # There is no constant text in the ListBox dialog. It is loaded dymanicaly
            pass
        elif o.Caption != 'by Hardi' and Left(o.Caption, 4) != 'http' and o.Caption != '*' and o.Caption != 'J':
            #o.Caption = Replace(Get_Language_Str(Replace(o.Caption, vbCr, "|"), False, xlWhole), "|", vbCr)   ' 30.01.20: Old:
            o.Caption = Get_Language_Str(o.Caption, False, xlWhole)
        # VB2PY (UntranslatedCode) On Error GoTo 0

def __Test_Change_Language_in_Dialog():
    #UT---------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    Copy_Select_GotoAct_Form.Show()

def Set_Tast_Txt_Var(ForceUpdate=VBMissingArgument):
    #-----------------------------------------------------------
    if ForceUpdate or Red_T == '':
        Red_T = Get_Language_Str('Rot')
        Green_T = Get_Language_Str('Grün')
        OnOff_T = Get_Language_Str('AnAus')
        Tast_T = Get_Language_Str('Tast')

def __Get_Dialog_Nr(Name):
    fn_return_value = None
    o = Variant()

    Nr = Long()
    #-----------------------------------------------------
    # Get the number of a loaded dialog
    # Generate an error message and abort the progra if the dialog is not available
    for o in UserForms:
        if o.Name == Name:
            fn_return_value = Nr
            return fn_return_value
        Nr = Nr + 1
    MsgBox('Internal Error: The Dialog \'' + Name + '\' is not loaded for some reasons', vbCritical, 'Internal Error')
    EndProg()
    return fn_return_value

def __Test_Translations():
    Res = String()

    c = Object()
    #UT----------------------------
    # Check it the translation works correct
    __Check_Languages = True
    Debug.Print(vbCr + '-------------------------------------------')
    Res = InputBox('Input the Language number' + vbCr + ' 0 = German' + vbCr + ' 1 = English' + vbCr + ' 2 = Dutch' + vbCr + ' 3 = French' + vbCr + ' 4 = Italian' + vbCr + ' 5 = Spain')
    if not IsNumeric(Res):
        return
    __Test_Language = Val(Res)
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    if ActiveSheet.Name == 'Multiplexer':
        Sheets(MAIN_SH).Select()
        # Otherwise the standard sheet description is moved to the Multiplexewr sheet for some reasons
    __Update_Language_in_All_Sheets()
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    for c in ThisWorkbook.VBProject.VBComponents:
        if c.Type == 3:
            # VB2PY (UntranslatedCode) On Error GoTo Err_Change_Language_in_Dialog
            if c.Designer is None:
                __Change_Language_in_Dialog(UserForms(__Get_Dialog_Nr(c.Name)))
            else:
                __Change_Language_in_Dialog(c.Designer)
            # VB2PY (UntranslatedCode) On Error GoTo 0
    return
    MsgBox('Internal error: Error changing the language in the dialog \'' + c.Name + '\'' + vbCr + 'For some reasons \'c.Designer\' is nothing when the dialog was called before.' + 'All variables are cleared now. Please try it again.')
    EndProg()
    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    __Change_Language_in_Dialog(Select_ProgGen_Dest_Form)
    __Change_Language_in_Dialog(Select_ProgGen_Src_Form)
    __Change_Language_in_Dialog(SelectMacros_Form)
    __Change_Language_in_Dialog(StatusMsg_UserForm)
    __Change_Language_in_Dialog(UserForm_Connector)
    __Change_Language_in_Dialog(UserForm_Description)
    __Change_Language_in_Dialog(UserForm_DialogGuide1)
    __Change_Language_in_Dialog(UserForm_Header_Created)
    __Change_Language_in_Dialog(UserForm_House)
    __Change_Language_in_Dialog(UserForm_Options)
    __Change_Language_in_Dialog(UserForm_Other)
    __Change_Language_in_Dialog(UserForm_Protokoll_Auswahl)
    __Change_Language_in_Dialog(UserForm_Select_Typ_DCC)
    __Change_Language_in_Dialog(UserForm_Select_Typ_SX)
    __Change_Language_in_Dialog(Wait_CheckColors_Form)
    __Change_Language_in_Dialog(Import_Hide_Unhide)
    __Change_Language_in_Dialog(Select_COM_Port_UserForm)
    assert False, '# UNTRANSLATED VB LINE #795 [#End If]'
    Set_Tast_Txt_Var(ForceUpdate=True)
    #UserForm_DialogGuide1.Show ' Debug

def __Test_Userform():
    c = Object()
    for c in ThisWorkbook.VBProject.VBComponents:
        if c.Name == 'MainMenu_Form':
            if c.Type == 3:
                MsgBox(c.Name)

# VB2PY (UntranslatedCode) Option Explicit
