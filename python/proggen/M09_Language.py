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

# fromx proggen.M02_Public import *

# fromx proggen.M28_divers import *
# fromx proggen.M30_Tools import *
# fromx proggen.M09_Translate_Examples import *

# fromx proggen.M80_Create_Mulitplexer import *

from ExcelAPI.XLC_Excel_Consts import *

import ExcelAPI.XLW_Workbook as P01

#import proggen.M09_Translate_Examples as M09TL

import proggen.M02_Public as M02
#import proggen.M02_Scripting as Scripting
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M06_Write_Header as M06
#import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
#import proggen.M09_Language as M09
#import proggen.M09_Translate_Examples as M09TE
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M40_ShellandWait as M40
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Mulitplexer as M80
import mlpyproggen.Prog_Generator as PG


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
  6 = Danish       "
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
     The "Alternativtext" mut contain the keyword "Language:"
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

Virtual_Channel_T = "V"         # 18.02.22 Juergen


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def __Update_Language_in_Sheet(Sh, DestLang):
    _ret = False
    LSh:P01.CWorksheet() = None
    #--------------------------------------------------------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    M25.Make_sure_that_Col_Variables_match(Sh)
    #Set OldSel = Selection
    LSh = PG.ThisWorkbook.Sheets(M02.LANGUAGES_SH)
    _with0 = Sh
    # Check if the language has to be changed by comparing the first string
    # Check the actual used language in the sheet
    ActLang = - 1
    FirstMsg = _with0.Range(LSh.Cells(FirstLangRow, LangParamCol))
    for c in vbForRange(FirstLangCol, M30.LastUsedColumnInRow(LSh, FirstLangRow)):
        if FirstMsg == LSh.Cells(FirstLangRow, c):
            ActLang = c - FirstLangCol
            break
    if ActLang == - 1:
        P01.MsgBox(r'Error:"'  + FirstMsg + r'" not found in the "Languages" sheet', vbCritical, r'Language Error')
        return _ret
    if ( ActLang == DestLang ) :
        return _ret
        # Language is correct
    # Unprotect the sheet
    WasProtected = Sh.ProtectContents
    if WasProtected:
        Sh.Unprotect()
    # Debug
    MaxLang = M30.LastUsedColumnInRow(LSh, FirstLangRow) - FirstLangCol
    if DestLang == - 1:
        DestLang = ActLang + 1
        if ActLang >= MaxLang:
            DestLang = 0
    # Replace the texts
    LangCol = FirstLangCol + DestLang
    for r in vbForRange(FirstLangRow, M30.LastUsedRowIn(LSh)):
        Param = LSh.Cells(r, LangParamCol)
        if Param != r'':
            Tmp = LSh.Cells(r, LangCol)
            _select0 = LSh.Cells(r, LangType_Col)
            if (_select0 == r''):
                pass
            elif (_select0 == r'Cell'):
                _with0.Range[Param].FormulaR1C1 = Tmp
                ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
            elif (_select0 == r'Cell_DCC'):
                if M25.Page_ID == r'DCC':
                    _with0.Range[Param].FormulaR1C1 = Tmp
                    # Cell values and formulas
            elif (_select0 == r'Cell_SX'):
                if M25.Page_ID == r'Selectrix':
                    _with0.Range[Param].FormulaR1C1 = Tmp
                    # Cell values and formulas
            elif (_select0 == r'Cell_CAN'):
                if M25.Page_ID == r'CAN':
                    _with0.Range[Param].FormulaR1C1 = Tmp
                    # Cell values and formulas
            elif (_select0 == r'NumberFormat'):
                _with0.Range[Param].NumberFormat = Tmp
            elif (_select0 == r'Button'):
                ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
                _with0.Shapes.Range(Array(Param)).Select()
                P01.Selection.Characters.Text = Tmp
            elif (_select0 == r'Comment'):
                _with1 = _with0.Range(Param).Comment
                _with1.Text(Text=Replace(Tmp, vbLf, Chr(10)))
                _with1.Shape.TextFrame.Characters[1, Len(Tmp)].Font.Bold = False
                ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
            elif (_select0 == r'Comment_DCC'):
                if M25.Page_ID == r'DCC':
                    if not _with0.Range(Param).Comment is None:
                        _with2 = _with0.Range(Param).Comment
                        _with2.Text(Text=Replace(Tmp, vbLf, Chr(10)))
                        _with2.Shape.TextFrame.Characters[1, Len(Tmp)].Font.Bold = False
            elif (_select0 == r'Comment_SX'):
                if M25.Page_ID == r'Selectrix':
                    if not _with0.Range(Param).Comment is None:
                        _with3 = _with0.Range(Param).Comment
                        _with3.Text(Text=Replace(Tmp, vbLf, Chr(10)))
                        _with3.Shape.TextFrame.Characters[1, Len(Tmp)].Font.Bold = False
            elif (_select0 == r'Comment_CAN'):
                if M25.Page_ID == r'CAN':
                    if not _with0.Range(Param).Comment is None:
                        _with4 = _with0.Range(Param).Comment
                        _with4.Text(Text=Replace(Tmp, vbLf, Chr(10)))
                        _with4.Shape.TextFrame.Characters[1, Len(Tmp)].Font.Bold = False
            elif (_select0 == r'ErrorMessage'):
                _with0.Range[Param].Validation.ErrorMessage = Tmp
            elif (_select0 == r'ErrorTitle'):
                _with0.Range[Param].Validation.ErrorTitle = Tmp
                # ToDo Warnungen
    if WasProtected:
        M30.Protect_Active_Sheet()
    #OldSel.Select
    _ret = True
    #Debug.Print "Updated Language in " & Sh.Name ' Debug
    return _ret

