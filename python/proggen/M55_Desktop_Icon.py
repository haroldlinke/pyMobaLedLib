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

import ExcelAPI.XLW_Workbook as P01

#from ExcelAPI.X01_Excel_Consts import *




def __TestCreateDesktopShortcut():
    #UT------------------------------------
    CreateDesktopShortcut('Aber Hallo', PG.ThisWorkbook.Name, 'mll_platine_ausschnitt3_icon.ico')

def CreateDesktopShortcut(LinkName, BookFullName, IconName):
    return True #*HL
    fn_return_value = None
    location = 'Desktop'

    LinkExt = '.lnk'

    oWsh = Object()

    oShortcut = Object()

    Sep = String()

    Path = String()

    DesktopPath = String()

    Shortcut = String()
    #---------------------------------------------------------------------------------------------------------------
    # Create a custom icon shortcut on the users desktop
    # Constant string values, you can replace "Desktop"
    # with any Special Folders name to create the shortcut there
    # Object variables
    # String variables
    # Initialize variables
    Sep = P01.Application.PathSeparator
    Path = PG.ThisWorkbook.Path
    # VB2PY (UntranslatedCode) On Error GoTo ErrHandle
    # The WScript.Shell object provides functions to read system
    # information and environment variables, work with the registry
    # and manage shortcuts
    oWsh = CreateObject('WScript.Shell')
    DesktopPath = oWsh.SpecialFolders(location)
    # Get the path where the shortcut will be located
    Shortcut = DesktopPath + Sep + LinkName + LinkExt
    oShortcut = oWsh.CreateShortcut(Shortcut)
    # Link it to this file
    with_0 = oShortcut
    with_0.TargetPath = BookFullName
    with_0.IconLocation = Path + Sep + IconName
    with_0.Save()
    # Explicitly clear memory
    oWsh = None
    oShortcut = None
    fn_return_value = True
    return fn_return_value
    #return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit