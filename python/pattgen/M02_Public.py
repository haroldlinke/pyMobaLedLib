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

"""--------------------------------------------------------------------"""


def Change_Board_Typ(LeftArduino, NewBrd):
    Col = Long()

    Brd = Integer()

    BuildOpt = String()

    Old_Board = String()
    #--------------------------------------------------------------------
    #  If Disable_Set_Arduino_Typ Then Exit Sub
    MsgBox('Todo: Change_Board_Typ')
    ## VB2PY (CheckDirective) VB directive took path 1 on 0
    if LeftArduino:
        Col = BUILDOP_COL
        Brd = 0
    else:
        Col = BUILDOpRCOL
        Brd = 1
    Old_Board = Get_Old_Board(LeftArduino)
    BuildOpt = Cells(SH_VARS_ROW, Col)
    if Old_Board == '':
        BuildOpt = NewBrd + ' ' + BuildOpt
    else:
        BuildOpt = Replace(BuildOpt, Old_Board, NewBrd)
    Cells[SH_VARS_ROW, Col] = Trim(BuildOpt)


