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

""" Different arangements:

   |     |  |         |   |  |  |     |    |  |    |
   |\____/  |         |   |  |  |     |    |  |    |
   \________/         \___\__/__/     \____/  \____/

----------------------------------------------------------------------------
UT-------------------------
"""

class GotoListEntry_t:
    def __init__(self):
        self.Start = Long()
        self.Ende = Long()
        self.Min = Long()
        self.Max = Long()
        self.Dist = Long()
        self.Inside_Cnt = Long()
        self.OutsideCnt = Long()


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: GotoArrowTab - ByVal 
def Calc_Height_GotoArrow(GotoArrowTab):
    fn_return_value = None
    StrEnt = Variant()

    GotoList = vbObjectInitialize(objtype=GotoListEntry_t)

    StrArray = vbObjectInitialize(objtype=String)

    Nr = Long()

    a = Long()

    t = Long()

    Res = String()
    #----------------------------------------------------------------------------
    # Fill the array
    StrArray = Split(GotoArrowTab, ' ')
    GotoList = vbObjectInitialize((UBound(StrArray),), Variant)
    for StrEnt in StrArray:
        Cols = Split(StrEnt, ',')
        GotoList[Nr].Start = Val(Cols(0))
        GotoList[Nr].Ende = Val(Cols(1))
        if GotoList(Nr).Start < GotoList(Nr).Ende:
            GotoList[Nr].Min = GotoList(Nr).Start
            GotoList[Nr].Max = GotoList(Nr).Ende
        else:
            GotoList[Nr].Min = GotoList(Nr).Ende
            GotoList[Nr].Max = GotoList(Nr).Start
        GotoList[Nr].Dist = Abs(GotoList(Nr).Start - GotoList(Nr).Ende)
        Nr = Nr + 1
    # Calc Inside_Cnt and OutsideCnt
    for a in vbForRange(0, UBound(GotoList)):
        Min = GotoList(a).Min
        Max = GotoList(a).Max
        for t in vbForRange(0, UBound(GotoList)):
            if a != t:
                if GotoList(t).Min <= Min and GotoList(t).Max >= Max:
                    GotoList[a].OutsideCnt = GotoList(a).OutsideCnt + 1
                elif GotoList(t).Min >= Min and GotoList(t).Max <= Max:
                    GotoList[a].Inside_Cnt = GotoList(a).Inside_Cnt + 1
    for Nr in vbForRange(0, UBound(GotoList)):
        h = ( 1 + GotoList(Nr).Inside_Cnt )  /  ( GotoList(Nr).OutsideCnt + GotoList(Nr).Inside_Cnt + 1 )
        Res = Res + GotoList(Nr).Start + ',' + GotoList(Nr).Ende + ',' + h + ' '
    fn_return_value = Left(Res, Len(Res) - 1)
    return fn_return_value

def __Test_GotoArrow():
    List_w_Height = String()
    #UT-------------------------
    List_w_Height = Calc_Height_GotoArrow('5,20 6,20 7,20 8,20 9,20 10,20 11,20 12,20 13,20 14,20 15,20 16,20 17,20 18,20 19,20')
    Delete_Goto_Graph()
    Draw_GotoArrowTab(List_w_Height, LastUsedColumnInRow(ActiveSheet, GoTo_Row))

# VB2PY (UntranslatedCode) Option Explicit