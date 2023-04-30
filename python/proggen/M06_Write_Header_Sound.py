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
# 2021-01-07 v4.02 HL: - Else:, ByRef check done - first PoC release


from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

# fromx proggen.M02_Public import *
# fromx proggen.M06_Write_Header_LED2Var import *
# fromx proggen.M06_Write_Header_Sound import *
# fromx proggen.M06_Write_Header_SW import *
# fromx proggen.M08_ARDUINO import *
# fromx proggen.M09_Language import *
# fromx proggen.M09_Select_Macro import *
# fromx proggen.M20_PageEvents_a_Functions import *
# fromx proggen.M25_Columns import *
# fromx proggen.M28_divers import *
# fromx proggen.M30_Tools import *
# fromx proggen.M80_Create_Mulitplexer import *

# fromx ExcelAPI.X02_Workbook import *

import proggen.M02_Public as M02
import proggen.M02_Scripting as Scripting
#import proggen.M03_Dialog as M03
#import proggen.M06_Write_Header_LED2Var as M06LED
#import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
#import proggen.M06_Write_Header as M06
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
#import proggen.M30_Tools as M30
#import proggen.M31_Sound as M31
#import proggen.M37_Inst_Libraries as M37
#import proggen.M60_CheckColors as M60
#import proggen.M70_Exp_Libraries as M70
#import proggen.M80_Create_Mulitplexer as M80
#*HL import proggen.clsNode

import ExcelAPI.XLW_Workbook as P01


""" Header file generation for the Sound functions

"""

SoundLines = Scripting.Dictionary()

def Init_HeaderFile_Generation_Sound(firstSheet):
    global SoundLines
    
    _fn_return_value = False
    #--------------------------------------------------------------
    SoundLines = Scripting.Dictionary()
    _fn_return_value = True
    #UseFullPacketMode = false                                                ' 19.10.21: Always use the full packed mode because this mode could be used with both types of JQ6500 modules
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cmd - ByRef 
def Add_SoundPin_Entry(Cmd, Channel):
    global SoundLines
    
    _fn_return_value = False
    Parts = vbObjectInitialize(objtype=String)

    #Typ = String()

    Pin = String()

    playerClass = String()
    Parts = Split(Replace(Replace(Replace(Trim(Cmd), M02.SF_SERIAL_SOUND_PIN, ''), ')', ''), ' ', ''), ',')
    if UBound(Parts) - LBound(Parts) != 1:
        # todo
        return _fn_return_value
    
    fret, M02.SF_SERIAL_SOUND_PIN = M06SW.Set_PinNrLst_if_Matching(M02.SF_SERIAL_SOUND_PIN + Parts(0) + ')', M02.SF_SERIAL_SOUND_PIN, Pin, 'O', 1)
    if fret == False:
        return _fn_return_value
    if M06SW.No_Duplicates_in_two_Lists('Sound', Serial_PinLst, Pin, M02.SF_SERIAL_SOUND_PIN) == False:
        return _fn_return_value
    Serial_PinLst = Serial_PinLst + Pin + ' '
    if not Check_Sound_Duplicates():
        return _fn_return_value
    playerClass = GetPlayerClass(Parts(1))
    if playerClass == '':
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Der Soundmodul Typ \'#1#\' wird nicht unterstützt.'), "#1#", Parts(1)), vbCritical, 'Fehler: Soundmodul')
        return _fn_return_value
    if SoundLines.Exists(Channel):
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Der Sound Kanal \'#1#\' ist schon definiert.'), "#1#", Channel), vbCritical, 'Fehler: Soundmodul')
        return _fn_return_value
    #If Parts(1) = "JQ6500_AA" Then UseFullPacketMode = True                 ' 19.10.21: Always use the full packed mode because this mode could be used with both types of JQ6500 modules
    SoundLines.Add(Channel, Array(Pin, playerClass))
    Cmd = '// ' + Cmd
    _fn_return_value = True
    return _fn_return_value, Cmd

