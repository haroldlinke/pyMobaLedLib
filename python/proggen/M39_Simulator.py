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
import proggen.M40_ShellandWait as M40
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80

import proggen.Prog_Generator as PG
import proggen.F00_mainbuttons as F00

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

import ctypes,ctypes.util
import sys,platform

"""# VB2PY (CheckDirective) VB directive took path 1 on VBA7"""
"""
extern "C" {
    __declspec(dllexport) int __stdcall GetWrapperVersion();
    __declspec(dllexport) const unsigned char* __stdcall Create(unsigned char* config, int configLenght);
    __declspec(dllexport) const unsigned char* __stdcall CreateSampleConfig();
    __declspec(dllexport) void __stdcall Update();
    __declspec(dllexport) int __stdcall GetLedColor(unsigned char ledNr);
    __declspec(dllexport) void __stdcall SetInput(unsigned char channel, unsigned char On);
    __declspec(dllexport) unsigned char __stdcall GetInput(unsigned char channel);
    __declspec(dllexport) void __stdcall ShowLEDWindow(unsigned char ledsX, unsigned char ledsY, unsigned char ledSize, unsigned char ledOffset, int windowPosX, int windowPosY, bool autoUpdate);
    __declspec(dllexport) void __stdcall CloseLEDWindow();
    __declspec(dllexport) bool __stdcall IsLEDWindowVisible();
    __declspec(dllexport) bool __stdcall GetLEDWindowRect(LPRECT rect);
}
"""

#Private Declare PtrSafe Function CreateSampleConfig Lib "MobaLedLibWrapper.dll" () As LongPtr
#Private Declare PtrSafe Function CreateSimulator Lib "MobaLedLibWrapper.dll" Alias "Create" ( configData As Any, ByVal configLength As Integer) As LongPtr

#Private Declare Sub SetInput Lib "MobaLedLibWrapper.dll" (ByVal Channel As Byte, ByVal IsOn As Byte)
#Private Declare Sub UpdateLeds Lib "MobaLedLibWrapper.dll" Alias "Update" ()
#Private Declare Function GetInput Lib "MobaLedLibWrapper.dll" (ByRef Channel As Byte) As Byte
#Private Declare Sub ShowLEDWindow Lib "MobaLedLibWrapper.dll" ( _
#        ByVal ledsX As Byte, ByVal ledsY As Byte, ByVal ledSize As Byte, ByVal ledOffset As Byte, _
#        ByVal windowPosX As Integer, ByVal windowPosY As Integer, automaticUpdate As Boolean)
#Private Declare Sub CloseLEDWindow Lib "MobaLedLibWrapper.dll" ()
#Private Declare Function IsLEDWindowVisible Lib "MobaLedLibWrapper.dll" () As Byte
#Private Declare Function GetLEDWindowRect Lib "MobaLedLibWrapper.dll" (lpRect As RECT) As Long
#Private Declare Function GetWrapperVersion Lib "MobaLedLibWrapper.dll" () As Long

MobaLedLibWrapper = None
CreateSampleConfig  = None
CreateSimulator = None
SetInput = None
UpdateLeds = None
GetInput = None
ShowLEDWindow = None
CloseLEDWindow = None
IsLEDWindowVisible = None
GetLEDWindowRect = None
GetWrapperVersion = None


__AddressMapping = None

class RECT(ctypes.Structure):
    __fields__ = [("left",ctypes.c_int),
                  ("top",ctypes.c_int),
                  ("right",ctypes.c_int),
                  ("bottom",ctypes.c_int)]
    def __init__(self):
        self.left = 0 
        self.top = 0
        self.right = 0
        self.bottom = 0


