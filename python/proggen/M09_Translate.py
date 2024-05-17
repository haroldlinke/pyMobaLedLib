from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLC_Excel_Consts as XLC
import ExcelAPI.XLA_Application as P01
import proggen.M10_Par_Description as M10
import proggen.M02_Public as M02
import proggen.M09_Language as M09
from urllib.request import urlopen
import re

""" Module to translate cells by Misha
# VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
 16.06.20: Added da = Danish
-------------------------------------------
------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
-----------------------------------------------
------------------------------------------
 PROG_GENERATOR_PROG
-----------------------------------------------
-------------------------------
"""

SrcLanguage = 'en'
DestLanguages = 'nl fr it es da'

def ConvertToGet(val):
    _fn_return_value = False
    ReplaceTxt = '()='

    i = Integer()

    c = String()
    #-------------------------------------------
    val = Replace(val, ' ', '+')
    val = Replace(val, '#', '_HASH')
    # 18.04.20: 09.05.20: Old "_HASH_", but Google adds an space ;-(  "_HASH _"
    #val = Replace(val, vbNewLine, "+")
    val = Replace(val, vbNewLine, '+VBNL+')
    # 17.06.20:
    val = Replace(val, vbCr, '+VBCR+')
    #    "
    val = Replace(val, vbLf, '+VBLF+')
    #    "
    val = Replace(val, '&', '&amp')
    val = Replace(val, '%', '_PERCENT')
    # 27.11.21:
    #val = Replace(val, "=", "&eq;")
    for i in vbForRange(1, Len(ReplaceTxt)):
        c = Mid(ReplaceTxt, i, 1)
        val = Replace(val, c, '%' + Hex(Asc(c)))
    _fn_return_value = val
    return _fn_return_value

def Clean(val):
    _fn_return_value = False
    #------------------------------------
    val = Replace(val, '&quot;', '"')
    val = Replace(val, '&gt;', '>')
    val = Replace(val, '&lt;', '<')
    val = Replace(val, '%2C', ',')
    val = Replace(val, '&#39;', '\'')
    val = Replace(val, '_HASH', '#')
    # 18.04.20: 09.05.20: Old "_HASH_", but Google adds an space ;-(  "_HASH _"
    val = Replace(val, 'VBNL', vbNewLine)
    # 17.06.20:
    val = Replace(val, 'VBCR', vbCr)
    #    "
    val = Replace(val, 'VBLF', vbLf)
    #    "
    val = Replace(val, '_PERCENT', '%')
    # 27.11.21:
    if Left(val, 1) == '=':
        val = '\'' + val
    _fn_return_value = val
    return _fn_return_value

def RegexExecute(Str, reg, matchIndex=VBMissingArgument, subMatchIndex=VBMissingArgument):
    p = re.compile(reg)
    m = p.findall(Str)
    if m != []:
        _fn_return_value = m[0]
    else:
        _fn_return_value = Str
    return _fn_return_value
    
    #old VBA part'
    _fn_return_value = False
    regex = Object()

    Matches = Object()
    #---------------------------------------------------------------------------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error GoTo ErrHandl
    regex = CreateObject('VBScript.RegExp')
    regex.Pattern = reg
    regex.Global = not ( matchIndex == 0 and subMatchIndex == 0 ) 
    if regex.Test(Str):
        Matches = regex.Execute(Str)
        _fn_return_value = Matches(matchIndex).submatches(subMatchIndex)
        return _fn_return_value
    _fn_return_value = CVErr(XLC.xlErrValue)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: translateFrom - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: translateTo - ByVal 
