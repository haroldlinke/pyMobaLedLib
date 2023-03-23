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

import proggen.Prog_Generator as PG

import ExcelAPI.XLW_Workbook as P01

from ExcelAPI.XLC_Excel_Consts import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

# ******************************
# *                            *
# *       M38_Extensions       *
# *                            *
# ******************************

Extensions = Collection()
ExtensionKey = 'EX.'
__ExtensionsActive = {}
__ExtensionLines = {}
__JSONData = Object()

def __Load_Extensions():
    OldEvents = Variant()

    ParamSheet = Variant()

    MacroSheet = Variant()

    #Extension = clsExtension()

    #Macro = clsExtensionMacro()

    #Parameter = clsExtensionParameter()

    #Constructor = clsExtensionConstructor()

    Argument = Variant()

    MacroRow = Integer()

    ParamRow = Integer()

    MacroStr = String()
    __CollectExtensions()
    RemoveExistingExtensions()
    OldEvents = P01.Application.EnableEvents
    P01.Application.EnableEvents = False
    ParamSheet = PG.ThisWorkbook.Sheets(M02.PAR_DESCR_SH)
    MacroSheet = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
    MacroRow = M30.LastUsedRowIn(MacroSheet) + 1
    ParamRow = M30.LastUsedRowIn(ParamSheet) + 1
    for Extension in Extensions:
        for Constructor in Extension.Constructors:
            # TODO translate
            MacroStr = ''
            for Argument in Constructor.Arguments:
                if MacroStr != '':
                    MacroStr = MacroStr + ', '
                # fully qualify the argument name if argument is defined withon the plugin
                if Extension.IsExtensionParameter(Argument):
                    MacroStr = MacroStr + ExtensionKey + Extension.Name + '.'
                MacroStr = MacroStr + Argument
            MacroStr = ExtensionKey + Constructor.TypeName + '(' + MacroStr + ')'
            MacroSheet.CellDict[MacroRow, M02.SM_Typ___COL] = 'EX.Constructor'
            MacroSheet.CellDict[MacroRow, M02.SM_Pic_N_COL] = 'Puzzle | IDE'
            MacroSheet.CellDict[MacroRow, M02.SM_LEDS__COL] = Constructor.LEDs
            MacroSheet.CellDict[MacroRow, M02.SM_InCnt_COL] = Constructor.InCnt
            MacroSheet.CellDict[MacroRow, M02.SM_Macro_COL] = MacroStr
            MacroSheet.CellDict[MacroRow, M02.SM_FindN_COL] = ExtensionKey + Constructor.TypeName + '('
            MacroSheet.CellDict[MacroRow, M02.SM_Name__COL] = ExtensionKey + Constructor.TypeName
            MacroSheet.CellDict[MacroRow, M02.SM_Group_COL] = 'Erweiterungen'
            MacroSheet.CellDict[MacroRow, M02.SM_LName_COL] = Constructor.Texts.GetText(DE, 'DisplayName')
            MacroSheet.CellDict[MacroRow, M02.SM_ShrtD_COL] = Constructor.Texts.GetText(DE, 'ShortDescription')
            MacroSheet.CellDict[MacroRow, M02.SM_DetailCOL] = Constructor.Texts.GetText(DE, 'DetailedDescription')
            MacroRow = MacroRow + 1
        for Parameter in Extension.Parameters:
            ParamSheet.CellDict[ParamRow, M02.ParName_COL] = 'EX.' + Extension.Name + '.' + Parameter.Name
            ParamSheet.CellDict[ParamRow, M02.ParType_COL] = Parameter.TypeName
            ParamSheet.CellDict[ParamRow, M02.Par_Min_COL] = Parameter.Min
            ParamSheet.CellDict[ParamRow, M02.Par_Max_COL] = Parameter.Max
            ParamSheet.CellDict[ParamRow, M02.Par_Def_COL] = Parameter.Default
            ParamSheet.CellDict[ParamRow, M02.Par_Opt_COL] = Parameter.Options
            ParamSheet.CellDict[ParamRow, M02.ParInTx_COL] = Parameter.Texts.GetText(DE, 'DisplayName')
            ParamSheet.CellDict[ParamRow, M02.ParHint_COL] = Parameter.Texts.GetText(DE, 'ShortDescription')
            ParamRow = ParamRow + 1
        for Macro in Extension.Macros:
            # TODO translate
            MacroStr = ''
            for Argument in Macro.Arguments:
                if MacroStr != '':
                    MacroStr = MacroStr + ', '
                MacroStr = MacroStr + Argument
            if MacroStr == '':
                MacroStr = Macro.Name
            else:
                MacroStr = Macro.Name + '(' + MacroStr + ')'
            MacroSheet.CellDict[MacroRow, M02.SM_Typ___COL] = 'EX.Macro'
            MacroSheet.CellDict[MacroRow, M02.SM_Pic_N_COL] = 'Puzzle | IDE'
            MacroSheet.CellDict[MacroRow, M02.SM_LEDS__COL] = Macro.LEDs
            MacroSheet.CellDict[MacroRow, M02.SM_InCnt_COL] = Macro.InCnt
            MacroSheet.CellDict[MacroRow, M02.SM_Macro_COL] = MacroStr
            MacroSheet.CellDict[MacroRow, M02.SM_FindN_COL] = MacroStr
            if Macro.Arguments.Count != 0:
                MacroSheet.CellDict[MacroRow, M02.SM_FindN_COL] = MacroSheet.Cells(MacroRow, SM_FindN_COL) + '('
            MacroSheet.CellDict[MacroRow, M02.SM_Name__COL] = Macro.Name
            MacroSheet.CellDict[MacroRow, M02.SM_Group_COL] = 'Erweiterungen'
            MacroSheet.CellDict[MacroRow, M02.SM_LName_COL] = Macro.Texts.GetText(DE, 'DisplayName')
            MacroSheet.CellDict[MacroRow, M02.SM_ShrtD_COL] = Macro.Texts.GetText(DE, 'ShortDescription')
            MacroSheet.CellDict[MacroRow, M02.SM_DetailCOL] = Macro.Texts.GetText(DE, 'DetailedDescription')
            MacroRow = MacroRow + 1
    P01.Application.EnableEvents = OldEvents