def loaddll():
    global MobaLedLibWrapper, CreateSampleConfig, CreateSimulator, SetInput, UpdateLeds, GetInput, ShowLEDWindow, CloseLEDWindow, IsLEDWindowVisible, GetLEDWindowRect, GetWrapperVersion 

    #if platform.system() == "Windows":
    #    MLL_DLL = ctypes.util.find_library("MobaLedLibWrapper")
    #else:
    #    MLL_DLL = None
    #    return
    
    # Get a handle to the sytem C library
    try:
    #   if MLL_DLL == None:
    #       print("MLL_DLL not found")
    #       return
    
        if F00.is_64bit():
            dllfilename = P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x64/MobaLedLibWrapper.dll'
        else:
            dllfilename = P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x86/MobaLedLibWrapper.dll'
        
        Debug.Print("LoadDll:"+dllfilename)    
        MobaLedLibWrapper = ctypes.CDLL(dllfilename)

    except OSError:
        Debug.Print("Unable to load MLL_DLL "+dllfilename)
        sys.exit()
    
    print(f'Succesfully loaded the MLL_DLL'+dllfilename) 
    
    #Private Declare PtrSafe Function CreateSampleConfig Lib "MobaLedLibWrapper.dll" () As LongPtr
    CreateSampleConfig = MobaLedLibWrapper.CreateSampleConfig
    CreateSampleConfig.argtypes=[]
    CreateSampleConfig.restype = ctypes.c_char_p
    
    #Private Declare PtrSafe Function CreateSimulator Lib "MobaLedLibWrapper.dll" Alias "Create" ( configData As Any, ByVal configLength As Integer) As LongPtr
    CreateSimulator = MobaLedLibWrapper.Create
    CreateSimulator.argtypes=[ctypes.c_char_p,ctypes.c_int]
    CreateSimulator.restype = ctypes.c_char_p
    
    #Private Declare Sub SetInput Lib "MobaLedLibWrapper.dll" (ByVal Channel As Byte, ByVal IsOn As Byte)
    SetInput = MobaLedLibWrapper.SetInput
    SetInput.argtypes=[ctypes.c_char,ctypes.c_char]
    SetInput.restype = None
    
    #Private Declare Sub UpdateLeds Lib "MobaLedLibWrapper.dll" Alias "Update" ()
    UpdateLeds = MobaLedLibWrapper.Update
    UpdateLeds.argtypes=[]
    UpdateLeds.restype = None
    
    #Private Declare Function GetInput Lib "MobaLedLibWrapper.dll" (ByRef Channel As Byte) As Byte
    GetInput = MobaLedLibWrapper.GetInput
    GetInput.argtypes=[ctypes.c_char]
    GetInput.restype = ctypes.c_char
        
    #Private Declare Sub ShowLEDWindow Lib "MobaLedLibWrapper.dll" ( _
    #        ByVal ledsX As Byte, ByVal ledsY As Byte, ByVal ledSize As Byte, ByVal ledOffset As Byte, _
    #        ByVal windowPosX As Integer, ByVal windowPosY As Integer, automaticUpdate As Boolean)
    ShowLEDWindow = MobaLedLibWrapper.ShowLEDWindow
    ShowLEDWindow.argtypes=[ctypes.c_char,ctypes.c_char,ctypes.c_char,ctypes.c_char,ctypes.c_int,ctypes.c_int,ctypes.c_bool]
    ShowLEDWindow.restype = None    
    
    #Private Declare Sub CloseLEDWindow Lib "MobaLedLibWrapper.dll" ()
    CloseLEDWindow = MobaLedLibWrapper.CloseLEDWindow
    CloseLEDWindow.argtypes=[]
    CloseLEDWindow.restype = None 
    
    #Private Declare Function IsLEDWindowVisible Lib "MobaLedLibWrapper.dll" () As Byte
    IsLEDWindowVisible = MobaLedLibWrapper.IsLEDWindowVisible
    IsLEDWindowVisible.argtypes=[]
    IsLEDWindowVisible.restype = ctypes.c_bool
    
    #Private Declare Function GetLEDWindowRect Lib "MobaLedLibWrapper.dll" (lpRect As RECT) As Long
    GetLEDWindowRect = MobaLedLibWrapper.GetLEDWindowRect
    GetLEDWindowRect.argtypes=[ctypes.POINTER(RECT)]
    GetLEDWindowRect.restype = ctypes.c_long
    
    #Private Declare Function GetWrapperVersion Lib "MobaLedLibWrapper.dll" () As Long    
    GetWrapperVersion = MobaLedLibWrapper.GetWrapperVersion
    GetWrapperVersion.argtypes=[]
    GetWrapperVersion.restype = ctypes.c_long