def __Test_Update_Language_in_Sheet():
    OldEvents = Boolean()

    OldUpdate = Boolean()
    #UT-------------------------------------------------------
    # Switches to the next language
    OldEvents = P01.Application.EnableEvents
    OldUpdate = P01.Application.ScreenUpdating
    P01.Application.EnableEvents = False
    P01.Application.ScreenUpdating = False
    __Update_Language_in_Sheet(P01.ActiveSheet, - 1)
    P01.Application.EnableEvents = OldEvents
    P01.Application.ScreenUpdating = OldUpdate

def __Update_Language_in_Config_Sheet(DestLang):
    _ret = False
    Row = int()

    Col = int()

    Sh = P01.CWorksheet()
    #-------------------------------------------------------------------------------
    Col = 2
    Sh = PG.ThisWorkbook.Sheets(M02.ConfigSheet)
    _with5 = Sh
    if _with5.Range(r'A1') == DestLang:
        return _ret
        # Pos A1 contains the actual language number (White text on white ground)
    for Row in vbForRange(1, M30.LastUsedRowIn(Sh)):
        _with6 = _with5.Cells(Row, Col)
        if _with6.Value != r'':
            _with6.Value = Get_Language_Str(_with6.Value)
        if not _with6.Comment is None:
            _with6.Comment.Text(Text=Get_Language_Str(_with6.Comment.Text))
    # Special cells
    _with7 = _with5.Range(r'Lib_Installed_other')
    if _with7.Value != r'':
        _with7.Value = Get_Language_Str(_with7.Value)
    _with5.Range[r'A1'] = DestLang
    _ret = True
    return _ret

