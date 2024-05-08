from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import proggen.M08_ARDUINO as M08
import ExcelAPI.XLW_Workbook as P01

"""-------------------------------------------------------------------------------------------------------------------------------
----------------------------------
"""

TimeCnt = 64
Width_Define = 76

def Write_one_Block(fp, MName, Params1, MTyp, Ram, Params2):
    line = String()

    i = Long()

    TNr = Long()

    Define = String()
    #-------------------------------------------------------------------------------------------------------------------------------
    MName = RTrim(MName)
    Define = '#define '
    if left(MName, Len('XPatternT')) == 'XPatternT':
        if MName == 'XPatternT':
            VBFiles.writeText(fp, '#define USE_XFADE // 220 Bytes Flash', '\n')
        VBFiles.writeText(fp, '#ifdef USE_XFADE', '\n')
        VBFiles.writeText(fp, '// Drittes Makro bei dem fuer jede LED ein Byte RAM Reserviert wird. Das wird benoetigt wenn das flag _PF_XFADE gesetzt ist.', '\n')
        VBFiles.writeText(fp, '// Dummerweise kann bei dieser Funktion keine Berechnung beim Parameter LED gemacht werden ;-(', '\n')
        Define = ' ' + Define
    if MName == ' PatternTE':
        VBFiles.writeText(fp, '// Same macros with an enable input 05.11.18:', '\n')
        VBFiles.writeText(fp, '', '\n')
    for TNr in vbForRange(1, TimeCnt):
        line = AddSpaceToLen(Define + MName + TNr + '(', 22) + Params1
        for i in vbForRange(1, TNr):
            line = line + 'T' + i + ','
        line = AddSpaceToLen(line + '...)', Width_Define + TimeCnt * 4) + AddSpaceToLen(MTyp + TNr + '_T,', 15) + '_CHKL(LED)+' + Ram + Params2
        for i in vbForRange(1, TNr):
            line = line + '_T2B(T' + i + '),'
        line = line + '_W2B(COUNT_VARARGS(__VA_ARGS__)), __VA_ARGS__,'
        VBFiles.writeText(fp, line, '\n')
    if left(MName, Len('XPatternT')) == 'XPatternT':
        VBFiles.writeText(fp, '#endif', '\n')
    VBFiles.writeText(fp, '', '\n')

def Create_Pattern_H_File():
    fp = Integer()

    fileName = String()
    #----------------------------------
    fileName = M08.GetWorkbookPath() + '\\Pattern_Macros.h'
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, fileName, 'w') 
    VBFiles.writeText(fp, '// Created by Create_Pattern_H_File() from ' + P01.ThisWorkbook.Name, '\n')
    VBFiles.writeText(fp, '', '\n')
    Write_one_Block(fp, ' PatternT ', 'LED,NStru,InCh,       LEDs,Val0,Val1,Off,Mode,', ' PATTERNT', 'RAM5,           ', '(NStru)&0xFF,_ChkIn(InCh),SI_1,  LEDs,Val0,Val1,Off,Mode,          ')
    Write_one_Block(fp, 'APatternT ', 'LED,NStru,InCh,       LEDs,Val0,Val1,Off,Mode,', 'APATTERNT', 'RAM7,           ', '(NStru)&0xFF,_ChkIn(InCh),SI_1,  LEDs,Val0,Val1,Off,Mode,          ')
    Write_one_Block(fp, 'XPatternT ', 'LED,NStru,InCh,       LEDs,Val0,Val1,Off,Mode,', 'APATTERNT', 'RAM7+RAMN(LEDs),', '(NStru)&0xFF,_ChkIn(InCh),SI_1,  LEDs,Val0,Val1,Off,Mode|_PF_XFADE,')
    Write_one_Block(fp, ' PatternTE', 'LED,NStru,InCh,Enable,LEDs,Val0,Val1,Off,Mode,', ' PATTERNT', 'RAM5,           ', '(NStru)&0xFF,_ChkIn(InCh),Enable,LEDs,Val0,Val1,Off,Mode,          ')
    Write_one_Block(fp, 'APatternTE', 'LED,NStru,InCh,Enable,LEDs,Val0,Val1,Off,Mode,', 'APATTERNT', 'RAM7,           ', '(NStru)&0xFF,_ChkIn(InCh),Enable,LEDs,Val0,Val1,Off,Mode,          ')
    Write_one_Block(fp, 'XPatternTE', 'LED,NStru,InCh,Enable,LEDs,Val0,Val1,Off,Mode,', 'APATTERNT', 'RAM7+RAMN(LEDs),', '(NStru)&0xFF,_ChkIn(InCh),Enable,LEDs,Val0,Val1,Off,Mode|_PF_XFADE,')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    return
    P01.MsgBox('Fehler beim Schreiben der Macro Datei')

# VB2PY (UntranslatedCode) Option Explicit