def IsSimualtorAvailable():
    fn_return_value = False
    WrapperVersion = Long()
    
    if not P01.checkplatform("Windows"): # Simulator only in Windows available
        return fn_return_value
    
    if F00.is_64bit():
        dllfilename = P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x64/MobaLedLibWrapper.dll'
        Debug.Print("IsSimulatorAvailable:"+dllfilename)
        if Dir(dllfilename) == '':
            Debug.Print("IsSimulatorAvailable:"+dllfilename + " Not found")
            return fn_return_value
        ChDir(P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x64')
    else:
        dllfilename = P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x86/MobaLedLibWrapper.dll'
        Debug.Print("IsSimulatorAvailable:"+dllfilename)
        if Dir(dllfilename) == '':
            Debug.Print("IsSimulatorAvailable:"+dllfilename + " Not found")
            return fn_return_value
        ChDir(P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'x86')
    # VB2PY (UntranslatedCode) On Error GoTo SimError
    # call any function to test binding
    loaddll()
    WrapperVersion = GetWrapperVersion()
    # major.minor.revision e.g. 10000 = 01.00.00
    # in case the exported function interface changes you need to increase major/and or minor version
    # if interface is compatible only revision changes
    fn_return_value = Int(WrapperVersion / 100) == 100
    return fn_return_value

def OpenSimulator():
    Debug.Print("OpenSimulator")
    loaddll()
    
    if not IsSimualtorAvailable():
        return
    __LoadConfiguration()
    __StorePosition()
    
    SimLedsX=M28.Get_Num_Config_Var_Range('SimLedsX', 1, 128, 8)
    SimLedsY=M28.Get_Num_Config_Var_Range('SimLedsY', 4, 64, 8)
    SimLedSize=M28.Get_Num_Config_Var_Range('SimLedSize', 4, 64, 24)
    SimOffset=M28.Get_Num_Config_Var_Range('SimOffset', 0, 255, 1)
    SimPosX=M28.Get_Num_Config_Var_Range('SimPosX', - 16383, 16383, 800)
    SimPosY=M28.Get_Num_Config_Var_Range('SimPosY', - 16383, 16383, 400)
    SimOnTop=M28.Get_Num_Config_Var_Range('SimOnTop', 0, 1, 1)==1
    
    Debug.Print("ShowLEDWindow",SimLedsX,SimLedsY,SimLedSize,SimOffset,SimPosX,SimPosY,SimOnTop)
    ShowLEDWindow(SimLedsX,SimLedsY,SimLedSize,SimOffset,SimPosX,SimPosY,SimOnTop)
    M30.Bring_Application_to_front()
    
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Buffer - ByRef 
def __LoadFile(FileName):
    Debug.Print("__LoadConfiguration:",FileName)
    #fileInt = Integer()
    fileInt = FreeFile()
    try:
        VBFiles.openFile(fileInt, FileName, 'rb')
        f=VBFiles.getFile(fileInt)
        mybytearray = b"" #bytearray()
        length = 0
        byte = f.read(1)
        while byte:
            # Do stuff with byte.
            mybytearray+=byte
            length += 1
            byte = f.read(1)
        
        #VBFiles.openFile(fileInt, FileName, 'rb') # VB2PY (UnknownFileMode) 'Access', 'Read'
        #if LOF(fileInt) == 0:
        #    Buffer = vbObjectInitialize((1,), Variant)
        #    Buffer[0] = 0
        #else:
        #    Buffer = vbObjectInitialize(((0, LOF(fileInt) - 1),), Variant)
        #    Get(fileInt, None , Buffer)
        VBFiles.closeFile(fileInt)
        return mybytearray,length
    except IOError:
        VBFiles.closeFile(fileInt)
        print('Error While Opening the file!')
        return None

def __LoadConfiguration():
    global __AddressMapping
    
    Debug.Print("__LoadConfiguration")
    Buffer = vbObjectInitialize(objtype=Byte)

    Index = Integer()

    Address = Long()

    Length = Integer()

    if not IsSimualtorAvailable():
        return
    Buffer,buflen = __LoadFile(P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + 'LEDConfig.bin')
    dllBuffer = ctypes.create_string_buffer(Buffer)

    print(repr(dllBuffer.raw))
    bufferLen = ctypes.c_int(buflen)
    print(bufferLen,bufferLen.value)
    
    res=CreateSimulator(dllBuffer, bufferLen)
    print(res)
    
    Buffer, buflen=__LoadFile(P01.ThisWorkbook.Path + '\\' + M02.Cfg_Dir_LED + 'AddressConfig.bin')
    Debug.Print(Buffer)
    Length = buflen #len(Buffer) #UBound(Buffer) - LBound(Buffer) + 1
    __AddressMapping = {} #Scripting.Dictionary()
    if Length >= 3:
        for Index in vbForRange(0, ( Length / 3 )  - 1):
            Address = Buffer[Index * 3 + 1]
            Address = 256 * Address + Buffer[Index * 3]
            __AddressMapping[Address] = Buffer[Index * 3 + 2]

def ReloadConfiguration():
    Debug.Print("ReloadConfiguration")
    if IsSimualtorAvailable():
        if IsLEDWindowVisible:
            __LoadConfiguration()

def UpdateSimulatorIfNeeded(CreateHeaderFile, AlwaysOpenWindow):
    Debug.Print("UpdateSimulatorIfNeeded")
    fn_return_value = True
    if IsSimualtorAvailable():
        if AlwaysOpenWindow or IsLEDWindowVisible():
            fn_return_value = UploadToSimulator(CreateHeaderFile)
    return fn_return_value
            

def CloseSimulator():
    if IsSimualtorAvailable():
        __StorePosition()
        CloseLEDWindow()

def IsSimulatorActive():
    fn_return_value = None
    if IsSimualtorAvailable():
        fn_return_value = IsLEDWindowVisible
    Debug.Print("IsSimulatorActive:",fn_return_value)
    return fn_return_value

def ToggleSimulator():
    Debug.Print("ToggleSimulator")
    if IsSimualtorAvailable():
        if IsLEDWindowVisible:
            CloseSimulator()
        else:
            OpenSimulator()
            time.sleep(( 50 ))
            # set focus back to excel
            #*HL AppActivate(ActiveWorkbook.Windows(1).Caption)
            M30.Bring_Application_to_front()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Addr - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Direction - ByVal 
def SendToSimulator(Addr, Direction):
    global __AddressMapping
    Debug.Print("SendToSimulator:",Addr,Direction)
    fn_return_value = False
    if not IsSimualtorAvailable():
        return fn_return_value
    if __AddressMapping is None:
        return fn_return_value
    if IsLEDWindowVisible():
        Channel = 0
        #*HL for Index in vbForRange(0, len(__AddressMapping) - 1):
        for key in __AddressMapping.keys():
            #Address = __AddressMapping.Keys(Index) and 16383
            Address = key & 16383
            Address = Address - P01.val(M28.Get_String_Config_Var("DCC_Offset"))                          # 24.03.21: Juergen
            #AddressType = ( ( __AddressMapping.Keys(Index) and 49152 )  / 16385 )
            
            AddressType = round((key & 49152) / 16385)
            #InCnt = __AddressMapping.Items(Index)
            InCnt = __AddressMapping[key]
            CurrentType = AddressType
            for Index2 in vbForRange(1, InCnt):
                if Address == Addr:
                    if AddressType == 0:
                        SetInput(Channel, Direction)
                        fn_return_value = True
                        return fn_return_value
                    elif CurrentType == 1 and Direction == 0:
                        SetInput(Channel, 1)
                        time.sleep(( 0.400 ))
                        SetInput(Channel, 0)
                        fn_return_value = True
                        return fn_return_value
                    elif CurrentType == 2 and Direction == 1:
                        SetInput(Channel, 1)
                        time.sleep(( 0.400 ))
                        SetInput(Channel, 0)
                        fn_return_value = True
                        return fn_return_value
                if (CurrentType == 0):
                    Address = Address + 1
                elif (CurrentType == 1):
                    CurrentType = 2
                elif (CurrentType == 2):
                    CurrentType = 1
                    Address = Address + 1
                Channel = Channel + 1
    return fn_return_value

def UploadToSimulator(CreateHeaderFiles):
    Debug.Print("UploadToSimulator")
    fn_return_value = False
    if not IsSimualtorAvailable():
        return fn_return_value
    if CreateHeaderFiles:
        fn_return_value = M06.Create_HeaderFile(True)
    else:
        fn_return_value = True

    if fn_return_value:
        CommandStr = P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + M02.CfgBuild_Script + " silent"
        if __Create_Compile_Script():
            fn_return_value = M40.ShellAndWait(CommandStr, 0, vbMinimizedNoFocus, M40.PromptUser) == M40.Success
            if fn_return_value:
                if Dir(P01.ThisWorkbook.Path + "/" + M02.Cfg_Dir_LED + "result.txt") == "" :
                    OpenSimulator()
                else:
                    #rerun command to show output to user
                    CommandStr = P01.ThisWorkbook.Path + "\\" + M02.Cfg_Dir_LED + M02.CfgBuild_Script
                    Res = PG.get_dialog_parent().execute_shell_cmd(CommandStr,"Compile Simulator")
                    #M40.ShellAndWait(CommandStr, 0, vbNormalFocus, M40.PromptUser)
        #*HL AppActivate(ActiveWorkbook.Windows(1).Caption)
        M30.Bring_Application_to_front()
    return fn_return_value

def __StorePosition():
    Debug.Print("StorePosition")
    currentPos = RECT()
    if GetLEDWindowRect(currentPos) == 1:
        M28.Set_String_Config_Var('SimPosX', Str(currentPos.left))
        M28.Set_String_Config_Var('SimPosY', Str(currentPos.top))

def __ConfigurationToFile():
    Debug.Print("ConfigurationToFile")
    fName = String()

    fName2 = String()

    Line = String()

    fn = Integer()

    fn2 = Integer()

    i = Integer()

    OutputFilename = String()
    fName = Environ(M02.Env_USERPROFILE) + '\\AppData\\Local\\Temp\\MobaLedLib_build\\ATMega\\LEDs_AutoProg.ino.elf.txt'
    fName2 = Environ(M02.Env_USERPROFILE) + '\\AppData\\Local\\Temp\\MobaLedLib_build\\ATMega\\LEDs_AutoProg.ino.with_bootloader.bin'
    if Dir(fName) == '':
        return
    if Dir(fName2) == '':
        return
    fn = FreeFile()
    VBFiles.openFile(fn, fName, 'r') 
    while not EOF(fn):
        Line = VBFiles.getLineInput(fn, 1)
        i = InStrRev(Line, ' ')
        if i > 0:
            TypeName = Mid(Line, i + 1)
            if TypeName == '_ZL6Config' or TypeName == '_ZL8Ext_Addr':
                Line = Replace(Line, '  ', ' ')
                Line = Replace(Line, '  ', ' ')
                Line = Replace(Line, '  ', ' ')
                Splits = Split(Line)
                Offset = CInt('&h0' + Splits(2))
                Length = P01.val(Splits(3))
                fn2 = FreeFile()
                VBFiles.openFile(fn2, fName2, 'b') 
                VBFiles.seekFile(fn2, Offset + 1)
                Buffer = vbObjectInitialize((Length - 1,), Variant)
                Get(fn2, VBGetMissingArgument(Get, 1), Buffer)
                VBFiles.closeFile(fn2)
                fn2 = FreeFile()
                if TypeName == '_ZL6Config':
                    OutputFilename = P01.ThisWorkbook.Path + '\\LEDs_AutoProg\\LEDConfig.bin'
                elif TypeName == '_ZL8Ext_Addr':
                    OutputFilename = P01.ThisWorkbook.Path + '\\LEDs_AutoProg\\DCCConfig.bin'
                if Dir(OutputFilename) != '':
                    Kill(OutputFilename)()
                VBFiles.openFile(fn2, OutputFilename, 'b') 
                Put(fn2, VBGetMissingArgument(Put, 1), Buffer)
                VBFiles.closeFile(fn2)
    VBFiles.closeFile(fn)
    ReloadConfiguration()

def __Create_Compile_Script():
   
    fn_return_value = None
    Name = String()

    fp = Integer()
    Name = P01.ThisWorkbook.Path + '/' + M02.Cfg_Dir_LED + M02.CfgBuild_Script
    Debug.Print("Create_Compile_Script:"+Name)
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '@ECHO OFF', '\n')
    VBFiles.writeText(fp, 'REM This file was generated by \'' + P01.ThisWorkbook.Name + '\'  ' + Time, '\n')
    if M30.Win10_or_newer():
        VBFiles.writeText(fp, 'CHCP 65001 >NUL', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'color 79', '\n')
    VBFiles.writeText(fp, 'set scriptDir=%~d0%~p0', '\n')
    VBFiles.writeText(fp, 'set errorfile="%~d0%~p0\\result.txt"', '\n')
    VBFiles.writeText(fp, '%~d0', '\n')
    VBFiles.writeText(fp, 'cd "%~p0"', '\n')
    VBFiles.writeText(fp, 'set packagePath=%USERPROFILE%\\' + M02.AppLoc_Ardu, '\n')
    VBFiles.writeText(fp, 'set toolPath=' + M30.FilePath(M08.Find_ArduinoExe()) + 'hardware\\tools\\avr\\bin', '\n')
    VBFiles.writeText(fp, 'set platformPath=' + M30.FilePath(M08.Find_ArduinoExe()) + 'hardware\\arduino\\avr', '\n')
    VBFiles.writeText(fp, 'set libraryPath=' + M08.GetShortPath(M30.DelLast(M02.Get_Ardu_LibDir())), '\n')
    VBFiles.writeText(fp, '"%toolPath%/avr-g++" -c -g -Os -Wall -std=gnu++11 -fpermissive -fno-exceptions -ffunction-sections -fdata-sections -fno-threadsafe-statics -Wno-error=narrowing -MMD -flto -mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=10813 -DARDUINO_AVR_NANO -DARDUINO_ARCH_AVR "-I%platformPath%\\cores\\\\arduino" "-I%platformPath%\\variants\\\\eightanaloginputs"  "-I%libraryPath%\\MobaLedLib\\src"  "%scriptDir%Configuration.cpp" -o "%scriptDir%Configuration.cpp.o"', '\n')
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')
    VBFiles.writeText(fp, '"%toolPath%/avr-gcc" -Wall -Os -g -flto -fuse-linker-plugin -Wl,--gc-sections -mmcu=atmega328p -o "%scriptDir%Configuration.elf" "%scriptDir%Configuration.cpp.o" -lm', '\n')
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'Rem "%toolPath%/avr-readelf" -a "%scriptDir%Configuration.elf" >"%scriptDir%Configuration.elf.txt"', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '"%toolPath%/avr-objcopy" -O binary -j .MLLLedConfig "%scriptDir%Configuration.elf" "%scriptDir%LEDConfig.bin"', '\n')
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')
    VBFiles.writeText(fp, '"%toolPath%/avr-objcopy" -O binary -j .MLLAddressConfig "%scriptDir%Configuration.elf" "%scriptDir%AddressConfig.bin"', '\n')
    VBFiles.writeText(fp, 'if errorlevel 1 goto :error', '\n')
    VBFiles.writeText(fp, 'if exist %errorfile% del %errorfile%', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, 'goto :eof', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, ':error', '\n')
    VBFiles.writeText(fp, 'if not "%1"==silent" (', '\n')
    VBFiles.writeText(fp, '   COLOR 4F', '\n')
    VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    VBFiles.writeText(fp, '   ECHO    Da ist was schief gegangen ;-(', '\n')
    VBFiles.writeText(fp, '   ECHO   ****************************************', '\n')
    VBFiles.writeText(fp, '   Pause', '\n')
    VBFiles.writeText(fp, ')', '\n')
    VBFiles.writeText(fp, 'echo fail>%errorfile%', '\n')
    VBFiles.writeText(fp, 'exit /b 1', '\n')
    VBFiles.closeFile(fp)
    fn_return_value = True
    return fn_return_value
    VBFiles.closeFile(fp)
    P01.MsgBox(M09.Get_Language_Str('Fehler beim Schreiben der Datei \'') + Name + '\'', vbCritical, M09.Get_Language_Str('Fehler beim erzeugen der Arduino Start Datei'))
    fn_return_value = False
    return fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CreateSampleConfig Lib "MobaLedLibWrapper.dll" () As LongPtr