def __Test_Update_Language_in_Config_Sheet():
    #-------------------------------------------------
    global __Test_Language, __Check_Languages
    __Test_Language = 0
    __Check_Languages = 1
    Debug.Print(__Update_Language_in_Config_Sheet(__Test_Language))

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def __Activate_Language_in_Example_Sheet(Sh):
    #o = Variant()

    #ActLanguage = Integer()

    #LanguageNr = Integer()
    #--------------------------------------------------------------------
    ActLanguage = Get_ExcelLanguage()
    for o in Sh.Shapes:
        _select1 = o.Type
        if (_select1 == msoTextBox):
            if Left(o.Name, Len(r'Goto_Graph')) != r'Goto_Graph' and o.Name != r'InternalTextBox':
                if Left(o.AlternativeText, Len(r'Language: ')) == r'Language: ':
                    LanguageNr = P01.val(Mid(o.AlternativeText, Len(r'Language: ') + 1))
                    o.Visible = ( LanguageNr == ActLanguage )
        elif (_select1 == msoFormControl):
            if o.AlternativeText != r'_Internal_Button_' and o.AlternativeText != r'Add_Del_Button':
                if Left(o.AlternativeText, Len(r'Language: ')) == r'Language: ':
                    LanguageNr = P01.val(Mid(o.AlternativeText, Len(r'Language: ') + 1))
                    o.Visible = ( LanguageNr == ActLanguage )
                #ToDo     Print_Typ_and_Pos FileNr, "msoFormControl", o, o.AlternativeText & Chr(pcfSep) & Replace(o.OnAction, ThisWorkbook.Name & "!", "")
            ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
            # Translate the buttons.
            # Attention: This part is not working in the Pattern_Configurator.
            #            ==> It overwrites the Button texts ;-(
            #            The problem is, that the buttons already had an alternative text. (05.06.20: Deleted the text)
            #            => At the moment (05.06.20) the Buttons "Import vom Prog. Gen.",
            #               "Programm Genarator" and "Zum Modul schicken" are not translated
        elif (_select1 == msoOLEControlObject):
            if o.AlternativeText == r'':
                o.AlternativeText = o.DrawingObject.Object.Caption
                # Store the original text
            o.DrawingObject.Object.Caption = Get_Language_Str(o.AlternativeText)
            # Todo: Change also the activation key

def __Activate_Language_in_Active_Sheet():
    #UT--------------------------------------------
    __Activate_Language_in_Example_Sheet(P01.ActiveSheet)

def __Update_Language_in_All_Sheets():
    return #*HL
    OldEvents = Boolean()

    OldUpdate = Boolean()

    OldSheet = P01.CWorksheet()

    Sh = P01.CWorksheet("")

    DestLang = Integer()

    Initialized = Boolean()
    #----------------------------------
    # Set the language of all sheets to the active display language in excel
    OldSheet = P01.ActiveSheet
    OldEvents = P01.Application.EnableEvents
    OldUpdate = P01.Application.ScreenUpdating
    P01.Application.EnableEvents = False
    P01.Application.ScreenUpdating = False
    DestLang = Get_ExcelLanguage()
    #DestLang = 1 ' debug
    for Sh in PG.ThisWorkbook.sheets:
        #If sh.Name <> LANGUAGES_SH And sh.Name <> GOTO_ACTIVATION_SH And sh.Name <> PAR_DESCRIPTION_SH Then ' 20.01.20: Old
        ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
        if Sh.Name == M02.START_SH or M28.Is_Data_Sheet(Sh.Name, Get_Language_Str(r'übersetzt')):
            if not Initialized:
                StatusMsg_UserForm.Set_Label(Get_Language_Str(r'Umstellung der Sprache'))
                #12.02.20:
            StatusMsg_UserForm.Set_ActSheet_Label(Sh.Name)
            if not Initialized:
                StatusMsg_UserForm.Show()
            Initialized = True
            # 07.03.20: sh.Activate ' Necessary for the button names ;-(
            ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
            if M28.Is_Data_Sheet(Sh):
                if __Update_Language_in_Sheet(Sh, DestLang):
                    Translate_Example_Texts_in_Sheet(Sh)
            __Activate_Language_in_Example_Sheet(Sh)
    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    __Update_Language_in_Config_Sheet(DestLang)
    M27.Update_Language_Name_Column_in_all_Sheets()
    #*HL U01.Unload(StatusMsg_UserForm)
    if not OldSheet is None:
        OldSheet.Activate()
    P01.Application.EnableEvents = OldEvents
    P01.Application.ScreenUpdating = OldUpdate