def __CollectExtensions():
    
    return #*HL
    
    oFSO = Variant()

    DirName = Variant()

    Id = Integer()

    Libs = Collection()
    Extensions = Collection()
    oFSO = CreateObject('Scripting.FileSystemObject')
    if not M37.CheckArduinoHomeDir():
        return
    Libs = Collection()
    DirName = Dir(M02.Sketchbook_Path + '\\libraries\\*.*', vbDirectory)
    while DirName != '':
        if DirName != '.' and DirName != '..':
            if oFSO.FolderExists(M02.Sketchbook_Path + '\\libraries\\' + DirName):
                if oFSO.FileExists(M02.Sketchbook_Path + '\\libraries\\' + DirName + '\\MobaLedLib.properties'):
                    Libs.Add(M02.Sketchbook_Path + '\\libraries\\' + DirName + '\\MobaLedLib.properties')
        DirName = Dir()
    Id = 1
    for DirName in Libs:
        LibName = DirName
        __JSONData = None
        # VB2PY (UntranslatedCode) On Error Resume Next
        __JSONData = M33.ParseJSON(Read_File_to_String(LibName))
        # VB2PY (UntranslatedCode) On Error GoTo 0
        if not __JSONData is None:
            #Extension = clsExtension()
            Extension.Platforms = __ToList('obj.platforms(#)')
            Extension.Name = __JSONData('obj.id')
            Extension.Path = Replace(LibName, '\\MobaLedLib.properties', '')
            Extension.Includes = __JSONData('obj.includes')
            Extension.MacroIncludes = __JSONData('obj.macroIncludes')
            for Index in __ToIndexList('obj.types(#).TypeName'):
                ctr = clsExtensionConstructor()
                ctr.TypeName = __GetDataAtIndex('obj.types(#).TypeName', Index)
                ctr.LEDs = __GetDataAtIndex('obj.types(#).LEDs', Index)
                ctr.InCnt = __GetDataAtIndex('obj.types(#).InCount', Index)
                ctr.Texts.SetText(DE, 'DisplayName', __GetDataAtIndex('obj.types(#).DisplayName', Index))
                ctr.Texts.SetText(DE, 'ShortDescription', __GetDataAtIndex('obj.types(#).ShortDescription', Index))
                ctr.Texts.SetText(DE, 'DetailedDescription', __GetDataAtIndex('obj.types(#).DetailedDescription', Index))
                for Index2 in __ToIndexList('obj.types(' + Index + ').Arguments(#)'):
                    ctr.Arguments.Add(__GetDataAtIndex('obj.types(' + Index + ').Arguments(#)', Index2))
                Extension.Constructors.Add(ctr)
            for Index in __ToIndexList('obj.macros(#).Macro'):
                mac = clsExtensionMacro()
                mac.Name = __GetDataAtIndex('obj.macros(#).Macro', Index)
                mac.LEDs = __GetDataAtIndex('obj.macros(#).LEDs', Index)
                mac.InCnt = __GetDataAtIndex('obj.macros(#).InCount', Index)
                mac.Texts.SetText(DE, 'DisplayName', __GetDataAtIndex('obj.macros(#).DisplayName', Index))
                mac.Texts.SetText(DE, 'ShortDescription', __GetDataAtIndex('obj.macros(#).ShortDescription', Index))
                mac.Texts.SetText(DE, 'DetailedDescription', __GetDataAtIndex('obj.macros(#).DetailedDescription', Index))
                for Index2 in __ToIndexList('obj.macros(' + Index + ').Arguments(#)'):
                    mac.Arguments.Add(__GetDataAtIndex('obj.macros(' + Index + ').Arguments(#)', Index2))
                Extension.Macros.Add(mac)
            for Index in __ToIndexList('obj.parameters(#).ParameterName'):
                par = clsExtensionParameter()
                par.Name = __GetDataAtIndex('obj.parameters(#).ParameterName', Index)
                par.TypeName = __GetDataAtIndex('obj.parameters(#).Type', Index)
                par.Min = __GetDataAtIndex('obj.parameters(#).Min', Index)
                par.Max = __GetDataAtIndex('obj.parameters(#).Max', Index)
                par.Default = __GetDataAtIndex('obj.parameters(#).Default', Index)
                par.Options = __GetDataAtIndex('obj.parameters(#).Options', Index)
                par.Texts.SetText(DE, 'DisplayName', __GetDataAtIndex('obj.parameters(#).DisplayName', Index))
                par.Texts.SetText(DE, 'ShortDescription', __GetDataAtIndex('obj.parameters(#).ShortDescription', Index))
                Extension.Parameters.Add(par)
            Message = Extension.CheckValid
            if Message == '':
                Extensions.Add(Extension)
                Id = Id + 1
            else:
                MsgBox(Replace('Extension \'#1#\' load error', '#1#', Extension.Name) + vbCrLf + Message, vbExclamation, 'MobaLedLib Extensions')

