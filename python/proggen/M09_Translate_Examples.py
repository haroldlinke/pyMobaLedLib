# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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

from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from proggen.M28_divers import *
from proggen.M30_Tools import *
from proggen.M09_Language import *

""" Translate the example strings
UT------------------------------------------------
-----------------------------------------------------------------
"""


def __Test_Translate_Example_Texts_in_Sheet():
    #UT------------------------------------------------
    Translate_Example_Texts_in_Sheet(P01.ActiveSheet)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
def Translate_Example_Texts_in_Sheet(Sh):
    r = int()

    Transl = String()
    #-----------------------------------------------------------------
    Make_sure_that_Col_Variables_match(Sh)
    # Description
    for r in vbForRange(FirstDat_Row, LastUsedRow):
        with_0 = Cells(r, Descrip_Col)
        if with_0.Value != '':
            Transl = Get_Language_Str(with_0.Value)
            if with_0.Value != Transl:
                with_0.Value = Transl
    # Typ column (Red/Green/...)                                              ' 07.03.20:
    for r in vbForRange(FirstDat_Row, LastUsedRow):
        with_1 = Cells(r, Inp_Typ_Col)
        if with_1.Value != '':
            Transl = Get_Language_Str(with_1.Value)
            if with_1.Value != Transl:
                with_1.Value = Transl

# VB2PY (UntranslatedCode) Option Explicit