def Check_SIMULATE_LANGUAGE():
    #-----------------------------------
    global __Simulate_Language
    if __Simulate_Language >= 0:
        P01.MsgBox(r'Attention the compiler switch "SIMULATE_LANGUAGE" is set to ' + __Simulate_Language + vbCr + r'This is used to test the languages. It must be disabled in the release version!', vbInformation)

def __Get_Language_Def():
    _ret = False
    LangStr = String()
    #------------------------------------------
    LangStr = str(PG.ThisWorkbook.Sheets(M02.ConfigSheet).Range(r'Language_Def'))
    if IsNumeric(LangStr):
        _ret = P01.val(LangStr)
    else:
        _ret = - 1
    return _ret

def Set_Language_Def(LanguageNr):
    #----------------------------------------------
    PG.ThisWorkbook.Sheets[M02.ConfigSheet].Range[r'Language_Def'] = LanguageNr

def Get_ExcelLanguage():
    global __Simulate_Language,__Check_Languages
    _ret = 0
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
    
    if __Simulate_Language >= 0:
        _ret = __Simulate_Language
        return _ret
    if __Check_Languages:
        _ret = __Test_Language
        return _ret
    _ret = 1
    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    __Simulate_Language = __Get_Language_Def()
    if __Simulate_Language >= 0:
        _ret = __Simulate_Language
        return _ret
    #Debug.Print "Achtung: Get_ExcelLanguage() liefert immer 1"
    #Exit Function
    _select2 = P01.Application.LanguageSettings.LanguageID(msoLanguageIDUI)
# Language ID's: https://docs.microsoft.com/en-us/previous-versions/office/developer/office-2007/aa432635(v=office.12)
    if (_select2 == msoLanguageIDGerman) or (_select2 == msoLanguageIDGermanAustria) or (_select2 == msoLanguageIDGermanLiechtenstein) or (_select2 == msoLanguageIDGermanLuxembourg) or (_select2 == msoLanguageIDSwissGerman):
        _ret = 0
    elif (_select2 == msoLanguageIDDutch) or (_select2 == msoLanguageIDBelgianDutch):
        _ret = 2
    elif (_select2 == msoLanguageIDFrench) or (_select2 == msoLanguageIDBelgianFrench) or (_select2 == msoLanguageIDFrenchCameroon) or (_select2 == msoLanguageIDFrenchCanadian) or (_select2 == msoLanguageIDFrenchCotedIvoire) or (_select2 == msoLanguageIDFrenchHaiti) or (_select2 == msoLanguageIDFrenchLuxembourg) or (_select2 == msoLanguageIDFrenchMali) or (_select2 == msoLanguageIDFrenchMonaco) or (_select2 == msoLanguageIDFrenchMorocco) or (_select2 == msoLanguageIDFrenchReunion) or (_select2 == msoLanguageIDFrenchSenegal) or (_select2 == msoLanguageIDFrenchWestIndies) or (_select2 == msoLanguageIDSwissFrench):
        _ret = 3
    elif (_select2 == msoLanguageIDItalian) or (_select2 == msoLanguageIDSwissItalian):
        _ret = 4
    elif (_select2 == msoLanguageIDSpanish) or (_select2 == msoLanguageIDSpanishArgentina) or (_select2 == msoLanguageIDSpanishBolivia) or (_select2 == msoLanguageIDSpanishChile) or (_select2 == msoLanguageIDSpanishColombia) or (_select2 == msoLanguageIDSpanishCostaRica) or (_select2 == msoLanguageIDSpanishDominicanRepublic) or (_select2 == msoLanguageIDSpanishEcuador) or (_select2 == msoLanguageIDSpanishElSalvador) or (_select2 == msoLanguageIDSpanishGuatemala) or (_select2 == msoLanguageIDSpanishHonduras) or (_select2 == msoLanguageIDSpanishModernSort) or (_select2 == msoLanguageIDSpanishNicaragua) or (_select2 == msoLanguageIDSpanishPanama) or (_select2 == msoLanguageIDSpanishParaguay) or (_select2 == msoLanguageIDSpanishPeru) or (_select2 == msoLanguageIDSpanishPuertoRico) or (_select2 == msoLanguageIDSpanishUruguay) or (_select2 == msoLanguageIDSpanishVenezuela) or (_select2 == msoLanguageIDMexicanSpanish):
        _ret = 5
    elif (_select2 == msoLanguageIDDanish):
        _ret = 6
    return _ret

