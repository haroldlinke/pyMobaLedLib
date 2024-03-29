from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLC_Excel_Consts as X01
import ExcelAPI.XLW_Workbook as X02
import pattgen.M09_Language
import pattgen.M01_Public_Constants_a_Var as M01

""" Module to translate cells by Misha
# VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
-------------------------------------------
------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
 PROG_GENERATOR_PROG
-----------------------------------------------
-------------------------------
"""

SrcLanguage = 'en'
DestLanguages = 'nl fr'

def ConvertToGet(Val):
    _fn_return_value = None
    ReplaceTxt = '()='

    i = Integer()

    c = String()
    #-------------------------------------------
    Val = Replace(Val, ' ', '+')
    Val = Replace(Val, '#', '_HASH')
    # 18.04.20: 09.05.20: Old "_HASH_", but Google adds an space ;-(  "_HASH _"
    Val = Replace(Val, vbNewLine, '+')
    Val = Replace(Val, '&', '&amp')
    #val = Replace(val, "=", "&eq;")
    for i in vbForRange(1, Len(ReplaceTxt)):
        c = Mid(ReplaceTxt, i, 1)
        Val = Replace(Val, c, '%' + Hex(Asc(c)))
    _fn_return_value = Val
    return _fn_return_value

def Clean(Val):
    _fn_return_value = None
    #------------------------------------
    Val = Replace(Val, '&quot;', '"')
    Val = Replace(Val, '&gt;', '>')
    Val = Replace(Val, '&lt;', '<')
    Val = Replace(Val, '%2C', ',')
    Val = Replace(Val, '&#39;', '\'')
    Val = Replace(Val, '_HASH', '#')
    # 18.04.20: 09.05.20: Old "_HASH_", but Google adds an space ;-(  "_HASH _"
    if Left(Val, 1) == '=':
        Val = '\'' + Val
    _fn_return_value = Val
    return _fn_return_value

def RegexExecute(p_str, reg, matchIndex=VBMissingArgument, subMatchIndex=VBMissingArgument):
    _fn_return_value = None
    regex = Object()

    matches = Object()
    #---------------------------------------------------------------------------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo ErrHandl
    regex = CreateObject('VBScript.RegExp')
    regex.Pattern = reg
    regex.Global = not ( matchIndex == 0 and subMatchIndex == 0 ) 
    if regex.Test(p_str):
        matches = regex.Execute(p_str)
        _fn_return_value = matches(matchIndex).SubMatches(subMatchIndex)
        return _fn_return_value
    _fn_return_value = CVErr(X01.xlErrValue)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: translateFrom - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: translateTo - ByVal 
def Translate_Text(Txt, translateFrom, translateTo):
    _fn_return_value = None
    Trans = String()

    objHTTP = Object()

    URL = String()

    getParam = String()
    #-------------------------------------------------------------------------------------------------------------------
    # Example parameters:
    # translateFrom = "de"
    # translateTo = "en"
    objHTTP = CreateObject('MSXML2.ServerXMLHTTP')
    getParam = ConvertToGet(Txt)
    URL = 'https://translate.google.pl/m?hl=' + translateFrom + '&sl=' + translateFrom + '&tl=' + translateTo + '&ie=UTF-8&prev=_m&q=' + getParam
    objHTTP.Open('GET', URL, False)
    objHTTP.setRequestHeader('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')
    objHTTP.send(( '' ))
    if InStr(objHTTP.responseText, 'div dir="ltr"') > 0:
        # "<html><head><title>Google Übersetzer</title><style>body{font:normal small arial,sans-serif,helvetica}body,html,form,div,p,img,input{margin:0padding:0}body{padding:3px}.nb{border:0}.s1{padding:5px}.ub{border-top:1px solid #36c}.db{border-bottom:1px so
        Trans = RegexExecute(objHTTP.responseText, 'div[^"]*?"ltr".*?>(.+?)</div>')
    elif InStr(objHTTP.responseText, '<div class="result-container">') > 0:
        # 19.01.21:
        Trans = RegexExecute(objHTTP.responseText, '<div class="result-container">(.+?)</div>')
        #    "
    else:
        X02.MsgBox('Error translating \'' + Txt + '\'' + vbCr + vbCr + 'Response: \'' + objHTTP.responseText + '\'', vbCritical, 'Error translating text')
    _fn_return_value = Clean(Trans)
    return _fn_return_value

def TranslateOneCell(Src, DeltaCol=1, StartOffs=0, SrcLng=SrcLanguage, DstLng=DestLanguages):
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
        if X02.Cells(Row, DestCol) == '':
            if Left(Src.Formula, 2) == '=$':
                # Don't translate it if the source is a formula like =$H$8
                Addr = Mid(Src.Formula, 2)
                DstRow = X02.Range(Addr).Row
                NewAddr = X02.Cells(DstRow, DestCol).Address
                Res = '=' + NewAddr
                _with84 = X02.Cells(Row, DestCol).Font
                _with84.ThemeColor = X01.xlThemeColorDark1
                _with84.TintAndShade = - 0.499984740745262
            elif Left(Src.Formula, 2) == '=C':
                # Don't translate it if the source  points to column C like =C
                Res = Src.Formula
                _with85 = X02.Cells(Row, DestCol).Font
                _with85.ThemeColor = X01.xlThemeColorDark1
                _with85.TintAndShade = - 0.499984740745262
            else:
                Res = Translate_Text(Txt, SrcLng, DestLang)
                # Translat the cell
            X02.CellDict[Row, DestCol] = Res
        DestCol = DestCol + DeltaCol

def Change_Language_in_Languages_Sheet():
    DeltaCol = 1

    StartOffs = 0

    SrcLng = String()

    DstLng = String()

    c = X02.Range()
    #-----------------------------------------------
    # Translate the selected range in the "Languages" sheet
    _select68 = X02.Selection.Column
# First column of the selection
    if (_select68 == pattgen.M09_Language.FirstLangCol):
        # German to English to be able to check the english translation which is used for all other translations
        SrcLng = 'de'
        DstLng = 'en'
    elif (_select68 == pattgen.M09_Language.FirstLangCol + 1):
        # English to all other languages
        SrcLng = 'en'
        DstLng = DestLanguages
    else:
        X02.MsgBox('Translation for this column is not defined in \'Change_Language_in_Lib_Macros()')
        return
    for c in X02.Selection:
        TranslateOneCell(c, DeltaCol, StartOffs, SrcLng=SrcLng, DstLng=DstLng)
    ## VB2PY (CheckDirective) VB directive took path 2 on 0

def Translate_Selection():
    #-------------------------------
    # This macro is called when CTRL+Shift+T is pressed
    _select69 = X02.ActiveSheet.Name
## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
    if (_select69 == M01.LANGUAGES_SH):
        Change_Language_in_Languages_Sheet()

# VB2PY (UntranslatedCode) Option Explicit
