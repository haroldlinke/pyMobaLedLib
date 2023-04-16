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
# fromx vb2py.vbdebug import *
import tkinter as tk
from tkinter import ttk
import sys
import ExcelAPI.XLW_Workbook as X02
#import mlpyproggen.Pattern_Generator as PG
import pattgen.M09_Language as M09

#**************************
#'  Port handling functions
#**************************

def port_is_busy(port):
    
    if type(port)==int:
        return port <0
    elif type(port)==str:
        return port.startswith("*")
    
def port_is_available(port):
    if type(port)==int:
        return port > 0
    elif type(port)==str or type(port)==X02.CRange:
        return not (port.startswith("*") or port=="COM?" or port==" " or port=="NO DEVICE")
    return False
    
def port_reset(port):
    if port.startswith("*"):
        return(port[1:])
    else:
        return port
    
def port_check_format(port):
    if IsNumeric(port):
        return "COM"+port
    else:
        return port
    
def port_set_busy(port):
    if port.startswith("*"):
        return(port)
    else:
        return "*"+port
    
   
def is_64bit() -> bool:
    return sys.maxsize > 2**32