def __ToList(Pattern):
    fn_return_value = None
    search = String()

    cnt = Integer()
    cnt = 0
    fn_return_value = Collection()
    while 1:
        search = Replace(Pattern, '#', cnt)
        if not __JSONData.Exists(search):
            break
        fn_return_value.Add(__JSONData(search))
        cnt = cnt + 1
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Index - ByVal 
def __GetDataAtIndex(Pattern, Index):
    fn_return_value = None
    search = String()
    fn_return_value = ''
    search = Replace(Pattern, '#', Index)
    if not __JSONData.Exists(search):
        return fn_return_value
    fn_return_value = __JSONData(search)
    return fn_return_value

def __ToIndexList(Pattern):
    fn_return_value = None
    search = String()

    cnt = Integer()
    cnt = 0
    fn_return_value = Collection()
    while 1:
        search = Replace(Pattern, '#', cnt)
        if not __JSONData.Exists(search):
            break
        fn_return_value.Add(cnt)
        cnt = cnt + 1
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Id - ByVal 
def GetExtension(Id):
    fn_return_value = None
    Extension = Variant()
    for Extension in Extensions:
        if Extension.Id == Id:
            fn_return_value = Extension
            return fn_return_value
    fn_return_value = None
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Key - ByVal 
def GetConstructor(Key):
    fn_return_value = None
    Splits = Variant()
    Splits = Split(Key, '.')
    if UBound(Splits) == 3 and Splits(0) == 'PI' and Splits(1) == 'Constructor':
        Extension = GetExtension(Splits(2))
        if not Extension is None:
            fn_return_value = Extension.GetConstructor(Splits(3))
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: TypeName - ByVal 
def GetExtensionByTypeName(TypeName):
    fn_return_value = None

    for Extension in Extensions:
        for Constructor in Extension.Constructors:
            if Constructor.TypeName == TypeName:
                fn_return_value = Extension
                return fn_return_value
    fn_return_value = None
    return fn_return_value

def IsExtensionKey(Key):
    fn_return_value = InStr(str(Key), ExtensionKey) == 1
    return fn_return_value

def Init_HeaderFile_Generation_Extension():
    global __ExtensionsActive, __ExtensionLines
    fn_return_value = None
    __ExtensionsActive = {} #Scripting.Dictionary()
    __ExtensionLines = {} #Scripting.Dictionary()
    __CollectExtensions()
    fn_return_value = True
    return fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cmd - ByRef 
def Add_Extension_Entry(Cmd):
    fn_return_value = None
    p_str = String()

    #Extension = clsExtension()
    Cmd = Mid(Cmd, Len(ExtensionKey) + 1)
    p_str = Cmd
    if InStr(Cmd, '(') > 0:
        p_str = Split(p_str, '(')(0)
    Extension = GetExtensionByTypeName(p_str)
    if Extension is None:
        MsgBox(Replace('Extension \'#1#\' not found', '#1#', p_str), vbCritical, 'MobaLedLib Extensions')
        fn_return_value = False
        return fn_return_value
    if not __ExtensionsActive.Exists(Extension.Id):
        __ExtensionsActive.Add(Extension.Id, Extension)
    __ExtensionLines.Add(__ExtensionLines.Count + 1, Cmd)
    fn_return_value = True
    return fn_return_value, Cmd #*HL ByRef