def Translate_Text(Txt, translateFrom, translateTo):
    _fn_return_value = False
    Trans = String()

    objHTTP = Object()

    URL = String()

    getParam = String()
    #-------------------------------------------------------------------------------------------------------------------
    # Example parameters:
    # translateFrom = "de"
    # translateTo = "en"
    #objHTTP = CreateObject('MSXML2.ServerXMLHTTP')
    getParam = ConvertToGet(Txt)
    # Hier kann auch "https://translate.google.de" verwendet werden   oder URL = "https://translate.google.pl
    URL = 'https://translate.google.pl/m?hl=' + translateFrom + '&sl=' + translateFrom + '&tl=' + translateTo + '&ie=UTF-8&prev=_m&q=' + getParam
    #objHTTP.Open('GET', URL, False)
    #objHTTP.setRequestHeader('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')
    #objHTTP.send(( '' ))
    
    with urlopen(URL) as response:
        body = response.read()
    decoded_body = body.decode("utf-8")

    if InStr(decoded_body, 'div dir="ltr"') > 0:
        # "<html><head><title>Google Übersetzer</title><style>body{font:normal small arial,sans-serif,helvetica}body,html,form,div,p,img,input{margin:0padding:0}body{padding:3px}.nb{border:0}.s1{padding:5px}.ub{border-top:1px solid #36c}.db{border-bottom:1px so
        Trans = RegexExecute(decoded_body, 'div[^"]*?"ltr".*?>(.+?)</div>')
    elif InStr(decoded_body, '<div class="result-container">') > 0:
        # 19.01.21:
        Trans = RegexExecute(decoded_body, r'<div class="result-container">(.+?)</div>')
        #    "
    else:
        P01.MsgBox('Error translating \'' + Txt + '\'' + vbCr + vbCr + 'Response: \'' + decoded_body + '\'', vbCritical, 'Error translating text')
    _fn_return_value = Clean(Trans)
    return _fn_return_value

def TranslateOneCell(src, DeltaCol=1, StartOffs=0, SrcLng=SrcLanguage, DstLng=DestLanguages, FirstCharUppercase=VBMissingArgument):
    Txt = String()

    DestCol = Long()

    DestLang = Variant()

    Row = Long()

    Res = String()
    #-------------------------------------------------------------------------------------------------------------------------------------------------
    # Translate the current cell to all languages
    if src == '':
        return
    Row = src.Row
    Txt = src
    DestCol = src.Column + DeltaCol + StartOffs
    for DestLang in Split(DstLng, ' '):
        if P01.Cells(Row, DestCol) == '':
            if Left(src.Formula, 2) == '=$':
                # Special translation if the the source starts with is a formula like =$H$8 (Used in the Group names)
                Addr = Split(Mid(src.Formula, 2), ' ')(0)
                # 07.10.21: Added "Splitt..." to be able to process lines with mixed content (Link and text)
                DstRow = P01.Range(Addr).Row
                NewAddr = P01.Cells(DstRow, DestCol).Address
                TailingTxt = Trim(Mid(src.Formula, Len(Addr) + 2))
                if left(TailingTxt, 2) == '& ':
                    TailingTxt = Replace(Mid(TailingTxt, 3), '"', '')
                    TailingTxt = ' & " ' + Translate_Text(TailingTxt, SrcLng, DestLang) + '"'
                Res = '=' + NewAddr + TailingTxt
                # 07.10.21:
                _with39 = P01.Cells(Row, DestCol).Font
                _with39.ThemeColor = XLC.xlThemeColorDark1
                _with39.TintAndShade = - 0.499984740745262
            elif Left(src.Formula, 2) == '=C':
                # Don't translate it if the source  points to column C like =C
                Res = src.Formula
                # Used in the 'Languages' sheet
                _with40 = P01.Cells(Row, DestCol).Font
                _with40.ThemeColor = XLC.xlThemeColorDark1
                _with40.TintAndShade = - 0.499984740745262
            else:
                Res = Translate_Text(Txt, SrcLng, DestLang)
                # Translat the cell
            if FirstCharUppercase:
                Res = Left(UCase(Res), 1) + Mid(Res, 2)
            # 26.10.21:
            P01.CellDict[Row, DestCol] = Res
        DestCol = DestCol + DeltaCol

def Change_Language_in_Par_Description():
    DeltaCol = 2

    StartOffs = Long()

    SrcLng = String()

    DstLng = String()

    c = P01.Range()
    #-----------------------------------------------
    # Translate the selected range in the "Par_Description" sheet
    # The columns G and H could be selected at once
    #
    _select10 = P01.Selection.Column
