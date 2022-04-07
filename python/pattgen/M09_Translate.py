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

""" Module to translate cells by Misha
# VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
-------------------------------------------
------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
-----------------------------------------------
------------------------------------------
-----------------------------------------------
-------------------------------
"""

__SrcLanguage = 'en'
__DestLanguages = 'nl fr it es'

def __ConvertToGet(Val):
    fn_return_value = None
    ReplaceTxt = '()='

    i = Integer()

    c = String()
    #-------------------------------------------
    Val = Replace(Val, ' ', '+')
    Val = Replace(Val, '#', '_HASH')
    Val = Replace(Val, vbNewLine, '+')
    Val = Replace(Val, '&', '&amp')
    #val = Replace(val, "=", "&eq;")
    for i in vbForRange(1, Len(ReplaceTxt)):
        c = Mid(ReplaceTxt, i, 1)
        Val = Replace(Val, c, '%' + Hex(Asc(c)))
    fn_return_value = Val
    return fn_return_value

def __Clean(Val):
    fn_return_value = None
    #------------------------------------
    Val = Replace(Val, '&quot;', '"')
    Val = Replace(Val, '&gt;', '>')
    Val = Replace(Val, '&lt;', '<')
    Val = Replace(Val, '%2C', ',')
    Val = Replace(Val, '&#39;', '\'')
    Val = Replace(Val, '_HASH', '#')
    if Left(Val, 1) == '=':
        Val = '\'' + Val
    fn_return_value = Val
    return fn_return_value

def __RegexExecute(str, reg, matchIndex=VBMissingArgument, subMatchIndex=VBMissingArgument):
    fn_return_value = None
    regex = Object()

    matches = Object()
    #---------------------------------------------------------------------------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo ErrHandl
    regex = CreateObject('VBScript.RegExp')
    regex.Pattern = reg
    regex.Global = not ( matchIndex == 0 and subMatchIndex == 0 ) 
    if regex.Test(str):
        matches = regex.Execute(str)
        fn_return_value = matches(matchIndex).SubMatches(subMatchIndex)
        return fn_return_value
    fn_return_value = CVErr(xlErrValue)
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: translateFrom - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: translateTo - ByVal 
def __Translate_Text(Txt, translateFrom, translateTo):
    fn_return_value = None
    Trans = String()

    objHTTP = Object()

    URL = String()

    getParam = String()
    #-------------------------------------------------------------------------------------------------------------------
    # Example parameters:
    # translateFrom = "de"
    # translateTo = "en"
    objHTTP = CreateObject('MSXML2.ServerXMLHTTP')
    getParam = __ConvertToGet(Txt)
    URL = 'https://translate.google.pl/m?hl=' + translateFrom + '&sl=' + translateFrom + '&tl=' + translateTo + '&ie=UTF-8&prev=_m&q=' + getParam
    objHTTP.Open('GET', URL, False)
    objHTTP.setRequestHeader('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')
    objHTTP.send(( '' ))
    if InStr(objHTTP.responseText, 'div dir="ltr"') > 0:
        # "<html><head><title>Google Übersetzer</title><style>body{font:normal small arial,sans-serif,helvetica}body,html,form,div,p,img,input{margin:0padding:0}body{padding:3px}.nb{border:0}.s1{padding:5px}.ub{border-top:1px solid #36c}.db{border-bottom:1px so
        Trans = __RegexExecute(objHTTP.responseText, 'div[^"]*?"ltr".*?>(.+?)</div>')
    elif InStr(objHTTP.responseText, '<div class="result-container">') > 0:
        Trans = __RegexExecute(objHTTP.responseText, '<div class="result-container">(.+?)</div>')
    else:
        MsgBox('Error translating \'' + Txt + '\'' + vbCr + vbCr + 'Response: \'' + objHTTP.responseText + '\'', vbCritical, 'Error translating text')
    fn_return_value = __Clean(Trans)
    return fn_return_value

