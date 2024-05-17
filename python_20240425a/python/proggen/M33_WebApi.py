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

import proggen.M02_Public as M02
import proggen.M02_global_variables as M02GV
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
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80

import mlpyproggen.Prog_Generator as PG

import ExcelAPI.XLA_Application as P01

from ExcelAPI.XLC_Excel_Consts import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

# **************************
# *                        *
# *       M33_WebApi       *
# *                        *
# **************************

__p = Variant()
__token = Variant()
__dic = Variant()

# VBA JSON Parser
# see https://medium.com/swlh/excel-vba-parse-json-easily-c2213f4d8e7a

def __ParseJSON(json , Key='obj'):
    fn_return_value = None
    __p = 1
    __token = __Tokenize(json)
    __dic = {}
    if __token(__p) == '{':
        __ParseObj(Key)
    else:
        __ParseArr(Key)
    fn_return_value = __dic
    return fn_return_value

def __ParseObj(Key):
    fn_return_value = None
    __p = __p + 1
    select_0 = __token(__p)
    if (select_0 == ']'):
        pass
    elif (select_0 == '['):
        __ParseArr(Key)
    elif (select_0 == '{'):
        if __token(__p + 1) == '}':
            __p = __p + 1
            __dic.Add(Key, 'null')
        else:
            fn_return_value(Key)
    elif (select_0 == '}'):
        Key = ReducePath(Key)
        break
    elif (select_0 == ':'):
        Key = Key + '.' + __token(__p - 1)
    elif (select_0 == ','):
        Key = ReducePath(Key)
    else:
        if __token(__p + 1) != ':':
            __dic.Add(Key, __token(__p))
    assert False, '# UNTRANSLATED VB LINE #39 [Loop]'
    return fn_return_value

def __ParseArr(Key):
    fn_return_value = None
    e = Variant()
    __p = __p + 1
    select_1 = __token(__p)
    if (select_1 == '}'):
        pass
    elif (select_1 == '{'):
        __ParseObj(Key + ArrayID(e))
    elif (select_1 == '['):
        fn_return_value(Key)
    elif (select_1 == ']'):
        break
    elif (select_1 == ':'):
        Key = Key + ArrayID(e)
    elif (select_1 == ','):
        e = e + 1
    else:
        __dic.Add(Key + ArrayID(e), __token(__p))
    assert False, '# UNTRANSLATED VB LINE #54 [Loop]'
    return fn_return_value

def __Tokenize(s):
    fn_return_value = None
    Pattern = '"(([^"\\\\]|\\\\.)*)"|[+\\-]?(?:0|[1-9]\\d*)(?:\\.\\d*)?(?:[eE][+\\-]?\\d+)?|\\w+|[^\\s"\']+?'
    fn_return_value = __RExtract(s, Pattern, True)
    return fn_return_value

def __RExtract(s, Pattern, bGroup1Bias=VBMissingArgument, bGlobal=True):
    fn_return_value = None
    c = Variant()

    m = Variant()

    n = Variant()

    v = Variant()
    with_0 = CreateObject('vbscript.regexp')
    with_0.Global = bGlobal
    with_0.MultiLine = False
    with_0.IgnoreCase = True
    with_0.Pattern = Pattern
    if with_0.Test(s):
        m = with_0.Execute(s)
        v = vbObjectInitialize(((1, m.Count),), Variant)
        for n in m:
            c = c + 1
            v[c] = n.Value
            if bGroup1Bias:
                if Len(n.submatches(0)) or n.Value == '""':
                    v[c] = n.submatches(0)
    fn_return_value = v
    return fn_return_value

def __ArrayID(e):
    fn_return_value = None
    ArrayID = '(' + e + ')'
    return fn_return_value

def __ReducePath(Key):
    fn_return_value = None
    if InStr(Key, '.'):
        ReducePath = left(Key, InStrRev(Key, '.') - 1)
    else:
        ReducePath = Key
    return fn_return_value

def __ListPaths(dic):
    fn_return_value = None
    s = Variant()

    v = Variant()
    for v in dic:
        s = s + v + ' --> ' + dic(v) + vbLf
    Debug.Print(s)
    return fn_return_value

def __GetFilteredValues(dic, Match):
    fn_return_value = None
    c = Variant()

    i = Variant()

    v = Variant()

    w = Variant()
    v = dic.Keys
    w = vbObjectInitialize(((1, dic.Count),), Variant)
    for i in vbForRange(0, UBound(v)):
        if Like(v(i), Match):
            c = c + 1
            w[c] = dic(v(i))
    w = vbObjectInitialize(((1, c),), Variant, w)
    fn_return_value = w
    return fn_return_value

def __GetFilteredTable(dic, cols):
    fn_return_value = None
    c = Variant()

    i = Variant()

    j = Variant()

    v = Variant()

    w = Variant()

    z = Variant()
    v = dic.Keys
    z = __GetFilteredValues(dic, cols(0))
    w = vbObjectInitialize(((1, UBound(z)), (1, UBound(cols) + 1),), Variant)
    for j in vbForRange(1, UBound(cols) + 1):
        z = __GetFilteredValues(dic, cols(j - 1))
        for i in vbForRange(1, UBound(z)):
            w[i, j] = z(i)
    fn_return_value = w
    return fn_return_value

def __OpenTextFile(f):
    fn_return_value = None
    with_1 = CreateObject('ADODB.Stream')
    with_1.Charset = 'utf-8'
    with_1.Open()
    with_1.LoadFromFile(f)
    OpenTextFile = with_1.ReadText
    return fn_return_value

def __ListAllBetas():
    fn_return_value = None
    Trans = String()

    objHTTP = Object()

    URL = String()

    getParam = String()

    Response = Variant()

    i = Variant()

    obj = Variant()
    objHTTP = CreateObject('MSXML2.ServerXMLHTTP')
    URL = 'https://api.github.com/repos/Hardi-St/MobaLedLib_Docu/commits?path=Betatest/MobaLedLib-master.zip'
    objHTTP.Open('GET', URL, False)
    objHTTP.setRequestHeader('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')
    objHTTP.send(( '' ))
    Response = __ParseJSON(objHTTP.responseText)
    i = 0
    while 1:
        obj = 'obj(' + i + ')'
        if Response.Exists(obj + '.url'):
            Debug.Print(Response(obj + '.commit.committer.date') + ': ' + Response(obj + '.commit.committer.name') + ': ' + Response(obj + '.commit.message'))
        else:
            break
        i = i + 1
    #Debug.Print ListPaths(Response)
    return fn_return_value