def __Test_Get_ExcelLanguage():
    #UT---------------------------------
    Debug.Print(r'Get_ExcelLanguage()=' + Get_ExcelLanguage())

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
def __Find_Cell_Pos_by_Name(Desc):
    _ret = False
    #LSh = P01.CWorksheet()

    #Res = Variant()
    #-------------------------------------------------------------
    # Find the given Desc in the language sheet and return the
    # destination position as string.
    #
    # If Desc is not found "" is returned
    LSh = PG.ThisWorkbook.Sheets(M02.LANGUAGES_SH)
    _with8 = LSh
    Res = LSh.Cells.Find(What= Desc, after= _with8.Range(r'A1'), LookIn= xlFormulas, LookAt= xlPart, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False)
    if not Res is None:
        _ret = _with8.Cells(Res.Row, LangParamCol).Value
    return _ret

def __Test_Find_Cell_Pos_by_Name():
    #UT-------------------------------------
    #Debug.Print(r'Find_Cell_Pos_by_Name("Bits pro Wert:")='' + __Find_Cell_Pos_by_Name(r'Bits pro Wert:') + r''')
    #Debug.Print(r'Find_Cell_Pos_by_Name("Bits per value:")='' + __Find_Cell_Pos_by_Name(r'Bits per value:') + r''')
    pass

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
def __Get_German_Name(Desc):
    _ret = ""
    #LSh = P01.CWorksheet()

    #Res = Variant()
    #-------------------------------------------------------
    LSh = PG.ThisWorkbook.Sheets(M02.LANGUAGES_SH)
    _with9 = LSh
    Res = LSh.Cells.Find(What= Desc, after= _with9.Range(r'A1'), LookIn= xlFormulas, LookAt= xlPart, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False)
    if not Res is None:
        _ret = _with9.Cells(Res.Row, FirstLangCol).Value
    else:
        P01.MsgBox(r'Error ' + Desc + r' not found in "Get_German_Name"', vbCritical, r'Error')
    return _ret

def __Add_Entry_to_Languages_Sheet(GermanTxt):
    #------------------------------------------------------------
    if Get_ExcelLanguage() == 0:
        LSh = PG.ThisWorkbook.Sheets(M02.LANGUAGES_SH)
        _with10 = LSh
        Row = M30.LastUsedRowIn(LSh) + 1
        _with10.CellDict[Row, FirstLangCol] = GermanTxt

