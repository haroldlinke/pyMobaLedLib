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



import proggen.M02_Public as M02
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header as M06
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
#import proggen.M06_Write_Header_SW as M06SW
#import proggen.M07_COM_Port as M07
#import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
#import proggen.M09_Select_Macro as M09SM
#import proggen.M09_SelectMacro_Treeview as M09SMT
#import proggen.M10_Par_Description as M10
#import proggen.M20_PageEvents_a_Functions as M20
#import proggen.M25_Columns as M25
#import proggen.M27_Sheet_Icons as M27
#import proggen.M28_divers as M28
import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Mulitplexer as M80
import mlpyproggen.Prog_Generator as PG

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *


from ExcelAPI.XLC_Excel_Consts import *
import ExcelAPI.XLA_Application as P01

ParName_COL = 1
Par_Cnt_COL = 2
ParType_COL = 3
Par_Min_COL = 4
Par_Max_COL = 5
Par_Def_COL = 6
Par_Opt_COL = 7
ParInTx_COL = 8
ParHint_COL = 9
CHAN_TYPE_NONE = 1
CHAN_TYPE_LED = 2
CHAN_TYPE_SERIAL = 3
__FirstDatRow = 2

def __Get_ParDesc_Row(Sh, Name):
    global ParName_COL
    fn_return_value = None
    #r = Range()

    #f = Variant()
    #------------------------------------------------------------------------
    with_0 = Sh
    r = with_0.Range(with_0.Cells(1, ParName_COL), with_0.Cells(M30.LastUsedRowIn(Sh), ParName_COL))
    f = r.Find(What= Name, after= r.CellsFct(__FirstDatRow, 1), LookIn= xlFormulas, LookAt= xlWhole, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False)
    if f is None:
        Debug.Print('Fehlender Parameter: ' + Name)
        P01.MsgBox('Fehler: Der Parameter Name \'' + Name + '\' wurde nicht im Sheet \'' + Sh.Name + '\' gefunden!', vbCritical, 'Internal Error')
        M30.EndProg()
    else:
        fn_return_value = f.Row
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Typ - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Min - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Max - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Def - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Opt - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpTxt - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Hint - ByRef 
def Get_Par_Data(ParName):
    DeltaCol = 2

    Row = int()

    #Sh = X02.Worksheet

    ActLanguage = Integer()

    Offs = int()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ActLanguage = M09.Get_ExcelLanguage()
    if ActLanguage != 0:
        Offs = 1
    Sh = PG.ThisWorkbook.Sheets(M02.PAR_DESCR_SH)
    Row = __Get_ParDesc_Row(Sh, ParName)
    with_1 = Sh
    Typ = with_1.Cells(Row, ParType_COL)
    Min = with_1.Cells(Row, Par_Min_COL)
    Max = with_1.Cells(Row, Par_Max_COL)
    Def = with_1.Cells(Row, Par_Def_COL)
    Opt = with_1.Cells(Row, Par_Opt_COL)
    InpTxt = with_1.Cells(Row, ParInTx_COL + ActLanguage * DeltaCol + Offs)
    if InpTxt == '':
        InpTxt = ParName
    Hint = with_1.Cells(Row, ParHint_COL + ActLanguage * DeltaCol + Offs)
    
    return Typ, Min, Max, Def, Opt, InpTxt, Hint


def __Get_Type_Only(TypeStr):
    fn_return_value = ""
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # type has the option to be seperated by "." - e.g. Domain.Class.Type Extension.Extension.List
    # the last part must always be either empty of a well known type e.g. List, Mode, Time
    if TypeStr == '':
        fn_return_value = ''
    else:
        Splits = Split(TypeStr, '.')
        #return the last part
        fn_return_value = Splits(UBound(Splits))
    return fn_return_value


def __Test_Get_Par_Data():

    #UT----------------------------
    Typ, Min, Max, Def, Opt, InpTxt, Hint = Get_Par_Data('Pin_List')
    Debug.Print('Typ:' + Typ, 'Min:' + Min + ' Max:' + Max + ' Def:' + Def + ' Opt:' + Opt + vbCr + 'InpTxt:' + InpTxt + vbCr + 'Hint:' + Hint)

# VB2PY (UntranslatedCode) Option Explicit