def GetPlayerClass(moduleType):
    _fn_return_value = False
    _select83 = moduleType
    if (_select83 == 'JQ6500'):
        _fn_return_value = 'JQ6500SoundPlayer'
    elif (_select83 == 'JQ6500_AA'):
        _fn_return_value = 'JQ6500SoundPlayer'
    elif (_select83 == 'MP3-TF-16P'):
        _fn_return_value = 'MP3TF16PSoundPlayer'
    elif (_select83 == 'MP3-TF-16P-NO-CRC'):
        _fn_return_value = 'MP3TF16PNoCRCSoundPlayer'
    else:
        _fn_return_value = ''
    return _fn_return_value

def Write_Header_File_Sound_Before_Config(fp):
    global SoundLines
    
    _fn_return_value = False
    if SoundLines.Count > 0:
        if Check_Sound_Duplicates() == False:
            return _fn_return_value
        VBFiles.writeText(fp, '// ----- Serial Onboard Sound Makros -----', '\n')
        VBFiles.writeText(fp, '  #include "SoundChannelMacros.h"', '\n')
        VBFiles.writeText(fp, '', '\n')
        Index = 0
        for _idx1 in SoundLines.Keys:
            proggen.clsNode.Key = _idx1
            VBFiles.writeText(fp, '  #define SOUND_CHANNEL_' + proggen.clsNode.Key + ' ' + Index, '\n')
            Index = Index + 1
        VBFiles.writeText(fp, '', '\n')
    _fn_return_value = True
    return _fn_return_value

def Write_Header_File_Sound_After_Config(fp):
    global SoundLines
    
    _fn_return_value = False
    #------------------------------------------------------------------
    if SoundLines.Count > 0:
        if Check_Sound_Duplicates() == False:
            return _fn_return_value
        VBFiles.writeText(fp, '// ----- Serial Onboard Sound -----', '\n')
        VBFiles.writeText(fp, '#ifndef _USE_EXT_PROC', '\n')
        VBFiles.writeText(fp, '  #error _USE_EXT_PROC must be enabled in MobaLebLib, see file \'Lib_Config.h\'', '\n')
        VBFiles.writeText(fp, '#else', '\n')
        VBFiles.writeText(fp, '  // includes for Onboard sound processing', '\n')
        #If UseFullPacketMode Then
        # 19.10.21: Always use the full packed mode because this mode could be used with both types of JQ6500 modules
        VBFiles.writeText(fp, '#define _SOUNDPROCCESSOR_SEND_FULL_PACKET', '\n')
        #End If
        VBFiles.writeText(fp, '  #include "SoundProcessor.h"', '\n')
        VBFiles.writeText(fp, '', '\n')
        VBFiles.writeText(fp, '  #ifndef _ENABLE_EXT_PROC', '\n')
        VBFiles.writeText(fp, '  #define _ENABLE_EXT_PROC', '\n')
        VBFiles.writeText(fp, '  #endif', '\n')
        VBFiles.writeText(fp, '  #ifndef _SOUND_SERBUFFER_SIZE', '\n')
        VBFiles.writeText(fp, '  #define _SOUND_SERBUFFER_SIZE ', 15 + SoundLines.Count * 5, '\n')
        VBFiles.writeText(fp, '  #endif', '\n')
        VBFiles.writeText(fp, '', '\n')
        #     Dim modulesArray As String, playersArray As String
        #     Dim ChannelToModuleIndex As Scripting.Dictionary
        #     Set ChannelToModuleIndex = New Scripting.Dictionary
        #     Dim Index As Byte, key
        #     Index = 0
        #     For Each key In SoundLines.Keys
        #        If modulesArray <> "" Then modulesArray = modulesArray + ", "
        #        modulesArray = modulesArray + "SoundProcessor::CreateSoftwareSerial(" + SoundLines(key)(0) + ", 9600)"
        #        'Debug.Print "Channel " & key & " Pin " & SoundLines(key)(0) & " for channel "; SoundLines(key)(1)
        #        'ChannelToModuleId.Add key, index
        #        If playersArray <> "" Then playersArray = playersArray + ", "
        #        playersArray = playersArray + "new " & SoundLines(key)(1) & "(" & Str(Index) & ", &serialDispatcher)"
        #        Index = Index + 1
        #     Next
        #     Print #fp, "  SOFTWARE_SERIAL_TYPE* mySerial[] { " + modulesArray + "};"
        #     Print #fp, "  uint8_t serBuffer[_SOUND_SERBUFFER_SIZE];"
        #     Print #fp, "  SoundSerialDispatcher serialDispatcher(serBuffer, _SOUND_SERBUFFER_SIZE, mySerial);"
        #     Print #fp, "  SoundPlayer* soundPlayers[] {" + playersArray + "};"
        #     Print #fp, "  SoundProcessor soundProcessor;"
        # 02.11.2021: Juergen add support of multiple sound module types
        # START_CHANGE
        #ChannelToModuleIndex = Scripting.Dictionary()
        Index = 0
        for _idx2 in SoundLines.Keys:
            proggen.clsNode.Key = _idx2
            module = 'SoundProcessor::CreateSoftwareSerial(' + SoundLines(proggen.clsNode.Key)(0) + ', 9600)'
            if playersArray != '':
                playersArray = playersArray + ', '
            playersArray = playersArray + 'new ' + SoundLines(proggen.clsNode.Key)(1) + '(' + Str(Index) + ', ' + module + ')'
            Index = Index + 1
        VBFiles.writeText(fp, '  uint8_t serBuffer[_SOUND_SERBUFFER_SIZE];', '\n')
        VBFiles.writeText(fp, '  SoundPlayer* soundPlayers[] {' + playersArray + '};', '\n')
        VBFiles.writeText(fp, '  SoundProcessor soundProcessor(serBuffer, _SOUND_SERBUFFER_SIZE, soundPlayers);', '\n')
        # END_CHANGE
        VBFiles.writeText(fp, '#endif', '\n')
        VBFiles.writeText(fp, '', '\n')
    _fn_return_value = True
    return _fn_return_value