def __Debug_Find_Diff(s1, s2):
    i = int()
    #------------------------------------------------------
    Debug.Print(r'Len:' + Len(s1) + r'  ' + Len(s2))
    for i in vbForRange(1, Len(s1)):
        if Mid(s1, i, 1) != Mid(s2, i, 1):
            Debug.Print(r'Different pos: ' + i)
            i = i - 3
            if i < 1:
                i = 1
            Debug.Print(Mid(s1, i - 3, 7))
            Debug.Print(Mid(s2, i - 3, 7))
            Debug.Print(Space(i - 1) + r'^')
            return
    Debug.Print(r'Strings are equal')

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At=xlPart - ByVal 
def Find_Language_Str_Row(Desc, Look_At=xlPart):
    _ret = ""
    #LSh = X02.Worksheet

    #Res = Variant()
    #--------------------------------------------------------------------------------------------------------------
    LSh = PG.ThisWorkbook.Sheets(M02.LANGUAGES_SH)
    _with11 = LSh
    # VB2PY (UntranslatedCode) On Error Resume Next
    # Maximal length for the find command: 255
    Start = LSh.Cells(1,1) #_with11.Range(r'A1')
    Desc = RTrim(Desc)
    #while 1:
    if Len(Desc) > 90:
        Look_At = xlPart
        Desc = Left(Desc, 90)
    #Res = LSh.Cells.Find(What= Left(Desc, 90), after= Start, LookIn= xlFormulas, LookAt= Look_At, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= True)
    Res=LSh.find_in_col_ret_row(Desc,FirstLangCol)
    #if Look_At == xlPart and not P01.IsEmpty(Res):
    #    Retry = ( RTrim(Res.Value) != RTrim(Desc) )  
    #    #Debug_Find_Diff Res.Value, Desc ' Debug
    #    if Retry:
            #If Len(Desc) >= 255 Then
            #   Debug.Print "Debug long string in Get_Language_Str"
            #End If
    #        Start = Res
    #        if FirstPos is None:
    #            FirstPos = Res
    #        else:
    #            if Res.Address == FirstPos.Address:
    #                Retry = False
    #                Res = None
    #if not (Retry):
    #    break
    if Res != None:
        return int(Res)
    else:
        return 0
        
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if not P01.IsEmpty(Res):
        if not Res is None:
            _ret = Res.Row
            ## VB2PY (CheckDirective) VB directive took path 1 on 0
            _with12 = Res.Interior
            _with12.PatternColorIndex = xlAutomatic
            _with12.Color = 5296274
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At=xlPart - ByVal 
def Get_Language_Str(Desc, GenError=False, Look_At=xlPart):
    
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
    Use_CrLf = False
    _ret = Desc
    if Desc == r'':
        return _ret
        # 23.01.20:
    Desc = Replace(Desc, "\n",vbCr)
    Desc = Replace(Desc, r'| ', r'|')
    if InStr(Desc, vbCr + vbLf) > 0:
        Use_CrLf = True
        Desc = Replace(Desc, vbCr, r'|')
    else:
        Desc = Replace(Desc, vbCr, r'|' + vbLf)
    Res = __Get_Language_Str_Sub(Desc, GenError, Look_At)
    if Use_CrLf:
        _ret = Replace(Res, r'|', vbCr)
    else:
        _ret = Replace(Replace(Res, r'|' + vbLf, vbCr), r'| ' + vbLf, vbCr)
    return _ret

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Desc - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Look_At - ByVal 
def __Get_Language_Str_Sub(Desc, GenError, Look_At):
    _ret = ""
    
    #-------------------------------------------------------------------------------------------------------------------
    # Find the given Desc in the language sheet and return the
    # string in the actual language
    #
    if IsNumeric(Desc):
        _ret = Desc
        return _ret
    
    LSh = PG.ThisWorkbook.Sheets(M02.LANGUAGES_SH)
    
    _ret = LSh.find_in_col_ret_col_val(Desc,FirstLangCol,FirstLangCol + Get_ExcelLanguage(),cache=True)
    
    if _ret:
        if _ret!="":
            return _ret
    else:
        _with13 = LSh
        Row = Find_Language_Str_Row(Desc, Look_At)
        if Row > 0:
            _ret = _with13.Cells(Row, FirstLangCol + Get_ExcelLanguage()).Value
            if __Get_Language_Str_Sub() != r'':
                return _ret
        # The language string was not found
        if GenError:
            P01.MsgBox(r'Error translation missing in sheet "Languages" for:' + vbCr + r'  '' + Desc + r''', vbCritical, r'Error: Translation missing')
        else:
            Debug.Print(r'*** Translation not found for:' + vbCr + Desc)
            
        # get English translation:
    _ret = LSh.find_in_col_ret_col_val(Desc,FirstLangCol,FirstLangCol+1)
    
    if _ret and _ret!="":
        return _ret
    else:
        return Desc
    
    if Row > 0:
        _ret = _with13.Cells(Row, FirstLangCol + 1).Value
        # Use the Enlish text if available  ' 26.01.20:
    if __Get_Language_Str_Sub() == r'':
        _ret = Desc
    __Add_Entry_to_Languages_Sheet(Desc)
    return _ret