def Write_Header_File_Extension_Before_Config(fp):
    fn_return_value = None
    #Extension = clsExtension()

    p_str = Variant()

    HeaderWritten = Boolean()
    #------------------------------------------------------------------
    # here we write include all the header files, that have definitions already needed inside the config block
    # e.g. macros
    HeaderWritten = False
    if len(__ExtensionsActive) > 0:
        for Extension in Extensions:
            if Extension.MacroIncludes != '':
                if HeaderWritten == False:
                    VBFiles.writeText(fp, '// ----- dynamic extensions section begin -----', '\n')
                    VBFiles.writeText(fp, '#define MLL_EXTENSIONS_ACTIVE', '\n')
                    VBFiles.writeText(fp, '#include <MLLExtension.h>', '\n')
                    VBFiles.writeText(fp, '', '\n')
                    HeaderWritten = True
                VBFiles.writeText(fp, '// Extension ' + Extension.Name, '\n')
                for p_str in Split(Extension.MacroIncludes, ','):
                    VBFiles.writeText(fp, '#include <' + p_str + '>')
                VBFiles.writeText(fp, '', '\n')
        if HeaderWritten:
            VBFiles.writeText(fp, '// ----- dynamic Extensions section end -----', '\n')
    fn_return_value = True
    return fn_return_value

def Write_Header_File_Extension_After_Config(fp):
    fn_return_value = None
    Extension = Variant()

    p_str = Variant()

    Index = Integer()
    #------------------------------------------------------------------
    if len(__ExtensionsActive) > 0:
        VBFiles.writeText(fp, '// ----- dynamic extensions section begin -----', '\n')
        VBFiles.writeText(fp, '#include <MLLExtension.h>', '\n')
        VBFiles.writeText(fp, '', '\n')
        for Extension in Extensions:
            if Extension.Includes != '':
                VBFiles.writeText(fp, '// Extension ' + Extension.Name, '\n')
                for p_str in Split(Extension.Includes, ','):
                    VBFiles.writeText(fp, '#include <' + p_str + '>')
            VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '', '\n')
        if __ExtensionLines.Count > 0:
            VBFiles.writeText(fp, '// ----- dynamic extensions section begin -----', '\n')
            VBFiles.writeText(fp, 'MLLExtension* mllExtensions[] = {', '\n')
            for Index in vbForRange(1, __ExtensionLines.Count):
                if Index == __ExtensionLines.Count:
                    VBFiles.writeText(fp, '  new ' + __ExtensionLines(Index), '\n')
                else:
                    VBFiles.writeText(fp, '  new ' + __ExtensionLines(Index) + ',', '\n')
            VBFiles.writeText(fp, '} ;', '\n')
            VBFiles.writeText(fp, '#define MLL_EXTENSIONS_COUNT ' + __ExtensionLines.Count, '\n')
            VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '// ----- dynamic Extensions section end -----', '\n')
        VBFiles.writeText(fp, '', '\n')
    fn_return_value = True
    return fn_return_value

def Write_PIO_Extension(fp):
    fn_return_value = False

    #for Index in vbForRange(0, len(__ExtensionsActive) - 1
    for Index in __ExtensionsActive.keys():
        VBFiles.writeText(fp, '    ' + __ExtensionsActive[Index].Name + '=file://' + M08.GetShortPath(__ExtensionsActive[Index].Path), '\n')
    fn_return_value = True
    return fn_return_value

def RemoveExistingExtensions():

    MacroSheet = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
    ParamSheet = PG.ThisWorkbook.Sheets(M02.PAR_DESCR_SH)
    
    
    for r in vbForRange(1, M30.LastUsedRowIn(ParamSheet)):
        if IsExtensionKey(ParamSheet.Cells(r, M10.ParName_COL)):
            ParamSheet.Rows(r).EntireRow.Delete()
            r = r - 1
            raise() #*HL diese For Schleifen funktionieren nicht, da die Schleifenvariable in der Schleife reduziert wird!!
    for r in vbForRange(M02.SM_DIALOGDATA_ROW1, M30.LastUsedRowIn(MacroSheet)):
        if IsExtensionKey(MacroSheet.Cells(r, M02.SM_Typ___COL)):
            MacroSheet.Rows(r).EntireRow.Delete()
            r = r - 1
            raise() #*HL diese For Schleifen funktionieren nicht, da die Schleifenvariable in der Schleife reduziert wird!!