def __TranslateOneCell(Src, DeltaCol=1, StartOffs=0, SrcLng=__SrcLanguage, DstLng=__DestLanguages):
    Txt = String()

    DestCol = Long()

    DestLang = Variant()

    Row = Long()

    Res = String()
    #-------------------------------------------------------------------------------------------------------------------------------------------------
    # Translate the current cell to all languages
    if Src == '':
        return
    Row = Src.Row
    Txt = Src
    DestCol = Src.Column + DeltaCol + StartOffs
    for DestLang in Split(DstLng, ' '):
        if Cells(Row, DestCol) == '':
            if Left(Src.Formula, 2) == '=$':
                Addr = Mid(Src.Formula, 2)
                DstRow = Range(Addr).Row
                NewAddr = Cells(DstRow, DestCol).Address
                Res = '=' + NewAddr
                with_0 = Cells(Row, DestCol).Font
                with_0.ThemeColor = xlThemeColorDark1
                with_0.TintAndShade = - 0.499984740745262
            elif Left(Src.Formula, 2) == '=C':
                Res = Src.Formula
                with_1 = Cells(Row, DestCol).Font
                with_1.ThemeColor = xlThemeColorDark1
                with_1.TintAndShade = - 0.499984740745262
            else:
                Res = __Translate_Text(Txt, SrcLng, DestLang)
            Cells[Row, DestCol] = Res
        DestCol = DestCol + DeltaCol

def __Change_Language_in_Par_Description():
    DeltaCol = 2

    StartOffs = Long()

    SrcLng = String()

    DstLng = String()

    c = Range()
    #-----------------------------------------------
    # Translate the selected range in the "Par_Description" sheet
    # The columns G and H could be selected at once
    #
    if (Selection.Column == ParInTx_COL) or (Selection.Column == ParHint_COL):
        SrcLng = 'de'
        DstLng = 'en'
        StartOffs = 1
    elif (Selection.Column == ParInTx_COL + 3) or (Selection.Column == ParHint_COL + 3):
        SrcLng = 'en'
        DstLng = __DestLanguages
        StartOffs = 0
    else:
        MsgBox('Translation for this column is not defined in \'Change_Language_in_Par_Description()')
        return
    for c in Selection:
        __TranslateOneCell(c, DeltaCol, StartOffs, SrcLng=SrcLng, DstLng=DstLng)

def __Change_Language_in_Lib_Macros():
    DeltaCol = 2

    StartOffs = 0

    SrcLng = String()

    DstLng = String()

    c = Range()
    #------------------------------------------
    # Translate the selected range in the "Lib_Macros" sheet
    if (Selection.Column == SM_ShrtD_COL) or (Selection.Column == SM_DetailCOL):
        SrcLng = 'de'
        DstLng = 'en'
    elif (Selection.Column == SM_ShrtD_COL + 2) or (Selection.Column == SM_DetailCOL + 2):
        SrcLng = 'en'
        DstLng = __DestLanguages
    else:
        MsgBox('Translation for this column is not defined in \'Change_Language_in_Lib_Macros()')
        return
    for c in Selection:
        __TranslateOneCell(c, DeltaCol, StartOffs, SrcLng=SrcLng, DstLng=DstLng)

def __Change_Language_in_Languages_Sheet():
    DeltaCol = 1

    StartOffs = 0

    SrcLng = String()

    DstLng = String()

    c = Range()

    DeltaCol = 1

    StartOffs = 0

    c = Range()
    #-----------------------------------------------
    # Translate the selected range in the "Languages" sheet
    if (Selection.Column == FirstLangCol):
        SrcLng = 'de'
        DstLng = 'en'
    elif (Selection.Column == FirstLangCol + 1):
        SrcLng = 'en'
        DstLng = __DestLanguages
    else:
        MsgBox('Translation for this column is not defined in \'Change_Language_in_Lib_Macros()')
        return
    for c in Selection:
        __TranslateOneCell(c, DeltaCol, StartOffs, SrcLng=SrcLng, DstLng=DstLng)
    ## VB2PY (CheckDirective) VB directive took path 1 on 0
    for c in Selection:
        __TranslateOneCell(c, DeltaCol, StartOffs)

def Translate_Selection():
    #-------------------------------
    # This macro is called when CTRL+Shift+T is pressed
## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    if (ActiveSheet.Name == PAR_DESCR_SH):
        __Change_Language_in_Par_Description()
    elif (ActiveSheet.Name == LIBMACROS_SH):
        __Change_Language_in_Lib_Macros()
    elif (ActiveSheet.Name == LANGUAGES_SH):
        __Change_Language_in_Languages_Sheet()

# VB2PY (UntranslatedCode) Option Explicit