def __Change_Lang_in_MultiPage(o):
    Pg = Variant()
    #-------------------------------------------------
    for Pg in o.Pages:
        #Pg.Caption = Replace(Get_Language_Str(Replace(Pg.Caption, vbCr, "|"), False, xlWhole), "|", vbCr)   ' Old 30.01.20:
        Pg.Caption = Get_Language_Str(Pg.Caption, False, xlWhole)

def __Change_Language_in_Dialog(dlg):
    #o = Variant()
    #-------------------------------------------
    dlg.Caption = Get_Language_Str(dlg.Caption)
    for o in dlg.Controls:
        if o.ControlTipText != r'':
            o.ControlTipText = Get_Language_Str(o.ControlTipText)
        #Debug.Print o.Name
        #If o.Name = "Label12" Then
        #   Debug.Print "Debug"
        #End If
        # VB2PY (UntranslatedCode) On Error Resume Next
        if Left(o.Name, Len(r'MultiPage')) == r'MultiPage':
            __Change_Lang_in_MultiPage(o)
        elif Left(o.Name, Len(r'ListBox')) == r'ListBox':
            # There is no constant text in the ListBox dialog. It is loaded dymanicaly
            pass
        elif o.Caption != r'by Hardi' and Left(o.Caption, 4) != r'http' and o.Caption != r'*' and o.Caption != r'J':
            #o.Caption = Replace(Get_Language_Str(Replace(o.Caption, vbCr, "|"), False, xlWhole), "|", vbCr)   ' 30.01.20: Old:
            o.Caption = Get_Language_Str(o.Caption, False, xlWhole)
        # VB2PY (UntranslatedCode) On Error GoTo 0

def __Test_Change_Language_in_Dialog():
    #UT---------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    Copy_Select_GotoAct_Form.Show()

def Set_Tast_Txt_Var(ForceUpdate=False):
    #-----------------------------------------------------------
    global Red_T,Green_T,OnOff_T,Tast_T
    
    if ForceUpdate or Red_T == r'':
        Red_T = Get_Language_Str(r'Rot')
        Green_T = Get_Language_Str(r'Grün')
        OnOff_T = Get_Language_Str(r'AnAus')
        Tast_T = Get_Language_Str(r'Tast')

def __Test_Translations():
    global __Check_Languages, __Test_Language
    
    Res = String()
    #UT----------------------------
    # Check it the translation works correct
    __Check_Languages = True
    Debug.Print(vbCr + r'-------------------------------------------')
    Res = P01.InputBox(r'Input the Language number' + vbCr + r' 0 = German' + vbCr + r' 1 = English' + vbCr + r' 2 = Dutch' + vbCr + r' 3 = French' + vbCr + r' 4 = Italian' + vbCr + r' 5 = Spain' + vbCr + r' 6 = Danish')
    if not IsNumeric(Res):
        return
    __Test_Language = P01.val(Res)
    __Update_Language_in_All_Sheets()

    ## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    __Change_Language_in_Dialog(Select_ProgGen_Dest_Form)
    __Change_Language_in_Dialog(Select_ProgGen_Src_Form)
    __Change_Language_in_Dialog(SelectMacros_Form)
    __Change_Language_in_Dialog(SelectMacrosTreeForm)
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
    Set_Tast_Txt_Var(ForceUpdate=True)
    #UserForm_DialogGuide1.Show ' Debug

