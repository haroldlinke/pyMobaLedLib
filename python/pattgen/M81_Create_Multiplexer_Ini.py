from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import pattgen.M80_Multiplexer_INI_Handling
import pattgen.M09_Language

"""-----------------------------------------------------------------------
--------------------------------------------------------------------------------------------
Private Sub Write_Header_IniFile(New_Multiplexer_Ini_File As Boolean)
"""


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def Create_Example_Ini_File(Name):
    _fn_return_value = None
    fp = Integer()
    # ' 04.06.20: Hardi
    #-----------------------------------------------------------------------
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Header]', '\n')
    VBFiles.writeText(fp, '****************************************************************************************************', '\n')
    VBFiles.writeText(fp, '*                                                                                                  *', '\n')
    VBFiles.writeText(fp, '* This Multiplexer configuration file is used in MobaLedLib by Hardi Stengelin: MobaLedLib@gmx.de. *', '\n')
    VBFiles.writeText(fp, '*                                                                                                  *', '\n')
    VBFiles.writeText(fp, '* Compatible with : - Prog_Generator version 0.76 and higher                                       *', '\n')
    VBFiles.writeText(fp, '*                   - Pattern_Generator version 0.98 and higher                                    *', '\n')
    VBFiles.writeText(fp, '*                                                                                                  *', '\n')
    VBFiles.writeText(fp, '* Autor           : Misha van der stam                                                             *', '\n')
    VBFiles.writeText(fp, '* Created         : 17 May 2020                                                                    *', '\n')
    VBFiles.writeText(fp, '*                                                                                                  *', '\n')
    VBFiles.writeText(fp, '****************************************************************************************************', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Section]', '\n')
    VBFiles.writeText(fp, 'KeyName=Value', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Multiplexer_Macro]', '\n')
    VBFiles.writeText(fp, 'INI_File_Production_Date=' + X02.Now, '\n')
    VBFiles.writeText(fp, 'Version=' + pattgen.M80_Multiplexer_INI_Handling.Version, '\n')
    VBFiles.writeText(fp, 'Number_Of_Multiplexers=' + pattgen.M80_Multiplexer_INI_Handling.Number_Of_Multiplexers, '\n')
    if pattgen.M80_Multiplexer_INI_Handling.ThreeD:
        VBFiles.writeText(fp, 'ThreeD=1', '\n')
    else:
        VBFiles.writeText(fp, 'ThreeD=0', '\n')
    if pattgen.M80_Multiplexer_INI_Handling.LED_Nrs_OnOff:
        VBFiles.writeText(fp, 'LED_Nrs_OnOff=1', '\n')
    else:
        VBFiles.writeText(fp, 'LED_Nrs_OnOff=0', '\n')
    if pattgen.M80_Multiplexer_INI_Handling.DisplayLEDs:
        VBFiles.writeText(fp, 'DisplayLEDs=1', '\n')
    else:
        VBFiles.writeText(fp, 'DisplayLEDs=0', '\n')
    VBFiles.writeText(fp, 'WiKi_URL=https://wiki.mobaledlib.de/anleitungen/spezial/multiplexing', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Multiplexer_RGB_Carousel]', '\n')
    VBFiles.writeText(fp, 'Description=Groups by 4 Leds for Carousel', '\n')
    VBFiles.writeText(fp, 'Number_Of_LEDs=4', '\n')
    VBFiles.writeText(fp, 'LED_Type=RGB LEDs', '\n')
    VBFiles.writeText(fp, 'Enable_DCC_Button=1', '\n')
    # 10.02.21: Old: 0
    VBFiles.writeText(fp, 'Option 1 Name=RGB_Multiplexer_3_4_Running_Blue (PC)', '\n')
    VBFiles.writeText(fp, 'Option 1 Pattern=PatternT1(LED,4,#LOC_INCH+0,12,0,128,0,PM_NORMAL,0.1 sec,48,0,0,0,12,0,0,0,3,0,0,192)', '\n')
    VBFiles.writeText(fp, 'Option 1 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 2 Name=RGB_Disco_3_4_Flashing_Red', '\n')
    VBFiles.writeText(fp, 'Option 2 Pattern=PatternT2(LED,4,#LOC_INCH+1,12,0,128,0,PM_NORMAL,0.1 sec,0.1 sec,0,0,0,195,48,12)', '\n')
    VBFiles.writeText(fp, 'Option 2 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 3 Name=RGB_4_Running_Green_Left', '\n')
    VBFiles.writeText(fp, 'Option 3 Pattern=PatternT1(LED,4,#LOC_INCH+2,12,0,128,0,PM_NORMAL,100 ms,0,0,48,0,192,0,0,3,0,12,0,0)', '\n')
    VBFiles.writeText(fp, 'Option 3 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 4 Name=RGB_4_2_Running_White_Left', '\n')
    VBFiles.writeText(fp, 'Option 4 Pattern=PatternT1(LED,4,#LOC_INCH+3,12,0,128,0,PM_NORMAL,100 ms,0,240,255,255,15,0)', '\n')
    VBFiles.writeText(fp, 'Option 4 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 5 Name=RGB_Disco_3_4_Running_Blue_PINGPONG', '\n')
    VBFiles.writeText(fp, 'Option 5 Pattern=PatternT1(LED,4,InCh,12,0,128,0,PM_PINGPONG,0.5 sec,48,0,0,0,12,0,0,0,3,0,0,192)', '\n')
    VBFiles.writeText(fp, 'Option 5 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 6 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 6 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 6 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 7 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 7 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 7 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 8 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 8 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 8 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'ControlNr=4923', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Multiplexer_RGB_Ferris wheel]', '\n')
    VBFiles.writeText(fp, 'Description=Groups by 8 Leds for Ferris wheel', '\n')
    VBFiles.writeText(fp, 'Number_Of_LEDs=8', '\n')
    VBFiles.writeText(fp, 'LED_Type=RGB LEDs', '\n')
    VBFiles.writeText(fp, 'Enable_DCC_Button=1', '\n')
    # 10.02.21: Old: 0
    VBFiles.writeText(fp, 'Option 1 Name=RGB_Disco_1_Moving_Yellows_To_Right', '\n')
    VBFiles.writeText(fp, 'Option 1 Pattern=PatternT1(LED,4,#LOC_INCH+0,24,0,128,0,PM_NORMAL,100 ms,12,192,0,12,192,0,0,3,48,0,3,48)', '\n')
    VBFiles.writeText(fp, 'Option 1 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 2 Name=RGB Multiplexer 2 1Running All_Green PingPong (pc)', '\n')
    VBFiles.writeText(fp, 'Option 2 Pattern=PatternT1(LED,4,#LOC_INCH+1,24,0,128,0,PM_PINGPONG,102 ms,0,195,48,12,195,48,12,192,48,12,195,48,12,3,48,12,195,48,12,195,0,12,195,48,12,195,48,0,195,48,12,195,48,12,192,48,12,195,48,12,3,48,12,195,48,12,195,0)', '\n')
    VBFiles.writeText(fp, 'Option 2 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 3 Name=RGB_Multiplexer_3_Running_Blue_PingPong (pc)', '\n')
    VBFiles.writeText(fp, 'Option 3 Pattern=PatternT1(LED,4,#LOC_INCH+2,24,0,128,0,PM_PINGPONG,103 ms,48,0,0,0,0,0,0,12,0,0,0,0,0,0,3,0,0,0,0,0,192,0,0,0,0,0,0,48,0,0,0,0,0,0,12,0,0,0,0,0,0,3,0,0,0,0,0,192)', '\n')
    VBFiles.writeText(fp, 'Option 3 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 4 Name=RGB_Multiplexer_5_Bouncing_Colors (pc)', '\n')
    VBFiles.writeText(fp, 'Option 4 Pattern=PatternT1(LED,4,#LOC_INCH+3,24,0,128,0,PM_NORMAL,105 ms,12,0,0,0,0,48,192,3,0,0,240,0,0,48,0,192,0,0,0,0,252,63,0,0,0,48,0,192,0,0,192,3,0,0,240,0,12,0,0,0,0,48)', '\n')
    VBFiles.writeText(fp, 'Option 4 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 5 Name=RGB_Multiplexer_6_Bouncing_Pink (pc)', '\n')
    VBFiles.writeText(fp, 'Option 5 Pattern=PatternT1(LED,8,#LOC_INCH+4,24,0,128,0,PM_NORMAL,106 ms,0,0,0,96,196,8,0,0,0,0,0,48,2,0,128,17,0,0,0,24,1,0,0,0,0,35,0,140,0,0,0,0,0,0,0,70,0,24,1,0,0,0,0,35,0,0,0,48,2,0,128,17,0,0,0,0,0,96,196,8,0,0,0)', '\n')
    VBFiles.writeText(fp, 'Option 5 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 6 Name=RGB_Multiplexer_7_Running_8_Colors (pc)', '\n')
    VBFiles.writeText(fp, 'Option 6 Pattern=APatternT1(LED,8,#LOC_INCH+5,24,0,128,0,PM_NORMAL,107 ms,7,112,252,0,126,28,255,255,227,56,14,224,248,1,252,56,254,255,63,112,28,192,241,3,248,113,252,192,127,224,56,128,227,7,240,227,199,129,255,192,113,0,199,15,224,248,143,3,255,129,227,0,142,31,199,241,31,7,254,3,199,1,28,255,143,227,63,14,252,7,142,3,248,255,31,199,127,28,248,15,28,199,241,255,63,142,255,56,240,31,192,143,227,255,127,28,255,113,224,63,128,31,199,255,255,56,254,227,56,126,0,63,142,255,255,113,252,7,112,252,0,126,28,255,255,227)', '\n')
    VBFiles.writeText(fp, 'Option 6 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 7 Name=RGB_Multiplexer_8_All Blue_PingPong (pc)', '\n')
    VBFiles.writeText(fp, 'Option 7 Pattern=PatternT1(LED,8,#LOC_INCH+6,24,0,128,0,PM_PINGPONG,108 ms,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,0,0,0,0,0,0,0,112,224,0,0,0,0,0,0,56,112,224,0,0,0,0,0,28,56,112,224,0,0,0,0,14,28,56,112,224,0,0,0,7,14,28,56,112,224,0,128,3,7,14,28,56,112,224,192,129,3,7,14,28,56,112,224,192,129,3,7,14,28,56,112,0,192,129,3,7,14,28,56,0,0,192,129,3,7,14,28,0,0,0,192,129,3,7,14,0,0,0,0,192,129,3,7,0,0,0,0,0,192,129,3,0,0,0,0,0,0,192,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)', '\n')
    VBFiles.writeText(fp, 'Option 7 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 8 Name=RGB_Multiplexer_9_4x4_Colored_Flashing (pc)', '\n')
    VBFiles.writeText(fp, 'Option 8 Pattern=PatternT1(LED,4,#LOC_INCH+7,24,0,128,0,PM_NORMAL,104 ms,0,0,0,0,0,0,195,48,12,195,48,12,0,0,0,0,0,0)', '\n')
    VBFiles.writeText(fp, 'Option 8 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'ControlNr=36449', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Multiplexer_BumpCars]', '\n')
    VBFiles.writeText(fp, 'Description=SingleLEDS For 6 LEDs', '\n')
    VBFiles.writeText(fp, 'Number_Of_LEDs=6', '\n')
    VBFiles.writeText(fp, 'LED_Type=Single LEDs', '\n')
    VBFiles.writeText(fp, 'Enable_DCC_Button=1', '\n')
    # 10.02.21: Old: 0
    VBFiles.writeText(fp, 'Option 1 Name=SGL6_Running_Blue_PingPong', '\n')
    VBFiles.writeText(fp, 'Option 1 Pattern=PatternT1(LED,4,InCh,6,0,128,0,PM_PINGPONG,0.5 sec,3,192,0,48,0,12,0,3,192)', '\n')
    VBFiles.writeText(fp, 'Option 1 SingleLED_Colors=0,00, 00, 255,00, 00, 255,00, 00, 255,00, 00, 255,00, 00, 255,00, 00, 255', '\n')
    VBFiles.writeText(fp, 'Option 2 Name=SGL6_Running_Green_PingPong', '\n')
    VBFiles.writeText(fp, 'Option 2 Pattern=PatternT1(LED,4,InCh,6,0,128,0,PM_PINGPONG,100,255,207,255,243,255,252,63,255,207,255,243,255)', '\n')
    VBFiles.writeText(fp, 'Option 2 SingleLED_Colors=0,00, 180, 00,00, 180, 00,00, 180, 00,00, 180, 00,00, 180, 00,00, 180, 00', '\n')
    VBFiles.writeText(fp, 'Option 3 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 3 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 3 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 4 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 4 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 4 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 5 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 5 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 5 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 6 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 6 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 6 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 7 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 7 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 7 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'Option 8 Name=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 8 Pattern=To be filled!', '\n')
    VBFiles.writeText(fp, 'Option 8 SingleLED_Colors=', '\n')
    VBFiles.writeText(fp, 'ControlNr=3793', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Debug.Print('Example Multiplexer.ini File created.')
    _fn_return_value = True
    return _fn_return_value
    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim erzeugen der cmd Datei'))
    VBFiles.closeFile(fp)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Name - ByVal 
def Create_Default_Ini_File(Name):
    _fn_return_value = None
    fp = Integer()
    #--------------------------------------------------------------------------------------------
    fp = FreeFile()
    # VB2PY (UntranslatedCode) On Error GoTo WriteError
    VBFiles.openFile(fp, Name, 'w') 
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Header]', '\n')
    VBFiles.writeText(fp, '****************************************************************************************************', '\n')
    VBFiles.writeText(fp, '*                                                                                                  *', '\n')
    VBFiles.writeText(fp, '* This Multiplexer configuration file is used in MobaLedLib by Hardi Stengelin: MobaLedLib@gmx.de. *', '\n')
    VBFiles.writeText(fp, '*                                                                                                  *', '\n')
    VBFiles.writeText(fp, '* Compatible with : - Prog_Generator version 0.76 and higher                                       *', '\n')
    VBFiles.writeText(fp, '*                   - Pattern_Generator version 0.98 and higher                                    *', '\n')
    VBFiles.writeText(fp, '*                                                                                                  *', '\n')
    VBFiles.writeText(fp, '* Autor           : Misha van der stam                                                             *', '\n')
    VBFiles.writeText(fp, '* Created         : 17 May 2020                                                                    *', '\n')
    VBFiles.writeText(fp, '*                                                                                                  *', '\n')
    VBFiles.writeText(fp, '****************************************************************************************************', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Section]', '\n')
    VBFiles.writeText(fp, 'KeyName=Value', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '[Multiplexer_Macro]', '\n')
    VBFiles.writeText(fp, 'INI_File_Production_Date=' + X02.Now, '\n')
    VBFiles.writeText(fp, 'Version=' + pattgen.M80_Multiplexer_INI_Handling.Version, '\n')
    VBFiles.writeText(fp, 'Number_Of_Multiplexers=' + pattgen.M80_Multiplexer_INI_Handling.Number_Of_Multiplexers, '\n')
    if pattgen.M80_Multiplexer_INI_Handling.ThreeD:
        VBFiles.writeText(fp, 'ThreeD=1', '\n')
    else:
        VBFiles.writeText(fp, 'ThreeD=0', '\n')
    if pattgen.M80_Multiplexer_INI_Handling.LED_Nrs_OnOff:
        VBFiles.writeText(fp, 'LED_Nrs_OnOff=1', '\n')
    else:
        VBFiles.writeText(fp, 'LED_Nrs_OnOff=0', '\n')
    if pattgen.M80_Multiplexer_INI_Handling.DisplayLEDs:
        VBFiles.writeText(fp, 'DisplayLEDs=1', '\n')
    else:
        VBFiles.writeText(fp, 'DisplayLEDs=0', '\n')
    VBFiles.writeText(fp, 'WiKi_URL=https://wiki.mobaledlib.de/anleitungen/spezial/multiplexing', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.writeText(fp, '', '\n')
    VBFiles.closeFile(fp)
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Debug.Print('Default Multiplexer.ini File created.')
    _fn_return_value = True
    return _fn_return_value
    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler beim schreiben der Datei \'') + Name + '\'', vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler beim erzeugen der cmd Datei'))
    VBFiles.closeFile(fp)
    return _fn_return_value

# VB2PY (UntranslatedCode) Option Explicit