# VB2PY (UntranslatedCode) Private Declare PtrSafe Function CreateSimulator Lib "MobaLedLibWrapper.dll" Alias "Create" ( _\nconfigData As Any, ByVal configLength As Integer) As LongPtr
# VB2PY (UntranslatedCode) Private Declare Sub SetInput Lib "MobaLedLibWrapper.dll" (ByVal Channel As Byte, ByVal IsOn As Byte)
# VB2PY (UntranslatedCode) Private Declare Sub UpdateLeds Lib "MobaLedLibWrapper.dll" Alias "Update" ()
# VB2PY (UntranslatedCode) Private Declare Function GetInput Lib "MobaLedLibWrapper.dll" (ByRef Channel As Byte) As Byte
# VB2PY (UntranslatedCode) Private Declare Sub ShowLEDWindow Lib "MobaLedLibWrapper.dll" ( _\nByVal ledsX As Byte, ByVal ledsY As Byte, ByVal ledSize As Byte, ByVal ledOffset As Byte, _\nByVal windowPosX As Integer, ByVal windowPosY As Integer, automaticUpdate As Boolean)
# VB2PY (UntranslatedCode) Private Declare Sub CloseLEDWindow Lib "MobaLedLibWrapper.dll" ()
# VB2PY (UntranslatedCode) Private Declare Function IsLEDWindowVisible Lib "MobaLedLibWrapper.dll" () As Byte
# VB2PY (UntranslatedCode) Private Declare Function GetLEDWindowRect Lib "MobaLedLibWrapper.dll" (lpRect As RECT) As Long
# VB2PY (UntranslatedCode) Private Declare Function GetWrapperVersion Lib "MobaLedLibWrapper.dll" () As Long