# First column of the selection
    if (_select10 == M10.ParInTx_COL) or (_select10 == M10.ParHint_COL):
        #
        # German to English to be able to check the english translation which is used for all other translations
        SrcLng = 'de'
        DstLng = 'en'
        StartOffs = 1
    elif (_select10 == M10.ParInTx_COL + 3) or (_select10 == M10.ParHint_COL + 3):
        # English to all other languages
        SrcLng = 'en'
        DstLng = DestLanguages
        StartOffs = 0
    else:
        P01.MsgBox('Translation for this column is not defined in \'Change_Language_in_Par_Description()')
        return
    for c in P01.Selection:
        TranslateOneCell(c, DeltaCol, StartOffs, SrcLng=SrcLng, DstLng=DstLng)

def Change_Language_in_Lib_Macros():
    DeltaCol = M02.DeltaCol_Lib_Macro_Lang

    StartOffs = 0

    SrcLng = String()

    DstLng = String()

    c = P01.Range()
    #------------------------------------------
    # Translate the selected range in the "Lib_Macros" sheet
    # 07.10.21: Old: 2
    _select11 = P01.Selection.Column
# First column of the selection
    if (_select11 == M02.SM_Group_COL) or (_select11 == M02.SM_LName_COL) or (_select11 == M02.SM_ShrtD_COL) or (_select11 == M02.SM_DetailCOL):
        #
        # German to English to be able to check the english translation which is used for all other translations
        SrcLng = 'de'
        DstLng = 'en'
    elif (_select11 == M02.SM_Group_COL + DeltaCol) or (_select11 == M02.SM_LName_COL + DeltaCol) or (_select11 == M02.SM_ShrtD_COL + DeltaCol) or (_select11 == M02.SM_DetailCOL + DeltaCol):
        # English to all other languages
        SrcLng = 'en'
        DstLng = DestLanguages
    else:
        P01.MsgBox('Translation for this column is not defined in \'Change_Language_in_Lib_Macros()')
        return
    for c in P01.Selection:
        TranslateOneCell(c, DeltaCol, StartOffs, SrcLng=SrcLng, DstLng=DstLng, FirstCharUppercase=( P01.Selection.Column == M02.SM_Group_COL ))
        # 26.10.21: Added: FirstCharUppercase ...

def Change_Language_in_Languages_Sheet():
    DeltaCol = 1

    StartOffs = 0

    SrcLng = String()

    DstLng = String()

    c = P01.Range()
    #-----------------------------------------------
    # Translate the selected range in the "Languages" sheet
    _select12 = P01.Selection.Column
# First column of the selection
    if (_select12 == M09.FirstLangCol):
        # German to English to be able to check the english translation which is used for all other translations
        SrcLng = 'de'
        DstLng = 'en'
    elif (_select12 == M09.FirstLangCol + 1):
        # English to all other languages
        SrcLng = 'en'
        DstLng = DestLanguages
    else:
        P01.MsgBox('Translation for this column is not defined in \'Change_Language_in_Lib_Macros()')
        return
    for c in P01.Selection.Cells:
        TranslateOneCell(c, DeltaCol, StartOffs, SrcLng=SrcLng, DstLng=DstLng)
    ## VB2PY (CheckDirective) VB directive took path 2 on 0

def Translate_Selection(event=None):
    #-------------------------------
    # This macro is called when CTRL+Shift+T is pressed
    _select13 = P01.ActiveSheet.Name
## VB2PY (CheckDirective) VB directive took path 1 on PROG_GENERATOR_PROG
    if (_select13 == M02.PAR_DESCR_SH):
        Change_Language_in_Par_Description()
    elif (_select13 == M02.LIBMACROS_SH):
        Change_Language_in_Lib_Macros()
    elif (_select13 == M02.LANGUAGES_SH):
        Change_Language_in_Languages_Sheet()

# VB2PY (UntranslatedCode) Option Explicit