def Check_Sound_Duplicates():
    global SwitchA_InpCnt,SwitchB_InpCnt,SwitchC_InpCnt,SwitchD_InpCnt
        
    _fn_return_value = False
    if M06SW.No_Duplicates_in_two_Lists('LED', M06SW.Serial_PinLst, M06SW.LED_PINNr_List, M02.SF_SERIAL_SOUND_PIN) == False:
        return _fn_return_value
    if M06SW.SwitchA_InpCnt:
        if M06SW.No_Duplicates_in_two_Lists('Switch A', M06SW.Serial_PinLst, M06SW.SwitchA_InpLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
    if M06SW.SwitchB_InpCnt:
        if M06SW.No_Duplicates_in_two_Lists('Switch B', M06SW.Serial_PinLst, M06SW.SwitchB_InpLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
    if M06SW.SwitchC_InpCnt:
        if M06SW.No_Duplicates_in_two_Lists('Switch C', M06SW.Serial_PinLst, M06SW.SwitchC_InpLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
    if M06SW.SwitchD_InpCnt:
        if M06SW.No_Duplicates_in_two_Lists('Switch D', M06SW.Serial_PinLst, M06SW.SwitchD_InpLst, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
    if M06SW.SwitchB_InpCnt > 0 or M06SW.SwitchC_InpCnt > 0:
        if M06SW.No_Duplicates_in_two_Lists('Switch B/C Clock', M06SW.Serial_PinLst, M06SW.CLK_Pin_Number, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
        if M06SW.No_Duplicates_in_two_Lists('Switch B/C Reset', M06SW.Serial_PinLst, M06SW.RST_Pin_Number, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
    if M06SW.Read_LDR:
        if M06SW.No_Duplicates_in_two_Lists('LDR_Pin_Number', M06SW.Serial_PinLst, M06SW.LDR_Pin_Number, M02.SF_SERIAL_SOUND_PIN) == False:
            return _fn_return_value
    if M06SW.No_Duplicates_in_two_Lists('LED', M06SW.Serial_PinLst, M06SW.LED_PINNr_List, M02.SF_SERIAL_SOUND_PIN) == False:
        return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

def CheckSoundChannelDefined(Channel):
    global SoundLines
    
    _fn_return_value = False
    if not SoundLines.Exists(Channel):
        P01.MsgBox(Replace(M09.Get_Language_Str('Fehler: Der Sound Kanal \'#1#\' ist nicht definiert.' + vbCr + 'Zur Definition muss das Makro ' + str(M02.SF_SERIAL_SOUND_PIN) + ' vor dieser Zeile verwendet werden'), "#1#", Channel), vbCritical, 'Fehler: Soundmodul')
        return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