# VB2PY (UntranslatedCode) Option Explicit
# Attention: One of the following preprcessor constants have to be defined in
# "Extras / Eigenschafteb VBA Projekt"'
#   PATTERN_CONFIG_PROG
#   PROG_GENERATOR_PROG
#
# Other languages could be added in the hidden sheet LANGUAGES_SH = "Languages"
# In addition Get_ExcelLanguage() must be adapted
# Current languages:
#  0 = German
#  1 = English
#  2 = Dutch
#  3 = French
#  4 = Italian  (Prog_Generator only)
#  5 = Spain        "
#  6 = Danish       "
# Strings which have not been translated could be found with
# The seach expression '[!r]("'  and ' "'   (Without ')
# and enabled "Mit Mustervergleich"
#   See also: https://docs.microsoft.com/de-de/office/vba/language/reference/user-interface-help/wildcard-characters-used-in-string-comparisons
# They could be translated by inserting 'Get_Language_Str'
#
#
# There are a lot of different locations where text messages are used:
# - In the sheets
# - Error messages in the sheets which are shown on certain condition
# - Hints in the sheets
# - Dialog boxes
#   - Some of them are changed from the program code
#   - Some messages are located in separate sheets: Special_Mode_Dlg, Par_Description
# - In the program code
# - Buttons
# - The Hotkeys have also to be adapted in the dialogs and single buttons
# - In the configuration files *.MLL_pcf
#   - Variable names
#   - Text messages
# - ...
#
# Some messages in the program are only called in case of an error.
# => They are not added automatically to the 'Languages' sheet
# ==> This is done by calling Add_All_VBA_Strings_to_the_Languages_Sheet()
#
# Location for the translations
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# - The most translations are stored in the hidden "Languages"
# - Some translations are stored in different locations
#   - The start page contains one text box for each language.
#     This is used because here several colors and fonts are used.
#     Normaly only the box which contains the current language
#     is visible. The language number is stored in the field
#     "Alternativtext" which could be changed using the right mouse
#     and the menu "Größe und Eigneschaften".
#     The "Alternativtext" mut contain the keyword "Language:"
#     Example: "Language: 0"
#     If a new language is created one text box has to be copied
#     and translated and the "Alternativtext" has to be changed to
#     the new number.
#   - The text messages in the example sheets in the Pattern_Configurator
#     have an own text box for each language. Here only the text box
#     for the actual language is visible. This method is used to be
#     independand from the Excel program. The number after the
#     keyword "msoTextBox" defines the language number. Old *.MLL_pcf
#     don't have a tailing number they are always shown.
#   - The buttons in the "Morsecode" sheet use a button for each
#     language fo the same reason as the text boxes.
#     (See Activate_Language_in_Example_Sheet(ByVal sh As Worksheet)
#     The Language number is stored in the "AlternativeText".
#   - Dialog functions which select their data form an Excel sheet
#     like the "SelectMacros_Form" or the "UserForm_Other" use
#     separate columns in the sheets "Lib_Macros" and "Par_Description
#
#
#
# Language specific messages in the example sheets                          ' 11.02.20:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Different languages could be used in the "msoTextBox" lines in the example sheets.
# The language number is added to the token:
#  "msoTextBox0" = German
#  "msoTextBox1" = Englisch
#  "msoTextBox2" = Dutch
#  "msoTextBox3" = French
# All Lines starting with "msoTextBox" are loaded to the sheet, but only the
# text box with the current language is visible. The Language is stored in
# ShapeRange.AlternativeText = "Language: 0"
# If the line line starts with "msoTextBox" it's an old file without different languages.
# This textbox is always shown.
# If the token has a tailing number it's assumed that there are matching lines for all languages.
# If the current language is missing nothing is displayed ;-( => It's importand to update
# the examples if a new language is added
#
#
#
# Debuging with othwer languages
# If this flag is not set the language could be changed
# temporary with the function "Test_Translations()"
#--------------------------------------------------------------------------------------------------------------
#UT-------------------------------------------------------
## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
#-------------------------------------------------------------------------------
## VB2PY (CheckDirective) VB directive took path 1 on 0
#-------------------------------------------------
#--------------------------------------------------------------------
#UT--------------------------------------------
#----------------------------------
## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
#-----------------------------------
## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
#------------------------------------------
#----------------------------------------------
#---------------------------------------------
#UT---------------------------------
#-------------------------------------------------------------
#UT-------------------------------------
#-------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
## VB2PY (CheckDirective) VB directive took path 1 on True
#------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------
#-------------------------------------------
#UT---------------------------------
#-----------------------------------------------------------
#UT----------------------------
