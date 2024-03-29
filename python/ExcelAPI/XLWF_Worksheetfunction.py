# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2022
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
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release

import ExcelAPI.XLW_Workbook as XLW

def RoundUp(v1,v2):
    #print("RoundUp")
    if v2 == 0:
        if v1 == int(v1):
            return int(v1)
        else:
            return int(v1 + 1)
    else:
        return "Error"
    
def Dec2Bin(value, bit_count):
    value=int(value)
    res=f"{value:0{bit_count}b}"
    #res="{0:08b}".format(value)
    return res

def Bin2Dec(bitstring):
    return int(bitstring,2)

def CDec(value):
    
    return int(value)

def Match(Lookup_value,Lookup_array, Match_type):
# Returns the relative position of an item in an array that matches a specified value in a specified order. Use Match instead of one of the Lookup functions when you need the position of an item in a range instead of the item itself.    
# Lookup_value: the value that you use to find the value that you want in a table.
# Lookup_array: a contiguous range of cells containing possible lookup values. Lookup_array must be an array or an array reference.    
# Match_type: the number -1, 0, or 1. Match_type specifies how Microsoft Excel matches lookup_value with values in lookup_array.
# Match returns the position of the matched value within lookup_array, not the value itself. For example, MATCH("b",{"a","b","c"},0) returns 2, the relative position of "b" within the array {"a","b","c"}.
    res = Lookup_array.Find(Lookup_value)
    if res == None:
        return 0
    else:
        return res.Row

def Min(*args):
    return min(*args)


    

