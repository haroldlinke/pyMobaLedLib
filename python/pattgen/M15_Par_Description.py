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

"""------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
UT----------------------------
"""

__ParName_COL = 1
__Par_Cnt_COL = 2
__ParType_COL = 3
__Par_Min_COL = 4
__Par_Max_COL = 5
__Par_Def_COL = 6
__ParInTx_COL = 7
__ParHint_COL = 8
__FirstDatRow = 2

def __Get_ParDesc_Row(Sh, Name):
    fn_return_value = None
    r = Range()

    f = Variant()
    #------------------------------------------------------------------------
    with_0 = Sh
    r = with_0.Range(with_0.Cells(1, __ParName_COL), with_0.Cells(LastUsedRowIn(Sh), __ParName_COL))
    f = r.Find(What= Name, After= r.Cells(__FirstDatRow, 1), LookIn= xlFormulas, LookAt= xlWhole, SearchOrder= xlByRows, SearchDirection= xlNext, MatchCase= True, SearchFormat= False)
    if f is None:
        MsgBox(Get_Language_Str('Fehler: Der Parameter Name \'') + Name + Get_Language_Str('\' wurde nicht im Sheet \'') + Sh.Name + Get_Language_Str('\' gefunden!'), vbCritical, Get_Language_Str('Internal Error'))
        EndProg()
    else:
        fn_return_value = f.Row
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Typ - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Min - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Max - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Def - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpTxt - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Hint - ByRef 
def Get_Par_Data(ParName, Typ, Min, Max, Def, InpTxt, Hint):
    Row = Long()

    Sh = Worksheet()
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Sh = Sheets(PAR_DESCRIPTION_SH)
    Row = __Get_ParDesc_Row(Sh, ParName)
    with_1 = Sh
    Typ = with_1.Cells(Row, __ParType_COL)
    Min = with_1.Cells(Row, __Par_Min_COL)
    Max = with_1.Cells(Row, __Par_Max_COL)
    Def = with_1.Cells(Row, __Par_Def_COL)
    InpTxt = with_1.Cells(Row, __ParInTx_COL)
    if InpTxt == '':
        InpTxt = ParName
    Hint = with_1.Cells(Row, __ParHint_COL)

def __Test_Get_Par_Data():
    Typ = String()

    Min = String()

    Max = String()

    Def = String()

    InpTxt = String()

    Hint = String()
    #UT----------------------------
    Get_Par_Data('Duration', Typ, Min, Max, Def, InpTxt, Hint)
    Debug.Print('Typ:' + Typ, 'Min:' + Min + ' Max:' + Max + ' Def:' + Def + vbCr + 'InpTxt:' + InpTxt + vbCr + 'Hint:' + Hint)

# VB2PY (UntranslatedCode) Option Explicit
